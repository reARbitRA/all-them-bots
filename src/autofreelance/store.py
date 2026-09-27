"""Durable SQLite state and compare-and-swap transitions for idempotent polling."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiosqlite

from .models import FreelanceJob, JobRecord, JobStatus

_SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS jobs (
    platform TEXT NOT NULL,
    external_id TEXT NOT NULL,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    budget_text TEXT,
    status TEXT NOT NULL,
    github_url TEXT,
    artifact_dir TEXT,
    error TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    PRIMARY KEY(platform, external_id)
);
CREATE INDEX IF NOT EXISTS idx_jobs_status_updated ON jobs(status, updated_at);
CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    external_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_job ON audit_events(platform, external_id, created_at);
"""


class JobStore:
    """Minimal persistent state store; a status can only advance through a CAS transition."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    async def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.database_path) as db:
            await db.executescript(_SCHEMA)
            await db.commit()

    async def save_discovered(self, job: FreelanceJob) -> JobRecord:
        now = _now()
        async with self._connect() as db:
            await db.execute(
                """
                INSERT INTO jobs(platform, external_id, url, title, description, budget_text, status,
                                 created_at, updated_at, last_seen_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(platform, external_id) DO UPDATE SET
                    url = excluded.url,
                    title = excluded.title,
                    description = excluded.description,
                    budget_text = excluded.budget_text,
                    last_seen_at = excluded.last_seen_at
                """,
                (
                    job.platform,
                    job.external_id,
                    job.url,
                    job.title,
                    job.description,
                    job.budget_text,
                    JobStatus.DISCOVERED.value,
                    now,
                    now,
                    now,
                ),
            )
            await self._audit(db, job.platform, job.external_id, "discovered", {"url": job.url})
            await db.commit()
        record = await self.get(job.platform, job.external_id)
        assert record is not None
        return record

    async def get(self, platform: str, external_id: str) -> JobRecord | None:
        async with self._connect() as db:
            cursor = await db.execute(
                "SELECT * FROM jobs WHERE platform = ? AND external_id = ?", (platform, external_id)
            )
            row = await cursor.fetchone()
        return self._record(row) if row else None

    async def list_by_status(self, statuses: Iterable[JobStatus], limit: int = 100) -> list[JobRecord]:
        values = tuple(status.value for status in statuses)
        if not values:
            return []
        placeholders = ", ".join("?" for _ in values)
        async with self._connect() as db:
            cursor = await db.execute(
                f"SELECT * FROM jobs WHERE status IN ({placeholders}) ORDER BY updated_at ASC LIMIT ?",
                (*values, limit),
            )
            rows = await cursor.fetchall()
        return [self._record(row) for row in rows]

    async def recent(self, limit: int = 100) -> list[JobRecord]:
        async with self._connect() as db:
            cursor = await db.execute(
                "SELECT * FROM jobs ORDER BY updated_at DESC LIMIT ?", (limit,)
            )
            rows = await cursor.fetchall()
        return [self._record(row) for row in rows]

    async def transition(
        self,
        platform: str,
        external_id: str,
        expected: Iterable[JobStatus],
        target: JobStatus,
        *,
        error: str | None = None,
        github_url: str | None = None,
        artifact_dir: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Transition only when the current status is one of ``expected``.

        It is the key idempotency primitive: concurrent web/API workers cannot submit
        the same bid or deliver the same source link after another worker has claimed it.
        """
        expected_values = tuple(item.value for item in expected)
        if not expected_values:
            raise ValueError("Transition needs at least one expected state")
        now = _now()
        placeholders = ", ".join("?" for _ in expected_values)
        async with self._connect() as db:
            cursor = await db.execute(
                f"""
                UPDATE jobs
                SET status = ?, error = ?,
                    github_url = COALESCE(?, github_url),
                    artifact_dir = COALESCE(?, artifact_dir),
                    metadata_json = CASE WHEN ? IS NULL THEN metadata_json ELSE ? END,
                    updated_at = ?
                WHERE platform = ? AND external_id = ? AND status IN ({placeholders})
                """,
                (
                    target.value,
                    error,
                    github_url,
                    artifact_dir,
                    None if metadata is None else "present",
                    json.dumps(metadata, ensure_ascii=False, separators=(",", ":"))
                    if metadata is not None
                    else None,
                    now,
                    platform,
                    external_id,
                    *expected_values,
                ),
            )
            changed = cursor.rowcount == 1
            if changed:
                await self._audit(
                    db,
                    platform,
                    external_id,
                    "transition",
                    {"from": list(expected_values), "to": target.value, "error": error},
                )
            await db.commit()
        return changed

    async def append_event(
        self, platform: str, external_id: str, event_type: str, details: dict[str, Any] | None = None
    ) -> None:
        async with self._connect() as db:
            await self._audit(db, platform, external_id, event_type, details or {})
            await db.commit()

    async def reset_for_retry(self, platform: str, external_id: str) -> bool:
        """Move a failed action back to its immediately safe predecessor state."""
        retry_map = {
            JobStatus.CLASSIFICATION_FAILED: JobStatus.DISCOVERED,
            JobStatus.BID_FAILED: JobStatus.READY_FOR_REVIEW,
            JobStatus.EXECUTION_FAILED: JobStatus.AWARDED,
            JobStatus.PUBLISHING_FAILED: JobStatus.ARTIFACTS_READY,
            JobStatus.DELIVERY_FAILED: JobStatus.CODE_PUBLISHED,
        }
        record = await self.get(platform, external_id)
        if record is None or record.status not in retry_map:
            return False
        return await self.transition(
            platform,
            external_id,
            (record.status,),
            retry_map[record.status],
            error=None,
        )

    @asynccontextmanager
    async def _connect(self) -> AsyncIterator[aiosqlite.Connection]:
        connection = await aiosqlite.connect(self.database_path)
        connection.row_factory = aiosqlite.Row
        try:
            yield connection
        finally:
            await connection.close()

    async def _audit(
        self,
        db: aiosqlite.Connection,
        platform: str,
        external_id: str,
        event_type: str,
        details: dict[str, Any],
    ) -> None:
        await db.execute(
            """
            INSERT INTO audit_events(platform, external_id, event_type, details_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (platform, external_id, event_type, json.dumps(details, ensure_ascii=False), _now()),
        )

    @staticmethod
    def _record(row: aiosqlite.Row | tuple[Any, ...]) -> JobRecord:
        values = dict(row) if isinstance(row, aiosqlite.Row) else row
        return JobRecord(
            platform=values["platform"],
            external_id=values["external_id"],
            url=values["url"],
            title=values["title"],
            description=values["description"],
            budget_text=values["budget_text"],
            status=JobStatus(values["status"]),
            github_url=values["github_url"],
            artifact_dir=values["artifact_dir"],
            error=values["error"],
            metadata=json.loads(values["metadata_json"]),
            updated_at=datetime.fromisoformat(values["updated_at"]),
        )


def _now() -> str:
    return datetime.now(UTC).isoformat()
