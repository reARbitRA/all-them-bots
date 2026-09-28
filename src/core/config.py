"""
Fable-Omega Core Configuration Engine
Central configuration, environment binding, and currency settings.
"""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)


class CurrencyConfig(BaseModel):
    usd_to_irt: float = 65000.0  # 1 USD = 65,000 Tomans
    xtr_to_usd: float = 0.02      # 1 Telegram Star = $0.02 USD
    ton_to_usd: float = 5.50      # 1 TON = $5.50 USD


class BotDefinition(BaseModel):
    id: str
    name: str
    category: str
    description: str
    default_monthly_price_irt: int
    default_monthly_price_xtr: int
    enabled: bool = True
    token: str = Field(default="")
    admin_ids: list[int] = Field(default_factory=list)


class AppConfig(BaseModel):
    env: str = Field(default_factory=lambda: os.getenv("APP_ENV", "production"))
    debug: bool = Field(default_factory=lambda: os.getenv("APP_DEBUG", "false").lower() == "true")
    server_host: str = Field(default_factory=lambda: os.getenv("SERVER_HOST", "0.0.0.0"))
    server_port: int = Field(default_factory=lambda: int(os.getenv("SERVER_PORT", "8000")))
    public_url: str = Field(default_factory=lambda: os.getenv("PUBLIC_URL", "http://localhost:8000"))
    
    # Database
    db_path: Path = DATA_DIR / "omnibot_production.db"
    
    # Master Admin Telegram IDs
    master_admin_ids: list[int] = Field(default_factory=lambda: [
        int(x.strip()) for x in os.getenv("ADMIN_IDS", "123456789").split(",") if x.strip().isdigit()
    ])
    
    # Financial Settings
    currency: CurrencyConfig = CurrencyConfig()
    
    # Bot Fleet Registry
    bots: dict[str, BotDefinition] = Field(default_factory=lambda: {
        "commerce": BotDefinition(
            id="commerce",
            name="Direct Commerce & Order CRM Bot",
            category="E-Commerce & CRM",
            description="Automated product catalog, cart checkout, receipt OCR verification, and delivery tracking for social channels.",
            default_monthly_price_irt=250000,
            default_monthly_price_xtr=150,
            enabled=True,
            token=os.getenv("COMMERCE_BOT_TOKEN", "")
        ),
        "vip_paywall": BotDefinition(
            id="vip_paywall",
            name="VIP Community & Media Paywall Bot",
            category="Monetization & VIP",
            description="Automated VIP channel/group subscription gatekeeper with auto-expiring single-use invite links and auto-kick.",
            default_monthly_price_irt=190000,
            default_monthly_price_xtr=100,
            enabled=True,
            token=os.getenv("VIP_BOT_TOKEN", "")
        ),
        "ai_gateway": BotDefinition(
            id="ai_gateway",
            name="AI Prompt & Text Studio Bot",
            category="AI Micro-SaaS",
            description="Pay-per-token AI assistant for content generation, resume optimization, and code review with Stars credit refills.",
            default_monthly_price_irt=350000,
            default_monthly_price_xtr=250,
            enabled=True,
            token=os.getenv("AI_BOT_TOKEN", "")
        ),
        "kata_runner": BotDefinition(
            id="kata_runner",
            name="Code Kata & Execution Sandbox Bot",
            category="EdTech & Developer Tools",
            description="Interactive algorithmic challenges with sandboxed code execution, test verification, and competitive leaderboards.",
            default_monthly_price_irt=290000,
            default_monthly_price_xtr=200,
            enabled=True,
            token=os.getenv("KATA_BOT_TOKEN", "")
        ),
        "license_reminder": BotDefinition(
            id="license_reminder",
            name="B2B License & Expiry Reminder Bot",
            category="B2B Utility SaaS",
            description="Automated expiry tracking for domains, permits, vehicle inspections, and contracts with scheduled multi-channel alerts.",
            default_monthly_price_irt=450000,
            default_monthly_price_xtr=300,
            enabled=True,
            token=os.getenv("LICENSE_BOT_TOKEN", "")
        ),
    })


# Global singleton configuration
CONFIG = AppConfig()
