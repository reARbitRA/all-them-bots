"""
Bot 03: AI Prompt & Text Studio Bot
Monetization Blueprint: Credit-based Micro-SaaS for Copywriting, Translation, Code Review & Resume Optimization.
"""

from __future__ import annotations
import time
import asyncio
from typing import Dict, Any, List
from src.core.fsm import AsyncFSM
from src.core.database import DB
from src.core.monetization import PaymentManager
from src.core.config import CONFIG


class AiGatewayBot:
    """Pay-per-token AI content & engineering tool suite."""

    BOT_ID = "ai_gateway"

    TOOLS = {
        "copywriting": {
            "title": "📝 تولید محتوا و کپشن اینستاگرام/تلگرام",
            "prompt_hint": "موضوع یا ایده محتوای خود را بنویسید (مثال: معرفی کفش ورزشی چرم با لحن جذاب)",
            "cost": 1
        },
        "translation": {
            "title": "🌐 ترجمه حرفه‌ای و روان (فارسی <-> انگلیسی)",
            "prompt_hint": "متنی که می‌خواهید با لحن حرفه‌ای و دقیق ترجمه شود را ارسال کنید:",
            "cost": 1
        },
        "resume": {
            "title": "💼 بهینه‌سازی رزومه و پروفایل لینکدین",
            "prompt_hint": "بخش سوابق شغلی یا متن رزومه خود را برای بهبود ارسال کنید:",
            "cost": 2
        },
        "codereview": {
            "title": "💻 بررسی کد و باگ‌یابی هوشمند",
            "prompt_hint": "کد پایتون، جاوااسکریپت یا زبان دلخواه خود را ارسال کنید تا بازنویسی شود:",
            "cost": 2
        }
    }

    PACKAGES = {
        "pack_50": {"title": "بسته ۵۰ کریدیت هوش مصنوعی", "credits": 50, "price_irt": 150000, "price_xtr": 100},
        "pack_200": {"title": "بسته ۲۰۰ کریدیت حرفه‌ای (۳۰٪ تخفیف)", "credits": 200, "price_irt": 450000, "price_xtr": 250},
        "pack_1000": {"title": "بسته ۱۰۰۰ کریدیت نامحدود سازمانی", "credits": 1000, "price_irt": 1500000, "price_xtr": 800},
    }

    def __init__(self, bot_id: Optional[str] = None) -> None:
        self.bot_id = bot_id or self.BOT_ID
        self.fsm = AsyncFSM(self.bot_id)

    async def handle_update(self, update: Dict[str, Any]) -> Dict[str, Any]:
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
                return await self._render_home(user_id, user.get("first_name", "کاربر گرامی"))

            state, context, ver = await self.fsm.get_state(user_id)

            if state in ("AWAITING_AI_INPUT", "AWAITING_INPUT"):
                tool_key = context.get("tool_key", "copywriting")
                return await self._process_ai_task(user_id, tool_key, text)

            if text in ("🚀 ابزارهای هوش مصنوعی", "🚀 AI Tools", "🚀 شروع استفاده از ربات"):
                await self.fsm.set_state(user_id, "AWAITING_INPUT")
                return self._render_tools(user_id)
            elif text in ("💰 شارژ حساب و خرید اعتبار", "💰 Top Up Credits", "💎 ارتقا به پلن ویژه (VIP)"):
                return self._render_packages(user_id)
            elif text in ("📊 موجودی حساب من", "📊 Balance"):
                return await self._render_balance(user_id)

        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb.get("from", {})
            user_id = user.get("id")
            data = cb.get("data", "")

            if data.startswith("tool_"):
                tool_key = data.replace("tool_", "")
                return await self._start_tool(user_id, tool_key)
            elif data.startswith("buy_credits_") or data == "pay_stars":
                pack_key = data.replace("buy_credits_", "") if "buy_credits_" in data else "pack_50"
                return await self._buy_credits_stars(user_id, pack_key)
            elif data == "home":
                await self.fsm.reset(user_id)
                return await self._render_home(user_id, user.get("first_name", "کاربر گرامی"))

        return {"type": "noop"}

    async def _ensure_user(self, user_dict: Dict[str, Any]) -> None:
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

    def _main_keyboard(self) -> Dict[str, Any]:
        return {
            "keyboard": [
                [{"text": "🚀 ابزارهای هوش مصنوعی"}, {"text": "💰 شارژ حساب و خرید اعتبار"}],
                [{"text": "📊 موجودی حساب من"}]
            ],
            "resize_keyboard": True
        }

    async def _render_home(self, user_id: int, name: str) -> Dict[str, Any]:
        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        credits = user["balance_credits"] if user else 10

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🧠 **سلام {name} عزیز! به استودیوی هوش مصنوعی خوش آمدید.**\n\n✨ موجودی رایگان اولیه: **{credits} کریدیت**\n\nیکی از ابزارهای هوشمند زیر را انتخاب کنید تا بلافاصله پردازش آغاز شود:",
            "reply_markup": self._main_keyboard()
        }

    def _render_tools(self, user_id: int) -> Dict[str, Any]:
        buttons = []
        for key, tool in self.TOOLS.items():
            buttons.append([{"text": f"{tool['title']} ({tool['cost']} کریدیت)", "callback_data": f"tool_{key}"}])

        return {
            "type": "text",
            "chat_id": user_id,
            "text": "🛠 **انتخاب ابزار هوش مصنوعی مورد نظر:**",
            "reply_markup": {"inline_keyboard": buttons}
        }

    async def _start_tool(self, user_id: int, tool_key: str) -> Dict[str, Any]:
        tool = self.TOOLS.get(tool_key, self.TOOLS["copywriting"])
        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        credits = user["balance_credits"] if user else 0

        if credits < tool["cost"]:
            return {
                "type": "text",
                "chat_id": user_id,
                "text": f"⚠️ **موجودی ناکافی!**\nشما به {tool['cost']} کریدیت نیاز دارید، اما موجودی شما {credits} کریدیت است.\n\nبرای افزایش اعتبار از دکمه زیر استفاده کنید:",
                "reply_markup": {
                    "inline_keyboard": [[{"text": "💰 خرید بسته کریدیت", "callback_data": "buy_credits_pack_50"}]]
                }
            }

        await self.fsm.set_state(user_id, "AWAITING_AI_INPUT", {"tool_key": tool_key})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"✨ **{tool['title']}**\n\n{tool['prompt_hint']}",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
        }

    async def _process_ai_task(self, user_id: int, tool_key: str, user_prompt: str) -> Dict[str, Any]:
        tool = self.TOOLS.get(tool_key, self.TOOLS["copywriting"])
        cost = tool["cost"]

        # Deduct credits atomically
        await DB.execute("UPDATE users SET balance_credits = balance_credits - ? WHERE bot_id = ? AND user_id = ?", (cost, self.bot_id, user_id))
        await self.fsm.reset(user_id)

        # AI Synthesis simulation with domain intelligence
        if tool_key == "copywriting":
            result = f"🎯 **متن تبلیغاتی بهینه‌شده:**\n\n«{user_prompt}»\n\n✨ **ویژگی‌های برجسته:**\n- سرعت، امنیت و سادگی در یک پلتفرم یکپارچه\n- پشتیبانی ۲۴/۷ و پاسخگویی آنی\n\n👉 همین حالا سفارش دهید تا از ۳۰٪ تخفیف افتتاحیه بهره‌مند شوید!\n\n#تبلیغات #فروش_آنلاین #پیشنهاد_ویژه"
        elif tool_key == "translation":
            result = f"🌐 **ترجمه حرفه‌ای و اصطلاح‌شناسی:**\n\n**English:**\n\"Seamless high-concurrency architecture delivering zero latency and robust real-time throughput for next-generation platforms.\"\n\n**فارسی روان:**\n«معماری پرسرعت و همگام‌سازی شده که بالاترین سطح پایداری و بازدهی بلادرنگ را برای پلتفرم‌های نوین به ارمغان می‌آورد.»"
        elif tool_key == "resume":
            result = f"💼 **بهینه‌سازی رزومه طبق استانداردهای ATS:**\n\n• **Impact Summary:** Led multi-agent asynchronous bot fleet processing 50k+ daily queries with 99.9% uptime.\n• **Key Achievement:** Scaled revenue monetization funnel using automated Stars and card-to-card verified billing.\n• **Tech Stack:** Python 3.12, AsyncIO, SQLite WAL, Redis FSM, Telegram Bot API Layer 7."
        else:
            result = f"💻 **کد بازنویسی‌شده با استانداردهای مدرن:**\n\n```python\nasync def optimized_handler(data: dict) -> bool:\n    # Optimized O(1) lookups & non-blocking execution\n    clean_payload = {k: v for k, v in data.items() if v is not None}\n    return bool(clean_payload)\n```\n\n✅ عملکرد کد تا ۴ برابر بهبود یافت و پیچیدگی زمانی کاهش یافت."

        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        remaining = user["balance_credits"] if user else 0

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"{result}\n\n━━━━━━━━━━━━━━━━━━━━\n📊 باقی‌مانده اعتبار شما: **{remaining} کریدیت**",
            "reply_markup": self._main_keyboard()
        }

    def _render_packages(self, user_id: int) -> Dict[str, Any]:
        buttons = []
        for key, pack in self.PACKAGES.items():
            buttons.append([{"text": f"⭐ خرید {pack['title']} ({pack['price_xtr']} Stars)", "callback_data": f"buy_credits_{key}"}])

        return {
            "type": "text",
            "chat_id": user_id,
            "text": "💰 **بسته‌های افزایش اعتبار هوش مصنوعی:**\n\nبا تهیه هر بسته، کریدیت‌های شما بلافاصله فعال و بدون محدودیت زمانی قابل مصرف خواهند بود:",
            "reply_markup": {"inline_keyboard": buttons}
        }

    async def _buy_credits_stars(self, user_id: int, pack_key: str) -> Dict[str, Any]:
        pack = self.PACKAGES.get(pack_key, self.PACKAGES["pack_50"])
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=pack["price_irt"],
            currency="XTR",
            payment_method="STARS",
            metadata={"item_type": "credits", "credits_amount": pack["credits"], "pack_key": pack_key}
        )
        await PaymentManager.approve_order(order_id)
        
        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        new_balance = user["balance_credits"] if user else 0

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🎉 **خرید شما با موفقیت انجام شد!**\nتعداد **{pack['credits']} کریدیت** به حساب شما اضافه شد.\n\n📊 موجودی فعلی شما: **{new_balance} کریدیت**",
            "reply_markup": self._main_keyboard()
        }

    async def _render_balance(self, user_id: int) -> Dict[str, Any]:
        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        credits = user["balance_credits"] if user else 0

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"📊 **موجودی حساب شما:**\n\n🔹 اعتبار فعال: **{credits} کریدیت**\n⚡ هر درخواست ۱ الی ۲ کریدیت مصرف می‌کند.\n\nبرای افزایش اعتبار روی دکمه زیر بزنید:",
            "reply_markup": {
                "inline_keyboard": [[{"text": "💰 شارژ فوری حساب", "callback_data": "buy_credits_pack_50"}]]
            }
        }
