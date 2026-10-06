"""
Fable-Omega Web Control Plane & Simulator
FastAPI web server providing live telemetry, bot management, and real-time interactive chat simulator for 445 catalogue scenarios.
"""

from __future__ import annotations

import asyncio
import hmac
import os
import time

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import CONFIG
from src.core.database import DB
from src.core.dispatcher import DISPATCHER
from src.core.hub_router import HUB_ROUTER, MEGA_HUBS
from src.core.monetization import PaymentManager
from src.core.omni_catalog import (
    OMNI_CATALOG,
    extract_ai_businesses,
    extract_chatgpt_150,
    extract_gemini_730,
    extract_opus_150,
    extract_rubika_56,
)
from src.core.resource_optimizer import (
    GLOBAL_BOT_POOL,
    GLOBAL_RESOURCE_MONITOR,
    GLOBAL_WRITE_BUFFER,
)

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SERVICE_API_KEY: str | None = os.getenv("SERVICE_API_KEY") or None
WEBHOOK_SECRET_TOKEN: str | None = os.getenv("WEBHOOK_SECRET_TOKEN") or None

_bearer_scheme = HTTPBearer(auto_error=False)
_admin_scheme = Depends(_bearer_scheme)  # module-level singleton (ruff B008)


def _compare(a: str, b: str) -> bool:
    """Constant-time string comparison to avoid timing oracles."""
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


async def require_admin_api_key(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = _admin_scheme,
) -> None:
    """Gate mutating / administrative endpoints behind SERVICE_API_KEY.

    Fail-closed: if SERVICE_API_KEY is unset in production, the admin surface
    returns 503 rather than silently opening to the internet.
    Accepts `Authorization: Bearer <key>` or `?api_key=<key>` for curl/webhook use.
    """
    if not SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin endpoints disabled: SERVICE_API_KEY is not configured.",
        )
    provided: str | None = None
    if creds is not None and creds.credentials:
        provided = creds.credentials
    if not provided:
        provided = request.query_params.get("api_key")
    if not provided or not _compare(provided, SERVICE_API_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def verify_webhook_secret(request: Request) -> None:
    """Verify Telegram `X-Telegram-Bot-Api-Secret-Token` header.

    When WEBHOOK_SECRET_TOKEN is set, Telegram must present it on every webhook
    call (this is the official Telegram secret_token mechanism). If unset we
    accept webhooks (useful for local dev) but operators are warned via the
    startup banner.
    """
    if not WEBHOOK_SECRET_TOKEN:
        return
    header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not header or not _compare(header, WEBHOOK_SECRET_TOKEN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


# CORS: closed by default. Configure ALLOWED_ORIGINS="https://a.com,https://b.com" to open.
_allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

app = FastAPI(title="Fable-Omega Bot Fleet Control Plane", version="5.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "HEAD", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.on_event("startup")
async def startup_event():
    """Start background resource optimization workers."""
    await GLOBAL_WRITE_BUFFER.start()
    if not SERVICE_API_KEY:
        # Surface a visible warning; do NOT crash the liveness/readiness probes.
        print("⚠  WARNING: SERVICE_API_KEY is not set — admin endpoints are disabled.")
    if not WEBHOOK_SECRET_TOKEN:
        print(
            "⚠  WARNING: WEBHOOK_SECRET_TOKEN is not set — /webhook accepts unauthenticated calls (dev only)."
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Flush pending write buffers on graceful termination."""
    await GLOBAL_WRITE_BUFFER.stop()


@app.get("/healthz")
async def health_check():
    """Liveness probe validating SQLite & Dispatcher status."""
    row = await DB.fetch_one("SELECT 1 as alive")
    return {
        "status": "HEALTHY",
        "db": bool(row),
        "catalog_count": len(OMNI_CATALOG),
        "timestamp": time.time(),
    }


# ---------------------------------------------------------------------------
# Public read-only endpoints (catalog, hubs, aggregate metrics) — intentionally
# do NOT expose user/order details or mutation hooks.
# ---------------------------------------------------------------------------


@app.get("/api/runtime/stats", dependencies=[Depends(require_admin_api_key)])
async def get_runtime_resource_stats():
    """Real-time process memory, LRU cache efficiency, loop latency, I/O metrics (admin)."""
    await GLOBAL_RESOURCE_MONITOR.measure_event_loop_lag()
    return GLOBAL_RESOURCE_MONITOR.get_system_telemetry(
        pool=GLOBAL_BOT_POOL,
        batch_buffer=GLOBAL_WRITE_BUFFER,
        total_catalog_size=len(OMNI_CATALOG),
    )


@app.post("/api/runtime/tune", dependencies=[Depends(require_admin_api_key)])
async def tune_runtime_parameters(request: Request):
    """Dynamically adjust LRU bot cache capacity and batch intervals at runtime."""
    data = await request.json()
    if "max_pool_capacity" in data:
        new_cap = int(data["max_pool_capacity"])
        GLOBAL_BOT_POOL.max_active = max(5, min(500, new_cap))
    if "flush_interval" in data:
        GLOBAL_WRITE_BUFFER.flush_interval = float(data["flush_interval"])
    return {
        "status": "SUCCESS",
        "current_pool_capacity": GLOBAL_BOT_POOL.max_active,
        "flush_interval": GLOBAL_WRITE_BUFFER.flush_interval,
    }


@app.post("/api/runtime/gc", dependencies=[Depends(require_admin_api_key)])
async def trigger_runtime_gc():
    """Purge LRU bot instances and trigger Python GC to minimize RSS footprint."""
    evicted_bots = GLOBAL_BOT_POOL.clear()
    flushed_writes = await GLOBAL_WRITE_BUFFER.flush()
    mem_after = GLOBAL_RESOURCE_MONITOR.get_memory_info()
    return {
        "status": "SUCCESS",
        "evicted_bots": evicted_bots,
        "flushed_writes": flushed_writes,
        "current_rss_mb": mem_after["rss_mb"],
        "peak_rss_mb": mem_after["peak_mb"],
        "memory_saved_mb": mem_after["memory_saved_mb"],
    }


@app.get("/api/catalog")
async def get_full_catalog():
    """Return all indexed scenario blueprints with source breakdown."""
    opus = extract_opus_150()
    gpt = extract_chatgpt_150()
    gemini = extract_gemini_730()
    rubika = extract_rubika_56()
    ai_biz = extract_ai_businesses()
    return {
        "total_count": len(OMNI_CATALOG),
        "breakdown": {
            "opus_150": len(opus),
            "chatgpt_150": len(gpt),
            "gemini_730": len(gemini),
            "rubika_56": len(rubika),
            "ai_biz": len(ai_biz),
        },
        "bots": OMNI_CATALOG,
    }


@app.get("/api/hubs")
async def get_all_mega_hubs():
    """Return all 15 Vertical Mega-Hub definitions with aggregated bot counts."""
    return {"total_hubs": len(MEGA_HUBS), "hubs": HUB_ROUTER.get_hub_summary()}


@app.get("/api/hubs/{hub_key}/bots")
async def get_bots_in_mega_hub(hub_key: str):
    """Return all bots aggregated under a specific mega hub."""
    bots = HUB_ROUTER.get_hub_bots(hub_key)
    hub_info = MEGA_HUBS.get(hub_key)
    if not hub_info:
        raise HTTPException(status_code=404, detail="Hub not found")
    return {"hub": hub_info, "total_bots": len(bots), "bots": bots}


@app.get("/api/metrics")
async def get_dashboard_metrics():
    """Aggregate FLEET-WIDE KPIs (totals only; no PII/order rows)."""
    users_count = await DB.fetch_one("SELECT COUNT(*) as cnt FROM users")
    orders_approved = await DB.fetch_all(
        "SELECT amount, currency FROM orders WHERE status = 'APPROVED'"
    )
    orders_pending = await DB.fetch_one(
        "SELECT COUNT(*) as cnt FROM orders WHERE status = 'PENDING'"
    )
    active_subs = await DB.fetch_one(
        "SELECT COUNT(*) as cnt FROM users WHERE is_premium = 1 AND premium_until > ?",
        (time.time(),),
    )
    total_revenue_irt = sum(o["amount"] for o in orders_approved if o["currency"] == "IRT")
    total_stars = sum(o["amount"] for o in orders_approved if o["currency"] == "XTR")
    return {
        "total_bots_available": len(OMNI_CATALOG),
        "total_users": users_count["cnt"] if users_count else 0,
        "total_revenue_irt": total_revenue_irt,
        "total_revenue_stars": total_stars,
        "active_subscriptions": active_subs["cnt"] if active_subs else 0,
        "pending_orders": orders_pending["cnt"] if orders_pending else 0,
    }


@app.get("/api/orders", dependencies=[Depends(require_admin_api_key)])
async def get_orders_list():
    """Fetch latest 30 orders (admin-only)."""
    return await DB.fetch_all("SELECT * FROM orders ORDER BY created_at DESC LIMIT 30")


@app.post("/api/orders/{order_id}/approve", dependencies=[Depends(require_admin_api_key)])
async def approve_order_endpoint(order_id: str):
    """Admin 1-click approve order."""
    success, order = await PaymentManager.approve_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": "SUCCESS", "order": order}


@app.post("/api/orders/{order_id}/reject", dependencies=[Depends(require_admin_api_key)])
async def reject_order_endpoint(order_id: str):
    """Admin reject order."""
    success = await PaymentManager.reject_order(order_id)
    return {"status": "SUCCESS" if success else "FAILED"}


@app.post("/api/simulate", dependencies=[Depends(require_admin_api_key)])
async def simulate_bot_message(request: Request):
    """Real-time interactive simulator (admin-only).

    Allows testing any catalogue scenario from the browser without needing a
    live Telegram webhook token.
    """
    body = await request.json()
    bot_id = body.get("bot_id", "opus_001")
    user_id = int(body.get("user_id", 99887766))
    user_name = body.get("user_name", "تست‌کننده")
    text = body.get("text", "")
    callback_data = body.get("callback_data")
    is_photo = body.get("is_photo", False)

    if callback_data:
        update = {
            "update_id": int(time.time()),
            "callback_query": {
                "id": f"cb_{int(time.time())}",
                "from": {"id": user_id, "first_name": user_name, "username": "tester_sim"},
                "data": callback_data,
            },
        }
    elif is_photo:
        update = {
            "update_id": int(time.time()),
            "message": {
                "message_id": int(time.time()),
                "from": {"id": user_id, "first_name": user_name, "username": "tester_sim"},
                "photo": [{"file_id": "sim_receipt_photo_123"}],
            },
        }
    else:
        update = {
            "update_id": int(time.time()),
            "message": {
                "message_id": int(time.time()),
                "from": {"id": user_id, "first_name": user_name, "username": "tester_sim"},
                "text": text,
            },
        }

    return await DISPATCHER.dispatch_update(bot_id, update, bypass_rate_limit=True)


@app.post("/webhook/{bot_id}", dependencies=[Depends(verify_webhook_secret)])
async def telegram_webhook_handler(bot_id: str, request: Request):
    """Production live Telegram Bot API Webhook receiver.

    Telegram secret-token verification is enforced when WEBHOOK_SECRET_TOKEN
    is configured. Rate limiting is applied by MultiTenantDispatcher.
    """
    update = await request.json()
    response = await DISPATCHER.dispatch_update(bot_id, update)
    return JSONResponse(content={"ok": True, "action": response.get("type", "noop")})


@app.get("/", response_class=HTMLResponse)
async def render_dashboard():
    """Render the master web control center and chat simulator."""
    template_path = CONFIG.db_path.parent.parent / "src" / "web" / "templates" / "dashboard.html"
    return await asyncio.to_thread(template_path.read_text, encoding="utf-8")
