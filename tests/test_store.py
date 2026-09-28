from __future__ import annotations

import pytest

from src.autofreelance.models import FreelanceJob, JobStatus
from src.autofreelance.store import JobStore


@pytest.mark.asyncio
async def test_compare_and_swap_prevents_double_claim(tmp_path):
    store = JobStore(tmp_path / "state.sqlite3")
    await store.initialize()
    job = FreelanceJob("test", "42", "https://example.test/jobs/42", "title", "description")
    await store.save_discovered(job)

    first = await store.transition("test", "42", (JobStatus.DISCOVERED,), JobStatus.BIDDING)
    second = await store.transition("test", "42", (JobStatus.DISCOVERED,), JobStatus.BIDDING)

    assert first is True
    assert second is False
    assert (await store.get("test", "42")).status == JobStatus.BIDDING
