"""
Fable-Omega High-Performance Async SQLite Database Layer
Implements zero-cost embedded persistence with WAL (Write-Ahead Logging) concurrency.
"""

from __future__ import annotations

import asyncio
import sqlite3
from pathlib import Path
from typing import Any

from src.core.config import CONFIG


class AsyncDatabase:
    """Non-blocking SQLite database driver with WAL mode and schema auto-migration."""

    def __init__(self, db_path: Path = CONFIG.db_path) -> None:
        self.db_path = str(db_path)
        self._lock = asyncio.Lock()
        self._init_db_sync()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA cache_size = -8000;")
        conn.execute("PRAGMA mmap_size = 268435456;")
        conn.execute("PRAGMA temp_store = MEMORY;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db_sync(self) -> None:
        """Run synchronous initial table creation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Users Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                bot_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                balance_credits INTEGER DEFAULT 10,
                is_premium INTEGER DEFAULT 0,
                premium_until INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                last_seen_at REAL NOT NULL,
                PRIMARY KEY (bot_id, user_id)
            );
            """)

            # FSM Sessions Table (Persistent State Storage)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fsm_sessions (
                bot_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                state TEXT NOT NULL DEFAULT 'IDLE',
                context_json TEXT NOT NULL DEFAULT '{}',
                version INTEGER DEFAULT 0,
                updated_at REAL NOT NULL,
                PRIMARY KEY (bot_id, user_id)
            );
            """)

            # Financial Transactions & Orders
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                bot_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL, -- IRT, XTR, TON, USD
                payment_method TEXT NOT NULL, -- STARS, CARD_RECEIPT, CRYPTO_TON, MOCK
                status TEXT NOT NULL, -- PENDING, APPROVED, REJECTED, REFUNDED
                receipt_path TEXT,
                metadata_json TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                resolved_at REAL
            );
            """)

            # Products & Digital Goods Catalog
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                bot_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                price_irt INTEGER NOT NULL,
                price_xtr INTEGER NOT NULL,
                stock INTEGER DEFAULT 100,
                is_digital INTEGER DEFAULT 1,
                digital_payload TEXT,
                is_active INTEGER DEFAULT 1
            );
            """)

            # Reminders & Expiry Tracking (B2B SaaS)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                reminder_id TEXT PRIMARY KEY,
                bot_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                target_date REAL NOT NULL,
                notified_30d INTEGER DEFAULT 0,
                notified_7d INTEGER DEFAULT 0,
                notified_1d INTEGER DEFAULT 0,
                metadata_json TEXT DEFAULT '{}',
                created_at REAL NOT NULL
            );
            """)

            # Coding Katas & Educational Tasks
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS katas (
                kata_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                difficulty TEXT NOT NULL, -- Easy, Medium, Hard
                description TEXT NOT NULL,
                starter_code TEXT NOT NULL,
                test_code TEXT NOT NULL,
                points INTEGER DEFAULT 50
            );
            """)

            # Seed initial products and katas if table empty
            cursor.execute("SELECT COUNT(*) FROM products;")
            if cursor.fetchone()[0] == 0:
                self._seed_initial_data(cursor)

            conn.commit()

    def _seed_initial_data(self, cursor: sqlite3.Cursor) -> None:
        """Seed initial products, katas, and pricing entries."""
        # Commerce products
        cursor.execute("""
        INSERT INTO products (product_id, bot_id, title, description, price_irt, price_xtr, stock, is_digital, digital_payload)
        VALUES 
        ('prod_01', 'commerce', '📚 Comprehensive Telegram Growth Blueprint (PDF + Video)', 'Complete guide to scaling Telegram channels to 100k+ subscribers and monetizing effectively.', 290000, 150, 999, 1, 'https://cdn.omnibot.io/blueprints/growth_blueprint.pdf'),
        ('prod_02', 'commerce', '🤖 Multi-Tenant Bot Creator Source Code Pack', 'Full clean source code with lifetime updates and Docker deployment scripts.', 890000, 450, 100, 1, 'https://cdn.omnibot.io/code/bot_source_v5.zip'),
        ('prod_03', 'commerce', '⚡ Private 1-on-1 Strategy Consulting (1 Hour)', 'Direct architectural and monetization advisory session with senior architects.', 1500000, 800, 15, 0, 'Consulting Session Slot');
        """)

        # Coding Katas
        cursor.execute("""
        INSERT INTO katas (kata_id, title, difficulty, description, starter_code, test_code, points)
        VALUES
        ('kata_01', 'Two Sum Invariant', 'Easy', 'Write a function `two_sum(nums, target)` that returns indices of two numbers that add up to target.', 'def two_sum(nums: list[int], target: int) -> list[int]:\n    # Implement solution\n    return []\n', 'assert two_sum([2, 7, 11, 15], 9) == [0, 1]\nassert two_sum([3, 2, 4], 6) == [1, 2]\n', 25),
        ('kata_02', 'Telegram Leaky Bucket Rate Limiter', 'Medium', 'Implement a class `LeakyBucket(capacity, leak_rate)` with an `allow_request()` method.', 'class LeakyBucket:\n    def __init__(self, capacity: int, leak_rate: float):\n        self.capacity = capacity\n        self.leak_rate = leak_rate\n    def allow_request(self) -> bool:\n        return True\n', 'b = LeakyBucket(5, 1.0)\nassert b.allow_request() == True\n', 50),
        ('kata_03', 'HMAC Constant-Time Verification', 'Hard', 'Implement timing-attack-safe string comparison without using standard hmac.compare_digest.', 'def safe_compare(a: str, b: str) -> bool:\n    # Implement constant-time XOR comparison\n    return False\n', 'assert safe_compare("secret123", "secret123") == True\nassert safe_compare("secret123", "wrong1234") == False\n', 100);
        """)

    async def execute(self, query: str, params: tuple = ()) -> int:
        """Execute write query asynchronously and return affected row count."""
        async with self._lock:
            loop = asyncio.get_running_loop()
            def _run():
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.rowcount
            return await loop.run_in_executor(None, _run)

    async def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        """Execute read query and return single row as dictionary."""
        loop = asyncio.get_running_loop()
        def _run():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        return await loop.run_in_executor(None, _run)

    async def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Execute read query and return all matching rows as list of dictionaries."""
        loop = asyncio.get_running_loop()
        def _run():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        return await loop.run_in_executor(None, _run)


# Global Database Singleton
DB = AsyncDatabase()
