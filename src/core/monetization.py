"""
Fable-Omega High-Monetization Payments & Billing Engine
Supports Telegram Stars (XTR), Card-to-Card Receipt Gateways, Crypto TON, and VIP Link Provisioning.
"""

from __future__ import annotations
import uuid
import time
import json
from typing import Dict, Any, Optional, Tuple
from src.core.database import DB
from src.core.config import CONFIG


class PaymentManager:
    """Unified multi-channel payment processor for high-conversion monetization."""

    @staticmethod
    async def create_order(
        bot_id: str,
        user_id: int,
        amount: float,
        currency: str,
        payment_method: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new pending order in database."""
        order_id = f"ord_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        now = time.time()
        meta_str = json.dumps(metadata or {})

        await DB.execute("""
        INSERT INTO orders (order_id, bot_id, user_id, amount, currency, payment_method, status, metadata_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)
        """, (order_id, bot_id, user_id, amount, currency, payment_method, meta_str, now))

        return order_id

    @staticmethod
    async def approve_order(order_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Mark an order as APPROVED and fulfill the digital asset / subscription / credits."""
        order = await DB.fetch_one("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        if not order:
            return False, None

        if order["status"] == "APPROVED":
            return True, order

        now = time.time()
        await DB.execute("""
        UPDATE orders SET status = 'APPROVED', resolved_at = ? WHERE order_id = ?
        """, (now, order_id))

        meta = {}
        try:
            meta = json.loads(order["metadata_json"])
        except Exception:
            pass

        bot_id = order["bot_id"]
        user_id = order["user_id"]

        # 1. Credit Top-up Fulfillment
        if meta.get("item_type") == "credits":
            credits_to_add = int(meta.get("credits_amount", 50))
            await DB.execute("""
            UPDATE users SET balance_credits = balance_credits + ? WHERE bot_id = ? AND user_id = ?
            """, (credits_to_add, bot_id, user_id))

        # 2. Premium VIP Subscription Fulfillment (30 days)
        elif meta.get("item_type") == "vip_subscription":
            duration_days = int(meta.get("duration_days", 30))
            premium_until = int(now + (duration_days * 86400))
            await DB.execute("""
            UPDATE users SET is_premium = 1, premium_until = ? WHERE bot_id = ? AND user_id = ?
            """, (premium_until, bot_id, user_id))

        # 3. Product Order Fulfillment
        elif meta.get("item_type") == "product":
            prod_id = meta.get("product_id")
            if prod_id:
                await DB.execute("UPDATE products SET stock = stock - 1 WHERE product_id = ?", (prod_id,))

        return True, order

    @staticmethod
    async def reject_order(order_id: str, reason: str = "Payment verification failed") -> bool:
        """Reject a pending order."""
        now = time.time()
        updated = await DB.execute("""
        UPDATE orders SET status = 'REJECTED', resolved_at = ? WHERE order_id = ? AND status = 'PENDING'
        """, (now, order_id))
        return updated > 0

    @staticmethod
    async def get_user_orders(bot_id: str, user_id: int) -> list[Dict[str, Any]]:
        """Fetch transaction history for a user."""
        return await DB.fetch_all(
            "SELECT * FROM orders WHERE bot_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 20",
            (bot_id, user_id)
        )

    @staticmethod
    def generate_stars_invoice_payload(
        title: str,
        description: str,
        payload: str,
        stars_amount: int
    ) -> Dict[str, Any]:
        """Generate Telegram Bot API sendInvoice payload for Telegram Stars (XTR)."""
        return {
            "title": title,
            "description": description,
            "payload": payload,
            "currency": "XTR",
            "prices": [{"label": title, "amount": stars_amount}]
        }
