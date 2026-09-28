from __future__ import annotations

import httpx
import pytest

from src.autofreelance.clients.executor import ArenaExecutionGatewayClient
from src.autofreelance.config import Settings
from src.autofreelance.models import FreelanceJob


@pytest.mark.asyncio
async def test_executor_polls_and_decodes_inline_files():
    calls: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        if request.method == "POST":
            assert request.headers["Idempotency-Key"] == "ponisha:77"
            return httpx.Response(202, json={"task_id": "task-1", "status": "queued", "status_url": "/v1/tasks/task-1"})
        return httpx.Response(
            200,
            json={
                "task_id": "task-1",
                "status": "completed",
                "files": [
                    {"path": "README.md", "content": "# راهنمای اجرا\nبرای اجرا دستور زیر را اجرا کنید."},
                    {"path": "main.py", "content": "print('ok')\n"},
                ],
            },
        )

    settings = Settings(
        arena_executor_url="https://executor.test/v1/tasks",
        arena_executor_token="token",
        github_token="github-token",
        github_owner="owner",
        arena_executor_poll_seconds=1,
    )
    client = ArenaExecutionGatewayClient(settings, httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    result = await client.execute(FreelanceJob("ponisha", "77", "https://ponisha.ir/project/77", "test", "desc"))
    assert result.task_id == "task-1"
    assert [item.path for item in result.files] == ["README.md", "main.py"]
    assert calls == ["https://executor.test/v1/tasks", "https://executor.test/v1/tasks/task-1"]
    await client.close()
