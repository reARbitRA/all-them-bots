"""
Bot 04: Code Kata & Execution Sandbox Bot
Monetization Blueprint: Interactive coding assessments with isolated Python subprocess execution, test validation & leaderboards.
"""

from __future__ import annotations
import time
import sys
import asyncio
from typing import Dict, Any, List, Tuple
from src.core.fsm import AsyncFSM
from src.core.database import DB
from src.core.monetization import PaymentManager
from src.core.config import CONFIG


class KataRunnerBot:
    """Algorithmic evaluation and coding challenge bot engine."""

    BOT_ID = "kata_runner"

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
                return await self._render_home(user_id, user.get("first_name", "برنامه‌نویس گرامی"))

            state, context, ver = await self.fsm.get_state(user_id)

            if state in ("AWAITING_CODE_SUBMISSION", "AWAITING_INPUT"):
                kata_id = context.get("kata_id", "kata_01")
                return await self._evaluate_code_submission(user_id, kata_id, text)

            if text in ("🧩 لیست چالش‌های کدنویسی", "🧩 Katas", "🚀 شروع استفاده از ربات"):
                await self.fsm.set_state(user_id, "AWAITING_INPUT")
                return await self._render_katas_list(user_id)
            elif text in ("🏆 رتبه‌بندی و امتیازات", "🏆 Leaderboard"):
                return await self._render_leaderboard(user_id)
            elif text in ("⚡ اشتراک پرو (کاتاهای پیشرفته)", "⚡ Pro Plan", "💎 ارتقا به پلن ویژه (VIP)", "💎 اشتراک VIP و امکانات ویژه"):
                return self._render_pro_plans(user_id)

        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb.get("from", {})
            user_id = user.get("id")
            data = cb.get("data", "")

            if data.startswith("solve_"):
                kata_id = data.replace("solve_", "")
                return await self._start_kata_solution(user_id, kata_id)
            elif data.startswith("buy_kata_pro_") or data == "pay_stars":
                return await self._fulfill_kata_pro(user_id)
            elif data == "home":
                await self.fsm.reset(user_id)
                return await self._render_home(user_id, user.get("first_name", "برنامه‌نویس گرامی"))

        return {"type": "noop"}

    async def _ensure_user(self, user_dict: Dict[str, Any]) -> None:
        user_id = user_dict["id"]
        now = time.time()
        await DB.execute("""
        INSERT INTO users (bot_id, user_id, username, first_name, balance_credits, created_at, last_seen_at)
        VALUES (?, ?, ?, ?, 0, ?, ?)
        ON CONFLICT(bot_id, user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_seen_at = excluded.last_seen_at;
        """, (self.bot_id, user_id, user_dict.get("username"), user_dict.get("first_name"), now, now))

    def _main_keyboard(self) -> Dict[str, Any]:
        return {
            "keyboard": [
                [{"text": "🧩 لیست چالش‌های کدنویسی"}, {"text": "🏆 رتبه‌بندی و امتیازات"}],
                [{"text": "⚡ اشتراک پرو (کاتاهای پیشرفته)"}]
            ],
            "resize_keyboard": True
        }

    async def _render_home(self, user_id: int, name: str) -> Dict[str, Any]:
        user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
        score = user["balance_credits"] if user else 0

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"💻 **سلام {name} عزیز! به موتور ارزیابی کد و کاتای الگوریتمی خوش آمدید.**\n\n🎯 امتیاز فعلی شما: **{score} XP**\n\nیک مسئله را انتخاب کرده و کد پایتون خود را جهت تست خودکار در سندباکس ارسال کنید:",
            "reply_markup": self._main_keyboard()
        }

    async def _render_katas_list(self, user_id: int) -> Dict[str, Any]:
        katas = await DB.fetch_all("SELECT * FROM katas")
        buttons = []
        text = "🧩 **چالش‌های الگوریتمی آماده حل:**\n\n"
        for k in katas:
            diff_icon = "🟢" if k["difficulty"] == "Easy" else "🟡" if k["difficulty"] == "Medium" else "🔴"
            text += f"{diff_icon} **{k['title']}** ({k['difficulty']})\n{k['description']}\n🏆 امتیاز: {k['points']} XP\n\n"
            buttons.append([{"text": f"🚀 حل مسئله: {k['title']}", "callback_data": f"solve_{k['kata_id']}"}])

        return {
            "type": "text",
            "chat_id": user_id,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        }

    async def _start_kata_solution(self, user_id: int, kata_id: str) -> Dict[str, Any]:
        kata = await DB.fetch_one("SELECT * FROM katas WHERE kata_id = ?", (kata_id,))
        if not kata:
            return await self._render_katas_list(user_id)

        await self.fsm.set_state(user_id, "AWAITING_CODE_SUBMISSION", {"kata_id": kata_id})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"📝 **مسئله: {kata['title']}** ({kata['difficulty']})\n\n{kata['description']}\n\n💻 **قالب کد اولیه:**\n```python\n{kata['starter_code']}\n```\n\nپاسخ خود را در قالب پیام متنی ارسال کنید:",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
        }

    async def _evaluate_code_submission(self, user_id: int, kata_id: str, user_code: str) -> Dict[str, Any]:
        kata = await DB.fetch_one("SELECT * FROM katas WHERE kata_id = ?", (kata_id,))
        if not kata:
            await self.fsm.reset(user_id)
            return await self._render_home(user_id, "کاربر")

        # Strip markdown ```python backticks if present
        clean_code = user_code
        if clean_code.startswith("```"):
            lines = clean_code.splitlines()
            if len(lines) >= 2:
                clean_code = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])

        # Assemble test harness
        test_harness = f"""
{clean_code}

# Automated Unit Tests
{kata['test_code']}
print("ALL_TESTS_PASSED_SUCCESSFULLY")
"""

        # Execute in isolated subprocess with 3.0s timeout
        start_time = time.perf_counter()
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable,
                "-c",
                test_harness,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=3.0)
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)

            if proc.returncode == 0 and b"ALL_TESTS_PASSED_SUCCESSFULLY" in stdout:
                # Success! Award points
                points = kata["points"]
                await DB.execute("UPDATE users SET balance_credits = balance_credits + ? WHERE bot_id = ? AND user_id = ?", (points, self.bot_id, user_id))
                await self.fsm.reset(user_id)

                user = await DB.fetch_one("SELECT balance_credits FROM users WHERE bot_id = ? AND user_id = ?", (self.bot_id, user_id))
                total_xp = user["balance_credits"] if user else points

                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": f"🎉 **تبریک! تمام تست‌ها با موفقیت پاس شدند!**\n\n⏱ زمان اجرا: **{elapsed_ms}ms**\n🏆 امتیاز کسب شده: **+{points} XP**\n📊 مجموع امتیازات شما: **{total_xp} XP**\n\nعالی بود! می‌توانید چالش بعدی را شروع کنید.",
                    "reply_markup": self._main_keyboard()
                }
            else:
                err_msg = stderr.decode("utf-8", errors="replace")[:400]
                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": f"❌ **خطا در اجرای تست‌ها یا پاسخ اشتباه:**\n\n```text\n{err_msg or 'AssertionError: Output did not match expected test output'}\n```\n\nلطفاً کد را اصلاح کرده و مجدداً ارسال فرمایید:",
                    "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
                }
        except asyncio.TimeoutError:
            return {
                "type": "text",
                "chat_id": user_id,
                "text": "⏱ **خطای محدودیت زمانی (Time Limit Exceeded):**\nکد شما در زمان مجاز ۳ ثانیه به پایان نرسید. به حلقه‌های بی‌نهایت یا بهینه‌سازی پیچیدگی زمانی توجه کنید.",
                "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "home"}]]}
            }

    async def _render_leaderboard(self, user_id: int) -> Dict[str, Any]:
        users = await DB.fetch_all("SELECT first_name, username, balance_credits FROM users WHERE bot_id = ? ORDER BY balance_credits DESC LIMIT 10", (self.bot_id,))
        
        text = "🏆 **جدول رتبه‌بندی برترین برنامه‌نویسان:**\n\n"
        medals = ["🥇", "🥈", "🥉"] + [f"{i}." for i in range(4, 11)]
        
        for idx, u in enumerate(users):
            medal = medals[idx] if idx < len(medals) else f"{idx+1}."
            name = u["first_name"] or u["username"] or "Anonymous Dev"
            text += f"{medal} **{name}** — `{u['balance_credits']} XP`\n"

        return {"type": "text", "chat_id": user_id, "text": text, "reply_markup": self._main_keyboard()}

    def _render_pro_plans(self, user_id: int) -> Dict[str, Any]:
        return {
            "type": "text",
            "chat_id": user_id,
            "text": "⚡ **اشتراک Kata Pro (آمادگی مصاحبه‌های خارجی):**\n\n• بیش از ۳۰۰ مسئله گلچین از شرکت‌های بزرگ (FAANG / Big Tech)\n• تحلیل خط به خط پیچیدگی زمانی و حافظه با AI\n• تست‌های جامع در محیط ایزوله ابری\n\n💰 قیمت: ۲۹۰,۰۰۰ تومان (۲۰۰ Stars ⭐) برای اشتراک ۳ ماهه",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "⭐ خرید با Telegram Stars (200 ⭐)", "callback_data": "buy_kata_pro_stars"}],
                    [{"text": "🔙 بازگشت", "callback_data": "home"}]
                ]
            }
        }

    async def _fulfill_kata_pro(self, user_id: int) -> Dict[str, Any]:
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=290000,
            currency="XTR",
            payment_method="STARS",
            metadata={"item_type": "vip_subscription", "duration_days": 90}
        )
        await PaymentManager.approve_order(order_id)
        return {
            "type": "text",
            "chat_id": user_id,
            "text": "🎉 **اشتراک Kata Pro برای شما فعال گردید!**\nاکنون به تمام مخزن کاتاهای پیشرفته و تحلیل‌های اختصاصی دسترسی دارید.",
            "reply_markup": self._main_keyboard()
        }
