"""Strongly typed values shared by browser strategies, APIs, and persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class JobStatus(StrEnum):
    DISCOVERED = "discovered"
    INELIGIBLE = "ineligible"
    CLASSIFICATION_FAILED = "classification_failed"
    READY_FOR_REVIEW = "ready_for_review"
    BIDDING = "bidding"
    BID_SUBMITTED = "bid_submitted"
    BID_FAILED = "bid_failed"
    AWARDED = "awarded"
    EXECUTING = "executing"
    EXECUTION_FAILED = "execution_failed"
    ARTIFACTS_READY = "artifacts_ready"
    PUBLISHING = "publishing"
    PUBLISHING_FAILED = "publishing_failed"
    CODE_PUBLISHED = "code_published"
    DELIVERING = "delivering"
    DELIVERY_FAILED = "delivery_failed"
    DELIVERED = "delivered"


@dataclass(frozen=True, slots=True)
class FreelanceJob:
    platform: str
    external_id: str
    url: str
    title: str
    description: str
    budget_text: str | None = None
    discovered_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def key(self) -> str:
        return f"{self.platform}:{self.external_id}"


@dataclass(frozen=True, slots=True)
class EligibilityDecision:
    automatable: bool
    confidence: float
    rationale: str
    risks: tuple[str, ...]
    proposal_fa: str | None
    estimated_days: int | None = None


@dataclass(frozen=True, slots=True)
class ArtifactFile:
    path: str
    content: bytes


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    task_id: str
    files: tuple[ArtifactFile, ...]


@dataclass(frozen=True, slots=True)
class JobRecord:
    platform: str
    external_id: str
    url: str
    title: str
    description: str
    budget_text: str | None
    status: JobStatus
    github_url: str | None
    artifact_dir: str | None
    error: str | None
    metadata: dict[str, Any]
    updated_at: datetime

    @property
    def key(self) -> str:
        return f"{self.platform}:{self.external_id}"
