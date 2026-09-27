---
fable_schema: "5.1.0"
urn: "urn:tgn:blueprint:core_architecture:c91326b5-0ac7-4543-83f6-54bcbc855c1b"
title: "Shared Core Architectural Kit & Reusable Bot Services"
transport: "BotAPI"
concurrency:
  paradigm: "AsyncIO"
  max_throughput_est: "500 req/s"
fsm:
  defined: true
  states:
    - "START"
    - "AUTH_VERIFICATION"
    - "INPUT_AWAITING"
    - "RATE_LIMITED"
    - "PROCESSING"
    - "ERROR_RETRY"
    - "COMPLETED"
  storage_driver: "Redis"
dependencies:
  external:
    - "python-telegram-bot>=20.0"
    - "aioredis>=2.0.0"
    - "pydantic>=2.0"
    - "fastapi>=0.100.0"
  internal_urns: []
breaking_changes_detected:
  - "aioredis package merged into redis-py >= 4.2.0 (redis.asyncio)"
verification_checksum: "7211b1928778a8f4af1894cf0e47e6084d9b94a88f6dab187992f0c6330c07df"
---
# Shared Core Kit (you’ll reuse in 90% of these bots)

## A) Core services (modules)
- **Bot Router**: handlers for commands, messages, callbacks.
- **State Machine (FSM)**: multi-step forms (booking, tickets, inspections, returns).
- **Scheduler / Jobs**: reminders, follow-ups, digest messages (cron + DB queue).
- **Admin Tools**: approve/assign, status changes, exports.
- **Payments** (optional):
  - **Physical goods/services**: Telegram Payments; Telegram takes **no commission**, provider fees apply.   
  - **Digital goods/services**: must use **Telegram Stars (`XTR`)**; deliver after `successful_payment`. 
- **Mini App (optional)**: dashboards, complex filtering; validate `initData` signature server-side. 

## B) Minimal tables you’ll reuse
- `users(id, telegram_id, timezone, language, created_at)`
- `plans(user_id, plan, status, start_at, end_at)`
- `jobs(id, run_at, type, payload_json, status)` (for reminders/digests)

## C) Deep-link tracking (campaign/source)
Telegram lets you pass a `start` param to `/start`:
- `t.me/YourBot?start=resto_123`
- `t.me/YourBot?start=ad_campaignX`
You store that as `source` on first interaction.