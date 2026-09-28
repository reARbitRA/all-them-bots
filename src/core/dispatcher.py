"""
Fable-Omega Omni-Tenant Fleet Dispatcher
Unified routing for all 445+ bot blueprints across Opus, ChatGPT, Gemini, Rubika, and AI taxonomy.
"""

from __future__ import annotations

from typing import Any

from src.bots.bot_01_commerce import CommerceBot
from src.bots.bot_02_vip_paywall import VipPaywallBot
from src.bots.bot_03_ai_gateway import AiGatewayBot
from src.bots.bot_04_kata_runner import KataRunnerBot
from src.bots.bot_05_license_reminder import LicenseReminderBot
from src.bots.dynamic_bot import DynamicArchetypeBot
from src.core.rate_limiter import RATE_LIMITER
from src.core.resource_optimizer import GLOBAL_BOT_POOL, GLOBAL_RESOURCE_MONITOR


class MultiTenantDispatcher:
    """Central bot fleet dispatcher and lifecycle coordinator with LRU memory optimization."""

    def __init__(self) -> None:
        self.dedicated_bots = {
            "commerce": CommerceBot("commerce"),
            "chatgpt_001": CommerceBot("chatgpt_001"),
            "vip_paywall": VipPaywallBot("vip_paywall"),
            "chatgpt_011": VipPaywallBot("chatgpt_011"),
            "ai_gateway": AiGatewayBot("ai_gateway"),
            "chatgpt_141": AiGatewayBot("chatgpt_141"),
            "kata_runner": KataRunnerBot("kata_runner"),
            "opus_007": KataRunnerBot("opus_007"),
            "license_reminder": LicenseReminderBot("license_reminder"),
            "chatgpt_126": LicenseReminderBot("chatgpt_126"),
        }
        self.bot_pool = GLOBAL_BOT_POOL

    def get_bot(self, bot_id: str):
        """Retrieve dedicated or dynamic bot instance from LRU pool (Lazy instantiation)."""
        if bot_id in self.dedicated_bots:
            return self.dedicated_bots[bot_id]

        bot = self.bot_pool.get(bot_id)
        if bot is None:
            bot = DynamicArchetypeBot(bot_id)
            self.bot_pool.put(bot_id, bot)

        return bot

    async def dispatch_update(
        self, bot_id: str, update: dict[str, Any], bypass_rate_limit: bool = False
    ) -> dict[str, Any]:
        """Route incoming update through rate limiter to target bot handler with telemetry tracking."""
        GLOBAL_RESOURCE_MONITOR.record_request()
        bot = self.get_bot(bot_id)

        # Extract peer id for per-chat rate limiting
        peer_id = None
        if "message" in update:
            peer_id = update["message"].get("from", {}).get("id")
        elif "callback_query" in update:
            peer_id = update["callback_query"].get("from", {}).get("id")

        # Acquire token bucket rate permit (30 req/s global, 1 req/s peer) unless in test mode
        await RATE_LIMITER.acquire(peer_id=peer_id, bypass=bypass_rate_limit)

        # Execute handler
        return await bot.handle_update(update)


# Global Dispatcher Singleton
DISPATCHER = MultiTenantDispatcher()
