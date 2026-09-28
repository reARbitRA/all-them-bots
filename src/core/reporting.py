"""Report metadata and schema validation utilities for FABLE OMEGA artifacts."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip() or "unknown"


def _memory_metadata() -> dict[str, float | None]:
    total_mb: float | None = None
    available_mb: float | None = None

    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        values: dict[str, int] = {}
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                values[parts[0].rstrip(":")] = int(parts[1])
        if "MemTotal" in values:
            total_mb = round(values["MemTotal"] / 1024.0, 2)
        if "MemAvailable" in values:
            available_mb = round(values["MemAvailable"] / 1024.0, 2)
    elif hasattr(os, "sysconf"):
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            total_mb = round((pages * page_size) / (1024.0 * 1024.0), 2)
        except (OSError, ValueError):
            pass

    return {"total_memory_mb": total_mb, "available_memory_mb": available_mb}


def collect_environment_metadata(root: Path | None = None) -> dict[str, Any]:
    """Return reproducibility metadata stored with committed reports."""
    repo_root = root or Path(__file__).resolve().parents[2]
    git_status = _run_git(repo_root, "status", "--porcelain")

    return {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
        "cpu_count": os.cpu_count(),
        **_memory_metadata(),
        "commit": _run_git(repo_root, "rev-parse", "HEAD"),
        "branch": _run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD"),
        "working_tree_dirty": bool(git_status and git_status != "unknown"),
    }


def read_json_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_full_fleet_report(report: dict[str, Any], expected_total: int = 445) -> None:
    required = {
        "report_schema_version",
        "timestamp",
        "environment",
        "catalogue",
        "total_bots_tested",
        "passed_count",
        "failed_count",
        "success_rate_percent",
        "total_duration_seconds",
        "avg_bot_lifecycle_latency_ms",
        "test_results",
    }
    missing = required - set(report)
    if missing:
        raise AssertionError(f"FULL_FLEET_TEST_REPORT missing keys: {sorted(missing)}")

    if report["total_bots_tested"] != expected_total:
        raise AssertionError(f"expected {expected_total} catalogue tests, got {report['total_bots_tested']}")
    if report["passed_count"] + report["failed_count"] != report["total_bots_tested"]:
        raise AssertionError("fleet passed + failed count does not match total")
    if len(report["test_results"]) != report["total_bots_tested"]:
        raise AssertionError("fleet test_results length does not match total")

    catalogue = report["catalogue"]
    if catalogue.get("total_entries") != expected_total:
        raise AssertionError("catalogue.total_entries does not match expected total")
    if sum(catalogue.get("source_counts", {}).values()) != expected_total:
        raise AssertionError("catalogue source counts do not add up to expected total")

    environment = report["environment"]
    for key in ("generated_at_utc", "python_version", "platform", "commit", "branch"):
        if not environment.get(key):
            raise AssertionError(f"environment.{key} is required")

    for item in report["test_results"]:
        if item.get("total_stages") != 5:
            raise AssertionError(f"{item.get('bot_id')} did not record the 5-stage lifecycle")


def validate_low_resource_report(report: dict[str, Any], expected_total: int = 445) -> None:
    required = {
        "report_schema_version",
        "timestamp",
        "environment",
        "catalogue",
        "test_parameters",
        "total_requests",
        "concurrency",
        "success_rate_percent",
        "total_time_seconds",
        "throughput_rps",
        "latencies_ms",
        "bot_pool",
        "resource_footprint",
    }
    missing = required - set(report)
    if missing:
        raise AssertionError(f"LOW_RESOURCE_BENCHMARK_REPORT missing keys: {sorted(missing)}")

    if report["catalogue"].get("total_entries") != expected_total:
        raise AssertionError("benchmark catalogue total does not match expected total")
    if report["total_requests"] != report["test_parameters"].get("total_requests"):
        raise AssertionError("benchmark request count differs from test parameters")
    if report["concurrency"] != report["test_parameters"].get("concurrency"):
        raise AssertionError("benchmark concurrency differs from test parameters")

    for key in ("avg", "p50", "p95", "p99", "event_loop_lag"):
        if key not in report["latencies_ms"]:
            raise AssertionError(f"latencies_ms.{key} is required")
    for key in ("initial_rss_mb", "under_load_rss_mb", "post_gc_rss_mb", "peak_rss_mb"):
        if key not in report["resource_footprint"]:
            raise AssertionError(f"resource_footprint.{key} is required")
    for key in ("generated_at_utc", "python_version", "platform", "commit", "branch"):
        if not report["environment"].get(key):
            raise AssertionError(f"environment.{key} is required")
