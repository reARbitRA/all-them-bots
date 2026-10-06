"""
Fable-Omega Batch Webhook Configurator
High-speed asynchronous webhook registrar for bulk Telegram Bot tokens with rate limiting and retry handling.
"""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp


async def register_bot_webhook(
    session: aiohttp.ClientSession,
    bot_token: str,
    bot_id: str,
    public_webhook_base_url: str,
    drop_pending_updates: bool = True,
    secret_token: str | None = None,
) -> dict[str, Any]:
    """Set webhook for a single bot token pointing to our multi-tenant server."""
    webhook_url = f"{public_webhook_base_url.rstrip('/')}/webhook/{bot_id}"
    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"

    payload: dict[str, Any] = {
        "url": webhook_url,
        "max_connections": 100,
        "drop_pending_updates": drop_pending_updates,
        "allowed_updates": ["message", "callback_query", "pre_checkout_query"],
    }
    if secret_token:
        # Telegram only accepts 1-256 characters of A-Za-z0-9_-
        payload["secret_token"] = secret_token

    try:
        async with session.post(api_url, json=payload, timeout=10) as resp:
            data = await resp.json()
            if data.get("ok"):
                return {"bot_id": bot_id, "status": "SUCCESS", "webhook_url": webhook_url}
            else:
                return {"bot_id": bot_id, "status": "FAILED", "error": data.get("description")}
    except Exception as e:
        return {"bot_id": bot_id, "status": "ERROR", "error": str(e)}


async def bulk_register_webhooks(
    tokens_map: dict[str, str],  # {"opus_001": "123456:ABC-DEF...", ...}
    public_webhook_base_url: str,
    max_concurrency: int = 15,
    secret_token: str | None = None,
) -> list[dict[str, Any]]:
    """Register hundreds of bot webhooks concurrently in seconds."""
    import os

    secret_token = secret_token or os.getenv("WEBHOOK_SECRET_TOKEN") or None
    semaphore = asyncio.Semaphore(max_concurrency)
    results = []

    async with aiohttp.ClientSession() as session:

        async def _worker(bot_id: str, token: str):
            async with semaphore:
                await asyncio.sleep(0.05)  # 50ms pacing under Telegram burst limits
                res = await register_bot_webhook(
                    session,
                    token,
                    bot_id,
                    public_webhook_base_url,
                    secret_token=secret_token,
                )
                results.append(res)
                return res

        tasks = [_worker(b_id, tok) for b_id, tok in tokens_map.items()]
        await asyncio.gather(*tasks)

    return results


if __name__ == "__main__":
    import os

    url = os.getenv("PUBLIC_WEBHOOK_BASE_URL")
    if not url:
        print("Set PUBLIC_WEBHOOK_BASE_URL=https://yourdomain.com to register.")
        raise SystemExit(1)
    # Pull bot tokens from env (e.g. COMMERCE_BOT_TOKEN, VIP_BOT_TOKEN, ...)
    bot_token_vars = [
        ("commerce", "COMMERCE_BOT_TOKEN"),
        ("vip_paywall", "VIP_BOT_TOKEN"),
        ("ai_gateway", "AI_BOT_TOKEN"),
        ("kata_runner", "KATA_BOT_TOKEN"),
        ("license_reminder", "LICENSE_BOT_TOKEN"),
    ]
    tokens = {bid: os.environ[var] for bid, var in bot_token_vars if os.getenv(var)}
    if not tokens:
        print("No BOT tokens found in environment. Set *_BOT_TOKEN before running.")
        raise SystemExit(1)
    results = asyncio.run(bulk_register_webhooks(tokens, url))
    for r in results:
        print(f"  {r['bot_id']:<18} {r['status']:<8} {r.get('error') or ''}")
