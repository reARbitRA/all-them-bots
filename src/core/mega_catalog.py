"""
Fable-Omega Mega-Catalog & Comprehensive Fleet Registry
Dynamically ingests and indexes all 150 Telegram Bot Blueprints from repository markdown.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, Any, List


BASE_DIR = Path(__file__).resolve().parent.parent.parent


CATEGORIES = {
    "A": {"name": "فروش، CRM و اتوماسیون کسب‌وکار", "range": (1, 10), "archetype": "commerce"},
    "B": {"name": "محتواسازها و کامیونیتی پولی", "range": (11, 20), "archetype": "subscription_gate"},
    "C": {"name": "آموزش، زبان و آزمون‌های تخصصی", "range": (21, 30), "archetype": "assessment_quiz"},
    "D": {"name": "بهره‌وری فردی و مدیریت کارها", "range": (31, 40), "archetype": "productivity_tool"},
    "E": {"name": "مالی، بودجه‌بندی و سرمایه‌گذاری", "range": (41, 50), "archetype": "productivity_tool"},
    "F": {"name": "استخدام، HR، فریلنسرها", "range": (51, 60), "archetype": "lead_capture"},
    "G": {"name": "املاک، خودرو و بازارهای محلی", "range": (61, 70), "archetype": "lead_capture"},
    "H": {"name": "سفر، رویداد، سبک زندگی شهری", "range": (71, 80), "archetype": "booking_scheduler"},
    "I": {"name": "املاک، خدمات خانه، کارهای روزمره", "range": (81, 90), "archetype": "lead_capture"},
    "J": {"name": "تجارت الکترونیک، لجستیک، پس از فروش", "range": (91, 100), "archetype": "commerce"},
    "K": {"name": "ابزار برای دولوپرها و تیم‌های فنی", "range": (101, 110), "archetype": "assessment_quiz"},
    "L": {"name": "مارکتینگ، فروش، شبکه‌های اجتماعی", "range": (111, 120), "archetype": "ai_agent"},
    "M": {"name": "حقوقی، قرارداد و اداری", "range": (121, 130), "archetype": "b2b_compliance"},
    "N": {"name": "رسانه، فایل، ابزارهای کوچک ولی پول‌ساز", "range": (131, 140), "archetype": "subscription_gate"},
    "O": {"name": "سرگرمی، بازی، سوشال و نیچ‌کامیونیتی", "range": (141, 150), "archetype": "ai_agent"},
}


def load_all_150_bots() -> Dict[str, Dict[str, Any]]:
    """Parse all 150 bot blueprints directly from 150 TELEGRAM BOT.md."""
    md_file = BASE_DIR / "docs" / "original_blueprints" / "150 TELEGRAM BOT.md"
    if not md_file.exists():
        md_file = BASE_DIR / "150 TELEGRAM BOT.md"
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Pattern: 1) **Title** — Pain — MVP — Monetization
    pattern = r'([0-9]{1,3})\)\s*\*\*([^\*]+)\*\*\s*[—–-]\s*([^—–\n]+)\s*[—–-]\s*([^—–\n]+)\s*[—–-]\s*([^\n]+)'
    matches = re.findall(pattern, text)

    catalog = {}
    for num_str, title, pain, mvp, mon in matches:
        num = int(num_str)
        bid = f"bot_{num:03d}"

        # Determine category
        cat_key = "A"
        for k, v in CATEGORIES.items():
            start, end = v["range"]
            if start <= num <= end:
                cat_key = k
                break

        cat_info = CATEGORIES.get(cat_key, {"name": "عمومی", "archetype": "productivity_tool"})

        catalog[bid] = {
            "id": bid,
            "number": num,
            "title": title.strip(),
            "category": cat_info["name"],
            "archetype": cat_info["archetype"],
            "pain_point": pain.strip(),
            "mvp_scope": mvp.strip(),
            "monetization": mon.strip(),
            "price_irt": 180000 + ((num % 7) * 40000),
            "price_xtr": 100 + ((num % 7) * 25),
        }

    return catalog


MEGA_CATALOG = load_all_150_bots()
