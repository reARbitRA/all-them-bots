"""
Fable-Omega 15-Mega-Hub Routing & Aggregation Kernel
Maps 445+ micro-SaaS bots into 15 high-converting Telegram Super-Hubs.
Allows running the entire fleet from just 15 BotFather handles on a single account with zero ban risk.
"""

from __future__ import annotations
import time
from typing import Dict, Any, List, Optional
from src.core.omni_catalog import OMNI_CATALOG
from src.core.fsm import AsyncFSM
from src.core.database import DB
from src.core.monetization import PaymentManager


# Master Definition of the 15 Vertical Mega-Hubs
MEGA_HUBS: Dict[str, Dict[str, Any]] = {
    "hub_01_commerce": {
        "title": "🛍️ هاب فروشگاه‌ساز و سفارش‌گیری هوشمند (Commerce Mega-Store)",
        "icon": "🛍️",
        "category": "E-Commerce & Retail",
        "bot_father_username": "Omni_Commerce_SuperBot",
        "description": "تجمیع فروشگاه‌ساز تلگرام، فروش محصولات دانلودی، پیگیری سفارش، فاکتورزن خودکار و تسویه آنی",
        "sub_categories": ["E-Commerce", "E-commerce", "Dropshipping", "Sales Automation"],
        "primary_action": "ورود به فروشگاه دیجیتال و سفارش"
    },
    "hub_02_vip_paywalls": {
        "title": "🔒 هاب اشتراک‌های ویژه و کانال‌های VIP (VIP Paywall Hub)",
        "icon": "🔒",
        "category": "Membership & Monetization",
        "bot_father_username": "Omni_Paywall_SuperBot",
        "description": "مدیریت حق اشتراک کانال و گروه‌های VIP، لینک‌های یک‌بار مصرف، سیستم همکاری در فروش و تمدید خودکار",
        "sub_categories": ["VIP Community", "Subscription", "Monetization", "Affiliate"],
        "primary_action": "خرید اشتراک VIP و لینک اختصاصی"
    },
    "hub_03_ai_studio": {
        "title": "🧠 هاب جامع استودیو هوش مصنوعی (AI Creative & Engineering Suite)",
        "icon": "🧠",
        "category": "AI & Automation",
        "bot_father_username": "Omni_AI_Studio_SuperBot",
        "description": "تجمیع ۹۵ ابزار و بیزینس هوش مصنوعی: تولید محتوا، بازنویسی کد، ترجمه حرفه‌ای، رزومه‌ساز و تحلیل متن",
        "sub_categories": ["AI Assistant", "AI Generation", "AI Content", "AI Business", "AI & Dev"],
        "primary_action": "انتخاب ابزار هوش مصنوعی و تولید محتوا"
    },
    "hub_04_coding_katas": {
        "title": "💻 هاب ارزیابی و مصاحبه برنامه‌نویسی (Developer Sandbox Hub)",
        "icon": "💻",
        "category": "Developer Tools",
        "bot_father_username": "Omni_Kata_Runner_SuperBot",
        "description": "سندباکس اجرای آنلاین کد پایتون، چالش‌های الگوریتمی، آمادگی مصاحبه Big Tech و جدول لیدربورد",
        "sub_categories": ["Coding Challenge", "Code Review", "Developer Tools", "Programming"],
        "primary_action": "حل مسئله الگوریتمی و تست کد"
    },
    "hub_05_b2b_compliance": {
        "title": "🛡️ هاب سررسید و یادآور انقضا (B2B Compliance & Expiry Sentinel)",
        "icon": "🛡️",
        "category": "B2B & Enterprise",
        "bot_father_username": "Omni_Compliance_SuperBot",
        "description": "مدیریت هوشمند تاریخ تمدید دامنه‌ها، سرورها، بیمه‌نامه‌ها، چک‌ها، قراردادها و مجوزهای کاری",
        "sub_categories": ["Compliance", "B2B SaaS", "Reminders", "Asset Management"],
        "primary_action": "ثبت یادآور انقضا و چک"
    },
    "hub_06_fintech_crypto": {
        "title": "📈 هاب فین‌تک، ارز و سیگنال‌های مالی (FinTech & Crypto Hub)",
        "icon": "📈",
        "category": "FinTech & Crypto",
        "bot_father_username": "Omni_Fintech_SuperBot",
        "description": "هشدار لحظه‌ای نرخ تتر، دلار و طلا، مانیتورینگ تراکنش‌های کیف‌پول و آربیتراژ صرافی‌ها",
        "sub_categories": ["FinTech", "Crypto", "Alerts", "Trading"],
        "primary_action": "مشاهده نرخ لحظه‌ای و تنظیم هشدار"
    },
    "hub_07_education_learning": {
        "title": "🎓 هاب آموزش، فلش‌کارت و زبان (Education & Trivia Hub)",
        "icon": "🎓",
        "category": "Education & EdTech",
        "bot_father_username": "Omni_Edu_Master_SuperBot",
        "description": "یادگیری روزانه لغات زبان، سیستم جعبه لایتنر (Spaced Repetition)، آزمون‌های آنلاین و کوییز مسابقه‌ای",
        "sub_categories": ["Education", "Language Learning", "Quiz", "Flashcards"],
        "primary_action": "شروع درس روزانه و حل کوئیز"
    },
    "hub_08_growth_leadgen": {
        "title": "🚀 هاب لیدجنریشن و وایرال مارکتینگ (Growth Hacking Hub)",
        "icon": "🚀",
        "category": "Marketing & Growth",
        "bot_father_username": "Omni_Growth_SuperBot",
        "description": "جمع‌آوری لید B2B، کمپین‌های قرعه‌کشی و زیرمجموعه‌گیری وایرال (Referral Engine) با لینک اختصاصی",
        "sub_categories": ["Marketing", "Lead Generation", "Referral", "Viral Engine"],
        "primary_action": "ساخت کمپین جذب لید و زیرمجموعه‌گیری"
    },
    "hub_09_health_fitness": {
        "title": "🏃 هاب سلامت، تناسب اندام و ردیاب عادت‌ها (Health & Habit Tracker)",
        "icon": "🏃",
        "category": "Health & Lifestyle",
        "bot_father_username": "Omni_Health_Habit_SuperBot",
        "description": "برنامه‌ریزی تمرینی، محاسبه کالری و ماکرو، ردیابی زنجیره عادت‌های روزانه و آب مصرفی",
        "sub_categories": ["Health", "Fitness", "Habit Tracker", "Productivity"],
        "primary_action": "ثبت فعالیت ورزشی و چک‌لیست روزانه"
    },
    "hub_10_real_estate_rental": {
        "title": "🏢 هاب املاک، اجاره‌نشینی و قراردادها (Real Estate & Tenant CRM)",
        "icon": "🏢",
        "category": "Real Estate & CRM",
        "bot_father_username": "Omni_RealEstate_SuperBot",
        "description": "سیستم یادآور سررسید اجاره، ثبت درخواست تعمیرات ملک، آرشیو قراردادها و مدیریت املاک",
        "sub_categories": ["Real Estate", "Tenant CRM", "Property Management"],
        "primary_action": "ثبت ملک و مدیریت اجاره‌نامه"
    },
    "hub_11_productivity_search": {
        "title": "📑 هاب اسناد، جست‌وجوی داخلی و بهره‌وری (Document & Knowledge Hub)",
        "icon": "📑",
        "category": "Productivity & Tools",
        "bot_father_username": "Omni_Doc_Search_SuperBot",
        "description": "جست‌وجوی اسناد و داکیومنت‌های شرکتی، تبدیل PDF به متن، خلاصه‌سازی فایل و بایگانی هوشمند",
        "sub_categories": ["Productivity", "Document Processing", "Search", "Internal Tools"],
        "primary_action": "آپلود و خلاصه‌سازی سند"
    },
    "hub_12_media_optimization": {
        "title": "🎨 هاب بهینه‌سازی فایل و ابزارهای رسانه (Media & Optimization Studio)",
        "icon": "🎨",
        "category": "Media & Design",
        "bot_father_username": "Omni_Media_Studio_SuperBot",
        "description": "فشرده‌سازی عکس بدون افت کیفیت، حذف پس‌زمینه، تبدیل ویس به متن (STT) و ساخت واترمارک",
        "sub_categories": ["Media", "Image Processing", "Audio", "Video Tools"],
        "primary_action": "ارسال تصویر و فشرده‌سازی فوری"
    },
    "hub_13_rubika_baleh_local": {
        "title": "🇮🇷 هاب پیام‌رسان‌های بومی و کارت‌به‌کارت (Rubika & Baleh Local Suite)",
        "icon": "🇮🇷",
        "category": "Local Messengers & Iran",
        "bot_father_username": "Omni_Local_Iran_SuperBot",
        "description": "۵۷ سناریوی بهینه‌شده برای روبیکا، بله و تلگرام، درگاه کارت‌به‌کارت با تایید فیش و پیامک خودکار",
        "sub_categories": ["Local Messengers", "Rubika", "Baleh", "Payment Gateway"],
        "primary_action": "مشاهده پکیج‌های بومی و درگاه کارت"
    },
    "hub_14_gamification_leagues": {
        "title": "🏆 هاب پیش‌بینی، گیمیفیکیشن و تورنمنت (Gaming & Prediction League)",
        "icon": "🏆",
        "category": "Gaming & Engagement",
        "bot_father_username": "Omni_Game_League_SuperBot",
        "description": "لیگ‌های پیش‌بینی مسابقات ورزشی بین دوستان، چالش‌های امتیازی و جوایز گروهی تلگرام",
        "sub_categories": ["Gaming", "Prediction", "Community", "Sports"],
        "primary_action": "ثبت پیش‌بینی مسابقه و جدول رده‌بندی"
    },
    "hub_15_agency_factory": {
        "title": "⚙️ کارخانه بات و پنل اختصاصی مشتریان (White-Label Agency Factory)",
        "icon": "⚙️",
        "category": "Enterprise & White-Label",
        "bot_father_username": "Omni_Agency_Factory_SuperBot",
        "description": "پنل نمایندگی، ساخت و تحویل بات برای مشتریان شرکتی، لایسنس‌گذاری و مدیریت شارژ اختصاصی",
        "sub_categories": ["Agency", "White-Label", "SaaS Factory", "Client Management"],
        "primary_action": "سفارش بات اختصاصی و مدیریت لایسنس"
    }
}


class MegaHubRouter:
    """Intelligent dispatcher for the 15 Mega-Hubs."""

    def __init__(self) -> None:
        self.hubs = MEGA_HUBS
        self._hub_to_bots_map: Dict[str, List[Dict[str, Any]]] = {}
        self._index_bots_into_hubs()

    def _index_bots_into_hubs(self) -> None:
        """Categorize all 445 bots into the 15 Strategic Vertical Hubs."""
        for hub_key in self.hubs:
            self._hub_to_bots_map[hub_key] = []

        for bot_id, spec in OMNI_CATALOG.items():
            assigned = False
            cat = spec.get("category", "")
            title = spec.get("title", "").lower()
            source = spec.get("source_key", "")

            # Match criteria
            if "commerce" in cat.lower() or "store" in title or "shop" in title or "سفارش" in title:
                self._hub_to_bots_map["hub_01_commerce"].append(spec)
                assigned = True
            elif "vip" in cat.lower() or "paywall" in title or "عضویت" in title or "کانال" in title:
                self._hub_to_bots_map["hub_02_vip_paywalls"].append(spec)
                assigned = True
            elif source == "ai_biz" or "ai" in cat.lower() or "هوش مصنوعی" in title:
                self._hub_to_bots_map["hub_03_ai_studio"].append(spec)
                assigned = True
            elif "code" in cat.lower() or "kata" in title or "برنامه‌نویسی" in title or "dev" in cat.lower():
                self._hub_to_bots_map["hub_04_coding_katas"].append(spec)
                assigned = True
            elif "license" in cat.lower() or "reminder" in title or "انقضا" in title or "مجوز" in title:
                self._hub_to_bots_map["hub_05_b2b_compliance"].append(spec)
                assigned = True
            elif "crypto" in cat.lower() or "currency" in title or "ارز" in title or "fintech" in cat.lower():
                self._hub_to_bots_map["hub_06_fintech_crypto"].append(spec)
                assigned = True
            elif "edu" in cat.lower() or "learn" in title or "quiz" in title or "زبان" in title:
                self._hub_to_bots_map["hub_07_education_learning"].append(spec)
                assigned = True
            elif "lead" in cat.lower() or "referral" in title or "وایرال" in title or "growth" in cat.lower():
                self._hub_to_bots_map["hub_08_growth_leadgen"].append(spec)
                assigned = True
            elif "health" in cat.lower() or "habit" in title or "عادت" in title or "ورزش" in title:
                self._hub_to_bots_map["hub_09_health_fitness"].append(spec)
                assigned = True
            elif "estate" in cat.lower() or "rental" in title or "اجاره" in title or "املاک" in title:
                self._hub_to_bots_map["hub_10_real_estate_rental"].append(spec)
                assigned = True
            elif "document" in cat.lower() or "search" in title or "داکیومنت" in title or "pdf" in title:
                self._hub_to_bots_map["hub_11_productivity_search"].append(spec)
                assigned = True
            elif "media" in cat.lower() or "image" in title or "compress" in title or "تصویر" in title:
                self._hub_to_bots_map["hub_12_media_optimization"].append(spec)
                assigned = True
            elif source == "rubika" or "rubika" in cat.lower() or "روبیکا" in title:
                self._hub_to_bots_map["hub_13_rubika_baleh_local"].append(spec)
                assigned = True
            elif "game" in cat.lower() or "league" in title or "پیش‌بینی" in title:
                self._hub_to_bots_map["hub_14_gamification_leagues"].append(spec)
                assigned = True
            else:
                self._hub_to_bots_map["hub_15_agency_factory"].append(spec)

    def get_hub_bots(self, hub_key: str) -> List[Dict[str, Any]]:
        """Return all bots aggregated under a given mega hub."""
        return self._hub_to_bots_map.get(hub_key, [])

    def get_hub_summary(self) -> Dict[str, Any]:
        """Summary of all 15 hubs with aggregated bot counts."""
        summary = {}
        for hub_key, hub_info in self.hubs.items():
            bots = self._hub_to_bots_map.get(hub_key, [])
            summary[hub_key] = {
                **hub_info,
                "bot_count": len(bots),
                "sample_bot_titles": [b["title"] for b in bots[:3]]
            }
        return summary


# Global Singleton Router
HUB_ROUTER = MegaHubRouter()
