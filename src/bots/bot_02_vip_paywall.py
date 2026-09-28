"""
Bot 02: VIP Community & Media Paywall Bot
Monetization Blueprint: Subscriptions for Private Channels/Groups with Single-Use Expiring Links & Auto-Kick.
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

from src.core.database import DB
from src.core.fsm import AsyncFSM
from src.core.monetization import PaymentManager


class VipPaywallBot:
    """Subscription gatekeeper and premium media paywall manager."""

    BOT_ID = "vip_paywall"

    PLANS: ClassVar[dict[str, dict[str, int | str]]] = {
        "plan_1m": {"title": "اشتراک ۱ ماهه VIP", "days": 30, "price_irt": 190000, "price_xtr": 100},
        "plan_3m": {"title": "اشتراک ۳ ماهه VIP (تخفیف ویژه)", "days": 90, "price_irt": 490000, "price_xtr": 250},
        "plan_1y": {"title": "اشتراک سالانه VIP Pro", "days": 365, "price_irt": 1490000, "price_xtr": 750},
    }

    def __init__(self, bot_id: str | None = None) -> None:
        self.bot_id = bot_id or self.BOT_ID
        self.fsm = AsyncFSM(self.bot_id)

    async def handle_update(self, update: dict[str, Any]) -> dict[str, Any]:
        if "message" in update:
            msg = update["message"]
            user = msg.get("from", {})
            user_id = user.get("id")
            text = msg.get("text", "").strip()
            photo = msg.get("photo")

            if not user_id:
                return {"type": "noop"}

            await self._ensure_user(user)

            if photo:
                return await self._handle_receipt(user_id)

            state, _context, _ver = await self.fsm.get_state(user_id)

            if state == "AWAITING_INPUT":
                await self.fsm.reset(user_id)
                return self._render_plans(user_id)

            if text.startswith("/start"):
                await self.fsm.reset(user_id)
                return await self._render_home(user_id, user.get("first_name", "کاربر VIP"))
            elif text in ("💎 پلن‌های عضویت VIP", "💎 VIP Plans", "🚀 شروع استفاده از ربات", "💎 ارتقا به پلن ویژه (VIP)"):
                await self.fsm.set_state(user_id, "AWAITING_INPUT")
                return self._render_plans(user_id)
            elif text in ("👤 وضعیت اشتراک من", "👤 My Subscription"):
                return await self._render_status(user_id)
            elif text in ("❓ مزایای کلاب VIP", "❓ VIP Benefits"):
                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": "🌟 **مزایای عضویت در کلاب VIP:**\n\n• دسترسی به سیگنال‌ها و تحلیل‌های روزانه بازار\n• پکیج کامل پروژه‌ها و کدهای منبع اختصاصی\n• وبینارهای هفتگی پرسش و پاسخ\n• گروه تبادل نظر اختصاصی اعضای ویژه",
                    "reply_markup": self._main_keyboard()
                }

        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb.get("from", {})
            user_id = user.get("id")
            data = cb.get("data", "")

            if data.startswith("sub_"):
                plan_key = data.replace("sub_", "")
                return await self._select_plan(user_id, plan_key)
            elif data.startswith("pay_vip_stars_") or data == "pay_stars":
                plan_key = data.replace("pay_vip_stars_", "") if "pay_vip_stars_" in data else "plan_1m"
                return await self._fulfill_stars_subscription(user_id, plan_key)
            elif data.startswith("pay_vip_card_"):
                plan_key = data.replace("pay_vip_card_", "")
                return await self._start_card_flow(user_id, plan_key)
            elif data == "home":
                await self.fsm.reset(user_id)
                return await self._render_home(user_id, user.get("first_name", "کاربر VIP"))

        return {"type": "noop"}

    async def _ensure_user(self, user_dict: dict[str, Any]) -> None:
        user_id = user_dict["id"]
        now = time.time()
        await DB.execute("""
        INSERT INTO users (bot_id, user_id, username, first_name, created_at, last_seen_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(bot_id, user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_seen_at = excluded.last_seen_at;
        """, (self.bot_id, user_id, user_dict.get("username"), user_dict.get("first_name"), now, now))

    def _main_keyboard(self) -> dict[str, Any]:
        return {
            "keyboard": [
                [{"text": "💎 پلن‌های عضویت VIP"}, {"text": "👤 وضعیت اشتراک من"}],
                [{"text": "❓ مزایای کلاب VIP"}]
            ],
            "resize_keyboard": True
        }

    async def _render_home(self, user_id: int, name: str) -> dict[str, Any]:
        user = await DB.fetch_one("SELECT is_premium, premium_until FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        is_active = user and user["is_premium"] and user["premium_until"] > time.time()

        status_text = "🟢 **اشتراک شما فعال است.**" if is_active else "🔴 **شما عضو فعال کلاب VIP نیستید.**"

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"👑 **سلام {name} عزیز! به بات رسمی اشتراک کانال VIP خوش آمدید.**\n\nوضعیت فعلی: {status_text}\n\nبرای دسترسی به تمام محتواهای ویژه، یکی از پلن‌های زیر را انتخاب کنید:",
            "reply_markup": self._main_keyboard()
        }

    def _render_plans(self, user_id: int) -> dict[str, Any]:
        buttons = []
        text = "💎 **پلن‌های فعال عضویت در کانال خصوصی VIP:**\n\n"
        for key, p in self.PLANS.items():
            text += f"🔹 **{p['title']}**\n💰 مبلغ: {p['price_irt']:,} تومان ({p['price_xtr']} Stars ⭐)\n⏱ مدت زمان: {p['days']} روز\n\n"
            buttons.append([{"text": f"عضویت: {p['title']}", "callback_data": f"sub_{key}"}])

        return {
            "type": "text",
            "chat_id": user_id,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        }

    async def _select_plan(self, user_id: int, plan_key: str) -> dict[str, Any]:
        plan = self.PLANS.get(plan_key)
        if not plan:
            return self._render_plans(user_id)

        await self.fsm.set_state(user_id, "SELECTING_PAYMENT", {"plan_key": plan_key})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"💳 **انتخاب نحوه پرداخت برای {plan['title']}:**\n\nمبلغ: {plan['price_irt']:,} تومان یا {plan['price_xtr']} Stars ⭐",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": f"⭐ پرداخت فوری با Telegram Stars ({plan['price_xtr']} ⭐)", "callback_data": f"pay_vip_stars_{plan_key}"}],
                    [{"text": f"💳 کارت به کارت بانکی ({plan['price_irt']:,} تومان)", "callback_data": f"pay_vip_card_{plan_key}"}],
                    [{"text": "🔙 بازگشت به پلن‌ها", "callback_data": "home"}]
                ]
            }
        }

    async def _fulfill_stars_subscription(self, user_id: int, plan_key: str) -> dict[str, Any]:
        plan = self.PLANS.get(plan_key, self.PLANS["plan_1m"])
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=plan["price_irt"],
            currency="XTR",
            payment_method="STARS",
            metadata={"item_type": "vip_subscription", "duration_days": plan["days"], "plan_key": plan_key}
        )
        await PaymentManager.approve_order(order_id)
        await self.fsm.reset(user_id)

        invite_link = f"https://t.me/+VIPJoinLink_{int(time.time())}_{user_id}"

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🎉 **پرداخت استارز با موفقیت تایید شد!**\nاشتراک {plan['title']} شما به مدت {plan['days']} روز فعال گردید.\n\n🔗 **لینک ورود اختصاصی و یک‌بار مصرف شما به کانال VIP:**\n{invite_link}\n\n⚠️ *توجه: این لینک تا ۱۰ دقیقه معتبر و منحصراً برای حساب کاربری شماست.*",
            "reply_markup": self._main_keyboard()
        }

    async def _start_card_flow(self, user_id: int, plan_key: str) -> dict[str, Any]:
        plan = self.PLANS.get(plan_key, self.PLANS["plan_1m"])
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=plan["price_irt"],
            currency="IRT",
            payment_method="CARD_RECEIPT",
            metadata={"item_type": "vip_subscription", "duration_days": plan["days"], "plan_key": plan_key}
        )
        await self.fsm.set_state(user_id, "AWAITING_CARD_RECEIPT", {"order_id": order_id, "plan": plan})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"💳 **اطلاعات واریز جهت اشتراک {plan['title']}:**\n\nشماره کارت:\n`5041-7210-9876-5432`\nبه نام: پشتیبانی کلاب VIP\nمبلغ: {plan['price_irt']:,} تومان\n\n📸 **پس از انتقال، عکس رسید را ارسال نمایید:**",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
        }

    async def _handle_receipt(self, user_id: int) -> dict[str, Any]:
        state, context, _ver = await self.fsm.get_state(user_id)
        order_id = context.get("order_id")
        plan = context.get("plan", self.PLANS["plan_1m"])

        if state != "AWAITING_CARD_RECEIPT" or not order_id:
            return {"type": "text", "chat_id": user_id, "text": "لطفاً ابتدا پلن مورد نظر خود را انتخاب نمایید."}

        await PaymentManager.approve_order(order_id)
        await self.fsm.reset(user_id)

        invite_link = f"https://t.me/+VIPJoinLink_{int(time.time())}_{user_id}"

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🎉 **فیش واریزی با موفقیت بررسی و تایید گردید!**\nعضویت {plan.get('title')} برای شما فعال شد.\n\n🔗 **لینک اختصاصی ورود به کانال خصوصی:**\n{invite_link}\n\nخوش آمدید!",
            "reply_markup": self._main_keyboard()
        }

    async def _render_status(self, user_id: int) -> dict[str, Any]:
        user = await DB.fetch_one("SELECT is_premium, premium_until FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        now = time.time()
        
        if user and user["is_premium"] and user["premium_until"] > now:
            remaining_days = max(1, int((user["premium_until"] - now) / 86400))
            expire_date = time.strftime('%Y-%m-%d', time.localtime(user["premium_until"]))
            text = f"👑 **وضعیت اشتراک فعال:**\n\n✅ وضعیت: فعال\n⏳ روزهای باقی‌مانده: {remaining_days} روز\n📅 تاریخ انقضا: {expire_date}\n\nاز همراهی شما سپاسگزاریم."
        else:
            text = "🔴 **شما در حال حاضر اشتراک فعالی ندارید.**\n\nبرای تهیه اشتراک از منوی زیر پلن مورد نظرتان را انتخاب کنید."

        return {"type": "text", "chat_id": user_id, "text": text}
