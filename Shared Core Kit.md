---
id: 01KD9AYAPY8P3VJJ2ZHAFGC2XN
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