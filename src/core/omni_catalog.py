"""
Fable-Omega Omni-Catalog: Multi-Source Repository Ingestion Engine
Compiles and indexes 600+ bots across Opus 150 (Code), ChatGPT 150 (Playbooks), Gemini 730 (Market), Rubika 56, and AI Taxonomy.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def find_md_file(filename: str) -> Path:
    """Resolve markdown file from docs/original_blueprints or root."""
    p1 = BASE_DIR / "docs" / "original_blueprints" / filename
    if p1.exists():
        return p1
    p2 = BASE_DIR / "docs" / filename
    if p2.exists():
        return p2
    return BASE_DIR / filename


def extract_opus_150() -> dict[str, dict[str, Any]]:
    """Extract Opus 150 Full-Code bot implementations from FULLOPUSTELBOT.md."""
    md_file = find_md_file("FULLOPUSTELBOT.md")
    if not md_file.exists():
        return {}
    with open(md_file, encoding="utf-8") as f:
        text = f.read()

    # Match Idea #N: Title
    pattern = r'#+\s*(?:Idea\s*#?|#)\s*([0-9]{1,3})\s*[:\)\-–]\s*([^\n]+)'
    matches = re.findall(pattern, text)
    
    bots = {}
    for num_str, title in matches:
        num = int(num_str)
        bid = f"opus_{num:03d}"
        bots[bid] = {
            "id": bid,
            "source": "Opus 150 (Full Python Code)",
            "source_key": "opus",
            "number": num,
            "title": f"Opus #{num}: {title.strip()}",
            "category": "کد کامل و پیاده‌سازی شده (Opus Guide)",
            "tier": "Tier S (Production-Ready Code)",
            "pain_point": "پیاده‌سازی سطح اول با مدل دیتابیس، FSM، هندلرها و پرداخت",
            "mvp_scope": "هسته پایتون + تلگرام BotAPI 7.x + اسکریپت دیتابیس + آزمون",
            "monetization": "اشتراک ماهانه / Telegram Stars / کریپتو",
            "price_irt": 290000 + ((num % 5) * 40000),
            "price_xtr": 180 + ((num % 5) * 25),
            "has_source_code": True
        }
    return bots


def extract_chatgpt_150() -> dict[str, dict[str, Any]]:
    """Extract ChatGPT 150 Playbook bots from 150 TELEGRAM BOT.md."""
    md_file = find_md_file("150 TELEGRAM BOT.md")
    if not md_file.exists():
        return {}
    with open(md_file, encoding="utf-8") as f:
        text = f.read()

    pattern = r'([0-9]{1,3})\)\s*\*\*([^\*]+)\*\*\s*[—–-]\s*([^—–\n]+)\s*[—–-]\s*([^—–\n]+)\s*[—–-]\s*([^\n]+)'
    matches = re.findall(pattern, text)
    
    bots = {}
    for num_str, title, pain, mvp, mon in matches:
        num = int(num_str)
        bid = f"chatgpt_{num:03d}"
        bots[bid] = {
            "id": bid,
            "source": "ChatGPT 150 (Playbooks)",
            "source_key": "chatgpt",
            "number": num,
            "title": f"GPT #{num}: {title.strip()}",
            "category": "پلی‌بوک‌های تجاری و MVP سریع (۲ تا ۸ هفته)",
            "tier": "Tier A (High ROI MVP)",
            "pain_point": pain.strip(),
            "mvp_scope": mvp.strip(),
            "monetization": mon.strip(),
            "price_irt": 180000 + ((num % 7) * 30000),
            "price_xtr": 100 + ((num % 7) * 20),
            "has_source_code": False
        }
    return bots


def extract_gemini_730() -> dict[str, dict[str, Any]]:
    """Extract Gemini 730 Ranked Bot Market Analysis from ANALYZE730.md."""
    md_file = find_md_file("ANALYZE730.md")
    if not md_file.exists():
        return {}
    with open(md_file, encoding="utf-8") as f:
        text = f.read()

    # Extract table rows: | Rank | Bot Idea | Category | Score | Effort | Monetization |
    pattern = r'\|\s*([0-9]{1,3})\s*\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([0-9\.]+)\s*\|\s*([^\|]+)\|\s*([^\|]+)\|'
    matches = re.findall(pattern, text)
    
    bots = {}
    for rank_str, title, cat, score, effort, mon in matches:
        num = int(rank_str)
        bid = f"gemini_{num:03d}"
        score_val = float(score.strip())
        tier = "Tier S (8.5+ Immediate Action)" if score_val >= 8.5 else "Tier A (7.5-8.4 High Potential)" if score_val >= 7.5 else "Tier B (Solid Opportunity)"
        
        bots[bid] = {
            "id": bid,
            "source": "Gemini 730 (Market Landscape)",
            "source_key": "gemini",
            "number": num,
            "title": f"Gemini #{num}: {title.strip()} ({score_val}/10)",
            "category": cat.strip(),
            "tier": tier,
            "pain_point": f"امتیاز بازار: {score_val}/10 • پیچیدگی اجرا: {effort.strip()}",
            "mvp_scope": "Node.js (Grammy) / Python 3.12 + PostgreSQL 15 + Redis",
            "monetization": mon.strip(),
            "price_irt": 350000,
            "price_xtr": 200,
            "has_source_code": False
        }
    return bots


def extract_rubika_56() -> dict[str, dict[str, Any]]:
    """Extract 56 Rubika/Baleh Domestic Micro-SaaS Opportunities from Untitled.md."""
    md_file = find_md_file("Untitled.md")
    if not md_file.exists():
        return {}
    with open(md_file, encoding="utf-8") as f:
        text = f.read()

    pattern = r'\|\s*([0-9]{1,2})\s*\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|'
    matches = re.findall(pattern, text)
    
    bots = {}
    seen = set()
    for row in matches:
        num_str, title, level, platform, persona = row
        num = int(num_str)
        if num in seen or num > 56:
            continue
        seen.add(num)
        
        bid = f"rubika_{num:02d}"
        bots[bid] = {
            "id": bid,
            "source": "Rubika & Baleh 56 (Domestic Micro-SaaS)",
            "source_key": "rubika",
            "number": num,
            "title": f"روبیکا/بله #{num}: {title.strip()}",
            "category": f"بازار داخلی ({level.strip()})",
            "tier": "Tier S (Zero-Dependency Domestic SaaS)",
            "pain_point": f"ویژه: {persona.strip()} روی پلتفرم {platform.strip()}",
            "mvp_scope": "ثبت سفارش بدون API پیچیده + فرم شیت + فیش واریز کارت‌به‌کارت",
            "monetization": "اشتراک ماهانه فروشندگان دایرکتی / درصد فروش",
            "price_irt": 200000 + ((num % 5) * 30000),
            "price_xtr": 120,
            "has_source_code": False
        }
    return bots


def extract_ai_businesses() -> dict[str, dict[str, Any]]:
    """Extract AI businesses from Listaibusinesses.md."""
    md_file = find_md_file("Listaibusinesses.md")
    if not md_file.exists():
        return {}
    with open(md_file, encoding="utf-8") as f:
        lines = f.readlines()

    bots = {}
    current_cat = "خدمات هوش مصنوعی"
    count = 0
    
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if re.match(r'^[A-H]\s+', line):
            current_cat = line
            continue
        if re.match(r'^[A-H][0-9]+\s+', line) or (line.startswith('-') and len(line) > 5):
            count += 1
            bid = f"ai_biz_{count:03d}"
            title = line.lstrip('-0123456789.ABCDEFGH ').strip()
            if not title:
                continue
            bots[bid] = {
                "id": bid,
                "source": "AI Business Taxonomy (Listaibusinesses)",
                "source_key": "ai_biz",
                "number": count,
                "title": f"AI-Biz #{count}: {title}",
                "category": current_cat,
                "tier": "Tier A (High Margin AI Service)",
                "pain_point": "خدمات هوش مصنوعی مستقل با کمترین هزینه زیرساخت",
                "mvp_scope": "OpenAI / Claude API Gateway + رابط تلگرام و وب‌اپ",
                "monetization": "فروش توکن / اشتراک ماهانه پرو",
                "price_irt": 300000,
                "price_xtr": 200,
                "has_source_code": False
            }
    return bots


def load_all_omnibot_collections() -> dict[str, dict[str, Any]]:
    """Merge all 5 collections into one comprehensive 600+ bot registry."""
    omni = {}
    
    # 1. Opus 150
    omni.update(extract_opus_150())
    
    # 2. ChatGPT 150
    omni.update(extract_chatgpt_150())
    
    # 3. Gemini 730
    omni.update(extract_gemini_730())
    
    # 4. Rubika/Baleh 56
    omni.update(extract_rubika_56())
    
    # 5. AI Businesses
    omni.update(extract_ai_businesses())
    
    return omni


OMNI_CATALOG = load_all_omnibot_collections()
