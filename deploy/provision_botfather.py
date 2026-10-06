"""
Fable-Omega BotFather Automated Provisioner & Safety Throttler
Automates the creation and configuration of Telegram Bots via MTProto Userbot session with strict anti-flood guardrails.
"""

from __future__ import annotations

import asyncio
import json
import random
from pathlib import Path
from typing import Any

# Minimum and maximum safety delays between BotFather commands to prevent FloodWait/Ban
MIN_COMMAND_DELAY_SEC = 15.0
MAX_COMMAND_DELAY_SEC = 35.0
MAX_BOTS_PER_ACCOUNT_SESSION = 18  # Safe margin below Telegram's 20-bot hard limit per account


class BotFatherProvisioner:
    """Safe programmatic creator for bulk Telegram bots."""

    @staticmethod
    def generate_unique_username(bot_id: str, prefix: str = "Omni", suffix: str = "bot") -> str:
        """Generate a valid, clean Telegram bot username ending in 'bot'."""
        clean_id = bot_id.replace("_", "").replace("-", "")[:15]
        rnd = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=4))
        return f"{prefix}_{clean_id}_{rnd}_{suffix}"

    @staticmethod
    def load_catalog_specs(json_catalog_path: Path) -> list[dict[str, Any]]:
        """Load bot specs from omni-catalog."""
        from src.core.omni_catalog import OMNI_CATALOG
        return list(OMNI_CATALOG.values())

    @staticmethod
    async def simulate_safe_creation_plan(target_count: int = 445) -> dict[str, Any]:
        """
        Calculates the required Telegram accounts, time schedule, and safety batching
        to create the fleet without triggering Telegram anti-spam detection.
        """
        accounts_needed = (target_count + MAX_BOTS_PER_ACCOUNT_SESSION - 1) // MAX_BOTS_PER_ACCOUNT_SESSION
        avg_delay = (MIN_COMMAND_DELAY_SEC + MAX_COMMAND_DELAY_SEC) / 2
        total_time_minutes = (target_count * avg_delay) / 60

        plan = {
            "total_bots_to_create": target_count,
            "max_bots_per_account": MAX_BOTS_PER_ACCOUNT_SESSION,
            "telegram_accounts_needed": accounts_needed,
            "avg_delay_between_creations_sec": avg_delay,
            "estimated_provisioning_duration_hours": round(total_time_minutes / 60, 2),
            "safety_rules": [
                "Use aged Telegram accounts (> 3 months old) to prevent instant spam flags",
                "Do not exceed 15-18 bots per Telegram phone number",
                "Maintain 15-35 second random jitter between BotFather chat interactions",
                "If FLOOD_WAIT is returned by Telegram, pause execution immediately for the requested seconds",
                "Store tokens directly into an encrypted JSON or environment file"
            ]
        }
        return plan


if __name__ == "__main__":
    plan = asyncio.run(BotFatherProvisioner.simulate_safe_creation_plan(445))
    print("=" * 70)
    print("📋 TELEGRAM BOT FLEET PROVISIONING & ANTI-BAN BLUEPRINT")
    print("=" * 70)
    print(json.dumps(plan, indent=2, ensure_ascii=False))
