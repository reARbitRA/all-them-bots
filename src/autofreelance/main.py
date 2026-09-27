"""CLI entry point for a one-shot, daemon worker, or FastAPI control plane."""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import asdict

import uvicorn

from .api import create_app
from .config import Settings
from .logging import configure_logging
from .runtime import build_runtime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Authorized freelance delivery pipeline")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="Run exactly one bounded pipeline cycle")
    mode.add_argument("--serve", action="store_true", help="Run the authenticated FastAPI control plane")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP bind address for --serve")
    parser.add_argument("--port", default=8000, type=int, help="HTTP port for --serve")
    return parser.parse_args()


async def _run_once() -> int:
    settings = Settings()
    configure_logging(settings.log_level)
    runtime = build_runtime(settings)
    await runtime.initialize()
    try:
        summary = await runtime.pipeline.run_once()
        print(asdict(summary))
        return 0
    finally:
        await runtime.close()


async def _run_worker() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    runtime = build_runtime(settings)
    await runtime.initialize()
    try:
        await runtime.pipeline.run_forever()
    finally:
        await runtime.close()


def main() -> None:
    args = parse_args()
    if args.serve:
        settings = Settings()
        configure_logging(settings.log_level)
        runtime = build_runtime(settings)
        uvicorn.run(create_app(runtime), host=args.host, port=args.port, log_level=settings.log_level.lower())
        return
    if args.once:
        raise SystemExit(asyncio.run(_run_once()))
    try:
        asyncio.run(_run_worker())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
