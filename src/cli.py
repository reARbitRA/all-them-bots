"""Command-line entry point for the FABLE OMEGA control plane."""

from __future__ import annotations

import argparse

import uvicorn

from src.core.config import CONFIG


def main() -> None:
    """Launch the FastAPI dashboard and scenario runtime."""
    parser = argparse.ArgumentParser(description="FABLE OMEGA multi-tenant scenario runtime")
    parser.add_argument("--host", default=CONFIG.server_host, help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=CONFIG.server_port, help="Bind port (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloader for development")
    args = parser.parse_args()

    print("=" * 65)
    print("⚡ FABLE OMEGA CONTROL PLANE STARTING")
    print("=" * 65)
    print(f"📡 Server Binding: http://{args.host}:{args.port}")
    print(f"📊 Dashboard:      http://{args.host}:{args.port}/")
    print(f"🔗 Health Probe:   http://{args.host}:{args.port}/healthz")
    print("=" * 65)

    uvicorn.run(
        "src.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        access_log=True,
    )


if __name__ == "__main__":
    main()
