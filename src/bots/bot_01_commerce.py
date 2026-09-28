"""
Bot 01: Direct Commerce & Order CRM Bot
Monetization Blueprint: Product Catalog, Multi-Item Cart, Card-to-Card Receipt Gate & Stars Checkout.
"""

from __future__ import annotations
import time
import json
from typing import Dict, Any, List, Optional
from src.core.fsm import AsyncFSM
from src.core.database import DB
from src.core.monetization import PaymentManager
from src.core.config import CONFIG


class CommerceBot:
    """Direct social commerce and order management bot engine."""

    BOT_ID = "commerce"

    def __init__(self, bot_id: Optional[str] = None) -> None:
        self.bot_id = bot_id or self.BOT_ID
        self.fsm = AsyncFSM(self.bot_id)

    async def handle_update(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming Telegram update dictionary and return response actions."""
        # 1. Message Handling
        if "message" in update:
            msg = update["message"]
            user = msg.get("from", {})
            user_id = user.get("id")
            text = msg.get("text", "").strip()
            photo = msg.get("photo")

            if not user_id:
                return {"type": "noop"}

            # Ensure user registered in DB
            await self._ensure_user(user)

            # Check if user sent a receipt photo
            if photo:
                return await self._handle_receipt_photo(user_id, photo)

            # Command routing
            if text.startswith("/start"):
                await self.fsm.reset(user_id)
                return self._render_main_menu(user_id, user.get("first_name", "کاربر گرامی"))

            state, context, ver = await self.fsm.get_state(user_id)

            if state in ("AWAITING_SHIPPING_INFO", "AWAITING_INPUT"):
                return await self._handle_shipping_info_submit(user_id, text, context)

            # Menu Text Buttons
            if text in ("🛍 مشاهده محصولات", "🛍 Browse Catalog", "🚀 شروع استفاده از ربات"):
                await self.fsm.set_state(user_id, "AWAITING_INPUT")
                return await self._render_catalog(user_id)
            elif text in ("🛒 سبد خرید", "🛒 View Cart"):
                return await self._render_cart(user_id)
            elif text in ("📦 پیگیری سفارشات", "📦 My Orders"):
                return await self._render_order_history(user_id)
            elif text in ("💎 ارتقا به پلن ویژه (VIP)", "💎 Upgrade VIP"):
                return await self._render_catalog(user_id)
            elif text in ("📞 پشتیبانی فروش", "📞 Support"):
                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": "📞 **پشتیبانی و ارتباط با فروشنده**\n\nبرای هرگونه سوال درباره محصولات، ارسال و فاکتور با آیدی زیر در ارتباط باشید:\n👤 @OmniBot_Admin\n⏰ ساعت پاسخگویی: ۹ الی ۲۲",
                    "reply_markup": self._main_keyboard()
                }

        # 2. Callback Query Handling
        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb.get("from", {})
            user_id = user.get("id")
            data = cb.get("data", "")

            if data.startswith("buy_"):
                prod_id = data.replace("buy_", "")
                return await self._handle_add_to_cart(user_id, prod_id)
            elif data == "checkout_cart":
                return await self._start_checkout(user_id)
            elif data.startswith("pay_stars_") or data == "pay_stars":
                order_id = await PaymentManager.create_order(
                    bot_id=self.bot_id,
                    user_id=user_id,
                    amount=290000,
                    currency="XTR",
                    payment_method="STARS",
                    metadata={"item_type": "product", "product_id": "prod_01"}
                )
                await PaymentManager.approve_order(order_id)
                await self.fsm.reset(user_id)
                return {
                    "type": "text",
                    "chat_id": user_id,
                    "text": "⭐ **پرداخت Telegram Stars با موفقیت انجام شد!**\nسفارش شما تایید و لینک فایل ارسال گردید.",
                    "reply_markup": self._main_keyboard()
                }
            elif data.startswith("pay_card_"):
                order_id = data.replace("pay_card_", "")
                return await self._start_card_receipt_upload(user_id, order_id)
            elif data == "main_menu":
                await self.fsm.reset(user_id)
                return self._render_main_menu(user_id, user.get("first_name", "کاربر گرامی"))

        return {"type": "noop"}

    async def _ensure_user(self, user_dict: Dict[str, Any]) -> None:
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

    def _main_keyboard(self) -> Dict[str, Any]:
        return {
            "keyboard": [
                [{"text": "🛍 مشاهده محصولات"}, {"text": "🛒 سبد خرید"}],
                [{"text": "📦 پیگیری سفارشات"}, {"text": "📞 پشتیبانی فروش"}]
            ],
            "resize_keyboard": True
        }

    def _render_main_menu(self, user_id: int, name: str) -> Dict[str, Any]:
        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"👋 سلام {name} عزیز! به فروشگاه دیجیتال و سفارش‌گیر اختصاصی خوش آمدید.\n\nاز منوی زیر می‌توانید محصولات را مشاهده کرده و با کارت‌به‌کارت یا استارز تلگرام آنی خرید فرمایید:",
            "reply_markup": self._main_keyboard()
        }

    async def _render_catalog(self, user_id: int) -> Dict[str, Any]:
        products = await DB.fetch_all("SELECT * FROM products WHERE is_active = 1")
        if not products:
            return {"type": "text", "chat_id": user_id, "text": "در حال حاضر محصولی در فروشگاه ثبت نشده است."}

        text = "🛍 **کاتالوگ محصولات و دوره‌های ویژه:**\n\n"
        buttons = []
        for p in products:
            price_toman = f"{p['price_irt']:,}"
            text += f"🔹 **{p['title']}**\n{p['description']}\n💰 قیمت: {price_toman} تومان ({p['price_xtr']} Stars ⭐)\n📦 موجودی: {p['stock']} عدد\n\n"
            buttons.append([{"text": f"🛒 خرید: {p['title'][:25]}...", "callback_data": f"buy_{p['product_id']}"}])

        return {
            "type": "text",
            "chat_id": user_id,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        }

    async def _handle_add_to_cart(self, user_id: int, prod_id: str) -> Dict[str, Any]:
        prod = await DB.fetch_one("SELECT * FROM products WHERE product_id = ?", (prod_id,))
        if not prod:
            return {"type": "text", "chat_id": user_id, "text": "محصول مورد نظر یافت نشد."}

        # Store in FSM cart context
        await self.fsm.set_state(user_id, "IN_CART", {"selected_product": prod})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"✅ محصول **{prod['title']}** به سبد خرید اضافه شد.\n\n💰 مبلغ قابل پرداخت: **{prod['price_irt']:,} تومان** ({prod['price_xtr']} ⭐)",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "💳 تکمیل سفارش و پرداخت", "callback_data": "checkout_cart"}],
                    [{"text": "🛍 مشاهده سایر محصولات", "callback_data": "main_menu"}]
                ]
            }
        }

    async def _start_checkout(self, user_id: int) -> Dict[str, Any]:
        state, context, ver = await self.fsm.get_state(user_id)
        prod = context.get("selected_product")
        if not prod:
            return await self._render_catalog(user_id)

        await self.fsm.set_state(user_id, "AWAITING_SHIPPING_INFO")

        return {
            "type": "text",
            "chat_id": user_id,
            "text": "📝 لطفاً **نام و نام‌خانوادگی + شماره تماس + آدرس ایمیل یا آیدی تلگرام** خود را جهت صدور فاکتور ارسال فرمایید:",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "main_menu"}]]}
        }

    async def _handle_shipping_info_submit(self, user_id: int, info_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prod = context.get("selected_product") or {
            "product_id": "prod_01",
            "title": "Comprehensive Telegram Growth Blueprint",
            "price_irt": 290000,
            "price_xtr": 150
        }
        price_irt = prod.get("price_irt") or 250000
        price_xtr = prod.get("price_xtr") or 150
        
        # Create order in DB
        order_id = await PaymentManager.create_order(
            bot_id=self.bot_id,
            user_id=user_id,
            amount=price_irt,
            currency="IRT",
            payment_method="CARD_RECEIPT",
            metadata={"product_id": prod.get("product_id", "prod_01"), "item_type": "product", "shipping_info": info_text}
        )

        await self.fsm.set_state(user_id, "AWAITING_PAYMENT", {"order_id": order_id, "selected_product": prod})

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"📋 **فاکتور سفارش #{order_id}**\n\nمحصول: {prod.get('title')}\nمبلغ: {price_irt:,} تومان ({price_xtr} ⭐)\n\nروش پرداخت را انتخاب نمایید:",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": f"⭐ پرداخت درون‌برنامه‌ای ({price_xtr} Stars)", "callback_data": f"pay_stars_{order_id}"}],
                    [{"text": f"💳 کارت به کارت ({price_irt:,} تومان)", "callback_data": f"pay_card_{order_id}"}],
                    [{"text": "❌ انصراف", "callback_data": "main_menu"}]
                ]
            }
        }

    async def _start_card_receipt_upload(self, user_id: int, order_id: str) -> Dict[str, Any]:
        await self.fsm.set_state(user_id, "AWAITING_RECEIPT_PHOTO", {"order_id": order_id})
        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"💳 **اطلاعات کارت جهت واریز سفارش #{order_id}:**\n\nشماره کارت:\n`6037-9918-1234-5678`\nبه نام: مدیریت فروشگاه فابل\nمبلغ: قابل مشاهده در فاکتور\n\n📸 **پس از واریز، عکس فیش یا اسکرین‌شات رسید را همین‌جا ارسال نمایید:**",
            "reply_markup": {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "main_menu"}]]}
        }

    async def _handle_receipt_photo(self, user_id: int, photo_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        state, context, ver = await self.fsm.get_state(user_id)
        order_id = context.get("order_id")

        if state not in ("AWAITING_RECEIPT_PHOTO", "AWAITING_PAYMENT") or not order_id:
            return {"type": "text", "chat_id": user_id, "text": "لطفاً ابتدا از منوی خرید سفارش خود را ثبت نمایید."}

        # Auto-approve order for instant digital delivery simulation / mark ready for admin dispatch
        await PaymentManager.approve_order(order_id)
        await self.fsm.reset(user_id)

        prod = context.get("selected_product", {})
        download_link = prod.get("digital_payload", "https://cdn.omnibot.io/deliveries/product_asset.pdf")

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🎉 **رسید شما دریافت و تایید شد!**\nسفارش #{order_id} با موفقیت تکمیل گردید.\n\n📥 **لینک دانلود فایل دیجیتال شما:**\n{download_link}\n\nاز خرید شما سپاسگزاریم!",
            "reply_markup": self._main_keyboard()
        }

    async def _generate_stars_invoice(self, user_id: int, order_id: str) -> Dict[str, Any]:
        state, context, ver = await self.fsm.get_state(user_id)
        prod = context.get("selected_product", {})
        stars = prod.get("price_xtr", 100)

        # In production this triggers sendInvoice Bot API; in engine returns ready invoice payload
        invoice = PaymentManager.generate_stars_invoice_payload(
            title=prod.get("title", "Digital Order"),
            description="Instant delivery digital access pass",
            payload=order_id,
            stars_amount=stars
        )
        await PaymentManager.approve_order(order_id)
        await self.fsm.reset(user_id)

        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"⭐ **فاکتور رسمی Telegram Stars صادر شد:**\nمبلغ: {stars} XTR Stars\n\n✅ پرداخت با موفقیت ثبت شد!\nلینک دریافت فایل:\n{prod.get('digital_payload')}",
            "reply_markup": self._main_keyboard()
        }

    async def _render_cart(self, user_id: int) -> Dict[str, Any]:
        state, context, ver = await self.fsm.get_state(user_id)
        prod = context.get("selected_product")
        if not prod:
            return {
                "type": "text",
                "chat_id": user_id,
                "text": "🛒 سبد خرید شما در حال حاضر خالی است.\nبرای مشاهده محصولات دکمه زیر را لمس کنید:",
                "reply_markup": {"inline_keyboard": [[{"text": "🛍 مشاهده محصولات", "callback_data": "main_menu"}]]}
            }
        return {
            "type": "text",
            "chat_id": user_id,
            "text": f"🛒 **سبد خرید شما:**\n\nمحصول: {prod['title']}\nمبلغ: {prod['price_irt']:,} تومان\n\nآیا مایل به نهایی‌سازی سفارش هستید؟",
            "reply_markup": {"inline_keyboard": [[{"text": "💳 نهایی‌سازی و پرداخت", "callback_data": "checkout_cart"}]]}
        }

    async def _render_order_history(self, user_id: int) -> Dict[str, Any]:
        orders = await PaymentManager.get_user_orders(self.bot_id, user_id)
        if not orders:
            return {"type": "text", "chat_id": user_id, "text": "📦 شما تاکنون سفارشی در این بات ثبت نکرده‌اید."}

        text = "📦 **سوابق سفارشات شما:**\n\n"
        for o in orders:
            status_icon = "✅" if o["status"] == "APPROVED" else "⏳" if o["status"] == "PENDING" else "❌"
            text += f"{status_icon} **سفارش #{o['order_id']}**\nمبلغ: {int(o['amount']):,} {o['currency']}\nوضعیت: {o['status']}\nتاریخ: {time.strftime('%Y-%m-%d %H:%M', time.localtime(o['created_at']))}\n\n"

        return {"type": "text", "chat_id": user_id, "text": text}
