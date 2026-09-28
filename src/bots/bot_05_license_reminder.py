"""
Bot 05: B2B License & Expiry Reminder Bot
Monetization Blueprint: Multi-Asset Expiry Tracking for Domains, SSLs, Licenses, Inspections & Warranties with Cron Notifications.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from src.core.database import DB
from src.core.fsm import AsyncFSM
from src.core.monetization import PaymentManager


class LicenseReminderBot:
    """B2B Compliance and asset expiry notification engine."""

    BOT_ID = "license_reminder"

    def __init__(self, bot_id: str | None = None) -> None:
        self.bot_id = bot_id or self.BOT_ID
        self.fsm = AsyncFSM(self.bot_id)

    async def handle_update(self, update: dict[str, Any]) -> dict[str, Any]:
        if "message" in update:
            msg = update["message"]
            user = msg.get("from", {})
            user_id = user.get("id")
            text = msg.get("text", "").strip()

            if not user_id:
                return {"type": "noop"}

            await self._ensure_user(user)

            if text.startswith("/start"):
                await self.fsm.reset(user_id)
                return await self._render_home(user_id, user.get("first_name", "مدیر گرامی"))

            if text in ("➕ ثبت یادآور انقضا جدید", "➕ Add Reminder", "🚀 شروع استفاده از ربات"):
                return await self._start_add_reminder(user_id)
            elif text in ("📋 لیست سررسیدهای من", "📋 My Reminders"):
                return await self._render_reminders_list(user_id)
            elif text in ("💼 پلن تجاری نامحدود (تیم‌ها)", "💼 Business Plan", "💎 ارتقا به پلن ویژه (VIP)", "💎 اشتراک VIP و امکانات ویژه"):
                return self._render_business_plans(user_id)

            state, context, _ver = await self.fsm.get_state(user_id)

            if state in ("AWAITING_TITLE", "AWAITING_INPUT"):
                await self.fsm.set_state(user_id, "AWAITING_DAYS", {"item_title": text})
                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": f"📅 **عنوان ثبت شد:** {text}\n\nچند روز دیگر تاریخ انقضا است؟ (یک عدد وارد کنید، مثلاً `45` یا `365`):",
                    "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
                }

            elif state == "AWAITING_DAYS":
                if not text.isdigit() or int(text) <= 0:
                    return {"type": "text", "chat_id": user_id, "text": "لطفاً یک عدد معتبر بزرگتر از صفر وارد کنید (مثال: `30`):"}

                days_ahead = int(text)
                title = context.get("item_title", "مورد بدون عنوان")
                target_timestamp = time.time() + (days_ahead * 86400)
                rem_id = f"rem_{uuid.uuid4().hex[:8]}"

                await DB.execute("""
                INSERT INTO reminders (reminder_id, bot_id, user_id, title, target_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (rem_id, self.bot_id, user_id, title, target_timestamp, time.time()))

                await self.fsm.reset(user_id)

                formatted_date = time.strftime('%Y-%m-%d', time.localtime(target_timestamp))
                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": f"✅ **یادآور با موفقیت فعال شد!**\n\n📌 موضوع: **{title}**\n📅 تاریخ سررسید: **{formatted_date}** ({days_ahead} روز دیگر)\n🔔 هشدارهای خودکار در ۳۰ روز، ۷ روز، ۱ روز و روز موعد ارسال خواهند شد.",
                    "reply_markup": self._main_keyboard()
                }

        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb.get("from", {})
            user_id = user.get("id")
            data = cb.get("data", "")

            if data.startswith("del_rem_"):
                rem_id = data.replace("del_rem_", "")
                await DB.execute("DELETE FROM reminders WHERE reminder_id = ? AND user_id = ?", (rem_id, user_id))
                return await self._render_reminders_list(user_id)
            elif data == "home" or data == "pay_stars":
                if data == "pay_stars":
                    order_id = await PaymentManager.create_order(
                        bot_id=self.bot_id,
                        user_id=user_id,
                        amount=450000,
                        currency="XTR",
                        payment_method="STARS",
                        metadata={"item_type": "vip_subscription", "duration_days": 365}
                    )
                    await PaymentManager.approve_order(order_id)
                await self.fsm.reset(user_id)
                return await self._render_home(user_id, user.get("first_name", "مدیر گرامی"))

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
                [{"text": "➕ ثبت یادآور انقضا جدید"}, {"text": "📋 لیست سررسیدهای من"}],
                [{"text": "💼 پلن تجاری نامحدود (تیم‌ها)"}]
            ],
            "resize_keyboard": True
        }

    async def _render_home(self, user_id: int, name: str) -> dict[str, Any]:
        count_row = await DB.fetch_one("SELECT COUNT(*) as cnt FROM reminders WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        count = count_row["cnt"] if count_row else 0

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🛡️ **سلام {name} عزیز! به سیستم مدیریت سررسید و تمدید انقضا خوش آمدید.**\n\n📌 تعداد یادآورهای فعال شما: **{count} مورد**\n\nبا این بات دیگر هیچ تمدید دامنه، مجوز کاری، بیمه، قسط یا قراردادی فراموش نمی‌شود:",
            "reply_markup": self._main_keyboard()
        }

    async def _start_add_reminder(self, user_id: int) -> dict[str, Any]:
        await self.fsm.set_state(user_id, "AWAITING_TITLE")
        return {
            "type": "text",
            "chat_id": user_id,
            "text": "📝 **عنوان یا موضوع مورد نظر را بنویسید:**\n(مثال: `تمدید دامنه سایت mycompany.ir` یا `مجوز فعالیت صنفی` یا `بیمه خودرو`):",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
        }

    async def _render_reminders_list(self, user_id: int) -> dict[str, Any]:
        items = await DB.fetch_all("SELECT * FROM reminders WHERE bot_id = ? AND user_id = ? ORDER BY target_date ASC", (self.bot_id, user_id))
        if not items:
            return {
                "type": "text",
                "chat_id": user_id,
                "text": "📋 در حال حاضر هیچ یادآور فعالی ندارید.\nبرای افزودن دکمه زیر را لمس کنید:",
                "reply_markup": {"inline_keyboard": [[{"text": "➕ افزودن یادآور جدید", "callback_data": "home"}]]}
            }

        text = "📋 **لیست سررسیدها و یادآورهای ثبت‌شده شما:**\n\n"
        now = time.time()
        buttons = []

        for it in items:
            remaining_days = int((it["target_date"] - now) / 86400)
            date_str = time.strftime('%Y-%m-%d', time.localtime(it["target_date"]))
            status = f"⏳ {remaining_days} روز مانده" if remaining_days > 0 else "🚨 منقضی شده!"
            text += f"🔹 **{it['title']}**\n📅 تاریخ: {date_str} ({status})\n\n"
            buttons.append([{"text": f"🗑 حذف: {it['title'][:20]}...", "callback_data": f"del_rem_{it['reminder_id']}"}])

        return {
            "type": "text",
            "chat_id": user_id,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        }

    def _render_business_plans(self, user_id: int) -> dict[str, Any]:
        return {
            "type": "text",
            "chat_id": user_id,
            "text": "💼 **پلن تجاری Business Compliance Pro:**\n\n• امکان ثبت نامحدود یادآور و سررسید برای شرکت‌ها\n• ارسال همزمان اعلان‌ها به ایمیل و پیامک مدیران\n• داشبورد تحت وب اختصاصی جهت گزارش‌گیری تیمی\n\n💰 هزینه: ۴۵۰,۰۰۰ تومان (۳۰۰ Stars ⭐) برای اشتراک سالانه",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "⭐ ارتقا به پلن تجاری (300 Stars)", "callback_data": "home"}]
                ]
            }
        }
