"""State-machine orchestration for discovery, qualification, execution, publishing, and delivery."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path

from .artifacts import materialize_artifacts, validate_artifacts, validate_relative_path
from .clients.executor import ArenaExecutionGatewayClient
from .clients.github import GitHubPublisher
from .clients.llm import FastLLMClient
from .config import Settings
from .exceptions import PipelineError
from .models import FreelanceJob, JobRecord, JobStatus
from .platforms.base import FreelancePlatform
from .store import JobStore
from .text import url_fingerprint

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CycleSummary:
    discovered: int = 0
    classified: int = 0
    bids_submitted: int = 0
    awards_found: int = 0
    artifacts_ready: int = 0
    published: int = 0
    delivered: int = 0
    failures: int = 0

    def add(self, **changes: int) -> CycleSummary:
        values = {field: getattr(self, field) for field in self.__dataclass_fields__}
        values.update({key: values[key] + value for key, value in changes.items()})
        return CycleSummary(**values)


class FreelancePipeline:
    """A resumable workflow driven by persistent status transitions, not in-memory queues."""

    def __init__(
        self,
        settings: Settings,
        store: JobStore,
        platforms: dict[str, FreelancePlatform],
        classifier: FastLLMClient | None,
        executor: ArenaExecutionGatewayClient | None,
        github: GitHubPublisher | None,
    ) -> None:
        self.settings = settings
        self.store = store
        self.platforms = platforms
        self.classifier = classifier
        self.executor = executor
        self.github = github
        self._cycle_lock = asyncio.Lock()

    async def run_once(self) -> CycleSummary:
        """Run one bounded cycle. A lock prevents overlapping cron/API triggers."""
        if self._cycle_lock.locked():
            logger.warning("cycle_skipped_already_running")
            return CycleSummary()
        async with self._cycle_lock:
            summary = CycleSummary()
            summary = await self._discover_and_classify(summary)
            summary = await self._find_awards(summary)
            summary = await self._execute_awarded(summary)
            summary = await self._publish_artifacts(summary)
            summary = await self._deliver_published(summary)
            return summary

    async def run_forever(self) -> None:
        while True:
            try:
                summary = await self.run_once()
                logger.info("cycle_completed", extra={"summary": {field: getattr(summary, field) for field in summary.__dataclass_fields__}})
            except Exception:
                logger.exception("cycle_crashed")
            await asyncio.sleep(self.settings.poll_interval_seconds)

    async def retry(self, platform: str, external_id: str) -> bool:
        return await self.store.reset_for_retry(platform, external_id)

    async def _discover_and_classify(self, summary: CycleSummary) -> CycleSummary:
        for platform_name, platform in self.platforms.items():
            try:
                jobs = await platform.discover_jobs()
            except PipelineError as exc:
                logger.warning("platform_discovery_failed", extra={"platform": platform_name, "error": str(exc)})
                summary = summary.add(failures=1)
                continue
            except Exception:
                logger.exception("platform_discovery_unexpected", extra={"platform": platform_name})
                summary = summary.add(failures=1)
                continue
            for job in jobs:
                record = await self.store.save_discovered(job)
                summary = summary.add(discovered=1)
                if record.status == JobStatus.DISCOVERED:
                    classified, submitted, failed = await self._classify_and_maybe_bid(job)
                    if classified:
                        summary = summary.add(classified=1)
                    if submitted:
                        summary = summary.add(bids_submitted=1)
                    if failed:
                        summary = summary.add(failures=1)
        return summary

    async def _classify_and_maybe_bid(self, job: FreelanceJob) -> tuple[bool, bool, bool]:
        if self.classifier is None:
            logger.info("classification_waiting_for_llm_configuration", extra={"job_key": job.key})
            return False, False, False
        try:
            decision = await self.classifier.classify(job)
            metadata = {
                "confidence": decision.confidence,
                "rationale": decision.rationale,
                "risks": list(decision.risks),
                "estimated_days": decision.estimated_days,
                "proposal_fa": decision.proposal_fa,
            }
            eligible = decision.automatable and decision.confidence >= self.settings.llm_min_automation_confidence
            if not eligible:
                await self.store.transition(
                    job.platform,
                    job.external_id,
                    (JobStatus.DISCOVERED,),
                    JobStatus.INELIGIBLE,
                    metadata=metadata,
                )
                return True, False, False
            if not await self.store.transition(
                job.platform,
                job.external_id,
                (JobStatus.DISCOVERED,),
                JobStatus.READY_FOR_REVIEW,
                metadata=metadata,
            ):
                return True, False, False
            if not (self.settings.automation_enabled and self.settings.auto_submit_bids):
                return True, False, False
            claimed = await self.store.transition(
                job.platform,
                job.external_id,
                (JobStatus.READY_FOR_REVIEW,),
                JobStatus.BIDDING,
            )
            if not claimed:
                return True, False, False
            try:
                await self.platforms[job.platform].submit_bid(job, decision.proposal_fa or "")
                await self.store.transition(
                    job.platform, job.external_id, (JobStatus.BIDDING,), JobStatus.BID_SUBMITTED
                )
                return True, True, False
            except Exception as exc:
                await self._fail(job, JobStatus.BIDDING, JobStatus.BID_FAILED, exc)
                return True, False, True
        except Exception as exc:
            await self._fail(job, JobStatus.DISCOVERED, JobStatus.CLASSIFICATION_FAILED, exc)
            return False, False, True

    async def _find_awards(self, summary: CycleSummary) -> CycleSummary:
        for record in await self.store.list_by_status((JobStatus.BID_SUBMITTED,)):
            platform = self.platforms.get(record.platform)
            if platform is None:
                continue
            job = self._to_job(record)
            try:
                if await platform.is_awarded(job):
                    if await self.store.transition(
                        record.platform,
                        record.external_id,
                        (JobStatus.BID_SUBMITTED,),
                        JobStatus.AWARDED,
                    ):
                        summary = summary.add(awards_found=1)
            except Exception as exc:
                await self.store.append_event(
                    record.platform,
                    record.external_id,
                    "award_check_failed",
                    {"error": self._error_text(exc)},
                )
                summary = summary.add(failures=1)
        return summary

    async def _execute_awarded(self, summary: CycleSummary) -> CycleSummary:
        if not self.settings.automation_enabled:
            return summary
        if self.executor is None:
            logger.warning("execution_waiting_for_gateway_configuration")
            return summary
        for record in await self.store.list_by_status((JobStatus.AWARDED,)):
            if not await self.store.transition(
                record.platform, record.external_id, (JobStatus.AWARDED,), JobStatus.EXECUTING
            ):
                continue
            job = self._to_job(record)
            try:
                result = await self.executor.execute(job)
                files = validate_artifacts(result.files)
                output_dir = self._artifact_dir_for(job)
                materialize_artifacts(output_dir, files)
                await self.store.transition(
                    record.platform,
                    record.external_id,
                    (JobStatus.EXECUTING,),
                    JobStatus.ARTIFACTS_READY,
                    artifact_dir=str(output_dir.resolve()),
                    metadata={"executor_task_id": result.task_id, "file_count": len(files)},
                )
                summary = summary.add(artifacts_ready=1)
            except Exception as exc:
                await self._fail(job, JobStatus.EXECUTING, JobStatus.EXECUTION_FAILED, exc)
                summary = summary.add(failures=1)
        return summary

    async def _publish_artifacts(self, summary: CycleSummary) -> CycleSummary:
        if not self.settings.automation_enabled:
            return summary
        if self.github is None:
            logger.warning("publishing_waiting_for_github_configuration")
            return summary
        for record in await self.store.list_by_status((JobStatus.ARTIFACTS_READY,)):
            if not await self.store.transition(
                record.platform, record.external_id, (JobStatus.ARTIFACTS_READY,), JobStatus.PUBLISHING
            ):
                continue
            job = self._to_job(record)
            try:
                if not record.artifact_dir:
                    raise ValueError("Artifact directory is missing")
                files = self._read_artifact_directory(Path(record.artifact_dir))
                publication = await self.github.publish(job, files)
                await self.store.transition(
                    record.platform,
                    record.external_id,
                    (JobStatus.PUBLISHING,),
                    JobStatus.CODE_PUBLISHED,
                    github_url=publication.repository_url,
                    metadata={
                        "github_branch": publication.branch,
                        "github_path_prefix": publication.path_prefix,
                        "github_commit": publication.commit_sha,
                    },
                )
                summary = summary.add(published=1)
            except Exception as exc:
                await self._fail(job, JobStatus.PUBLISHING, JobStatus.PUBLISHING_FAILED, exc)
                summary = summary.add(failures=1)
        return summary

    async def _deliver_published(self, summary: CycleSummary) -> CycleSummary:
        if not self.settings.automation_enabled:
            return summary
        for record in await self.store.list_by_status((JobStatus.CODE_PUBLISHED,)):
            platform = self.platforms.get(record.platform)
            if platform is None or not record.github_url:
                continue
            if not await self.store.transition(
                record.platform, record.external_id, (JobStatus.CODE_PUBLISHED,), JobStatus.DELIVERING
            ):
                continue
            job = self._to_job(record)
            try:
                await platform.send_delivery(job, record.github_url)
                await self.store.transition(
                    record.platform, record.external_id, (JobStatus.DELIVERING,), JobStatus.DELIVERED
                )
                summary = summary.add(delivered=1)
            except Exception as exc:
                await self._fail(job, JobStatus.DELIVERING, JobStatus.DELIVERY_FAILED, exc)
                summary = summary.add(failures=1)
        return summary

    async def _fail(
        self, job: FreelanceJob, expected: JobStatus, target: JobStatus, exc: Exception
    ) -> None:
        error = self._error_text(exc)
        logger.warning("pipeline_step_failed", extra={"job_key": job.key, "target": target.value, "error": error})
        await self.store.transition(job.platform, job.external_id, (expected,), target, error=error)

    def _artifact_dir_for(self, job: FreelanceJob) -> Path:
        # Never let untrusted platform IDs become filesystem paths.
        return self.settings.artifact_root / job.platform / url_fingerprint(job.key)

    @staticmethod
    def _read_artifact_directory(root: Path):
        if not root.is_dir():
            raise ValueError(f"Artifact directory does not exist: {root}")
        resolved_root = root.resolve()
        from .models import ArtifactFile

        files: list[ArtifactFile] = []
        for candidate in sorted(root.rglob("*")):
            if candidate.is_symlink():
                raise ValueError(f"Symlink is not permitted in artifacts: {candidate.name}")
            if not candidate.is_file():
                continue
            resolved = candidate.resolve()
            if resolved_root not in resolved.parents:
                raise ValueError("Artifact file escaped root")
            relative = validate_relative_path(resolved.relative_to(resolved_root).as_posix())
            files.append(ArtifactFile(path=relative, content=resolved.read_bytes()))
        return validate_artifacts(tuple(files))

    @staticmethod
    def _to_job(record: JobRecord) -> FreelanceJob:
        return FreelanceJob(
            platform=record.platform,
            external_id=record.external_id,
            url=record.url,
            title=record.title,
            description=record.description,
            budget_text=record.budget_text,
        )

    @staticmethod
    def _error_text(exc: Exception) -> str:
        return f"{type(exc).__name__}: {str(exc)[:800]}"
