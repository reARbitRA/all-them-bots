---
id: 01KD9BHRXPYKTBEESK6RP42V0Z
---
درست می‌گویید؛ هنوز «حجم کلمات به‌ازای هر ایده» با نمونه‌ای که از کلاد-اوپوس دیدید برابری نکرده است.  
برای اثباتِ سقف واقعی خروجی، یک ایده را این‌بار با تقریباً ۷۰۰ – ۸۰۰ واژه (≈ ۴٫۵k کاراکتر) باز می‌کنم؛ یعنی چیزی نزدیک به همان دانسیته‌ای که از رقیب دیده‌اید. اگر این نمونه را هم‌سطح یا بهتر ارزیابی کردید، عدد و بازه را اعلام کنید تا بقیّهٔ ۱۵۰ ایده را دقیقاً به همین ضخامت تحویل بدهم.

══════════════════════════════════════════════════════════════════════
Idea #26 “Build-a-Compiler” Micro-Course Bot (ultra-detailed blueprint)
══════════════════════════════════════════════════════════════════════
📋 Concept Overview  
یک بوت تلگرام که طی ۶۰ جلسهٔ میکرو (روزانه یا سه‌روزه) به کاربر یاد می‌دهد از صفر یک کامپایلر ساده (فرانت‌اِندِ لکس/پارس و بک‌اِندِ کُد ژنریشن برای ماشین مجازی) بنویسد. هر درس شامل PDF مفهومی، کد اسنیپت، تکلیف، ویدیوی ۵ دقیقه‌ای توضیح و تست اتوماتیک تکلیف است.

🎯 Target Personas  
• دانشجوی CS که درس «طراحی کامپایلر» دارد ولی استاد فقط اسلاید می‌دهد.  
• مهندسان بک‌اندی که می‌خواهند DSL یا لنگویج تو‌لینگ بسازند.  
• مدرسان بوت‌کمپ که به کورس ازپیش‌ساخته نیاز دارند تا زیر برند خود بفروشند.

😫 Problem It Solves  
1. منابع رایگان پراکنده است؛ نظم در تسک‌بندی ندارند.  
2. کورس‌های Udemy / Coursera طولانی (۲۰ + ساعت)، زبان انگلیسی، و نیازمند VPN هستند.  
3. دانشجوها معمولاً در فاز «کد ژنریشن» رها می‌شوند؛ نمونهٔ پروژهٔ انتهابه‌انتها کم است.  
4. زمان استاد برای تصحیح تکلیف محدود است. بوت با sandbox تست را لحظه‌ای انجام می‌دهد.

⭐ Feature Roadmap & MVP

Phase 1 — Week 1-2 (MVP)  
• /start → انتخاب «زبان پیاده‌سازی» (Go یا Python).  
• Lesson 0 ارسال می‌شود: «مقدمه + نصب ابزار» (PDF و ویدیو).  
• /next → درس بعدی (هر درس <= 2 MB ضمیمه).  
• /homework → توضیح تکلیف + لینک Git repo قالب.  
• /upload zip → تست اتوماتیک در Docker؛ نمره و لاگ برمی‌گردد.  
• پیش‌نمایش سرفصلِ ۱۰ درس آینده برای حفظ انگیزه.

Phase 2 — Week 3-4  
• Scheduler روزانه درس را «پوش» ‌می‌کند (opt-out ممکن).  
• SM-2 spaced-repetition روی کارت‌های «اصطلاحات کامپایلر» (lexer, AST, IR …).  
• Leaderboard «کمترین خطا در تست‌ها».  
• گواهی PDF پس از 80 ٪ نمره نهایی (امضا + QR).

Phase 3 — Week 5-6  
• White-label API: مدرس بوت‌کمپ بتواند همان محتوا را با لوگوی خود منتشر کند.  
• IntelliJ Plugin (اختیاری)‌: حل تمرین داخل IDE و ارسال با Webhook.  
• پرداخت اشتراک تیمی (۵-کاربره + پنل progress CSV).

🏗 Technical Architecture (ASCII Diagram)

```
┌────────────── USER (Telegram) ──────────────┐
│  /start   /next   /upload ZIP   /stats      │
└───────────────────┬─────────────────────────┘
                    │ HTTPS long-polling
                    ▼
┌───────────── TELEGRAM BOT API ──────────────┐
└───────────────────┬─────────────────────────┘
                    │ aiohttp (aiogram v3)
                    ▼
┌───────────────────────── BOT APP (FastAPI) ─────────────────────────┐
│  Routers: lesson, homework, payment, webhook                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ LessonSvc    │  │  TestRunner  │  │  PaymentSvc  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │ Async task      │ gRPC docker-pool │ Stripe & ZarinPal   │
│         ▼                 ▼                 ▼                      │
│  S3 (Bunny)          Docker-Swarm (3×)      Supabase (PostgreSQL)  │
│  pdf/vid assets      kata-runner images     users • lessons • txs  │
└─────────────────────────────────────────────────────────────────────┘
```

🔑 Security Notes  
• ZIP محدود به 1 MB؛ در docker-in-docker اجرا با `--network=none`.  
• Anti-plagiarism توکن AST hash روی کد دانشجو؛ شناسایی copy-paste 1-Edit-Distance.

👨‍💻 Week-by-Week Dev Tasks (+ Key Code)

Week 1 — Bot Skeleton & Asset CDN  
```bash
# upload PDFs to Bunny
bunny push lessons/ pdf/
bunny push videos/ mp4/
```
```python
# models.py
class User(Base):
    id          = Column(Integer, primary_key=True)
    tg_id       = Column(BigInteger, unique=True)
    lang        = Column(String(2), default='fa')
    plan        = Column(Enum('free','premium','white'), default='free')
class Progress(Base):
    user_id     = Column(FK(User.id))
    lesson_id   = Column(Integer)
    grade       = Column(Float)      # last test %
    completed   = Column(Boolean)
```

Week 2 — Docker Test-Runner  
Dockerfile (python 3.12-slim) installs `pytest`, `lark-parser`.  
FastAPI endpoint  
```python
@app.post("/run_kata")
async def run_kata(zip: UploadFile):
    path = save_tmp(zip)
    result = await async_run(["docker","run","-v",f"{path}:/code","kata:latest"])
    return JSONResponse(result)
```

Week 3 — Scheduler & SM-2 Cards  
`apscheduler.add_job(send_lesson, trigger='cron', hour=7, tz=user.tz)`  
SM-2 algorithm identical به مثال قبلی ولی روی جدول Vocabulary.

Week 4 — Payments & Certificate  
Stripe Checkout session; موفق → `plan='premium'`.  
WeasyPrint اچ‌تی‌ام‌ال تمپلیت Certificate با QR (`/verify/<uuid>`).

Week 5-6 — White-label API  
endpoint `POST /v1/white/lessons` با JWT مدرس؛ auto-brand pdf.  
Team invoice via Stripe → تعداد صندلی * 4.99 $.

💰 Monetization Timeline & Financial Model

| Month | Total Users | Paid (Premium) | ARPU $ | MRR $ | CAC* |
|-------|-------------|----------------|--------|-------|------|
| 3     | 2 000       | 80 (4 %)       | 6.5    | 520   | 0.8$ |
| 6     | 6 000       | 420 (7 %)      | 6.2    | 2 600 | 0.9$ |
| 12    | 15 000      | 1 500 (10 %)   | 6.0    | 9 000 | 1.1$ |

*CAC ≈ تبلیغ کلیکی تلگرام ۵۰۰ تومان/کاربر ورودی × 30 % ثبت‌نام.

Revenue Streams (Year-1 Projection)  
• Premium Individuals (6 $/qtr) …… 55 %  
• White-label Seats (4.99 $/mo/user) … 35 %  
• Affiliate IDE plug-ins …………………… 7 %  
• Certificate Verification Fees ……… 3 %

Cost Stack (steady-state 15 k users)  
• Bunny CDN (200 GB/mo) …………… 9 $  
• Hetzner CPX21 (runner swarm) …… 14 $  
• Supabase Pro tier …………………… 29 $  
• OpenAI tokens (60 k TPM) ………… 25 $  
Total OPEX ≈ 77 $/mo → Gross Margin ≈ 99 %

📈 KPIs to Track  
1. Day-7 Lesson Completion Rate → health of cohorts.  
2. Median Test Run Latency (< 7 s).  
3. ARPU vs Token-Spend Ratio (> 80).  
4. Instructor White-label Churn (< 5 %/quarter).

🎯 Go-to-Market Plan (90 days)  
• Launch on r/programming_IR, StackOverflow Telegram, و گروه‌های “CompilerDev”.  
• محتوای رایگان «Lexer در ۱۰ دقیقه» در Aparat + لینک بوت.  
• Early-bird 50 ٪ تخفیف تا درس 10 → FOMO.  
• بعد از ماه ۲: مسابقهٔ “Metalang Hackathon” با جایزه لپ‌تاپ (اسپانسر).  

══════════════════════════════════════════════════════════════════════
این ایده حدود ۷۶۰ واژه دارد (می‌توانید کلمات را بشمارید). اگر از نظر «دانسیته و عمق» هم‌تراز یا جلوتر از خروجی کلاد تلقی شد، عدد بازهٔ بعدی را اعلام کنید (مثلاً 27-36) تا همین الگو را ادامه دهم؛ اگر هنوز کم‌جزئیات است، دقیقاً بگویید کجا را پرتر کنم (فاز مالی، کد، مارکتینگ، یا معماری).