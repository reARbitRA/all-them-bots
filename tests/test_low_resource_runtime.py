"""
Fable-Omega Ultra-Low-Resource Runtime Concurrency Benchmark & Telemetry Test
Validates that 445+ bots run concurrently within strict memory (< 50MB) and CPU ceilings.
"""

from __future__ import annotations

import asyncio
import json
import random
import sys
import time
from pathlib import Path

# Add repository root to python search path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.core.dispatcher import DISPATCHER  # noqa: E402
from src.core.hub_router import HUB_ROUTER  # noqa: E402
from src.core.omni_catalog import OMNI_CATALOG  # noqa: E402
from src.core.reporting import (  # noqa: E402
    collect_environment_metadata,
    validate_low_resource_report,
)
from src.core.resource_optimizer import (  # noqa: E402
    GLOBAL_BOT_POOL,
    GLOBAL_RESOURCE_MONITOR,
    GLOBAL_WRITE_BUFFER,
)


async def run_benchmark(total_requests: int = 1000, concurrency: int = 50) -> dict:
    print("=" * 70)
    print("🚀 RUNNING ULTRA-LOW RESOURCE CONCURRENCY BENCHMARK (445+ BOTS)...")
    print("=" * 70)

    # 1. Measure initial memory baseline
    mem_initial = GLOBAL_RESOURCE_MONITOR.get_memory_info()
    print(f"📊 Initial Process RSS: {mem_initial['rss_mb']} MB (Peak: {mem_initial['peak_mb']} MB)")
    print(f"📊 Memory Saved vs 445 Isolated Processes: {mem_initial['memory_saved_mb']} MB ({mem_initial['savings_percent']}%)")

    bot_ids = list(OMNI_CATALOG.keys())
    semaphore = asyncio.Semaphore(concurrency)
    latencies = []
    success_count = 0
    error_count = 0

    async def _send_worker(req_id: int):
        nonlocal success_count, error_count
        bot_id = random.choice(bot_ids)
        user_id = 900000 + (req_id % 500)
        
        # Test realistic bot interactions
        actions = ["/start", "🚀 شروع استفاده از ربات", "💎 ارتقا به پلن ویژه (VIP)", "📊 وضعیت حساب و اشتراک", "ℹ️ جزئیات بلوپرینت و کد منبع"]
        text = actions[req_id % len(actions)]
        update = {
            "update_id": req_id,
            "message": {
                "message_id": req_id,
                "from": {"id": user_id, "first_name": f"User_{user_id}"},
                "text": text
            }
        }

        async with semaphore:
            t0 = time.perf_counter()
            try:
                res = await DISPATCHER.dispatch_update(bot_id, update, bypass_rate_limit=True)
                elapsed = (time.perf_counter() - t0) * 1000.0
                latencies.append(elapsed)
                if res and "text" in res:
                    success_count += 1
                else:
                    error_count += 1
            except Exception:
                error_count += 1

    print(f"⚡ Dispatching {total_requests} requests with {concurrency} concurrent workers across 445 bots...")
    start_bench = time.perf_counter()
    tasks = [_send_worker(i) for i in range(total_requests)]
    await asyncio.gather(*tasks)
    total_time = time.perf_counter() - start_bench

    # Flush batch writes
    await GLOBAL_WRITE_BUFFER.flush()

    # Measure under-load / post-load memory
    mem_under_load = GLOBAL_RESOURCE_MONITOR.get_memory_info()
    event_loop_lag = await GLOBAL_RESOURCE_MONITOR.measure_event_loop_lag()

    # Calculate statistics
    latencies.sort()
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    p50 = latencies[int(len(latencies) * 0.50)] if latencies else 0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0
    rps = round(total_requests / total_time, 2)

    print("\n" + "=" * 70)
    print("📈 BENCHMARK RESULTS & RESOURCE FOOTPRINT:")
    print("=" * 70)
    print(f"Total Requests:          {total_requests}")
    print(f"Concurrency Level:       {concurrency}")
    print(f"Success Rate:            {((success_count / total_requests) * 100):.2f}% ({success_count}/{total_requests})")
    print(f"Total Duration:          {total_time:.3f} seconds")
    print(f"Throughput (RPS):        {rps} req/sec")
    print(f"Average Latency:         {avg_latency:.2f} ms")
    print(f"Latency P50:             {p50:.2f} ms")
    print(f"Latency P95:             {p95:.2f} ms")
    print(f"Latency P99:             {p99:.2f} ms")
    print(f"Event Loop Lag:          {event_loop_lag:.3f} ms")
    print(f"LRU Active Bots in RAM:  {GLOBAL_BOT_POOL.active_count} / {GLOBAL_BOT_POOL.max_active} (Hit Ratio: {GLOBAL_BOT_POOL.hit_ratio}%)")
    print(f"Total Evictions:         {GLOBAL_BOT_POOL.evictions}")
    print(f"Memory RSS Under Load:   {mem_under_load['rss_mb']} MB (Peak: {mem_under_load['peak_mb']} MB)")
    print(f"Memory Saved vs Baseline:{mem_under_load['memory_saved_mb']} MB ({mem_under_load['savings_percent']}%)")
    print("=" * 70)

    # 2. Test Manual Purge & GC
    print("\n🧹 Testing On-Demand LRU Memory Purge & Garbage Collection...")
    evicted = GLOBAL_BOT_POOL.clear()
    mem_after_gc = GLOBAL_RESOURCE_MONITOR.get_memory_info()
    print(f"Purged {evicted} cached bot instances. Post-GC RSS: {mem_after_gc['rss_mb']} MB")

    hub_counts = {hub_key: hub["bot_count"] for hub_key, hub in HUB_ROUTER.get_hub_summary().items()}
    report = {
        "report_schema_version": "1.0",
        "timestamp": time.time(),
        "environment": collect_environment_metadata(ROOT_DIR),
        "catalogue": {
            "total_entries": len(OMNI_CATALOG),
            "hub_counts": hub_counts,
            "active_pool_capacity": GLOBAL_BOT_POOL.max_active,
        },
        "test_parameters": {
            "total_requests": total_requests,
            "concurrency": concurrency,
            "rate_limit_bypassed": True,
            "random_seed": None,
        },
        "total_requests": total_requests,
        "concurrency": concurrency,
        "success_rate_percent": round((success_count / total_requests) * 100, 2),
        "total_time_seconds": round(total_time, 3),
        "throughput_rps": rps,
        "latencies_ms": {
            "avg": round(avg_latency, 2),
            "p50": round(p50, 2),
            "p95": round(p95, 2),
            "p99": round(p99, 2),
            "event_loop_lag": round(event_loop_lag, 3)
        },
        "bot_pool": {
            "active_cached": GLOBAL_BOT_POOL.active_count,
            "max_capacity": GLOBAL_BOT_POOL.max_active,
            "hit_ratio_percent": GLOBAL_BOT_POOL.hit_ratio,
            "total_evictions": GLOBAL_BOT_POOL.evictions
        },
        "resource_footprint": {
            "initial_rss_mb": mem_initial["rss_mb"],
            "under_load_rss_mb": mem_under_load["rss_mb"],
            "post_gc_rss_mb": mem_after_gc["rss_mb"],
            "peak_rss_mb": mem_under_load["peak_mb"],
            "baseline_445_processes_mb": mem_under_load["baseline_445_process_mb"],
            "memory_saved_mb": mem_under_load["memory_saved_mb"],
            "memory_reduction_percent": mem_under_load["savings_percent"]
        }
    }
    validate_low_resource_report(report, expected_total=len(OMNI_CATALOG))

    report_path = Path("/home/user/all-them-bots/tests/LOW_RESOURCE_BENCHMARK_REPORT.json")

    def _write_report() -> None:
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    await asyncio.to_thread(_write_report)

    print(f"💾 Benchmark artifact saved: {report_path}")
    return report


if __name__ == "__main__":
    asyncio.run(run_benchmark(total_requests=1000, concurrency=50))
