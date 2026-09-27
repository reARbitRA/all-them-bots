"""Optional authenticated FastAPI control plane for an operator's scheduler/dashboard."""

from __future__ import annotations

import hmac
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import asdict

from fastapi import Depends, FastAPI, HTTPException, Request, status

from .runtime import Runtime


def create_app(runtime: Runtime) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await runtime.initialize()
        try:
            yield
        finally:
            await runtime.close()

    app = FastAPI(
        title="Autofreelance Pipeline",
        version="0.1.0",
        description="Control plane for a compliant, authorized freelance delivery worker.",
        lifespan=lifespan,
    )

    async def require_key(request: Request) -> None:
        configured = runtime.settings.secret_value(runtime.settings.service_api_key)
        if not configured:
            return
        supplied = request.headers.get("Authorization", "").removeprefix("Bearer ")
        if not hmac.compare_digest(supplied, configured):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    @app.get("/healthz")
    async def health() -> dict[str, object]:
        return {
            "ok": True,
            "automation_enabled": runtime.settings.automation_enabled,
            "platforms": list(runtime.pipeline.platforms),
        }

    @app.post("/v1/cycles", dependencies=[Depends(require_key)])
    async def run_cycle() -> dict[str, int]:
        return asdict(await runtime.pipeline.run_once())

    @app.get("/v1/jobs", dependencies=[Depends(require_key)])
    async def list_jobs(limit: int = 100) -> list[dict[str, object]]:
        if not 1 <= limit <= 500:
            raise HTTPException(status_code=422, detail="limit must be between 1 and 500")
        records = await runtime.store.recent(limit)
        # Do not expose full client descriptions or generated proposals from an operational endpoint.
        return [
            {
                "key": record.key,
                "platform": record.platform,
                "external_id": record.external_id,
                "title": record.title,
                "url": record.url,
                "status": record.status.value,
                "github_url": record.github_url,
                "error": record.error,
                "updated_at": record.updated_at.isoformat(),
            }
            for record in records
        ]

    @app.post("/v1/jobs/{platform}/{external_id}/retry", dependencies=[Depends(require_key)])
    async def retry_job(platform: str, external_id: str) -> dict[str, bool]:
        changed = await runtime.pipeline.retry(platform, external_id)
        if not changed:
            raise HTTPException(status_code=409, detail="Job is not in a retryable failed state")
        return {"retry_scheduled": True}

    return app
