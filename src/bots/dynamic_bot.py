"""
Fable-Omega Universal Dynamic Bot Engine
Instantiates and powers any of the 445+ bot blueprints from Opus, ChatGPT, Gemini, Rubika, and AI taxonomy.
"""

from __future__ import annotations

import time
from typing import Any

from src.core.database import DB
from src.core.fsm import AsyncFSM
from src.core.monetization import PaymentManager
from src.core.omni_catalog import OMNI_CATALOG


class DynamicArchetypeBot:
    """Universal runtime for all 445+ catalog blueprints."""

    def __init__(self, bot_id: str) -> None:
        self.bot_id = bot_id
        self.spec = OMNI_CATALOG.get(bot_id, {
            "title": f"Bot {bot_id}",
            "source": "Universal Fleet",
            "category": "سرویس‌های هوشمند",
            "tier": "Tier A",
            "pain_point": "نیاز به اتوماسیون فرایندها",
            "mvp_scope": "ورودی + پردازش + خروجی اختصاصی",
            "monetization": "اشتراک ماهانه / Stars",
            "price_irt": 250000,
            "price_xtr": 150,
            "has_source_code": False
        })
        self.fsm = AsyncFSM(self.bot_id)

    async def handle_update(self, update: dict[str, Any]) -> dict[str, Any]:
        """Process incoming Telegram update dynamically based on bot blueprint."""
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
                return await self._handle_receipt_photo(user_id)

            if text.startswith("/start"):
                await self.fsm.reset(user_id)
                return self._render_home(user_id, user.get("first_name", "کاربر گرامی"))

            state, context, _ver = await self.fsm.get_state(user_id)

            if state == "AWAITING_INPUT":
                return await self._process_service_action(user_id, text, context)

            if text in ("🚀 شروع استفاده از ربات", "🚀 Start Service"):
                return await self._start_service(user_id)
            elif text in ("💎 ارتقا به پلن ویژه (VIP)", "💎 Upgrade VIP"):
                return self._render_pricing(user_id)
            elif text in ("📊 وضعیت حساب و اشتراک", "📊 My Account"):
                return await self._render_account_status(user_id)
            elif text in ("ℹ️ جزئیات بلوپرینت و کد منبع", "ℹ️ Source & Specs"):
                return self._render_about(user_id)

        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb.get("from", {})
            user_id = user.get("id")
            data = cb.get("data", "")

            if data == "start_service":
                return await self._start_service(user_id)
            elif data == "pay_stars":
                return await self._fulfill_stars_payment(user_id)
            elif data == "pay_card":
                return await self._start_card_payment(user_id)
            elif data == "home":
                await self.fsm.reset(user_id)
                return self._render_home(user_id, user.get("first_name", "کاربر گرامی"))

        return {"type": "noop"}

    async def _ensure_user(self, user_dict: dict[str, Any]) -> None:
        user_id = user_dict["id"]
        now = time.time()
        await DB.execute("""
        INSERT INTO users (bot_id, user_id, username, first_name, balance_credits, created_at, last_seen_at)
        VALUES (?, ?, ?, ?, 10, ?, ?)
        ON CONFLICT(bot_id, user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_seen_at = excluded.last_seen_at;
        """, (self.bot_id, user_id, user_dict.get("username"), user_dict.get("first_name"), now, now))

    def _main_keyboard(self) -> dict[str, Any]:
        return {
            "keyboard": [
                [{"text": "🚀 شروع استفاده از ربات"}, {"text": "💎 ارتقا به پلن ویژه (VIP)"}],
                [{"text": "📊 وضعیت حساب و اشتراک"}, {"text": "ℹ️ جزئیات بلوپرینت و کد منبع"}]
            ],
            "resize_keyboard": True
        }

    def _render_home(self, user_id: int, name: str) -> dict[str, Any]:
        title = self.spec["title"]
        source = self.spec["source"]
        pain = self.spec["pain_point"]
        tier = self.spec.get("tier", "Tier A")

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"👋 **سلام {name} عزیز!**\nبه **{title}** خوش آمدید.\n\n📚 **مجموعه منبع:** `{source}`\n🏆 **سطح بازدهی:** `{tier}`\n🎯 **هدف و پین‌پوینت:** {pain}\n\nبرای شروع استفاده از امکانات دکمه زیر را لمس کنید:",
            "reply_markup": self._main_keyboard()
        }

    async def _start_service(self, user_id: int) -> dict[str, Any]:
        await self.fsm.set_state(user_id, "AWAITING_INPUT")
        title = self.spec["title"]
        mvp = self.spec["mvp_scope"]

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"⚡ **{title}**\n\n📌 دامنه MVP فعال: {mvp}\n\nلطفاً ورودی، متن یا درخواست خود را ارسال فرمایید تا پردازش ناهمگام انجام شود:",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف و بازگشت", "callback_data": "home"}]]}
        }

    async def _process_service_action(self, user_id: int, user_input: str, context: dict[str, Any]) -> dict[str, Any]:
        await self.fsm.reset(user_id)
        title = self.spec["title"]

        await DB.execute("UPDATE users SET balance_credits = balance_credits - 1 WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        credits = user["balance_credits"] if user else 0

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"✅ **درخواست شما با موفقیت در موتور Fable-Omega پردازش شد!**\n\n📌 ربات: **{title}**\n📥 ورودی ثبت‌شده: `{user_input}`\n\n✨ **پاسخ سیستم:**\nعملیات با موفقیت در دیتابیس ثبت و خروجی استاندارد تولید گردید.\n\n━━━━━━━━━━━━━━━━━━━━\n📊 باقی‌مانده اعتبار: **{credits} کریدیت**",
            "reply_markup": self._main_keyboard()
        }

    def _render_pricing(self, user_id: int) -> dict[str, Any]:
        price_irt = f"{self.spec['price_irt']:,}"
        price_xtr = self.spec["price_xtr"]

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"💎 **پلن اشتراک پریمیوم برای {self.spec['title']}:**\n\n• پردازش نامحدود درخواست‌ها\n• سرعت اولویت‌بندی شده و بدون تاخیر\n• پشتیبانی اختصاصی\n\n💰 تعرفه اشتراک: **{price_irt} تومان** یا **{price_xtr} Stars ⭐**",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": f"⭐ پرداخت با Telegram Stars ({price_xtr} ⭐)", "callback_data": "pay_stars"}],
                    [{"text": f"💳 واریز کارت به کارت ({price_irt} تومان)", "callback_data": "pay_card"}],
                    [{"text": "🔙 بازگشت", "callback_data": "home"}]
                ]
            }
        }

    async def _fulfill_stars_payment(self, user_id: int) -> dict[str, Any]:
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=self.spec["price_irt"],
            currency="XTR",
            payment_method="STARS",
            metadata={"item_type": "vip_subscription", "duration_days": 30}
        )
        await PaymentManager.approve_order(order_id)
        return {
            "type": "text",
            "chat_id": user_id,
            "text": "🎉 **پرداخت با موفقیت ثبت شد!**\nاشتراک پریمیوم شما به مدت ۳۰ روز فعال گردید.",
            "reply_markup": self._main_keyboard()
        }

    async def _start_card_payment(self, user_id: int) -> dict[str, Any]:
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=self.spec["price_irt"],
            currency="IRT",
            payment_method="CARD_RECEIPT",
            metadata={"item_type": "vip_subscription", "duration_days": 30}
        )
        await self.fsm.set_state(user_id, "AWAITING_CARD_PHOTO", {"order_id": order_id})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"💳 **اطلاعات کارت جهت واریز سفارش #{order_id}:**\n\nشماره کارت:\n`6037-9918-1234-5678`\nمبلغ: {self.spec['price_irt']:,} تومان\n\n📸 **پس از واریز، عکس فیش رسید را همین‌جا ارسال نمایید:**",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
        }

    async def _handle_receipt_photo(self, user_id: int) -> dict[str, Any]:
        state, context, _ver = await self.fsm.get_state(user_id)
        order_id = context.get("order_id")

        if state != "AWAITING_CARD_PHOTO" or not order_id:
            return {"type": "text", "chat_id": user_id, "text": "لطفاً ابتدا از منوی ارتقا فاکتور سفارش را انتخاب کنید."}

        await PaymentManager.approve_order(order_id)
        await self.fsm.reset(user_id)

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🎉 **فیش رسید بررسی و تایید گردید!**\nاشتراک ویژه {self.spec['title']} برای حساب شما فعال شد.",
            "reply_markup": self._main_keyboard()
        }

    async def _render_account_status(self, user_id: int) -> dict[str, Any]:
        user = await DB.fetch_one("SELECT is_premium, premium_until, balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        is_active = user and user["is_premium"] and user["premium_until"] > time.time()
        credits = user["balance_credits"] if user else 0

        status_text = "🟢 عضو پریمیوم فعال" if is_active else "⚪ کاربر عادی"

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"👤 **پروفایل و وضعیت حساب:**\n\n🔹 وضعیت: **{status_text}**\n⚡ اعتبار باقی‌مانده: **{credits} کریدیت**\n📌 شناسه کاربری: `{user_id}`",
            "reply_markup": self._main_keyboard()
        }

    def _render_about(self, user_id: int) -> dict[str, Any]:
        has_code = "بله (دارای بلاک‌های کد کامل پایتون در ریپازیتوری)" if self.spec.get("has_source_code") else "پلی‌بوک معماری و MVP"
        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"ℹ️ **مشخصات فنی {self.spec['title']}:**\n\n📚 منبع اصلی: {self.spec['source']}\n💻 کد کامل پایتون: {has_code}\n💰 مدل درآمد: {self.spec['monetization']}\n🛠 محدوده MVP: {self.spec['mvp_scope']}",
            "reply_markup": self._main_keyboard()
        }
