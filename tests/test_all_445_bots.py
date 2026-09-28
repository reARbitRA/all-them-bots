"""
Fable-Omega Comprehensive Fleet Verification & Stress Test Suite
Executes real end-to-end transactional lifecycle tests across all 445+ bot blueprints.
"""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add project root to sys.path for direct script execution.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.core.database import DB  # noqa: E402
from src.core.dispatcher import DISPATCHER  # noqa: E402
from src.core.omni_catalog import (  # noqa: E402
    OMNI_CATALOG,
    extract_ai_businesses,
    extract_chatgpt_150,
    extract_gemini_730,
    extract_opus_150,
    extract_rubika_56,
)
from src.core.reporting import (  # noqa: E402
    collect_environment_metadata,
    validate_full_fleet_report,
)


async def run_exhaustive_test_on_bot(bot_id: str, spec: dict, test_user_id: int) -> dict:
    """Execute complete 5-stage transactional workflow on a specific bot."""
    start_time = time.perf_counter()
    result = {
        "bot_id": bot_id,
        "title": spec.get("title", ""),
        "source": spec.get("source", ""),
        "passed_stages": 0,
        "total_stages": 5,
        "status": "FAILED",
        "latency_ms": 0.0,
        "errors": []
    }

    try:
        # Stage 1: /start Handshake
        res1 = await DISPATCHER.dispatch_update(bot_id, {
            "message": {
                "from": {"id": test_user_id, "first_name": "QA_Tester", "username": "qa_tester"},
                "text": "/start"
            }
        }, bypass_rate_limit=True)
        if not res1 or "text" not in res1 or "reply_markup" not in res1:
            result["errors"].append("Stage 1 (/start) failed: Invalid response structure.")
        else:
            result["passed_stages"] += 1

        # Stage 2: Service Action Request (FSM transition to AWAITING_INPUT)
        res2 = await DISPATCHER.dispatch_update(bot_id, {
            "message": {
                "from": {"id": test_user_id, "first_name": "QA_Tester"},
                "text": "🚀 شروع استفاده از ربات"
            }
        }, bypass_rate_limit=True)
        if not res2 or "text" not in res2:
            result["errors"].append("Stage 2 (Service Action Request) failed.")
        else:
            result["passed_stages"] += 1

        # Stage 3: Input Processing & Credit Deduction
        res3 = await DISPATCHER.dispatch_update(bot_id, {
            "message": {
                "from": {"id": test_user_id, "first_name": "QA_Tester"},
                "text": "درخواست تست واقعی اتوماسیون و پردازش دیتابیس"
            }
        }, bypass_rate_limit=True)
        if not res3 or "text" not in res3:
            result["errors"].append("Stage 3 (Input Processing) failed.")
        else:
            result["passed_stages"] += 1

        # Stage 4: Upgrade / VIP Pricing Request
        res4 = await DISPATCHER.dispatch_update(bot_id, {
            "message": {
                "from": {"id": test_user_id, "first_name": "QA_Tester"},
                "text": "💎 ارتقا به پلن ویژه (VIP)"
            }
        }, bypass_rate_limit=True)
        if not res4 or "reply_markup" not in res4:
            result["errors"].append("Stage 4 (Pricing Inquiry) failed.")
        else:
            result["passed_stages"] += 1

        # Stage 5: Payment Fulfillment & Database Check
        res5 = await DISPATCHER.dispatch_update(bot_id, {
            "callback_query": {
                "from": {"id": test_user_id, "first_name": "QA_Tester"},
                "data": "pay_stars"
            }
        }, bypass_rate_limit=True)
        if not res5 or "text" not in res5:
            result["errors"].append("Stage 5 (Payment Fulfillment) failed.")
        else:
            result["passed_stages"] += 1

        # Verify DB Records
        user_row = await DB.fetch_one("SELECT * FROM users WHERE bot_id = ? AND user_id = ?", (bot_id, test_user_id))
        order_row = await DB.fetch_one("SELECT * FROM orders WHERE bot_id = ? AND user_id = ? AND status = 'APPROVED'", (bot_id, test_user_id))
        
        if not user_row or not order_row:
            result["errors"].append("Database verification failed: User or Order record missing.")
        
        elapsed = (time.perf_counter() - start_time) * 1000
        result["latency_ms"] = round(elapsed, 2)
        
        if result["passed_stages"] == result["total_stages"] and not result["errors"]:
            result["status"] = "PASSED"

    except Exception as e:
        result["errors"].append(f"Unhandled exception during execution: {e!s}")

    return result


async def main():
    print("=" * 70)
    print("⚡ STARTING EXHAUSTIVE REAL VERIFICATION OF ALL 445+ BOTS...")
    print("=" * 70)

    total_bots = len(OMNI_CATALOG)
    passed_count = 0
    failed_count = 0
    reports = []
    start_all = time.perf_counter()

    base_user_id = 800000

    for idx, (bot_id, spec) in enumerate(OMNI_CATALOG.items(), 1):
        test_uid = base_user_id + idx
        res = await run_exhaustive_test_on_bot(bot_id, spec, test_uid)
        reports.append(res)

        if res["status"] == "PASSED":
            passed_count += 1
            status_symbol = "✅"
        else:
            failed_count += 1
            status_symbol = "❌"

        if idx % 25 == 0 or idx == total_bots:
            print(f"[{idx:03d}/{total_bots:03d}] {status_symbol} {bot_id} | {res['title'][:35]} | {res['latency_ms']}ms | Stages: {res['passed_stages']}/5")

    total_time = time.perf_counter() - start_all
    avg_latency = round((total_time / total_bots) * 1000, 2)

    source_counts = {
        "opus": len(extract_opus_150()),
        "chatgpt": len(extract_chatgpt_150()),
        "gemini": len(extract_gemini_730()),
        "rubika": len(extract_rubika_56()),
        "ai_biz": len(extract_ai_businesses()),
    }
    summary = {
        "report_schema_version": "1.0",
        "timestamp": time.time(),
        "environment": collect_environment_metadata(ROOT_DIR),
        "catalogue": {
            "total_entries": total_bots,
            "source_counts": source_counts,
            "lifecycle_stages": ["start", "state", "input", "credit", "order_or_payment"],
        },
        "total_bots_tested": total_bots,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "success_rate_percent": round((passed_count / total_bots) * 100, 2),
        "total_duration_seconds": round(total_time, 2),
        "avg_bot_lifecycle_latency_ms": avg_latency,
        "test_results": reports
    }
    validate_full_fleet_report(summary, expected_total=total_bots)

    out_file = Path("tests/FULL_FLEET_TEST_REPORT.json")
    out_file.parent.mkdir(exist_ok=True, parents=True)

    def _write_report() -> None:
        out_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    await asyncio.to_thread(_write_report)

    print("=" * 70)
    print("📊 FORMAL FLEET VERIFICATION SUMMARY:")
    print("=" * 70)
    print(f"Total Bots Tested:       {total_bots}")
    print(f"Passed (100% 5-Stage):   {passed_count} ✅")
    print(f"Failed:                  {failed_count} ❌")
    print(f"Success Rate:            {summary['success_rate_percent']}%")
    print(f"Total Execution Time:    {summary['total_duration_seconds']}s (Avg: {avg_latency}ms/bot)")
    print(f"Artifact Saved:          {out_file}")
    print("=" * 70)

    if failed_count > 0:
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
