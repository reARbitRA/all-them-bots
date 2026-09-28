#!/usr/bin/env bash
# ==============================================================================
# FABLE-OMEGA: Ultra-Low-Resource Launcher Script
# Configures Linux allocator thresholds, Python bytecode optimization, and starts server
# ==============================================================================

set -e

# Memory Allocator Tuning (Forces glibc malloc to release free memory back to OS kernel)
export MALLOC_TRIM_THRESHOLD_=100000
export MALLOC_MMAP_THRESHOLD_=131072
export PYTHONUNBUFFERED=1
export PYTHONOPTIMIZE=2
export PYTHONDONTWRITEBYTECODE=1

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

echo "======================================================================"
echo "⚡ Starting Fable-Omega Ultra-Low-Resource Multi-Tenant Engine..."
echo "======================================================================"
echo "• Catalog Size: 445+ Autonomous Telegram & Messaging Bots"
echo "• Runtime Mode: Single-Process Multi-Tenant Async Kernel"
echo "• Target Memory: < 45 MB RAM total"
echo "• I/O Strategy: SQLite WAL with In-Memory Batch Buffer"
echo "======================================================================"

exec python3 run.py
