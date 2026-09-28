#!/usr/bin/env python3
"""Verify README SVG assets, report schemas and README local references."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from build_assets import ASSET_DIR, ASSETS, build_assets, load_context  # noqa: E402

from src.core.hub_router import HUB_ROUTER  # noqa: E402
from src.core.omni_catalog import OMNI_CATALOG  # noqa: E402
from src.core.reporting import (  # noqa: E402
    read_json_report,
    validate_full_fleet_report,
    validate_low_resource_report,
)

FLEET_REPORT = ROOT / "tests" / "FULL_FLEET_TEST_REPORT.json"
BENCH_REPORT = ROOT / "tests" / "LOW_RESOURCE_BENCHMARK_REPORT.json"
README = ROOT / "README.md"
SVG_NS = "{http://www.w3.org/2000/svg}"
FORBIDDEN_SVG_TOKENS = ("<script", "<foreignObject", "xlink:href", " href=", "url(http")


def _asset_files() -> list[Path]:
    return [ASSET_DIR / name for name in sorted(ASSETS)]


def verify_expected_assets_exist() -> None:
    missing = [str(path.relative_to(ROOT)) for path in _asset_files() if not path.exists()]
    if missing:
        raise AssertionError(f"missing README assets: {missing}")


def verify_svg_xml_accessibility() -> None:
    for path in _asset_files():
        raw = path.read_text(encoding="utf-8")
        lowered = raw.lower()
        forbidden = [token for token in FORBIDDEN_SVG_TOKENS if token.lower() in lowered]
        if forbidden:
            raise AssertionError(f"{path.name} contains Camo-unsafe tokens: {forbidden}")
        root = ET.fromstring(raw)
        if root.tag != f"{SVG_NS}svg":
            raise AssertionError(f"{path.name} root is not svg")
        if root.attrib.get("role") != "img":
            raise AssertionError(f"{path.name} missing role=img")
        if "aria-labelledby" not in root.attrib:
            raise AssertionError(f"{path.name} missing aria-labelledby")
        if "viewBox" not in root.attrib or root.attrib.get("width") != "100%":
            raise AssertionError(f"{path.name} missing responsive viewBox/width")
        if root.find(f"{SVG_NS}title") is None or root.find(f"{SVG_NS}desc") is None:
            raise AssertionError(f"{path.name} missing title or desc")
        drawable_count = sum(
            len(root.findall(f".//{SVG_NS}{tag}")) for tag in ("path", "rect", "circle", "text")
        )
        if drawable_count < 5:
            raise AssertionError(f"{path.name} has too few vector elements")


def _slugify_heading(text: str) -> str:
    slug = re.sub(r"<[^>]+>", "", text).strip().lower()
    slug = re.sub(r"[`*_]", "", slug)
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug


def verify_readme_paths_and_anchors() -> None:
    if not README.exists():
        return
    raw = README.read_text(encoding="utf-8")
    paths = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", raw))
    paths.update(re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", raw))
    links = set(re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", raw))

    headings = set()
    for line in raw.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            headings.add(_slugify_heading(match.group(2)))

    for value in sorted(paths | links):
        parsed = urlparse(value)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue
        target = unquote(parsed.path)
        fragment = parsed.fragment
        if target:
            candidate = (ROOT / target).resolve()
            if ROOT not in candidate.parents and candidate != ROOT:
                raise AssertionError(f"README path escapes repository: {value}")
            if not candidate.exists():
                raise AssertionError(f"README references missing path: {value}")
        if fragment and not target:
            if fragment not in headings:
                raise AssertionError(f"README references missing anchor: #{fragment}")


def verify_manifest_counts() -> None:
    ctx = load_context()
    if ctx.total != 445 or len(ctx.hubs) != 15:
        raise AssertionError("catalogue or hub total changed unexpectedly")
    if sum(hub.count for hub in ctx.hubs) != len(OMNI_CATALOG):
        raise AssertionError("hub counts do not sum to catalogue total")
    current_counts = {key: hub["bot_count"] for key, hub in HUB_ROUTER.get_hub_summary().items()}
    if current_counts != {hub.key: hub.count for hub in ctx.hubs}:
        raise AssertionError("asset context hub counts diverge from router")


def verify_report_schemas() -> None:
    validate_full_fleet_report(read_json_report(FLEET_REPORT), expected_total=len(OMNI_CATALOG))
    validate_low_resource_report(read_json_report(BENCH_REPORT), expected_total=len(OMNI_CATALOG))


def verify_deterministic_generation() -> None:
    tracked = _asset_files()
    before = {path: path.read_text(encoding="utf-8") for path in tracked}
    build_assets()
    first = {path: path.read_text(encoding="utf-8") for path in tracked}
    if before != first:
        changed = [str(path.relative_to(ROOT)) for path in tracked if before[path] != first[path]]
        raise AssertionError(f"assets were not up to date before verification: {changed}")
    build_assets()
    second = {path: path.read_text(encoding="utf-8") for path in tracked}
    if first != second:
        changed = [str(path.relative_to(ROOT)) for path in tracked if first[path] != second[path]]
        raise AssertionError(f"asset generation is not deterministic: {changed}")


def main() -> None:
    verify_expected_assets_exist()
    verify_svg_xml_accessibility()
    verify_manifest_counts()
    verify_report_schemas()
    verify_readme_paths_and_anchors()
    verify_deterministic_generation()
    print(f"verified {len(ASSETS)} README SVG assets, report schemas, README paths and deterministic generation")


if __name__ == "__main__":
    main()
