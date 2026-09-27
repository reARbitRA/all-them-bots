"""Client for a user-operated coding-execution gateway.

The official Arena.ai Agent Mode help describes interactive workspace/GitHub delivery, not a
public job-execution API.  This concrete client therefore targets the documented contract in
``docs/executor-contract.md``.  An organization may implement that gateway using Arena.ai,
an internal runner, or another authorized coding agent without fabricating a vendor endpoint.
"""

from __future__ import annotations

import asyncio
import io
import logging
import time
import zipfile
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx

from ..artifacts import (
    MAX_FILE_BYTES,
    MAX_FILE_COUNT,
    MAX_TOTAL_BYTES,
    decode_base64,
    validate_artifacts,
    validate_relative_path,
)
from ..config import Settings
from ..exceptions import ExecutionError
from ..models import ArtifactFile, ExecutionResult, FreelanceJob

logger = logging.getLogger(__name__)


class ArenaExecutionGatewayClient:
    """Submit a bounded coding task and poll until its generated files are available."""

    def __init__(self, settings: Settings, http_client: httpx.AsyncClient | None = None) -> None:
        settings.require_execution()
        self.settings = settings
        self._client = http_client or httpx.AsyncClient(
            timeout=httpx.Timeout(connect=20, read=60, write=30, pool=20), follow_redirects=False
        )
        self._owns_client = http_client is None

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def execute(self, job: FreelanceJob) -> ExecutionResult:
        task_payload = {
            "idempotency_key": job.key,
            "task": {
                "title": job.title,
                "description": job.description,
                "budget_text": job.budget_text,
                "language": "fa",
                "instructions": self._execution_instructions(job),
            },
            "output": {
                "format": "files",
                "required_files": ["README.md"],
                "readme_language": "fa",
                "tests_required": True,
            },
        }
        headers = self._headers(job.key)
        try:
            response = await self._client.post(self.settings.arena_executor_url, json=task_payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ExecutionError("Could not create execution task") from exc
        if not isinstance(data, dict):
            raise ExecutionError("Executor task response must be a JSON object")
        if self._is_completed(data):
            return await self._result_from_payload(data, fallback_task_id=job.key)
        task_id = data.get("task_id") or data.get("id")
        if not isinstance(task_id, str) or not task_id:
            raise ExecutionError("Executor did not provide task_id or completed artifacts")
        status_url = data.get("status_url")
        if not isinstance(status_url, str) or not status_url:
            status_url = urljoin(f"{self.settings.arena_executor_url.rstrip('/')}/", task_id)
        status_url = urljoin(f"{self.settings.arena_executor_url.rstrip('/')}/", status_url)
        self._ensure_executor_origin(status_url)
        return await self._poll(task_id, status_url, headers)

    async def _poll(self, task_id: str, status_url: str, headers: dict[str, str]) -> ExecutionResult:
        deadline = time.monotonic() + self.settings.arena_executor_timeout_seconds
        last_state = "unknown"
        while time.monotonic() < deadline:
            try:
                response = await self._client.get(status_url, headers=headers)
                if response.status_code in {408, 429, 500, 502, 503, 504}:
                    await asyncio.sleep(self.settings.arena_executor_poll_seconds)
                    continue
                response.raise_for_status()
                data = response.json()
            except (httpx.HTTPError, ValueError) as exc:
                raise ExecutionError(f"Could not read executor status for task {task_id}") from exc
            if not isinstance(data, dict):
                raise ExecutionError("Executor status response must be an object")
            state = str(data.get("status", "")).casefold()
            last_state = state or last_state
            if self._is_completed(data):
                return await self._result_from_payload(data, fallback_task_id=task_id)
            if state in {"failed", "cancelled", "canceled", "expired"}:
                detail = str(data.get("error") or data.get("message") or state)
                raise ExecutionError(f"Executor task {task_id} ended as {state}: {detail[:500]}")
            await asyncio.sleep(self.settings.arena_executor_poll_seconds)
        raise ExecutionError(f"Executor task {task_id} timed out while {last_state}")

    async def _result_from_payload(self, payload: dict[str, Any], fallback_task_id: str) -> ExecutionResult:
        task_id = str(payload.get("task_id") or payload.get("id") or fallback_task_id)
        files_data = payload.get("files")
        if isinstance(files_data, list):
            files = tuple(self._file_from_json(item) for item in files_data)
        else:
            artifact_url = payload.get("artifact_url") or payload.get("archive_url")
            if not isinstance(artifact_url, str) or not artifact_url:
                raise ExecutionError("Completed task does not contain files or artifact_url")
            files = tuple(await self._download_zip(artifact_url))
        return ExecutionResult(task_id=task_id, files=validate_artifacts(files))

    def _file_from_json(self, item: Any) -> ArtifactFile:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ExecutionError("Executor files must contain string paths")
        path = validate_relative_path(item["path"])
        if isinstance(item.get("content_base64"), str):
            content = decode_base64(item["content_base64"], path)
        elif isinstance(item.get("content"), str):
            content = item["content"].encode("utf-8")
        else:
            raise ExecutionError(f"File {path} needs content or content_base64")
        return ArtifactFile(path=path, content=content)

    async def _download_zip(self, artifact_url: str) -> list[ArtifactFile]:
        artifact_url = urljoin(f"{self.settings.arena_executor_url.rstrip('/')}/", artifact_url)
        self._ensure_executor_origin(artifact_url)
        try:
            response = await self._client.get(artifact_url, headers=self._headers("artifact-download"))
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExecutionError("Could not download executor artifact archive") from exc
        if len(response.content) > MAX_TOTAL_BYTES:
            raise ExecutionError("Artifact archive exceeds compressed-size limit")
        try:
            archive = zipfile.ZipFile(io.BytesIO(response.content))
        except zipfile.BadZipFile as exc:
            raise ExecutionError("Executor artifact_url was not a valid ZIP archive") from exc
        files: list[ArtifactFile] = []
        total = 0
        with archive:
            members = [item for item in archive.infolist() if not item.is_dir()]
            if len(members) > MAX_FILE_COUNT:
                raise ExecutionError("Artifact archive has too many files")
            for member in members:
                path = validate_relative_path(member.filename)
                # Unix symlink bit: archives must contain ordinary files only.
                if (member.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ExecutionError(f"Artifact archive contains symlink: {path}")
                if member.file_size > MAX_FILE_BYTES:
                    raise ExecutionError(f"Artifact archive entry exceeds limit: {path}")
                total += member.file_size
                if total > MAX_TOTAL_BYTES:
                    raise ExecutionError("Artifact archive expands beyond total-size limit")
                with archive.open(member, "r") as opened:
                    content = opened.read(MAX_FILE_BYTES + 1)
                if len(content) != member.file_size or len(content) > MAX_FILE_BYTES:
                    raise ExecutionError(f"Artifact archive entry size mismatch: {path}")
                files.append(ArtifactFile(path=path, content=content))
        return files

    def _headers(self, idempotency_key: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.settings.secret_value(self.settings.arena_executor_token)}",
            "Content-Type": "application/json",
            "Idempotency-Key": idempotency_key,
        }

    def _ensure_executor_origin(self, candidate_url: str) -> None:
        configured = urlparse(self.settings.arena_executor_url or "")
        candidate = urlparse(candidate_url)
        if candidate.scheme != configured.scheme or candidate.netloc != configured.netloc:
            raise ExecutionError("Executor returned a status/artifact URL on a different origin")

    @staticmethod
    def _is_completed(payload: dict[str, Any]) -> bool:
        return str(payload.get("status", "")).casefold() in {"completed", "succeeded", "success"} or (
            "files" in payload and "status" not in payload
        )

    @staticmethod
    def _execution_instructions(job: FreelanceJob) -> str:
        return f"""Implement the client project below as a complete, runnable repository.
Project title: {job.title}

Requirements:
1. Implement all requested code; do not merely describe code or leave TODO placeholders.
2. Validate inputs, use robust error handling, and include focused automated tests.
3. Do not add credentials, scrape behind authentication without permission, bypass access controls, or make unsupported claims.
4. Generate a root README.md in Persian. It must explain prerequisites, installation, configuration, execution, tests, and known limitations.
5. Return every source file as UTF-8 text or base64 content with a relative path.
"""
