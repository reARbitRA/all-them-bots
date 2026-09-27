"""Composition root for the service; creates optional clients only when configured."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from .browser import CdpBrowser
from .clients.executor import ArenaExecutionGatewayClient
from .clients.github import GitHubPublisher
from .clients.llm import FastLLMClient
from .config import Settings
from .pipeline import FreelancePipeline
from .platforms import create_platforms
from .store import JobStore

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Runtime:
    settings: Settings
    browser: CdpBrowser
    store: JobStore
    pipeline: FreelancePipeline
    classifier: FastLLMClient | None
    executor: ArenaExecutionGatewayClient | None

    async def initialize(self) -> None:
        await self.store.initialize()

    async def close(self) -> None:
        if self.classifier:
            await self.classifier.close()
        if self.executor:
            await self.executor.close()
        await self.browser.close()


def build_runtime(settings: Settings) -> Runtime:
    browser = CdpBrowser(settings)
    store = JobStore(settings.database_path)
    classifier = None
    if settings.llm_api_url and settings.llm_api_key:
        classifier = FastLLMClient(settings)
    elif settings.automation_enabled:
        logger.warning("llm_not_configured_discovery_only")

    executor = None
    github = None
    execution_values = (
        settings.arena_executor_url,
        settings.arena_executor_token,
        settings.github_token,
        settings.github_owner,
    )
    if all(execution_values):
        executor = ArenaExecutionGatewayClient(settings)
        github = GitHubPublisher(settings)
    elif any(execution_values):
        logger.warning("execution_configuration_incomplete")

    pipeline = FreelancePipeline(
        settings=settings,
        store=store,
        platforms=create_platforms(browser, settings),
        classifier=classifier,
        executor=executor,
        github=github,
    )
    return Runtime(
        settings=settings,
        browser=browser,
        store=store,
        pipeline=pipeline,
        classifier=classifier,
        executor=executor,
    )
