#!/usr/bin/env python3
"""
Fable-Omega Bot Fleet Master Entrypoint & CLI Orchestrator
Launches the Webhook Server, Live Control Dashboard, and Multi-Tenant Engine.
"""

import sys
import os
import argparse
import uvicorn
from src.core.config import CONFIG


def main():
    parser = argparse.ArgumentParser(description="Fable-Omega Multi-Tenant Bot Fleet Launcher")
    parser.add_argument("--host", default=CONFIG.server_host, help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=CONFIG.server_port, help="Bind port (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloader for development")

    args = parser.parse_args()

    print("=" * 65)
    print("⚡ FABLE-OMEGA BOT FLEET & CONTROL CENTER STARTING...")
    print("=" * 65)
    print(f"📡 Server Binding: http://{args.host}:{args.port}")
    print(f"📊 Live Dashboard: http://{args.host}:{args.port}/")
    print(f"🔗 Health Probe:   http://{args.host}:{args.port}/healthz")
    print("=" * 65)

    uvicorn.run(
        "src.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        access_log=True
    )


if __name__ == "__main__":
    main()
