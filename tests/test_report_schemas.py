from __future__ import annotations

from pathlib import Path

from src.core.omni_catalog import OMNI_CATALOG
from src.core.reporting import (
    read_json_report,
    validate_full_fleet_report,
    validate_low_resource_report,
)

ROOT = Path(__file__).resolve().parent.parent


def test_full_fleet_report_schema_matches_catalogue() -> None:
    report = read_json_report(ROOT / "tests" / "FULL_FLEET_TEST_REPORT.json")
    validate_full_fleet_report(report, expected_total=len(OMNI_CATALOG))


def test_low_resource_report_schema_matches_catalogue() -> None:
    report = read_json_report(ROOT / "tests" / "LOW_RESOURCE_BENCHMARK_REPORT.json")
    validate_low_resource_report(report, expected_total=len(OMNI_CATALOG))
