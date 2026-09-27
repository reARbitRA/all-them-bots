"""GitHub publisher using PyGithub's Git database API for one atomic project commit."""

from __future__ import annotations

import asyncio
import base64
import logging
import time
from dataclasses import dataclass

from github import Github, GithubException, InputGitTreeElement

from ..artifacts import validate_artifacts
from ..config import Settings
from ..exceptions import GitHubDeliveryError
from ..models import ArtifactFile, FreelanceJob
from ..text import repository_slug, url_fingerprint

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class GitHubPublication:
    repository_url: str
    branch: str
    path_prefix: str
    commit_sha: str


class GitHubPublisher:
    """Create project repositories or atomically append to one configured delivery repository."""

    def __init__(self, settings: Settings) -> None:
        settings.require_execution()
        self.settings = settings

    async def publish(self, job: FreelanceJob, files: tuple[ArtifactFile, ...]) -> GitHubPublication:
        checked = validate_artifacts(files)
        return await asyncio.to_thread(self._publish_sync, job, checked)

    def _publish_sync(self, job: FreelanceJob, files: tuple[ArtifactFile, ...]) -> GitHubPublication:
        token = self.settings.secret_value(self.settings.github_token)
        assert token is not None
        github = Github(login_or_token=token, timeout=30)
        try:
            owner = self.settings.github_owner
            assert owner is not None
            target_repo = self.settings.github_delivery_repository
            if target_repo:
                repo = self._get_existing_repo(github, owner, target_repo)
                prefix = f"deliveries/{job.platform}/{url_fingerprint(job.key)}/"
            else:
                repo = self._create_project_repo(github, owner, job)
                prefix = ""
            commit_sha = self._commit_files(repo, files, prefix, job)
            repo_url = repo.html_url
            if prefix:
                repo_url = f"{repo_url}/tree/{self.settings.github_branch}/{prefix.rstrip('/')}"
            logger.info("github_published", extra={"job_key": job.key, "repository_url": repo_url})
            return GitHubPublication(
                repository_url=repo_url,
                branch=self.settings.github_branch,
                path_prefix=prefix,
                commit_sha=commit_sha,
            )
        except GithubException as exc:
            detail = exc.data.get("message", str(exc)) if isinstance(exc.data, dict) else str(exc)
            raise GitHubDeliveryError(f"GitHub API failed ({exc.status}): {detail}") from exc
        except Exception as exc:
            if isinstance(exc, GitHubDeliveryError):
                raise
            raise GitHubDeliveryError("GitHub publication failed") from exc
        finally:
            github.close()

    def _get_existing_repo(self, github: Github, configured_owner: str, configured_repo: str):
        if "/" in configured_repo:
            supplied_owner, repo_name = configured_repo.split("/", 1)
            if supplied_owner.lower() != configured_owner.lower():
                raise GitHubDeliveryError("GITHUB_DELIVERY_REPOSITORY owner must match GITHUB_OWNER")
        else:
            repo_name = configured_repo
        return github.get_repo(f"{configured_owner}/{repo_name}")

    def _create_project_repo(self, github: Github, owner: str, job: FreelanceJob):
        requested = repository_slug(job.title, job.external_id)
        for suffix in ("", "-2", "-3"):
            name = f"{requested[:96-len(suffix)]}{suffix}"
            try:
                if self._owner_is_current_user(github, owner):
                    return github.get_user().create_repo(
                        name=name,
                        description=f"Freelance delivery for {job.platform}:{job.external_id}",
                        private=self.settings.github_private,
                        auto_init=False,
                    )
                return github.get_organization(owner).create_repo(
                    name=name,
                    description=f"Freelance delivery for {job.platform}:{job.external_id}",
                    private=self.settings.github_private,
                    auto_init=False,
                )
            except GithubException as exc:
                if exc.status == 422 and suffix != "-3":
                    continue
                raise
        raise GitHubDeliveryError("Could not allocate a unique delivery repository name")

    @staticmethod
    def _owner_is_current_user(github: Github, owner: str) -> bool:
        return github.get_user().login.casefold() == owner.casefold()

    def _commit_files(self, repo, files: tuple[ArtifactFile, ...], prefix: str, job: FreelanceJob) -> str:
        """Write all files in one Git commit rather than one REST request per source file."""
        elements: list[InputGitTreeElement] = []
        for file in files:
            blob = repo.create_git_blob(base64.b64encode(file.content).decode("ascii"), "base64")
            elements.append(
                InputGitTreeElement(
                    path=f"{prefix}{file.path}",
                    mode="100644",
                    type="blob",
                    sha=blob.sha,
                )
            )
        branch_ref_name = f"heads/{self.settings.github_branch}"
        message = f"Deliver {job.platform} project {job.external_id}"
        # Ref updates are optimistic: a shared delivery repo may receive another project
        # between our read and edit. Rebuild from the latest tree a bounded number of times.
        for attempt in range(3):
            try:
                ref = repo.get_git_ref(branch_ref_name)
            except GithubException as exc:
                if exc.status not in {404, 409}:
                    raise
                tree = repo.create_git_tree(elements)
                commit = repo.create_git_commit(f"Initial {message.lower()}", tree, [])
                try:
                    repo.create_git_ref(f"refs/{branch_ref_name}", commit.sha)
                    return commit.sha
                except GithubException as ref_exc:
                    if ref_exc.status in {409, 422} and attempt < 2:
                        time.sleep(1 + attempt)
                        continue
                    raise
            else:
                parent = repo.get_git_commit(ref.object.sha)
                tree = repo.create_git_tree(elements, base_tree=parent.tree)
                commit = repo.create_git_commit(message, tree, [parent])
                try:
                    ref.edit(commit.sha, force=False)
                    return commit.sha
                except GithubException as exc:
                    if exc.status in {409, 422} and attempt < 2:
                        time.sleep(1 + attempt)
                        continue
                    raise
        raise GitHubDeliveryError("GitHub branch changed too often to publish safely")
