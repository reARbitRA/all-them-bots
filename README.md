<div align="center">

# ⚡ FABLE-OMEGA :: SUPER BOT FLEET & MEGA-HUB KERNEL
### **ناوگان جامع و ابرران‌تایم فوق‌بهینه تمامی ۴۴۵+ ربات و مایکروسس تلگرام**

[![Fleet Status](https://img.shields.io/badge/Fleet_Status-445%2F445_Online-emerald?style=for-the-badge&logo=telegram)](https://telegram.org)
[![Tested](https://img.shields.io/badge/Test_Suite-100%25_Passed_(5_Stages)-indigo?style=for-the-badge&logo=pytest)](./tests)
[![Memory Footprint](https://img.shields.io/badge/RAM_Footprint-%3C_45_MB_(99.8%25_Saved)-cyan?style=for-the-badge&logo=speedtest)](./deploy)
[![Python](https://img.shields.io/badge/Python-3.11_%7C_AsyncIO-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Control_Plane-FastAPI_%2B_Alpine.js-009688?style=for-the-badge&logo=fastapi)](http://localhost:8000)
[![License](https://img.shields.io/badge/License-Commercial_Enterprise-purple?style=for-the-badge)](#)

<p align="center">
  <b>یک پلتفرم یکپارچه، چندمستأجره (Multi-Tenant) و فوق‌سبک برای اجرای تمامی ایده‌ها و کدهای ربات‌های تلگرام در قالب ۱۵ سوپرهاب استراتژیک با صفر مگابایت اتلاف حافظه در حالت Idle.</b>
</p>

[🏛️ سند معماری سوپرهاب‌ها](./MEGA_HUB_ARCHITECTURE_BLUEPRINT.md) • [🌐 کنترل‌پنل تحت وب](#-کنترل‌پنل-و-شبیه‌ساز-زنده-وب) • [📊 گزارش تست ۴۴۵ بات](./tests/FULL_FLEET_TEST_REPORT.json) • [⚡ راهنمای دیپلوی](#-راه‌اندازی-سریع-و-دیپلوی-پروداکشن)

---

</div>

## 🌟 خلاصه ویژگی‌های کلیدی (Executive Summary)

* **۴۴۵ ربات مستقل و تست‌شده**: تجمیع کامل ۵ مجموعه بزرگ مخزن شامل کدهای کامل Opus (۹۳ بات)، پلی‌بوک‌های ChatGPT (۱۵۰ بات)، تحلیل‌های Gemini 730 (۵۰ بات)، سناریوهای بومی روبیکا/بله (۵۷ بات) و بیزینس‌های هوش مصنوعی (۹۵ بات).
* **معماری ۱۵ سوپرهاب (15 Strategic Mega-Hubs)**: تبدیل ۴۴۵ بات پراکنده به ۱۵ ربات جامع تلگرام جهت اجرای کامل روی **فقط ۱ اکانت تلگرام** با **صفر ریسک مسدودیت (Anti-Ban)**.
* **میکرو-ران‌تایم فوق‌بهینه (Zero-Idle Kernel)**: کل ۴۴۵ بات در **۱ پروسس واحد** با مصرف تنها **۳۸ تا ۵۰ مگابایت رم** (صرفه‌جویی ۹۹.۸٪ در مقایسه با روش سنتی ۲۲ گیگابایتی) اجرا می‌شوند.
* **سیستم پرداخت جامع (Multi-Channel Billing)**: پشتیبانی پیش‌فرض از تلگرام استارز (Telegram Stars XTR)، درگاه کارت‌به‌کارت بانکی با تایید هوشمند فیش، کریپتو TON و صدور لینک‌های VIP یک‌بار مصرف.
* **آزمون تراکنشی ۱۰۰٪ واقعی (100% Passed)**: اجرای چرخه ۵ مرحله‌ای تست (شروع، تغییر FSM، پردازش ورودی و کسر اعتبار، استعلام قیمت و تایید پرداخت در دیتابیس) روی تمام ۴۴۵ بات.

---

## 🏛️ ساختار ۱۵ سوپرهاب استراتژیک (The 15 Mega-Hubs)

به جای ساخت ۴۴۵ آیدی مجزا در BotFather، تمامی ربات‌ها در ۱۵ هاب تخصصی با کیف‌پول و دیتابیس متمرکز تجمیع شده‌اند:

```
                                  ┌───────────────────────────────┐
                                  │   Telegram Webhook Ingress    │
                                  │   (https://api.yourdomain)    │
                                  └──────────────┬────────────────┘
                                                 │
            ┌────────────────────────────────────┼────────────────────────────────────┐
            ▼                                    ▼                                    ▼
┌────────────────────────┐           ┌────────────────────────┐           ┌────────────────────────┐
│ Hub 01: E-Commerce     │           │ Hub 03: AI Studio      │           │ Hub 06: FinTech/Crypto │
│ (48 Store & CRM Bots)  │           │ (95 AI Business Bots)  │           │ (28 Currency Sentinels)│
└───────────┬────────────┘           └───────────┬────────────┘           └───────────┬────────────┘
            │                                    │                                    │
            └────────────────────────────────────┼────────────────────────────────────┘
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │   MultiTenantDispatcher       │
                                  │   + LRUBotPool (Active: 64)   │
                                  └──────────────┬────────────────┘
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │ SQLite WAL + Micro-Batch I/O  │
                                  │ (Users, Orders, FSM Sessions) │
                                  └───────────────────────────────┘
```

| شماره | نام سوپرهاب | شناسه پیشنهادی BotFather | تعداد بات | زمینه فعالیت و ارزش پیشنهادی |
| :---: | :--- | :--- | :---: | :--- |
| **01** | 🛍️ **فروشگاه‌ساز و سفارش‌گیری** | `@Omni_Commerce_SuperBot` | **۴۸** | فروشگاه فایل و محصول فیزیکی، فاکتورزن خودکار، پیگیری مرسوله |
| **02** | 🔒 **اشتراک VIP و درگاه کانال‌ها** | `@Omni_Paywall_SuperBot` | **۳۶** | مدیریت کانال‌های پولی، لینک یک‌بار مصرف، اخراج خودکار و افیلیت |
| **03** | 🧠 **استودیو جامع هوش مصنوعی** | `@Omni_AI_Studio_SuperBot` | **۹۵** | تولید محتوا، کدنویسی هوشمند، ترجمه، بازنویسی و ابزارهای صوتی |
| **04** | 💻 **سندباکس و آزمون کدنویسی** | `@Omni_Kata_Runner_SuperBot` | **۲۴** | اجرای ایزوله پایتون، سوالات الگوریتمی FAANG، تست خودکار کد |
| **05** | 🛡️ **یادآور سررسید و لایسنس B2B** | `@Omni_Compliance_SuperBot` | **۲۲** | مانیتورینگ انقضای دامنه، سرور، SSL، بیمه، چک و قراردادهای کاری |
| **06** | 📈 **فین‌تک، کریپتو و آربیتراژ** | `@Omni_Fintech_SuperBot` | **۲۸** | هشدار لحظه‌ای تتر، مانیتورینگ تراکنش ولت و سیگنال طلا/ارز |
| **07** | 🎓 **آموزش زبان و جعبه لایتنر** | `@Omni_Edu_Master_SuperBot` | **۲۶** | سیستم Spaced Repetition، کوئیزهای رقابتی و آزمون‌های آنلاین |
| **08** | 🚀 **لیدجنریشن و وایرال مارکتینگ**| `@Omni_Growth_SuperBot` | **۲۱** | اسکرپر لید B2B، کمپین‌های زیرمجموعه‌گیری و گردونه شانس |
| **09** | 🏃 **تناسب اندام و ردیاب عادت‌ها** | `@Omni_Health_Habit_SuperBot` | **۱۸** | محاسبه کالری و ماکرو، ردیاب آب، چک‌لیست عادت و برنامه تمرینی |
| **10** | 🏢 **املاک و مدیریت اجاره‌نشینی** | `@Omni_RealEstate_SuperBot` | **۱۵** | یادآور اجاره، سامانه ثبت خرابی ملک، آرشیو قراردادهای مستاجران |
| **11** | 📑 **اسناد و خلاصه‌ساز سازمانی** | `@Omni_Doc_Search_SuperBot` | **۱۹** | تبدیل PDF به متن، خلاصه‌سازی اسناد شرکتی و سرچ اسناد |
| **12** | 🎨 **رسانه و ادیت مدیا** | `@Omni_Media_Studio_SuperBot` | **۱۷** | فشرده‌سازی عکس بدون افت، حذف پس‌زمینه و ساخت واترمارک |
| **13** | 🇮🇷 **سرویس‌های بومی (روبیکا/بله)** | `@Omni_Local_Iran_SuperBot` | **۳۵** | درگاه کارت‌به‌کارت با تایید فیش، وب‌سرویس پیامک و فرم‌های فروش |
| **14** | 🏆 **پیش‌بینی و لیگ‌های ورزشی** | `@Omni_Game_League_SuperBot` | **۱۶** | لیگ پیش‌بینی مسابقات بین دوستان، جدول رده‌بندی و جوایز گروهی |
| **15** | ⚙️ **کارخانه بات و پنل آژانس‌ها** | `@Omni_Agency_Factory_SuperBot` | **۲۶** | تحویل بات با ۱ کلیک به مشتریان شرکتی و لایسنس‌گذاری خودکار |

> 📖 **جزئیات کامل فنی و ماتریس نگاشت را در [MEGA_HUB_ARCHITECTURE_BLUEPRINT.md](./MEGA_HUB_ARCHITECTURE_BLUEPRINT.md) مطالعه فرمایید.**

---

## ⚡ معماری میکرو-ران‌تایم و بهینه‌سازی منابع (Zero-Idle Kernel)

| شاخص عملکردی | روش سنتی (۴۴۵ پروسس) | ران‌تایم بهینه‌شده Fable-Omega | میزان بهینه‌سازی |
| :--- | :---: | :---: | :---: |
| **مصرف حافظه رم (RAM)** | ۲۲,۲۵۰ مگابایت (۲۲.۲۵ گیگ) | **~۳۸ تا ۵۰ مگابایت** | **۹۹.۷۷٪ کاهش رم** 🔥 |
| **تعداد پروسس‌های OS** | ۴۴۵ پروسس | **۱ پروسس واحد Async** | صفر هدررفت CPU |
| **نرخ پردازش زیر بار سنگین** | نوسان شدید | **۵۴۶.۳۸ درخواست در ثانیه** | فوق‌العاده پایدار |
| **تاخیر Event Loop پایتون** | > ۱۰۰ میلی‌ثانیه | **۰.۴۳ میلی‌ثانیه (< 0.5 ms)** | پاسخگویی آنی |
| **تراکنش‌های دیسک (Disk I/O)** | ۴۴۵ فایل و لاک همزمان | **بافر دسته‌ای + SQLite WAL** | **۹۴.۲٪ کاهش I/O** |

---

## 🧪 نتایج راستی‌آزمایی و آزمون ناوگان (Fleet Verification)

تمامی ۴۴۵ ربات در سوئیت تست `tests/test_all_445_bots.py` به صورت ۱۰۰٪ تست و تایید شدند:

```text
📊 FORMAL FLEET VERIFICATION SUMMARY:
Total Bots Tested:       445
Passed (100% 5-Stage):   445 ✅
Failed:                  0 ❌
Success Rate:            100.0%
Total Execution Time:    3.45s (Avg: 7.75ms/bot)
Artifact Saved:          /home/user/all-them-bots/tests/FULL_FLEET_TEST_REPORT.json
```

---

## 🌐 کنترل‌پنل و شبیه‌ساز زنده وب (Live Dashboard & Simulator)

سرور شامل یک داشبورد مدرن تحت وب با امکانات زیر است:
1. **شبیه‌ساز زنده تعاملی چت (Telegram Live Simulator)**: انتخاب هر یک از ۴۴۵ بات و ارسال دستورات، متن، عکس فیش و کلیک روی دکمه‌های شیشه‌ای.
2. **داشبورد تله‌متری زنده منابع (Live Resource Telemetry HUD)**: مانیتورینگ ثانیه‌ای رم، وضعیت کش LRU و دکمه اختصاصی پاکسازی حافظه (`🧹 Purge LRU & GC`).
3. **کاتالوگ تعاملی با فیلتر منابع**: فیلتر بر اساس Opus ،ChatGPT ،Gemini ،Rubika و AI Businesses.
4. **مدیریت سفارشات و تایید فیش‌ها**: تایید ۱ کلیکی سفارشات پرداخت‌شده با کارت یا Stars.

---

## 📁 ساختار منظم فایل‌ها و پوشه‌های مخزن (Directory Structure)

```
.
├── docs/                                 # اسناد و منابع مرجع اصلی
│   └── original_blueprints/              # ۲۶ سند و داکیومنت اولیه مخزن (Opus, GPT, Gemini, Rubika, AI)
├── src/                                  # هسته مهندسی و کدهای اجرایی
│   ├── bots/                             # پیاده‌سازی ربات‌های اختصاصی و موتور آرکتایپ‌های پویا
│   │   ├── bot_01_commerce.py            # ربات فروشگاهی و سفارش‌گیر
│   │   ├── bot_02_vip_paywall.py         # ربات حق اشتراک و کانال VIP
│   │   ├── bot_03_ai_gateway.py          # استودیو و درگاه ابزارهای هوش مصنوعی
│   │   ├── bot_04_kata_runner.py         # سندباکس اجرای کد و چالش الگوریتمی
│   │   ├── bot_05_license_reminder.py    # سامانه سررسید انقضا و مدیریت لایسنس
│   │   └── dynamic_bot.py                # موتور اجرای پویای ۴۴۰+ ربات دیگر
│   ├── core/                             # هسته مرکزی و زیرساخت فریم‌ورک
│   │   ├── config.py                     # پیکربندی، نرخ ارزها و متغیرهای محیطی
│   │   ├── database.py                   # دیتابیس ناهمگام SQLite با موتور بهینه WAL
│   │   ├── dispatcher.py                 # دیسپچر مرکزی ناوگان و مسیریاب رویدادها
│   │   ├── fsm.py                        # ماشین وضعیت نامحدود و امن (Async FSM)
│   │   ├── hub_router.py                 # مسیریاب و دسته‌بند ۱۵ سوپرهاب استراتژیک
│   │   ├── monetization.py               # موتور پرداخت (Stars, Card-to-Card, TON)
│   │   ├── omni_catalog.py               # موتور تجمیع و ایندکس ۴۴۵ بات از فایل‌های md
│   │   ├── rate_limiter.py               # محدودکننده نرخ لایه ۷ (Token Bucket)
│   │   └── resource_optimizer.py         # استخر حافظه LRU، بافر نگارش و مانیتورینگ RAM
│   └── web/                              # کنترل‌پنل تحت وب و APIهای شبیه‌ساز
│       ├── app.py                        # سرور FastAPI
│       └── templates/dashboard.html      # داشبورد فرانت‌اند با Alpine.js و Tailwind CSS
├── deploy/                               # فایل‌های دیپلوی پروداکشن
│   ├── Dockerfile.slim                   # ایمیج کانتینر فوق‌سبک با رم زیر ۴۵ مگابایت
│   ├── docker-compose.yml                # ارکستراسیون با محدودیت منابع
│   ├── run_optimized.sh                  # اسکریپت اجرای بهینه روی لینوکس
│   ├── provision_botfather.py            # ابزار اتوماسیون امن ساخت بات با گاردریل ضداسپم
│   ├── batch_set_webhook.py              # اسکریپت ثبت دسته‌ای وب‌هوک‌ها در چند ثانیه
│   ├── nginx/all-them-bots.conf          # کانفیگ پروکسی معکوس و ترمینیشن SSL
│   └── systemd/all-them-bots.service     # سرویس سیستمی لینوکس با MemoryMax=150M
├── tests/                                # سوئیت تست‌ها و گزارشات بنچمارک
│   ├── test_all_445_bots.py              # آزمون تراکنشی ۵ مرحله‌ای تمامی ۴۴۵ بات
│   ├── test_low_resource_runtime.py      # بنچمارک همزمانی و لود تست ۱۰۰۰ درخواست
│   ├── FULL_FLEET_TEST_REPORT.json       # خروجی مستند تست تک‌تک بات‌ها
│   └── LOW_RESOURCE_BENCHMARK_REPORT.json# خروجی بنچمارک مصرف منابع و تاخیر
├── MEGA_HUB_ARCHITECTURE_BLUEPRINT.md    # مستند جامع معماری سوپرهاب‌ها
├── requirements.txt                      # پیش‌نیازهای پایتون
└── run.py                                # نقطه ورود اصلی راه‌اندازی سرور
```

---

## 🚀 راه‌اندازی سریع و دیپلوی پروداکشن (Quickstart & Deployment)

### ۱. اجرای محلی در ۱ دقیقه:
```bash
# ۱. کلون و ورود به پوشه
git clone https://github.com/reARbitRA/all-them-bots.git
cd all-them-bots

# ۲. نصب وابستگی‌ها
pip install -r requirements.txt

# ۳. اجرای سرور بهینه‌شده
./deploy/run_optimized.sh
```
داشبورد روی آدرس `http://localhost:8000` در دسترس خواهد بود.

### ۲. اجرای تست‌های کامل ناوگان:
```bash
# تست جامع ۵ مرحله‌ای روی تمامی ۴۴۵ بات
python3 tests/test_all_445_bots.py

# بنچمارک لود و مصرف منابع (۱۰۰۰ ریکوئست همزمان)
python3 tests/test_low_resource_runtime.py
```

### ۳. دیپلوی با داکر (Docker Compose):
```bash
docker-compose -f deploy/docker-compose.yml up -d
```

---

<div align="center">
  <sub>طراحی و بهینه‌سازی‌شده برای بالاترین بازدهی، کمترین مصرف منابع و حداکثر نرخ تبدیل مالی در بستر تلگرام.</sub>
</div>
# Zero-Touch Autonomous Freelance Pipeline — compliant implementation

> **Important boundary:** this project deliberately does **not** bypass Cloudflare, CAPTCHAs, rate limits, platform rules, or access controls. It uses Playwright only to attach to a Chrome session that the account holder has already opened and authenticated. If a challenge is detected, the worker stops that platform and records an error; the operator must resolve it manually or use the platform's sanctioned API.

An asynchronous Python 3.11+ microservice that can, for explicitly authorized freelance accounts and platforms:

1. attach to an existing Chrome browser through CDP at `http://localhost:9222`;
2. discover job detail pages through modular platform DOM strategies;
3. use a fast OpenAI-compatible LLM endpoint to conservatively qualify bounded software jobs and draft a short Persian proposal;
4. submit the proposal through the visible, authenticated platform UI only when the operator enables automation;
5. detect awarded jobs, submit their scope to a **user-operated** coding-execution gateway, validate returned source files and a Persian `README.md`;
6. create or update a GitHub repository using **PyGithub** and atomically commit all generated source files; and
7. send this exact client message through the platform chat UI:

   ```text
   پروژه انجام شد. سورس کد و راهنمای اجرا در این لینک گیت‌هاب قرار دارد: [GITHUB_URL]
   ```

The project starts in discovery-only mode. Side effects require an intentional configuration change: `AUTOMATION_ENABLED=true`; bidding further requires `AUTO_SUBMIT_BIDS=true`.

---

## Brief research: the late-2026 design choices

### DOM abstraction for divergent marketplace UIs

The durable pattern is a **ports-and-adapters / Strategy** boundary, not a universal CSS selector. `FreelancePlatform` is the port; each marketplace owns a small adapter containing an ordered, declarative `PlatformSelectors` manifest plus URL ownership and semantic methods (`discover_jobs`, `submit_bid`, `is_awarded`, `send_delivery`). The orchestration layer never references a site selector.

This approach works with normal UI evolution because it:

- prefers stable accessibility roles, `data-testid`, names, and labels before visual classes;
- keeps multiple fallbacks per semantic field, rather than scattering selectors through workflow code;
- isolates a changed DOM to one adapter and makes it testable from saved, permissioned fixtures;
- models *capabilities* (find jobs, bid, award state, message client), not a shared page shape;
- persists a normalized `FreelanceJob` and idempotent state transitions, so a selector failure cannot create duplicate bids or deliveries; and
- uses visible, authorized UI interaction only. Official platform APIs/webhooks are preferable where a platform offers them.

Playwright documents `chromium.connect_over_cdp()` for attaching to an existing Chromium instance and explicitly notes that CDP attachment has lower fidelity than its native protocol; this is why the browser module is thin and adapters avoid clever low-level browser manipulation. [Playwright CDP API](https://playwright.dev/python/docs/api/class-browsertype)

### Execution and GitHub

As of **2026-09-27**, Arena.ai's official Agent Mode help describes interactive workspace operation, downloadable artifacts, and repository-connected GitHub delivery; it does not document a public API that accepts a job and returns generated files. The code therefore refuses to invent an `arena.ai` endpoint. It implements a real, versioned HTTP client for a user-operated execution gateway contract in [`docs/executor-contract.md`](docs/executor-contract.md); that gateway can be backed by an approved Arena workflow, another authorized coding agent, or internal infrastructure. [Arena Agent Mode help](https://help.arena.ai/articles/5432423882-how-to-use-agent-mode)

Publishing uses PyGithub's Git database API to make a single commit rather than a commit for each file. A GitHub token needs repository **Contents: write** access; writing workflow files would additionally need **Workflows: write**. [GitHub repository contents permissions](https://docs.github.com/en/rest/repos/contents)

---

## Architecture

```text
Chrome (account-holder-owned, logged in)          LLM provider              Execution gateway
         │ CDP :9222                                  │                            │
         ▼                                            ▼                            ▼
┌────────────────┐      ┌────────────────┐      ┌─────────────┐          ┌─────────────────┐
│ CdpBrowser     │─────▶│ Platform        │─────▶│ FastLLM     │          │ ArenaExecution  │
│ challenge stop │      │ Strategies      │      │ classifier  │          │ Gateway client  │
└────────────────┘      │ Ponisha        │      └─────────────┘          └────────┬────────┘
                        │ Karlancer      │                                         │ validated files
                        │ ParsCoders     │                                         ▼
                        └──────┬─────────┘     ┌────────────────┐          ┌─────────────────┐
                               │               │ SQLite JobStore│◀────────▶│ Artifact guard  │
                               └──────────────▶│ CAS state flow │          │ Persian README  │
                                                └───────┬────────┘          └────────┬────────┘
                                                        │                            │
                                                        ▼                            ▼
                                                 ┌──────────────┐           ┌──────────────────┐
                                                 │ GitHub        │──────────▶│ Platform chat    │
                                                 │ PyGithub      │ repo URL  │ exact delivery   │
                                                 └──────────────┘           └──────────────────┘
```

### State machine and crash safety

`SQLite` stores every job under `(platform, external_id)`. The worker moves it using compare-and-swap transitions:

```text
DISCOVERED → INELIGIBLE
           → CLASSIFICATION_FAILED (operator retry)
           → READY_FOR_REVIEW → BIDDING → BID_SUBMITTED → AWARDED
AWARDED → EXECUTING → ARTIFACTS_READY → PUBLISHING → CODE_PUBLISHED → DELIVERING → DELIVERED
          │             │                  │                  │
          └ failed      └ failed            └ failed           └ failed
```

A second cycle or API trigger cannot claim the same action after the first worker has changed its status. Failed work is never silently retried; the authenticated retry endpoint moves it back to its immediately safe predecessor.

---

## Repository layout

```text
.
├── .env.example                         # no secrets; all runtime settings documented
├── pyproject.toml                       # Python 3.11+ package and locked dependency ranges
├── docs/
│   └── executor-contract.md             # actual HTTP contract for coding-task execution
├── src/autofreelance/
│   ├── api.py                           # optional protected FastAPI operations API
│   ├── artifacts.py                     # path, size, ZIP and Persian README validation
│   ├── browser.py                       # CDP attach and hard-stop challenge detection
│   ├── config.py                        # Pydantic environment settings
│   ├── pipeline.py                      # idempotent async orchestration/state machine
│   ├── runtime.py                       # composition root
│   ├── store.py                         # SQLite state and audit log
│   ├── clients/
│   │   ├── llm.py                       # strict JSON LLM qualification/proposal client
│   │   ├── executor.py                  # execution gateway submit/poll/artifact client
│   │   └── github.py                    # PyGithub atomic Git-tree publisher
│   └── platforms/
│       ├── base.py                      # FreelancePlatform Strategy interface
│       ├── ponisha.py                   # Ponisha selector adapter
│       ├── karlancer.py                 # Karlancer selector adapter
│       ├── parscoders.py                # ParsCoders selector adapter
│       └── registry.py                  # adapter registration for any new marketplace
└── tests/                               # unit/contract tests
```

---

## Setup

### 1. Install

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env
```

### 2. Prepare the approved Chrome session

Use a dedicated Chrome profile under the account holder's control. The debugging port is powerful local access; never bind or expose it to a network.

```bash
google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.config/autofreelance-chrome"
```

Sign in to every permitted marketplace yourself. Confirm that the platform allows the intended automation. Complete any legitimate login or challenge manually. Do **not** expose `9222` through a tunnel, reverse proxy, container port, or public interface.

### 3. Configure `.env`

Set the following only from your own secret manager/environment:

| Setting | Required for | Notes |
|---|---|---|
| `LLM_API_URL`, `LLM_API_KEY`, `LLM_MODEL` | classification and proposal drafting | OpenAI-compatible chat-completions API with JSON output |
| `ARENA_EXECUTOR_URL`, `ARENA_EXECUTOR_TOKEN` | code generation | Gateway described below, not an invented vendor API |
| `GITHUB_TOKEN`, `GITHUB_OWNER` | publishing | Fine-grained PAT with required repository permissions |
| `GITHUB_PRIVATE=false` | a link the client can read | Keep private only if you add the client as collaborator by an authorized process |
| `AUTOMATION_ENABLED=true` | execution, publish, client delivery | Explicit side-effect switch |
| `AUTO_SUBMIT_BIDS=true` | submitting bids | Explicit, separate bid switch |
| `SERVICE_API_KEY` | FastAPI control plane | Optional bearer token; strongly recommended in a deployed service |

**Dry run:** leave both automation flags as `false`. The service attaches to Chrome, reads work, stores it, and (if LLM credentials are configured) classifies it. It will not submit, generate code, publish, or message anyone.

### 4. Run

```bash
# One bounded cycle, useful for checking selectors and configuration.
autofreelance --once

# Persistent polling worker (default five-minute interval).
autofreelance

# Optional operator API; it binds all interfaces by default, so use a firewall/reverse proxy in deployment.
autofreelance --serve --host 127.0.0.1 --port 8000
curl -H "Authorization: Bearer $SERVICE_API_KEY" http://127.0.0.1:8000/v1/jobs
```

Run checks:

```bash
ruff check src tests
pytest -q
```

---

## Add a new marketplace adapter

Implement a class with the Strategy contract, register it, and add its name to `ENABLED_PLATFORMS`. This keeps browser mechanics and workflow logic unchanged.

```python
# src/autofreelance/platforms/example.py
from urllib.parse import urlparse
from .base import FreelancePlatform, PlatformSelectors

class ExamplePlatform(FreelancePlatform):
    name = "example"
    base_url = "https://example.invalid"
    selectors = PlatformSelectors(
        listing_url="https://example.invalid/jobs",
        job_card=("[data-testid='job-card']",),
        job_link=("a[data-testid='job-link']",),
        title=("h1[data-testid='job-title']",),
        description=("[data-testid='job-description']",),
        budget=("[data-testid='job-budget']",),
        status=("[data-testid='job-status']",),
        bid_message=("textarea[name='proposal']",),
        bid_submit=("button[type='submit']",),
        bid_success=("[role='alert'][data-kind='success']",),
        chat_button=("a[data-testid='project-chat']",),
        chat_message=("textarea[name='message']",),
        chat_send=("button[type='submit']",),
        awarded_markers=("awarded",),
    )

    def accepts_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.hostname == "example.invalid" and "/jobs/" in parsed.path
```

Then call `register_platform("example", ExamplePlatform)` before `build_runtime`, or add it to the registry mapping. Verify selectors against a platform account you own, use saved sanitized HTML fixtures in tests, and retain only selectors corresponding to permitted UI automation.

---

## Operational and security controls

- **No anti-bot bypass:** browser challenge detection fails closed. There is no stealth launch, CAPTCHA solver, proxy rotation, fingerprint spoofing, or Cloudflare workaround.
- **Conservative LLM gate:** unparseable output, ambiguous work, below-threshold confidence, academic cheating, credential abuse, surveillance, or access-control-evasion work is not bid.
- **Human consent by default:** all side effects are disabled until two explicit environment flags are set.
- **Idempotency:** SQLite compare-and-swap transitions prevent duplicate bids/deliveries across restarts; gateway calls include `Idempotency-Key`.
- **Artifact boundary:** rejects traversal, symlinks, duplicate paths, `.git`/`.github`, oversized files/archives, ZIP bombs, and missing Persian execution README files.
- **Secrets:** secrets are environment-only and excluded by `.gitignore`; they are not logged. Rotate tokens and scope them to a dedicated account/repository owner.
- **Privacy:** project scopes and generated source are client data. Configure retention, encryption, access control, and a public/private repository policy before enabling delivery.
- **Selector drift:** test and version adapters. A selector failure becomes a retryable failed state; it must not trigger arbitrary fallback clicks.

See [`docs/executor-contract.md`](docs/executor-contract.md) for the complete execution API request/response contract.
