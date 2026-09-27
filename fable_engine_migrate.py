#!/usr/bin/env python3
"""
Fable Engine Migration & Topological Ingestion Pipeline
Claude Fable 5.1 / Mythos-Class Multi-Agent Engine
Zero-Dependency Autonomous Repository Reconstruction Protocol
"""

import os
import sys
import re
import ast
import json
import uuid
import hashlib
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Optional, Any


# ---------------------------------------------------------------------------
# DETERMINISTIC IDENTIFIERS & REGISTRY
# ---------------------------------------------------------------------------

def compute_deterministic_uuid(filepath: str) -> str:
    """Generate a deterministic RFC 4122 v4 UUID from filepath."""
    relpath = os.path.basename(filepath)
    h = hashlib.sha256(relpath.encode('utf-8')).digest()
    b = bytearray(h[:16])
    b[6] = (b[6] & 0x0f) | 0x40  # version 4
    b[8] = (b[8] & 0x3f) | 0x80  # variant 10xx
    return str(uuid.UUID(bytes=bytes(b)))


# Canonical metadata specifications for each repository document
BLUEPRINT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "1-25.md": {
        "category": "education_productivity_batch",
        "title": "Telegram Bot Blueprints Batch 1: Ideas #1-#25",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "250 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "SELECT_LANG",
            "AWAITING_PROMPT",
            "FLASHCARD_REVIEW",
            "EXPENSE_INPUT",
            "SET_REMINDER",
            "SUBSCRIPTION_CHECK",
            "COMPLETED"
        ],
        "storage_driver": "Redis",
        "dependencies_external": [
            "python-telegram-bot>=20.0",
            "aioredis>=2.0.0",
            "pydantic>=2.0",
            "aiohttp>=3.8.0"
        ],
        "internal_deps": ["Shared Core Kit.md", "150.md"],
        "breaking_changes": [
            "python-telegram-bot v20+ async handler signature migration required",
            "FastAPI webhook lifespan event updates"
        ]
    },
    "126-150.md": {
        "category": "b2b_compliance_batch",
        "title": "Telegram Bot Blueprints Batch 6: Ideas #126-#150",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "200 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "PERMIT_DATA_INPUT",
            "EXPIRY_DATE_SET",
            "CRON_SCHEDULE_CONFIRM",
            "INVOICE_GENERATION",
            "AWAITING_PAYMENT",
            "COMPLETED"
        ],
        "storage_driver": "SQL",
        "dependencies_external": [
            "python-telegram-bot>=20.0",
            "SQLAlchemy>=2.0",
            "apscheduler>=3.10.0",
            "pydantic>=2.0"
        ],
        "internal_deps": ["Shared Core Kit.md", "76-100.md", "150.md"],
        "breaking_changes": [
            "SQLAlchemy 2.0 declarative base transition",
            "python-telegram-bot ApplicationBuilder async context requirement"
        ]
    },
    "150 TELEGRAM BOT.md": {
        "category": "monetization_catalog",
        "title": "Master 150 Monetizable Telegram Bot Concepts Catalog",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "python-telegram-bot>=20.0"
        ],
        "internal_deps": ["150.md", "Shared Core Kit.md"],
        "breaking_changes": []
    },
    "150.md": {
        "category": "mvp_catalog",
        "title": "Rapid MVP 150 Telegram Bot Catalog",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "python-telegram-bot>=20.0"
        ],
        "internal_deps": ["Shared Core Kit.md"],
        "breaking_changes": []
    },
    "26-50.md": {
        "category": "finance_education_batch",
        "title": "Telegram Bot Blueprints Batch 2: Ideas #26-#50",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "300 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "MAIN_MENU",
            "ADDING_STEP_1",
            "ADDING_STEP_2",
            "AWAITING_RECEIPT",
            "PAYWALL_DISPLAY",
            "XTR_INVOICE_SENT",
            "COMPLETED"
        ],
        "storage_driver": "Redis",
        "dependencies_external": [
            "aiogram>=3.0.0",
            "python-telegram-bot>=20.0",
            "aioredis>=2.0.0",
            "fastapi>=0.100.0"
        ],
        "internal_deps": ["Shared Core Kit.md", "1-25.md", "150.md"],
        "breaking_changes": [
            "aiogram 2.x executor.start_polling deprecated in favor of aiogram 3.x Dispatcher/Router",
            "aiogram filters.Text replaced with MagicFilter (F.text)"
        ]
    },
    "51-75.md": {
        "category": "hr_operations_batch",
        "title": "Telegram Bot Blueprints Batch 3: Ideas #51-#75",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "250 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "RESUME_SUBMIT",
            "SCREENING_Q1",
            "SCREENING_Q2",
            "INTERVIEW_SLOT_SELECT",
            "ONBOARDING_DAY_1",
            "LEAVE_REQUEST",
            "COMPLETED"
        ],
        "storage_driver": "SQL",
        "dependencies_external": [
            "python-telegram-bot>=20.0",
            "SQLAlchemy>=2.0",
            "pydantic>=2.0",
            "aiosqlite>=0.19.0"
        ],
        "internal_deps": ["Shared Core Kit.md", "26-50.md", "150.md"],
        "breaking_changes": [
            "python-telegram-bot v20+ ConversationHandler state dictionary typing changes"
        ]
    },
    "76-100.md": {
        "category": "lifestyle_utility_batch",
        "title": "Telegram Bot Blueprints Batch 4: Ideas #76-#100",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "200 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "BUDGET_INPUT",
            "VIBE_SELECT",
            "TIME_FRAME_SET",
            "RECOMMENDATION_VIEW",
            "BOOKING_CONFIRM",
            "COMPLETED"
        ],
        "storage_driver": "Redis",
        "dependencies_external": [
            "python-telegram-bot>=20.0",
            "httpx>=0.24.0",
            "aioredis>=2.0.0",
            "pydantic>=2.0"
        ],
        "internal_deps": ["Shared Core Kit.md", "51-75.md", "150.md"],
        "breaking_changes": [
            "python-telegram-bot v20+ async context handler migration"
        ]
    },
    "ANALYZE730.md": {
        "category": "market_intelligence",
        "title": "Advanced 730 Telegram Bot Market Landscape & Opportunity Analysis",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "500 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "grammy>=1.18.0",
            "python-telegram-bot>=20.0",
            "fastapi>=0.100.0",
            "postgres>=15.0"
        ],
        "internal_deps": ["150 TELEGRAM BOT.md", "Listaibusinesses.md"],
        "breaking_changes": [
            "Node.js Grammy plugin interface updates"
        ]
    },
    "AuditReportHtml56v2.md": {
        "category": "quality_audit",
        "title": "Quality Audit & Production Readiness Report: HTML56 Dashboard v2",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "chart.js>=4.0.0",
            "tailwindcss>=3.3.0"
        ],
        "internal_deps": ["Html56v2.md", "Untitled.md"],
        "breaking_changes": []
    },
    "AuditReprtHtml56v3.md": {
        "category": "quality_audit",
        "title": "Quality Audit & Metric Scoring Report: HTML56 Dashboard v3",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "chart.js>=4.0.0",
            "lucide-icons>=0.263.0"
        ],
        "internal_deps": ["Html56v3.md", "Untitled.md"],
        "breaking_changes": []
    },
    "CASHFLOW.md": {
        "category": "monetization_engine",
        "title": "CashFlow Architect: Monetization Engine & Bot Assessment Dashboard",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "500 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "LANDING",
            "ASSESSMENT_PROFILE",
            "ASSESSMENT_BUDGET",
            "ASSESSMENT_TIME",
            "CALCULATING_METRICS",
            "DASHBOARD_VIEW",
            "EXPORT_REPORT"
        ],
        "storage_driver": "Memory",
        "dependencies_external": [
            "react>=18.2.0",
            "react-dom>=18.2.0",
            "lucide-react>=0.263.0",
            "tailwindcss>=3.3.0"
        ],
        "internal_deps": ["ANALYZE730.md", "Untitled 1.md"],
        "breaking_changes": [
            "React 18 concurrent rendering root API (createRoot) requirement"
        ]
    },
    "FULLOPUSTELBOT.md": {
        "category": "monolith_guide",
        "title": "Complete Opus Telegram Bot Production Guide & 150 Implementations",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "1000 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "ONBOARDING",
            "AWAITING_INPUT",
            "PROCESSING",
            "EVALUATION",
            "FEEDBACK",
            "PAYMENT_GATEWAY",
            "SUBSCRIPTION_ACTIVE",
            "COMPLETED",
            "CANCELLED"
        ],
        "storage_driver": "Redis",
        "dependencies_external": [
            "python-telegram-bot>=20.0",
            "aiohttp>=3.8.0",
            "aiosqlite>=0.19.0",
            "pydantic>=2.0",
            "matplotlib>=3.7.0",
            "pillow>=10.0.0",
            "openai>=1.0.0",
            "reportlab>=4.0.0"
        ],
        "internal_deps": [
            "Shared Core Kit.md",
            "1-25.md",
            "26-50.md",
            "51-75.md",
            "76-100.md",
            "126-150.md",
            "150.md",
            "150 TELEGRAM BOT.md"
        ],
        "breaking_changes": [
            "python-telegram-bot v13 to v20+ async migration",
            "OpenAI API v1.0.0 client interface migration",
            "Pydantic v1 to v2 BaseModel validator deprecation"
        ]
    },
    "Html56v1.md": {
        "category": "dashboard_app",
        "title": "Domestic Opportunity Matrix Interactive Dashboard v1",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "html5",
            "vanilla-js"
        ],
        "internal_deps": ["Untitled.md"],
        "breaking_changes": []
    },
    "Html56v2.md": {
        "category": "dashboard_app",
        "title": "Domestic Opportunity Matrix Interactive Dashboard v2",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "tailwindcss>=3.0.0",
            "vanilla-js"
        ],
        "internal_deps": ["Html56v1.md", "Untitled.md"],
        "breaking_changes": []
    },
    "Html56v3.md": {
        "category": "dashboard_app",
        "title": "Domestic Opportunity Matrix Interactive Dashboard v3 (Self-Contained LTR)",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [
            "chart.js>=4.0.0",
            "tailwindcss>=3.3.0",
            "lucide-icons>=0.263.0"
        ],
        "internal_deps": ["Html56v2.md", "Untitled.md"],
        "breaking_changes": []
    },
    "Listaibusinesses.md": {
        "category": "business_taxonomy",
        "title": "Comprehensive AI Business Taxonomy & Service Opportunities Catalog",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [],
        "internal_deps": [],
        "breaking_changes": []
    },
    "README.md": {
        "category": "root_manifest",
        "title": "All-Them-Bots Blueprint Repository Root Manifest",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [],
        "internal_deps": [
            "Shared Core Kit.md",
            "FULLOPUSTELBOT.md",
            "150 TELEGRAM BOT.md",
            "ANALYZE730.md",
            "Untitled.md"
        ],
        "breaking_changes": []
    },
    "Shared Core Kit.md": {
        "category": "core_architecture",
        "title": "Shared Core Architectural Kit & Reusable Bot Services",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "500 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "AUTH_VERIFICATION",
            "INPUT_AWAITING",
            "RATE_LIMITED",
            "PROCESSING",
            "ERROR_RETRY",
            "COMPLETED"
        ],
        "storage_driver": "Redis",
        "dependencies_external": [
            "python-telegram-bot>=20.0",
            "aioredis>=2.0.0",
            "pydantic>=2.0",
            "fastapi>=0.100.0"
        ],
        "internal_deps": [],
        "breaking_changes": [
            "aioredis package merged into redis-py >= 4.2.0 (redis.asyncio)"
        ]
    },
    "Telegram & Discord Bot Creator Application.md": {
        "category": "visual_builder",
        "title": "Multi-Platform Visual Bot Creator Studio Specification",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "1000 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "NODE_INITIALIZED",
            "CANVAS_EDITING",
            "SYNTAX_VALIDATING",
            "CONTAINER_PROVISIONING",
            "DEPLOYING",
            "ACTIVE",
            "PAUSED"
        ],
        "storage_driver": "SQL",
        "dependencies_external": [
            "next>=14.0.0",
            "react>=18.2.0",
            "prisma>=5.0.0",
            "fastapi>=0.100.0",
            "docker>=6.1.0",
            "pydantic>=2.0"
        ],
        "internal_deps": ["Shared Core Kit.md", "README.md"],
        "breaking_changes": [
            "Next.js 14 App Router migration from Pages Router",
            "Prisma client edge runtime restrictions"
        ]
    },
    "Untitled 1.md": {
        "category": "financial_model",
        "title": "Economic Feasibility & Portfolio Revenue Model for Telegram Bots",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [],
        "internal_deps": ["150 TELEGRAM BOT.md", "1-25.md"],
        "breaking_changes": []
    },
    "Untitled 2.md": {
        "category": "sandboxed_execution",
        "title": "Coding Kata & Sandboxed Execution Telegram Bot Blueprint",
        "transport": "BotAPI",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "150 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "START",
            "KATA_SELECT",
            "AWAITING_ZIP_SUBMISSION",
            "SANDBOX_RUNNING",
            "TESTS_EVALUATING",
            "STATS_DISPLAY",
            "COMPLETED"
        ],
        "storage_driver": "SQL",
        "dependencies_external": [
            "fastapi>=0.100.0",
            "sqlalchemy>=2.0.0",
            "python-telegram-bot>=20.0",
            "docker>=6.1.0",
            "pydantic>=2.0"
        ],
        "internal_deps": ["Shared Core Kit.md"],
        "breaking_changes": [
            "SQLAlchemy 2.0 query syntax (select vs query)"
        ]
    },
    "Untitled.md": {
        "category": "market_inventory",
        "title": "Master Opportunity Inventory: Rubika & Baleh Messenger Ecosystems",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [],
        "internal_deps": ["150.md"],
        "breaking_changes": []
    },
    "روبیکابله.md": {
        "category": "commerce_playbook",
        "title": "Domestic Messenger Commerce & Direct-Sales Automation Playbook",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "CUSTOMER_INQUIRY",
            "PRODUCT_CATALOG",
            "ORDER_FORM_STEP_1",
            "ORDER_FORM_STEP_2",
            "RECEIPT_UPLOAD",
            "OPERATOR_APPROVAL",
            "FULFILLMENT_TRACKING"
        ],
        "storage_driver": "SQL",
        "dependencies_external": [
            "pydantic>=2.0",
            "httpx>=0.24.0"
        ],
        "internal_deps": ["Untitled.md"],
        "breaking_changes": []
    },
    "روبیکابله۱.md": {
        "category": "seller_mvp",
        "title": "Domestic Messenger Bot MVP Scopes & Seller Workflows",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "INQUIRY_RECEIVED",
            "CART_BUILDING",
            "RECEIPT_AWAITING",
            "MANUAL_VERIFICATION",
            "ORDER_DISPATCHED"
        ],
        "storage_driver": "Memory",
        "dependencies_external": [
            "pydantic>=2.0"
        ],
        "internal_deps": ["روبیکابله.md", "Untitled.md"],
        "breaking_changes": []
    },
    "روبیکابله۲.md": {
        "category": "friction_matrix",
        "title": "Domestic Messenger Persona Decomposition & JTBD Analysis",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": False,
        "fsm_states": [],
        "storage_driver": "Memory",
        "dependencies_external": [],
        "internal_deps": ["روبیکابله۱.md", "Untitled.md"],
        "breaking_changes": []
    },
    "روبیکابله۳.md": {
        "category": "micro_saas",
        "title": "Low-Maintenance Micro-SaaS Blueprint for Domestic Messengers",
        "transport": "HybridBridge",
        "concurrency_paradigm": "AsyncIO",
        "max_throughput_est": "100 req/s",
        "fsm_defined": True,
        "fsm_states": [
            "SUBSCRIBER_REGISTER",
            "CHANNEL_VERIFY",
            "NOTIFICATION_CONFIG",
            "DISPATCH_DIGEST",
            "RENEWAL_CHECK"
        ],
        "storage_driver": "SQL",
        "dependencies_external": [
            "fastapi>=0.100.0",
            "pydantic>=2.0",
            "aiosqlite>=0.19.0"
        ],
        "internal_deps": ["روبیکابله۲.md", "Untitled.md"],
        "breaking_changes": []
    }
}


def get_urn_for_file(filepath: str) -> str:
    """Generate canonical URN for a given file path."""
    filename = os.path.basename(filepath)
    meta = BLUEPRINT_REGISTRY.get(filename, {})
    category = meta.get("category", "unclassified")
    file_uuid = compute_deterministic_uuid(filename)
    return f"urn:tgn:blueprint:{category}:{file_uuid}"


# ---------------------------------------------------------------------------
# SUB-AGENT ALPHA: AST GRAMMAR & TRANSPORT INFERENCE
# ---------------------------------------------------------------------------

@dataclass
class AstAnalysisReport:
    total_code_blocks: int = 0
    language_breakdown: Dict[str, int] = field(default_factory=dict)
    python_blocks_parsed: int = 0
    python_syntax_errors: int = 0
    inferred_transport: str = "BotAPI"
    breaking_changes: List[str] = field(default_factory=list)


class SubAgentAlpha:
    """Sub-Agent Alpha: AST Grammar & Transport Inference Engine."""

    def analyze(self, raw_text: str) -> AstAnalysisReport:
        report = AstAnalysisReport()
        blocks = re.findall(r'```([a-zA-Z0-9_+-]*)\n(.*?)```', raw_text, re.DOTALL)
        report.total_code_blocks = len(blocks)

        for lang, code in blocks:
            lang_key = lang.lower() if lang else "unspecified"
            report.language_breakdown[lang_key] = report.language_breakdown.get(lang_key, 0) + 1

            if lang_key in ("python", "py"):
                try:
                    ast.parse(code)
                    report.python_blocks_parsed += 1
                except SyntaxError:
                    report.python_syntax_errors += 1

        # Check for framework version breaking points
        if re.search(r'executor\.start_polling|Dispatcher\(bot\)|@dp\.message_handler', raw_text):
            report.breaking_changes.append(
                "aiogram 2.x executor.start_polling/message_handler deprecated in aiogram 3.x"
            )
        if re.search(r'Updater\(|dispatcher\.add_handler', raw_text):
            report.breaking_changes.append(
                "python-telegram-bot v13 sync Updater deprecated; use v20+ ApplicationBuilder"
            )
        if re.search(r'TelethonClient|StringSession', raw_text):
            report.breaking_changes.append(
                "Legacy Telethon session format require explicit StringSession upgrade"
            )

        # Transport tier inference
        has_rubika_baleh = bool(re.search(r'روبیکا|بله|Rubika|Baleh', raw_text, re.IGNORECASE))
        has_discord = bool(re.search(r'discord', raw_text, re.IGNORECASE))
        has_mtproto = bool(re.search(r'MTProto|telethon|pyrogram', raw_text, re.IGNORECASE))

        if (has_rubika_baleh and "telegram" in raw_text.lower()) or has_discord:
            report.inferred_transport = "HybridBridge"
        elif has_mtproto and not re.search(r'BotAPI|telegram\.ext', raw_text):
            report.inferred_transport = "MTProto"
        else:
            report.inferred_transport = "BotAPI"

        return report


# ---------------------------------------------------------------------------
# SUB-AGENT BETA: FSM FORMALIZER
# ---------------------------------------------------------------------------

@dataclass
class FsmTuple:
    Q: List[str]       # States
    Sigma: List[str]   # Alphabet / Input Events
    delta_count: int   # Transitions count
    q0: str            # Initial State
    F: List[str]       # Final / Accepting States
    storage_driver: str
    state_explosion_risk: bool


class SubAgentBeta:
    """Sub-Agent Beta: Conversation Handler & FSM Formalizer."""

    def formalize(self, filename: str, raw_text: str) -> FsmTuple:
        meta = BLUEPRINT_REGISTRY.get(filename, {})
        defined = meta.get("fsm_defined", False)
        states = meta.get("fsm_states", [])
        driver = meta.get("storage_driver", "Memory")

        if not defined or not states:
            return FsmTuple(
                Q=[],
                Sigma=[],
                delta_count=0,
                q0="",
                F=[],
                storage_driver=driver,
                state_explosion_risk=False
            )

        q0 = states[0]
        final_candidates = [s for s in states if s in ("COMPLETED", "CANCELLED", "ACTIVE", "PAUSED", "EXPORT_REPORT")]
        f_states = final_candidates if final_candidates else [states[-1]]

        sigma = [
            "/start",
            "text_message",
            "callback_query",
            "inline_button_press",
            "invoice_payment",
            "timeout_event"
        ]

        # Check for state explosion risks (lack of user-level mutex or concurrent state transitions)
        state_explosion_risk = False
        if "ConversationHandler" in raw_text or "FSMContext" in raw_text or "StatesGroup" in raw_text:
            if "mutex" not in raw_text.lower() and "lock" not in raw_text.lower() and "rate_limit" not in raw_text.lower():
                state_explosion_risk = True

        return FsmTuple(
            Q=states,
            Sigma=sigma,
            delta_count=max(len(states) - 1, 1),
            q0=q0,
            F=f_states,
            storage_driver=driver,
            state_explosion_risk=state_explosion_risk
        )


# ---------------------------------------------------------------------------
# SUB-AGENT GAMMA: SECURITY & CRITICALITY SCANNER
# ---------------------------------------------------------------------------

@dataclass
class SecurityAuditReport:
    secrets_detected: List[str] = field(default_factory=list)
    tma_hmac_safe: bool = True
    vulnerabilities_flagged: List[str] = field(default_factory=list)


class SubAgentGamma:
    """Sub-Agent Gamma: Security, Secrets & Mini App HMAC Scanner."""

    def scan(self, raw_text: str) -> SecurityAuditReport:
        report = SecurityAuditReport()

        # Check hardcoded real secrets vs mock placeholders
        token_matches = re.findall(r'[0-9]{8,10}:[a-zA-Z0-9_-]{35}', raw_text)
        for t in token_matches:
            if not t.startswith("123456789") and not t.startswith("000000000"):
                report.secrets_detected.append(f"Potential live Telegram Bot Token: {t[:10]}...")

        raw_api_hashes = re.findall(r'api_hash\s*=\s*[\'"]([a-f0-9]{32})[\'"]', raw_text, re.IGNORECASE)
        for h in raw_api_hashes:
            if h != "0123456789abcdef0123456789abcdef":
                report.secrets_detected.append(f"Potential MTProto API Hash: {h[:8]}...")

        # Check Telegram Mini App HMAC timing-attack vulnerability
        if "initData" in raw_text or "check_hash" in raw_text:
            if "hmac.compare_digest" not in raw_text and "compare_digest" not in raw_text:
                report.tma_hmac_safe = False
                report.vulnerabilities_flagged.append(
                    "TMA initData verification lacks constant-time HMAC comparison (hmac.compare_digest)"
                )

        return report


# ---------------------------------------------------------------------------
# SUB-AGENT DELTA: DAG COMPILER & TOPOLOGICAL ENGINE
# ---------------------------------------------------------------------------

@dataclass
class DagReport:
    total_nodes: int
    total_edges: int
    adjacency_list: Dict[str, List[str]]
    in_degrees: Dict[str, int]
    out_degrees: Dict[str, int]
    orphan_nodes: List[str]
    root_nodes: List[str]
    leaf_nodes: List[str]
    cycles_detected: List[List[str]]
    topological_order: List[str]


class DagCompiler:
    """In-Memory Dependency DAG Compiler & Topological Ordering Engine."""

    def __init__(self, registry: Dict[str, Dict[str, Any]]):
        self.registry = registry

    def compile(self) -> DagReport:
        nodes = sorted(list(self.registry.keys()))
        adj: Dict[str, List[str]] = {node: [] for node in nodes}
        in_deg: Dict[str, int] = {node: 0 for node in nodes}
        out_deg: Dict[str, int] = {node: 0 for node in nodes}

        # Build edges: A -> B means A depends on B (or A references B)
        for src, data in self.registry.items():
            for target in data.get("internal_deps", []):
                if target in adj and target not in adj[src]:
                    adj[src].append(target)
                    out_deg[src] += 1
                    in_deg[target] += 1

        total_edges = sum(len(v) for v in adj.values())

        # Cycle detection using Tarjan's strongly connected components algorithm
        cycles = self._find_cycles(nodes, adj)

        # Topological sort (Kahn's algorithm on reverse dependency or dependency graph)
        # Note: If graph is DAG, Kahn gives ordering
        topological_order = self._kahn_topological_sort(nodes, adj)

        # Classify nodes
        root_nodes = [node for node in nodes if in_deg[node] == 0 and out_deg[node] > 0]
        leaf_nodes = [node for node in nodes if out_deg[node] == 0 and in_deg[node] > 0]
        orphan_nodes = [node for node in nodes if in_deg[node] == 0 and out_deg[node] == 0]

        return DagReport(
            total_nodes=len(nodes),
            total_edges=total_edges,
            adjacency_list=adj,
            in_degrees=in_deg,
            out_degrees=out_deg,
            orphan_nodes=orphan_nodes,
            root_nodes=root_nodes,
            leaf_nodes=leaf_nodes,
            cycles_detected=cycles,
            topological_order=topological_order
        )

    def _find_cycles(self, nodes: List[str], adj: Dict[str, List[str]]) -> List[List[str]]:
        visited: Dict[str, int] = {n: 0 for n in nodes}  # 0=unvisited, 1=visiting, 2=visited
        path: List[str] = []
        cycles: List[List[str]] = []

        def dfs(curr: str):
            visited[curr] = 1
            path.append(curr)

            for neighbor in adj.get(curr, []):
                if visited[neighbor] == 1:
                    cycle_start_idx = path.index(neighbor)
                    cycles.append(path[cycle_start_idx:] + [neighbor])
                elif visited[neighbor] == 0:
                    dfs(neighbor)

            path.pop()
            visited[curr] = 2

        for node in nodes:
            if visited[node] == 0:
                dfs(node)

        return cycles

    def _kahn_topological_sort(self, nodes: List[str], adj: Dict[str, List[str]]) -> List[str]:
        # in Kahn: in_degree refers to incoming edges
        in_degree = {n: 0 for n in nodes}
        for u in nodes:
            for v in adj.get(u, []):
                in_degree[v] += 1

        queue = deque([n for n in nodes if in_degree[n] == 0])
        order = []

        while queue:
            u = queue.popleft()
            order.append(u)
            for v in adj.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return order


# ---------------------------------------------------------------------------
# STRICT YAML 1.2 FRONTMATTER SYNTHESIZER & PARSER
# ---------------------------------------------------------------------------

class FrontmatterEngine:
    """Strict YAML 1.2 Frontmatter Parser, Synthesizer & Checksum Validator."""

    @staticmethod
    def extract_body(raw_content: str) -> str:
        """Strip existing YAML frontmatter and return clean Markdown body."""
        if raw_content.startswith('---'):
            parts = raw_content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2]
                if body.startswith('\n'):
                    body = body[1:]
                return body
        return raw_content

    @staticmethod
    def compute_body_sha256(body: str) -> str:
        """Compute SHA-256 hex digest of the raw markdown body."""
        return hashlib.sha256(body.encode('utf-8')).hexdigest()

    @classmethod
    def synthesize_frontmatter(cls, filename: str, body: str) -> str:
        """Generate strict YAML 1.2 frontmatter compliant with Fable 5.1.0 schema."""
        meta = BLUEPRINT_REGISTRY.get(filename, {})
        category = meta.get("category", "unclassified")
        file_uuid = compute_deterministic_uuid(filename)
        urn = f"urn:tgn:blueprint:{category}:{file_uuid}"
        title = meta.get("title", f"Functional Blueprint: {filename}")
        transport = meta.get("transport", "BotAPI")
        paradigm = meta.get("concurrency_paradigm", "AsyncIO")
        max_throughput = meta.get("max_throughput_est", "100 req/s")
        fsm_defined = meta.get("fsm_defined", False)
        fsm_states = meta.get("fsm_states", [])
        storage_driver = meta.get("storage_driver", "Memory")
        external_deps = meta.get("dependencies_external", [])

        # Map internal filenames to their canonical URNs
        internal_urns = []
        for dep_file in meta.get("internal_deps", []):
            dep_meta = BLUEPRINT_REGISTRY.get(dep_file, {})
            dep_cat = dep_meta.get("category", "unclassified")
            dep_uuid = compute_deterministic_uuid(dep_file)
            internal_urns.append(f"urn:tgn:blueprint:{dep_cat}:{dep_uuid}")

        breaking_changes = meta.get("breaking_changes", [])
        checksum = cls.compute_body_sha256(body)

        # Build clean YAML 1.2 lines
        yaml_lines = [
            "---",
            'fable_schema: "5.1.0"',
            f'urn: "{urn}"',
            f'title: "{title}"',
            f'transport: "{transport}"',
            "concurrency:",
            f'  paradigm: "{paradigm}"',
            f'  max_throughput_est: "{max_throughput}"',
            "fsm:",
            f"  defined: {'true' if fsm_defined else 'false'}",
        ]

        if fsm_states:
            yaml_lines.append("  states:")
            for s in fsm_states:
                yaml_lines.append(f'    - "{s}"')
        else:
            yaml_lines.append("  states: []")

        yaml_lines.append(f'  storage_driver: "{storage_driver}"')
        yaml_lines.append("dependencies:")

        if external_deps:
            yaml_lines.append("  external:")
            for ext in external_deps:
                yaml_lines.append(f'    - "{ext}"')
        else:
            yaml_lines.append("  external: []")

        if internal_urns:
            yaml_lines.append("  internal_urns:")
            for i_urn in internal_urns:
                yaml_lines.append(f'    - "{i_urn}"')
        else:
            yaml_lines.append("  internal_urns: []")

        if breaking_changes:
            yaml_lines.append("breaking_changes_detected:")
            for bc in breaking_changes:
                yaml_lines.append(f'  - "{bc}"')
        else:
            yaml_lines.append("breaking_changes_detected: []")

        yaml_lines.append(f'verification_checksum: "{checksum}"')
        yaml_lines.append("---")
        yaml_lines.append("")

        return "\n".join(yaml_lines)

    @classmethod
    def assemble_document(cls, filename: str, raw_content: str) -> str:
        """Strip old frontmatter, compute checksum on body, prepend new frontmatter."""
        body = cls.extract_body(raw_content)
        frontmatter = cls.synthesize_frontmatter(filename, body)
        return frontmatter + body


# ---------------------------------------------------------------------------
# ATOMIC GIT TRANSACTION MANAGER
# ---------------------------------------------------------------------------

class GitTransactionManager:
    """Manages atomic Git state guarantees, rollback and status verification."""

    @staticmethod
    def get_status() -> str:
        try:
            res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception as e:
            return f"Git error: {e}"

    @staticmethod
    def create_checkpoint() -> Optional[str]:
        """Create a git stash checkpoint before destructive changes."""
        try:
            res = subprocess.run(["git", "stash", "create"], capture_output=True, text=True, check=True)
            stash_hash = res.stdout.strip()
            return stash_hash if stash_hash else None
        except Exception:
            return None

    @staticmethod
    def rollback():
        """Atomic rollback: checkout working tree to HEAD."""
        try:
            subprocess.run(["git", "checkout", "."], check=True)
            subprocess.run(["git", "clean", "-fd"], check=True)
            print("[ROLLBACK] Successfully restored repository to HEAD state.")
        except Exception as e:
            print(f"[ROLLBACK ERROR] Failed to rollback git state: {e}")


# ---------------------------------------------------------------------------
# REPOSITORY ORCHESTRATOR
# ---------------------------------------------------------------------------

class RepositoryOrchestrator:
    """Main orchestration controller for autonomous repository reconstruction."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.sub_alpha = SubAgentAlpha()
        self.sub_beta = SubAgentBeta()
        self.sub_gamma = SubAgentGamma()
        self.dag_compiler = DagCompiler(BLUEPRINT_REGISTRY)

    def discover_markdown_files(self) -> List[Path]:
        """Discover 100% of .md files in the repository tree."""
        md_files = []
        for p in self.root_dir.rglob("*.md"):
            # Skip hidden directories like .git, .pytest_cache
            if any(part.startswith('.') for part in p.parts[:-1]):
                continue
            md_files.append(p)
        return sorted(md_files)

    def run_subagent_analysis(self) -> Dict[str, Any]:
        """Execute full 4-subagent formal extraction pipeline."""
        files = self.discover_markdown_files()
        results = {}

        for p in files:
            fname = p.name
            with open(p, "r", encoding="utf-8") as fp:
                raw = fp.read()
            body = FrontmatterEngine.extract_body(raw)

            alpha_res = self.sub_alpha.analyze(body)
            beta_res = self.sub_beta.formalize(fname, body)
            gamma_res = self.sub_gamma.scan(body)
            urn = get_urn_for_file(fname)

            results[fname] = {
                "urn": urn,
                "ast": asdict(alpha_res),
                "fsm": asdict(beta_res),
                "security": asdict(gamma_res),
                "body_sha256": FrontmatterEngine.compute_body_sha256(body)
            }

        dag_report = self.dag_compiler.compile()
        results["__DAG__"] = asdict(dag_report)
        return results

    def verify(self) -> Tuple[bool, List[str]]:
        """Verify repository compliance against Fable 5.1.0 schema and checksums."""
        files = self.discover_markdown_files()
        errors = []

        if len(files) != len(BLUEPRINT_REGISTRY):
            errors.append(f"Expected {len(BLUEPRINT_REGISTRY)} markdown files, but discovered {len(files)}.")

        for p in files:
            fname = p.name
            if fname not in BLUEPRINT_REGISTRY:
                errors.append(f"File {fname} is not registered in BLUEPRINT_REGISTRY.")
                continue

            with open(p, "r", encoding="utf-8") as fp:
                content = fp.read()

            if not content.startswith("---\n"):
                errors.append(f"File {fname} is missing YAML frontmatter opening delimiter.")
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append(f"File {fname} has malformed YAML frontmatter structure.")
                continue

            fm_text = parts[1]
            body = parts[2]
            if body.startswith("\n"):
                body = body[1:]

            # Validate fields
            expected_uuid = compute_deterministic_uuid(fname)
            expected_cat = BLUEPRINT_REGISTRY[fname]["category"]
            expected_urn = f"urn:tgn:blueprint:{expected_cat}:{expected_uuid}"
            expected_checksum = FrontmatterEngine.compute_body_sha256(body)

            if f'urn: "{expected_urn}"' not in fm_text:
                errors.append(f"File {fname} has invalid URN in frontmatter (expected {expected_urn}).")

            if f'verification_checksum: "{expected_checksum}"' not in fm_text:
                errors.append(f"File {fname} has invalid verification_checksum.")

            if 'fable_schema: "5.1.0"' not in fm_text:
                errors.append(f"File {fname} is missing fable_schema: '5.1.0'.")

        # Verify DAG properties
        dag = self.dag_compiler.compile()
        if dag.cycles_detected:
            errors.append(f"Cyclical dependencies detected in DAG: {dag.cycles_detected}")

        return (len(errors) == 0, errors)

    def migrate(self, dry_run: bool = False) -> bool:
        """Synthesize and prepend YAML 1.2 frontmatter to 100% of discovered files."""
        files = self.discover_markdown_files()
        print(f"[INGESTION] Discovered {len(files)} markdown documents in repository tree.")

        modified_files = []
        try:
            for p in files:
                fname = p.name
                with open(p, "r", encoding="utf-8") as fp:
                    raw_content = fp.read()

                new_doc = FrontmatterEngine.assemble_document(fname, raw_content)

                if not dry_run:
                    with open(p, "w", encoding="utf-8") as fp:
                        fp.write(new_doc)
                    modified_files.append(p)
                    print(f"  [UPDATED] {fname} (URN: {get_urn_for_file(fname)})")
                else:
                    print(f"  [DRY-RUN] Would update {fname} (URN: {get_urn_for_file(fname)})")

            if not dry_run:
                # Post-migration verification
                is_valid, errors = self.verify()
                if not is_valid:
                    print(f"[ERROR] Post-migration validation failed with {len(errors)} errors:")
                    for err in errors:
                        print(f"  - {err}")
                    print("[ABORT] Initiating atomic Git rollback...")
                    GitTransactionManager.rollback()
                    return False

            print("[SUCCESS] Autonomous repository reconstruction & topological ingestion completed.")
            return True

        except Exception as e:
            print(f"[FATAL EXCEPTION] Migration encountered error: {e}")
            if not dry_run:
                print("[ABORT] Initiating atomic Git rollback...")
                GitTransactionManager.rollback()
            return False


# ---------------------------------------------------------------------------
# CLI ENTRYPOINT
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fable Engine 5.1 / Mythos-Class Migration & Topological Ingestion Pipeline"
    )
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Execute idempotent repository frontmatter migration"
    )
    parser.add_argument(
        "--verify",
        "--check",
        action="store_true",
        help="Verify repository frontmatters, DAG integrity and checksums"
    )
    parser.add_argument(
        "--dag",
        action="store_true",
        help="Display inter-file dependency DAG, cycles, and topological sorting"
    )
    parser.add_argument(
        "--subagents",
        action="store_true",
        help="Run Sub-Agents Alpha, Beta, Gamma, Delta analysis report"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Atomic rollback of working tree changes to HEAD"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate migration without modifying files"
    )

    args = parser.parse_args()
    orchestrator = RepositoryOrchestrator()

    if args.rollback:
        GitTransactionManager.rollback()
        return

    if args.dag:
        dag = orchestrator.dag_compiler.compile()
        print("=" * 60)
        print("DEPENDENCY DAG & TOPOLOGICAL ANALYSIS REPORT")
        print("=" * 60)
        print(f"Total Nodes: {dag.total_nodes}")
        print(f"Total Directed Edges: {dag.total_edges}")
        print(f"Root Components (In-degree 0): {len(dag.root_nodes)} -> {dag.root_nodes}")
        print(f"Leaf Components (Out-degree 0): {len(dag.leaf_nodes)} -> {dag.leaf_nodes}")
        print(f"Orphan Components (Isolated): {len(dag.orphan_nodes)} -> {dag.orphan_nodes}")
        print(f"Cyclical Imports Detected: {len(dag.cycles_detected)}")
        if dag.cycles_detected:
            for c in dag.cycles_detected:
                print(f"  Cycle: {' -> '.join(c)}")
        else:
            print("  [DAG VERIFIED: Strict Directed Acyclic Graph - 0 Cycles]")
        print("\nTopological Processing Order:")
        for idx, node in enumerate(dag.topological_order, 1):
            print(f"  {idx:02d}. {node}")
        return

    if args.subagents:
        analysis = orchestrator.run_subagent_analysis()
        print("=" * 60)
        print("VIRTUAL SUB-AGENT EXTRACTION AUDIT")
        print("=" * 60)
        for fname, data in sorted(analysis.items()):
            if fname == "__DAG__":
                continue
            print(f"\nDOCUMENT: {fname}")
            print(f"  URN: {data['urn']}")
            print(f"  Transport: {data['ast']['inferred_transport']}")
            print(f"  Code Blocks: {data['ast']['total_code_blocks']} {data['ast']['language_breakdown']}")
            print(f"  FSM Defined: {data['fsm']['Q'] != []} (States: {len(data['fsm']['Q'])}, Driver: {data['fsm']['storage_driver']})")
            print(f"  Security Flagged: {len(data['security']['secrets_detected'])} secrets, TMA Safe: {data['security']['tma_hmac_safe']}")
            print(f"  Verification Checksum: {data['body_sha256'][:16]}...")
        return

    if args.verify:
        is_valid, errors = orchestrator.verify()
        if is_valid:
            print("[VERIFICATION PASSED] All 26 markdown files strictly conform to Fable 5.1.0 schema.")
            print("[DAG INTEGRITY] Dependency graph is acyclic and verified.")
            sys.exit(0)
        else:
            print(f"[VERIFICATION FAILED] {len(errors)} issues identified:")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)

    if args.migrate or args.dry_run:
        success = orchestrator.migrate(dry_run=args.dry_run)
        if not success:
            sys.exit(1)
        return

    # Default to running migration
    orchestrator.migrate(dry_run=False)


if __name__ == "__main__":
    main()
