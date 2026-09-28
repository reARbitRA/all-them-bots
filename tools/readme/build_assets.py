#!/usr/bin/env python3
"""Generate deterministic README SVG assets for the FABLE OMEGA presentation."""

from __future__ import annotations

import math
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.hub_router import HUB_ROUTER  # noqa: E402
from src.core.omni_catalog import (  # noqa: E402
    OMNI_CATALOG,
    extract_ai_businesses,
    extract_chatgpt_150,
    extract_gemini_730,
    extract_opus_150,
    extract_rubika_56,
)
from src.core.reporting import (  # noqa: E402
    read_json_report,
    validate_full_fleet_report,
    validate_low_resource_report,
)

ASSET_DIR = ROOT / "assets" / "readme"
FLEET_REPORT = ROOT / "tests" / "FULL_FLEET_TEST_REPORT.json"
BENCH_REPORT = ROOT / "tests" / "LOW_RESOURCE_BENCHMARK_REPORT.json"

KERNEL_BLACK = "#07090C"
OMEGA_CYAN = "#22D3EE"
TELEGRAM_BLUE = "#2AABEE"
BILLING_VIOLET = "#8B5CF6"
RUNTIME_GREEN = "#34D399"
INK = "#E6F7FB"
MUTED = "#93A4B7"
GRID = "#162130"
AMBER = "#FBBF24"
RED = "#F87171"


@dataclass(frozen=True)
class HubRow:
    key: str
    index: int
    title: str
    category: str
    username: str
    count: int


@dataclass(frozen=True)
class AssetContext:
    total: int
    source_counts: dict[str, int]
    hubs: list[HubRow]
    fleet_report: dict[str, Any]
    benchmark_report: dict[str, Any]


def _clean_title(title: str) -> str:
    title = re.sub(r"^[^\w\d]+\s*", "", title).strip()
    title = re.sub(r"\s*\([^)]*\)", "", title).strip()
    return title


def load_context() -> AssetContext:
    fleet = read_json_report(FLEET_REPORT)
    benchmark = read_json_report(BENCH_REPORT)
    validate_full_fleet_report(fleet, expected_total=len(OMNI_CATALOG))
    validate_low_resource_report(benchmark, expected_total=len(OMNI_CATALOG))

    hub_summary = HUB_ROUTER.get_hub_summary()
    hubs = []
    for index, (key, info) in enumerate(hub_summary.items(), start=1):
        hubs.append(
            HubRow(
                key=key,
                index=index,
                title=_clean_title(str(info["title"])),
                category=str(info["category"]),
                username="@" + str(info["bot_father_username"]),
                count=int(info["bot_count"]),
            )
        )

    source_counts = {
        "Opus": len(extract_opus_150()),
        "ChatGPT": len(extract_chatgpt_150()),
        "Gemini": len(extract_gemini_730()),
        "Rubika/Baleh": len(extract_rubika_56()),
        "AI taxonomy": len(extract_ai_businesses()),
    }

    return AssetContext(
        total=len(OMNI_CATALOG),
        source_counts=source_counts,
        hubs=hubs,
        fleet_report=fleet,
        benchmark_report=benchmark,
    )


def svg_shell(title: str, desc: str, body: str, width: int = 1200, height: int = 630) -> str:
    title_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") + "-title"
    desc_id = title_id.replace("-title", "-desc")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{title_id} {desc_id}" width="100%" height="auto" viewBox="0 0 {width} {height}" preserveAspectRatio="xMidYMid meet">
  <title id="{title_id}">{escape(title)}</title>
  <desc id="{desc_id}">{escape(desc)}</desc>
  <defs>
    <linearGradient id="g-cyan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{OMEGA_CYAN}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{TELEGRAM_BLUE}" stop-opacity="0.65"/>
    </linearGradient>
    <linearGradient id="g-violet" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BILLING_VIOLET}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{OMEGA_CYAN}" stop-opacity="0.4"/>
    </linearGradient>
    <filter id="soft-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.13 0 0 0 0 0.83 0 0 0 0 0.93 0 0 0 0.7 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .bg {{ fill:{KERNEL_BLACK}; }}
      .panel {{ fill:#0B1118; stroke:{GRID}; stroke-width:1.4; rx:22; }}
      .panel2 {{ fill:#091019; stroke:#203044; stroke-width:1.2; rx:18; }}
      .line {{ stroke:{OMEGA_CYAN}; stroke-width:2; stroke-opacity:.58; fill:none; }}
      .rail {{ stroke:{TELEGRAM_BLUE}; stroke-width:4; stroke-linecap:round; stroke-opacity:.78; fill:none; }}
      .violet {{ stroke:{BILLING_VIOLET}; fill:none; }}
      .green {{ stroke:{RUNTIME_GREEN}; fill:none; }}
      .label {{ font: 700 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill:{INK}; }}
      .small {{ font: 500 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill:{MUTED}; }}
      .tiny {{ font: 600 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill:{MUTED}; letter-spacing:.08em; }}
      .mega {{ font: 900 52px ui-sans-serif, Inter, Arial, sans-serif; fill:{INK}; letter-spacing:-.05em; }}
      .num {{ font: 900 36px ui-sans-serif, Inter, Arial, sans-serif; fill:{OMEGA_CYAN}; }}
      .metric {{ font: 900 28px ui-sans-serif, Inter, Arial, sans-serif; fill:{RUNTIME_GREEN}; }}
      .cyan-fill {{ fill:{OMEGA_CYAN}; }} .blue-fill {{ fill:{TELEGRAM_BLUE}; }} .violet-fill {{ fill:{BILLING_VIOLET}; }} .green-fill {{ fill:{RUNTIME_GREEN}; }}
    </style>
  </defs>
  <rect class="bg" width="{width}" height="{height}"/>
  <path d="M0 72 H{width} M0 558 H{width}" stroke="{GRID}" stroke-width="1"/>
  {body}
</svg>
'''


def text(x: float, y: float, value: str, cls: str = "label", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'


def rect(x: float, y: float, w: float, h: float, cls: str = "panel", extra: str = "") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" class="{cls}" {extra}/>'


def circle(x: float, y: float, r: float, fill: str, extra: str = "") -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" {extra}/>'


def pill(x: float, y: float, label: str, value: str, color: str, w: int = 210) -> str:
    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="18" fill="#0B1118" stroke="{color}" stroke-opacity="0.55"/>',
            text(x + 18, y + 28, label.upper(), "tiny"),
            f'<text x="{x + 18}" y="{y + 56}" class="num" fill="{color}">{escape(value)}</text>',
        ]
    )


def hero_omega(ctx: AssetContext) -> str:
    parts: list[str] = []
    parts.append(text(72, 130, "FABLE OMEGA", "mega"))
    parts.append(text(76, 164, "445 catalogue signals converging into 15 hubs and one async kernel", "small"))
    parts.append(pill(74, 205, "Catalogue", str(ctx.total), OMEGA_CYAN, 170))
    parts.append(pill(262, 205, "Hubs", str(len(ctx.hubs)), TELEGRAM_BLUE, 150))
    parts.append(pill(430, 205, "Kernel", "1", BILLING_VIOLET, 150))

    cx, cy = 820, 322
    # 445 deterministic signal particles.
    for i in range(ctx.total):
        angle = i * 2.399963229728653
        radius = 245 - (i % 37) * 3.15
        x = cx + math.cos(angle) * radius * (0.92 + (i % 5) * 0.012)
        y = cy + math.sin(angle) * radius * 0.62
        opacity = 0.28 + (i % 7) * 0.055
        fill = OMEGA_CYAN if i % 3 else TELEGRAM_BLUE
        parts.append(circle(x, y, 1.35, fill, f'opacity="{opacity:.2f}"'))

    # Fifteen hub collectors.
    hub_points: list[tuple[float, float]] = []
    for i, hub in enumerate(ctx.hubs):
        angle = -math.pi / 2 + i * (2 * math.pi / len(ctx.hubs))
        x = cx + math.cos(angle) * 210
        y = cy + math.sin(angle) * 210 * 0.68
        hub_points.append((x, y))
        parts.append(f'<path d="M{x:.1f},{y:.1f} Q{(x + cx) / 2:.1f},{(y + cy) / 2 - 42:.1f} {cx:.1f},{cy:.1f}" class="line" opacity="0.35"/>')
        parts.append(circle(x, y, 18, "#0B1118", f'stroke="{TELEGRAM_BLUE}" stroke-width="2"'))
        parts.append(text(x, y + 5, f"{hub.index:02d}", "tiny", "middle"))
    parts.append(circle(cx, cy, 78, "#0B1118", 'stroke="url(#g-cyan)" stroke-width="5" filter="url(#soft-glow)"'))
    parts.append(text(cx, cy - 8, "Ω", "mega", "middle"))
    parts.append(text(cx, cy + 35, "ASYNC KERNEL", "tiny", "middle"))

    parts.append(rect(70, 420, 510, 118, "panel2"))
    parts.append(text(96, 456, "KONKRED 60/25/15", "label"))
    parts.append(text(96, 486, "60% visual mega-hub system", "small"))
    parts.append(text(96, 512, "25% runtime engineering narrative", "small"))
    parts.append(text(96, 538, "15% install · benchmark · deploy", "small"))
    return svg_shell("FABLE OMEGA hero", "445 catalogue signals converge into 15 hubs and one async kernel.", "\n  ".join(parts))


def fleet_counter(ctx: AssetContext) -> str:
    fleet = ctx.fleet_report
    source_items = list(ctx.source_counts.items())
    parts = [text(70, 120, "FLEET COUNTER", "mega"), text(74, 154, "Catalogue scope and freshly executed verification report", "small")]
    parts.append(pill(74, 195, "catalogue scenarios verified", f'{fleet["passed_count"]}/{fleet["total_bots_tested"]}', RUNTIME_GREEN, 360))
    parts.append(pill(462, 195, "5-stage lifecycle", f'{fleet["success_rate_percent"]:.1f}%', OMEGA_CYAN, 240))
    parts.append(pill(730, 195, "avg lifecycle", f'{fleet["avg_bot_lifecycle_latency_ms"]} ms', TELEGRAM_BLUE, 260))
    parts.append(rect(74, 315, 1048, 210, "panel2"))
    max_count = max(ctx.source_counts.values())
    for idx, (name, count) in enumerate(source_items):
        y = 360 + idx * 32
        bar_w = 690 * count / max_count
        parts.append(text(105, y + 5, name, "label"))
        parts.append(f'<rect x="260" y="{y-14}" width="720" height="18" rx="9" fill="#111827"/>')
        parts.append(f'<rect x="260" y="{y-14}" width="{bar_w:.1f}" height="18" rx="9" fill="url(#g-cyan)"/>')
        parts.append(text(1000, y + 5, str(count), "label"))
    parts.append(text(105, 505, f'Report: tests/FULL_FLEET_TEST_REPORT.json · generated {fleet["environment"]["generated_at_utc"]}', "tiny"))
    return svg_shell("FABLE OMEGA fleet counter", "Fresh fleet verification counts by catalogue source.", "\n  ".join(parts))


def mega_hub_topology(ctx: AssetContext) -> str:
    parts = [text(70, 116, "MEGA-HUB TOPOLOGY", "mega"), text(74, 150, "Fifteen strategic Telegram surfaces share one dispatcher and one runtime", "small")]
    cx, cy = 600, 345
    parts.append(circle(cx, cy, 84, "#0B1118", f'stroke="{OMEGA_CYAN}" stroke-width="5" filter="url(#soft-glow)"'))
    parts.append(text(cx, cy - 6, "DISPATCH", "label", "middle"))
    parts.append(text(cx, cy + 24, "KERNEL", "label", "middle"))
    for hub in ctx.hubs:
        angle = -math.pi / 2 + (hub.index - 1) * 2 * math.pi / len(ctx.hubs)
        x = cx + math.cos(angle) * 430
        y = cy + math.sin(angle) * 210
        color = RUNTIME_GREEN if hub.count else RED
        parts.append(f'<path d="M{cx:.1f},{cy:.1f} C{cx + math.cos(angle)*170:.1f},{cy + math.sin(angle)*90:.1f} {x - math.cos(angle)*90:.1f},{y - math.sin(angle)*50:.1f} {x:.1f},{y:.1f}" class="rail" opacity="0.45"/>')
        parts.append(circle(x, y, 28, "#0B1118", f'stroke="{color}" stroke-width="2.5"'))
        parts.append(text(x, y - 2, f"{hub.index:02d}", "label", "middle"))
        parts.append(text(x, y + 18, str(hub.count), "tiny", "middle"))
    parts.append(text(80, 545, "Counts are produced by src.core.hub_router.HUB_ROUTER at asset build time.", "tiny"))
    return svg_shell("FABLE OMEGA mega-hub topology", "Fifteen hubs connected to one dispatcher kernel.", "\n  ".join(parts))


def fifteen_hub_matrix(ctx: AssetContext) -> str:
    parts = [text(58, 98, "FIFTEEN-HUB MATRIX", "mega"), text(62, 130, "Exact current code counts from HUB_ROUTER.get_hub_summary()", "small")]
    parts.append(rect(50, 160, 1100, 412, "panel2"))
    max_count = max(h.count for h in ctx.hubs)
    for idx, hub in enumerate(ctx.hubs):
        row = idx % 8
        col = idx // 8
        x = 82 + col * 540
        y = 194 + row * 45
        bw = 260 * (hub.count / max_count) if max_count else 0
        color = RUNTIME_GREEN if hub.count else RED
        parts.append(text(x, y, f"{hub.index:02d}", "tiny"))
        parts.append(text(x + 35, y, hub.title[:38], "small"))
        parts.append(f'<rect x="{x+315}" y="{y-14}" width="150" height="16" rx="8" fill="#111827"/>')
        parts.append(f'<rect x="{x+315}" y="{y-14}" width="{min(150, bw):.1f}" height="16" rx="8" fill="{color}" opacity="0.9"/>')
        parts.append(text(x + 480, y, str(hub.count), "label"))
    parts.append(text(76, 548, f'Total routed catalogue entries: {sum(h.count for h in ctx.hubs)} / {ctx.total}', "label"))
    return svg_shell("FABLE OMEGA fifteen-hub matrix", "Matrix of all fifteen hubs with exact catalogue counts from code.", "\n  ".join(parts))


def dispatcher_kernel(ctx: AssetContext) -> str:
    columns = [
        (90, "TENANT", ["Telegram webhook", "Dashboard simulator", "admin API"]),
        (330, "HUB", ["15 strategic hubs", "BotFather identity", "category routing"]),
        (570, "SCENARIO", ["catalogue lookup", "archetype adapter", "LRU activation"]),
        (810, "USER", ["peer rate bucket", "FSM session", "credit/order state"]),
    ]
    parts = [text(70, 110, "DISPATCHER KERNEL", "mega"), text(74, 146, "Tenant → hub → scenario → user routing in one async control plane", "small")]
    for x, head, rows in columns:
        parts.append(rect(x, 220, 190, 220, "panel2"))
        parts.append(text(x + 24, 260, head, "label"))
        for i, row in enumerate(rows):
            parts.append(circle(x + 30, 302 + i * 42, 5, OMEGA_CYAN))
            parts.append(text(x + 48, 307 + i * 42, row, "small"))
    for x1, x2 in [(280, 330), (520, 570), (760, 810)]:
        parts.append(f'<path d="M{x1},330 H{x2}" class="rail" marker-end="url(#arrow)"/>')
    arrow_def = '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#22D3EE"/></marker></defs>'
    parts.append(rect(410, 490, 380, 68, "panel"))
    parts.append(text(600, 532, "MultiTenantDispatcher.dispatch_update()", "label", "middle"))
    return svg_shell("FABLE OMEGA dispatcher kernel", "Dispatcher route from tenant to hub to scenario to user.", arrow_def + "\n  " + "\n  ".join(parts))


def scenario_lifecycle(ctx: AssetContext) -> str:
    stages = ctx.fleet_report["catalogue"]["lifecycle_stages"]
    labels = ["START", "STATE", "INPUT", "CREDIT", "ORDER / PAYMENT"]
    parts = [text(70, 112, "SCENARIO LIFECYCLE", "mega"), text(74, 148, "All tested stages in tests/test_all_445_bots.py", "small")]
    x0, y = 112, 320
    for i, label in enumerate(labels):
        x = x0 + i * 220
        parts.append(circle(x, y, 54, "#0B1118", f'stroke="{OMEGA_CYAN if i < 3 else BILLING_VIOLET}" stroke-width="3"'))
        parts.append(text(x, y - 7, f"0{i+1}", "num", "middle"))
        parts.append(text(x, y + 24, label, "tiny", "middle"))
        parts.append(text(x, y + 86, stages[i], "small", "middle"))
        if i < len(labels) - 1:
            parts.append(f'<path d="M{x+60},{y} H{x+160}" class="rail"/>')
    parts.append(pill(228, 480, "verified", f'{ctx.fleet_report["passed_count"]} passed', RUNTIME_GREEN, 240))
    parts.append(pill(498, 480, "failed", str(ctx.fleet_report["failed_count"]), RED, 180))
    parts.append(pill(708, 480, "catalogue", str(ctx.total), OMEGA_CYAN, 200))
    return svg_shell("FABLE OMEGA scenario lifecycle", "The five lifecycle stages exercised by the fleet verification report.", "\n  ".join(parts))


def lru_runtime(ctx: AssetContext) -> str:
    bench = ctx.benchmark_report
    pool = bench["bot_pool"]
    parts = [text(70, 112, "LRU RUNTIME RACK", "mega"), text(74, 148, "Lazy scenario activation with bounded hot-object pool", "small")]
    parts.append(rect(82, 190, 500, 330, "panel2"))
    parts.append(rect(626, 190, 490, 330, "panel2"))
    parts.append(text(112, 230, "HOT POOL", "label"))
    parts.append(text(656, 230, "EVICTION / GC", "label"))
    capacity = int(pool["max_capacity"])
    for i in range(capacity):
        x = 112 + (i % 16) * 27
        y = 270 + (i // 16) * 46
        fill = RUNTIME_GREEN if i < 48 else OMEGA_CYAN
        parts.append(f'<rect x="{x}" y="{y}" width="18" height="28" rx="5" fill="{fill}" opacity="0.72"/>')
    parts.append(text(112, 478, f'capacity {capacity} · post-GC active {pool["active_cached"]}', "small"))
    evictions = int(pool["total_evictions"])
    for i in range(18):
        x = 676 + (i % 9) * 44
        y = 276 + (i // 9) * 70
        parts.append(f'<path d="M{x},{y} l26,0 l-8,20 l-26,0 z" fill="{BILLING_VIOLET}" opacity="{0.35 + i * 0.02:.2f}"/>')
    parts.append(text(656, 424, f'{evictions} total evictions in benchmark', "label"))
    parts.append(text(656, 462, f'hit ratio {pool["hit_ratio_percent"]}% · active after GC {pool["active_cached"]}', "small"))
    return svg_shell("FABLE OMEGA LRU runtime", "Active and evicted scenario objects in the LRU runtime pool.", "\n  ".join(parts))


def sqlite_wal(ctx: AssetContext) -> str:
    parts = [text(70, 112, "SQLITE WAL BUFFER", "mega"), text(74, 148, "Buffered state flow: users · FSM · orders · products · reminders · katas", "small")]
    labels = ["updates", "FSM patch", "order event", "credit delta", "audit row"]
    for i, label in enumerate(labels):
        y = 220 + i * 58
        parts.append(rect(90, y - 28, 180, 38, "panel2"))
        parts.append(text(118, y - 3, label, "small"))
        parts.append(f'<path d="M274,{y-10} C380,{y-10} 400,318 510,318" class="line"/>')
    parts.append(rect(510, 246, 190, 144, "panel"))
    parts.append(text(605, 302, "WAL", "mega", "middle"))
    parts.append(text(605, 336, "write-ahead log", "tiny", "middle"))
    for i, table in enumerate(["users", "fsm_sessions", "orders", "products"]):
        y = 210 + i * 74
        parts.append(f'<path d="M700,318 C790,318 790,{y} 890,{y}" class="rail"/>')
        parts.append(rect(890, y - 25, 210, 42, "panel2"))
        parts.append(text(920, y + 2, table, "label"))
    parts.append(text(92, 540, "PRAGMA journal_mode=WAL · synchronous=NORMAL · busy_timeout=5000", "tiny"))
    return svg_shell("FABLE OMEGA SQLite WAL", "Buffered state flow through SQLite WAL persistence.", "\n  ".join(parts))


def monetization_rail(ctx: AssetContext) -> str:
    parts = [text(70, 112, "MONETIZATION RAIL", "mega"), text(74, 148, "Shared order, credit and subscription state across scenarios", "small")]
    rails = [("Telegram Stars", TELEGRAM_BLUE), ("Card receipt", BILLING_VIOLET), ("TON / crypto", OMEGA_CYAN), ("Internal credits", RUNTIME_GREEN)]
    for i, (name, color) in enumerate(rails):
        y = 225 + i * 70
        parts.append(rect(92, y - 30, 230, 44, "panel2", f'stroke="{color}"'))
        parts.append(text(122, y, name, "label"))
        parts.append(f'<path d="M326,{y-8} H506" class="rail" stroke="{color}"/>')
    parts.append(circle(610, 314, 76, "#0B1118", f'stroke="{BILLING_VIOLET}" stroke-width="4"'))
    parts.append(text(610, 306, "Payment", "label", "middle"))
    parts.append(text(610, 334, "Manager", "label", "middle"))
    for i, name in enumerate(["orders", "balance", "premium_until", "stock"]):
        y = 225 + i * 70
        parts.append(f'<path d="M686,{y-8} H870" class="line"/>')
        parts.append(rect(870, y - 30, 220, 44, "panel2"))
        parts.append(text(904, y, name, "label"))
    return svg_shell("FABLE OMEGA monetization rail", "Shared monetization rail for Stars, receipt, TON and credit flows.", "\n  ".join(parts))


def control_plane(ctx: AssetContext) -> str:
    capabilities = [
        ("/api/catalog", "browse and filter catalogue"),
        ("/api/hubs", "inspect hub routing counts"),
        ("/api/runtime/stats", "memory, RPS and LRU telemetry"),
        ("/api/runtime/gc", "controlled cache cleanup"),
        ("/api/simulate", "dashboard chat simulator"),
        ("/api/orders", "manual order review surface"),
    ]
    parts = [text(70, 112, "CONTROL PLANE", "mega"), text(74, 148, "FastAPI dashboard capabilities represented from src/web/app.py", "small")]
    parts.append(rect(70, 190, 1060, 340, "panel2"))
    for i, (route, desc) in enumerate(capabilities):
        x = 110 + (i % 2) * 520
        y = 248 + (i // 2) * 88
        parts.append(rect(x, y - 38, 440, 58, "panel"))
        parts.append(text(x + 24, y - 8, route, "label"))
        parts.append(text(x + 24, y + 16, desc, "small"))
    parts.append(text(600, 502, "Dashboard + simulator exercise the shared runtime without claiming live Telegram availability.", "tiny", "middle"))
    return svg_shell("FABLE OMEGA control plane", "Actual FastAPI dashboard and simulator routes.", "\n  ".join(parts))


def telemetry_hud(ctx: AssetContext) -> str:
    bench = ctx.benchmark_report
    res = bench["resource_footprint"]
    lat = bench["latencies_ms"]
    pool = bench["bot_pool"]
    parts = [text(70, 112, "TELEMETRY HUD", "mega"), text(74, 148, "Control-plane telemetry and benchmark resource readings", "small")]
    metrics = [
        ("throughput", f'{bench["throughput_rps"]} rps', OMEGA_CYAN),
        ("p95 latency", f'{lat["p95"]} ms', TELEGRAM_BLUE),
        ("RSS under load", f'{res["under_load_rss_mb"]} MB', RUNTIME_GREEN),
        ("event-loop lag", f'{lat["event_loop_lag"]} ms', BILLING_VIOLET),
        ("LRU capacity", str(pool["max_capacity"]), AMBER),
        ("evictions", str(pool["total_evictions"]), RED),
    ]
    for i, (label, value, color) in enumerate(metrics):
        x = 82 + (i % 3) * 350
        y = 215 + (i // 3) * 150
        parts.append(pill(x, y, label, value, color, 300))
    parts.append(text(90, 540, f'Benchmark report: tests/LOW_RESOURCE_BENCHMARK_REPORT.json · {bench["environment"]["generated_at_utc"]}', "tiny"))
    return svg_shell("FABLE OMEGA telemetry HUD", "Telemetry HUD with fresh benchmark values.", "\n  ".join(parts))


def verification_console(ctx: AssetContext) -> str:
    fleet = ctx.fleet_report
    parts = [text(70, 112, "VERIFICATION CONSOLE", "mega"), text(74, 148, "Freshly executed report values; compatibility does not mean live bot status", "small")]
    parts.append(rect(82, 190, 1036, 320, "panel2"))
    console_lines = [
        '$ python tests/test_all_445_bots.py',
        f'catalogue entries tested: {fleet["total_bots_tested"]}',
        f'five-stage lifecycle passed: {fleet["passed_count"]}',
        f'failed entries: {fleet["failed_count"]}',
        f'success rate: {fleet["success_rate_percent"]:.1f}%',
        f'total duration: {fleet["total_duration_seconds"]}s',
        f'average lifecycle latency: {fleet["avg_bot_lifecycle_latency_ms"]}ms',
        f'report generated: {fleet["environment"]["generated_at_utc"]}',
    ]
    for i, line in enumerate(console_lines):
        color = RUNTIME_GREEN if i in (0, 2) else INK
        parts.append(f'<text x="122" y="{240 + i*32}" class="label" fill="{color}">{escape(line)}</text>')
    parts.append(text(122, 486, "Metric language: 445 catalogue scenarios verified; no live-status claim.", "tiny"))
    return svg_shell("FABLE OMEGA verification console", "Fresh full-fleet verification console.", "\n  ".join(parts))


def benchmark_panel(ctx: AssetContext) -> str:
    bench = ctx.benchmark_report
    env = bench["environment"]
    res = bench["resource_footprint"]
    parts = [text(70, 104, "BENCHMARK PANEL", "mega"), text(74, 138, "Low-resource report with environment metadata", "small")]
    parts.append(rect(70, 170, 520, 370, "panel2"))
    parts.append(rect(620, 170, 510, 370, "panel2"))
    left = [
        ("requests", str(bench["total_requests"])),
        ("concurrency", str(bench["concurrency"])),
        ("throughput", f'{bench["throughput_rps"]} rps'),
        ("success", f'{bench["success_rate_percent"]}%'),
        ("under-load RSS", f'{res["under_load_rss_mb"]} MB'),
        ("post-GC RSS", f'{res["post_gc_rss_mb"]} MB'),
    ]
    for i, (k, v) in enumerate(left):
        y = 220 + i * 48
        parts.append(text(105, y, k.upper(), "tiny"))
        parts.append(text(285, y, v, "label"))
    right = [
        ("python", env["python_version"]),
        ("platform", env["platform"][:36]),
        ("machine", env["machine"]),
        ("cpu count", str(env["cpu_count"])),
        ("total memory", f'{env["total_memory_mb"]} MB'),
        ("commit", str(env["commit"])[:12]),
        ("branch", env["branch"]),
    ]
    for i, (k, v) in enumerate(right):
        y = 220 + i * 40
        parts.append(text(655, y, k.upper(), "tiny"))
        parts.append(text(820, y, str(v), "small"))
    parts.append(text(655, 510, f'generated {env["generated_at_utc"]}', "tiny"))
    return svg_shell("FABLE OMEGA benchmark panel", "Benchmark panel including environment metadata.", "\n  ".join(parts))


def deployment_stack(ctx: AssetContext) -> str:
    layers = [
        ("operator", "README · .env · fable-omega CLI", OMEGA_CYAN),
        ("control plane", "FastAPI · Uvicorn · dashboard", TELEGRAM_BLUE),
        ("runtime", "Async dispatcher · FSM · LRU pool", RUNTIME_GREEN),
        ("state", "SQLite WAL · orders · credits", BILLING_VIOLET),
        ("deployment", "Docker Compose · Dockerfile.slim · Caddy", AMBER),
    ]
    parts = [text(70, 112, "DEPLOYMENT STACK", "mega"), text(74, 148, "Installation, benchmarking and deployment path", "small")]
    for i, (name, desc, color) in enumerate(layers):
        y = 205 + i * 72
        parts.append(rect(150 + i * 22, y, 850 - i * 44, 50, "panel2", f'stroke="{color}"'))
        parts.append(text(190 + i * 22, y + 32, name.upper(), "label"))
        parts.append(text(420 + i * 22, y + 32, desc, "small"))
    parts.append(text(85, 560, "Primary local command: python run.py · package script: fable-omega · container path: deploy/docker-compose.yml", "tiny"))
    return svg_shell("FABLE OMEGA deployment stack", "Deployment stack from local CLI to Docker Compose.", "\n  ".join(parts))


def footer_omega(ctx: AssetContext) -> str:
    parts = [text(600, 185, "CATALOGUE THE WORK", "mega", "middle"), text(600, 260, "SHARE THE RUNTIME", "mega", "middle"), text(600, 335, "MEASURE THE CLAIMS", "mega", "middle")]
    parts.append(circle(600, 430, 54, "#0B1118", f'stroke="{OMEGA_CYAN}" stroke-width="4" filter="url(#soft-glow)"'))
    parts.append(text(600, 448, "Ω", "mega", "middle"))
    parts.append(text(600, 530, f'{ctx.total} catalogue scenarios · {len(ctx.hubs)} hubs · reports committed under tests/', "label", "middle"))
    return svg_shell("FABLE OMEGA footer", "Footer mark for the FABLE OMEGA README.", "\n  ".join(parts))


ASSETS: dict[str, Callable[[AssetContext], str]] = {
    "hero-omega.svg": hero_omega,
    "fleet-counter.svg": fleet_counter,
    "mega-hub-topology.svg": mega_hub_topology,
    "fifteen-hub-matrix.svg": fifteen_hub_matrix,
    "dispatcher-kernel.svg": dispatcher_kernel,
    "scenario-lifecycle.svg": scenario_lifecycle,
    "lru-runtime.svg": lru_runtime,
    "sqlite-wal.svg": sqlite_wal,
    "monetization-rail.svg": monetization_rail,
    "control-plane.svg": control_plane,
    "telemetry-hud.svg": telemetry_hud,
    "verification-console.svg": verification_console,
    "benchmark-panel.svg": benchmark_panel,
    "deployment-stack.svg": deployment_stack,
    "footer-omega.svg": footer_omega,
}


def build_assets() -> dict[str, Path]:
    ctx = load_context()
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, builder in ASSETS.items():
        path = ASSET_DIR / filename
        content = builder(ctx)
        path.write_text(content, encoding="utf-8")
        written[filename] = path
    return written


def main() -> None:
    written = build_assets()
    for name, path in written.items():
        print(f"generated {name}: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
