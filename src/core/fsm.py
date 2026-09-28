"""
Fable-Omega Asynchronous Finite State Machine (FSM) Engine
Provides transactional state transitions, context isolation, and zero state-explosion guarantees.
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from src.core.database import DB


class AsyncFSM:
    """Persistent Finite State Machine manager for multi-bot sessions."""

    def __init__(self, bot_id: str) -> None:
        self.bot_id = bot_id
        self._memory_cache: dict[int, tuple[str, dict[str, Any], int]] = {}
        self._user_locks: dict[int, asyncio.Lock] = {}

    def _get_user_lock(self, user_id: int) -> asyncio.Lock:
        if user_id not in self._user_locks:
            self._user_locks[user_id] = asyncio.Lock()
        return self._user_locks[user_id]

    async def get_state(self, user_id: int) -> tuple[str, dict[str, Any], int]:
        """Fetch current state, context data, and version for a user."""
        if user_id in self._memory_cache:
            return self._memory_cache[user_id]

        row = await DB.fetch_one(
            "SELECT state, context_json, version FROM fsm_sessions WHERE bot_id = ? AND user_id = ?",
            (self.bot_id, user_id)
        )

        if row:
            try:
                context = json.loads(row["context_json"])
            except Exception:
                context = {}
            res = (row["state"], context, row["version"])
        else:
            res = ("IDLE", {}, 0)
            await DB.execute(
                "INSERT OR IGNORE INTO fsm_sessions (bot_id, user_id, state, context_json, version, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (self.bot_id, user_id, "IDLE", "{}", 0, time.time())
            )

        self._memory_cache[user_id] = res
        return res

    async def set_state(
        self,
        user_id: int,
        state: str,
        context_patch: dict[str, Any] | None = None,
        clear_context: bool = False
    ) -> bool:
        """
        Transition user to target state under an atomic per-user lock.
        Merges context updates or resets context if clear_context is True.
        """
        async with self._get_user_lock(user_id):
            _curr_state, curr_context, curr_ver = await self.get_state(user_id)
            
            if clear_context:
                new_context = context_patch or {}
            else:
                new_context = {**curr_context, **(context_patch or {})}

            new_ver = curr_ver + 1
            now = time.time()
            context_str = json.dumps(new_context)

            await DB.execute("""
            INSERT INTO fsm_sessions (bot_id, user_id, state, context_json, version, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(bot_id, user_id) DO UPDATE SET
                state = excluded.state,
                context_json = excluded.context_json,
                version = excluded.version,
                updated_at = excluded.updated_at;
            """, (self.bot_id, user_id, state, context_str, new_ver, now))

            self._memory_cache[user_id] = (state, new_context, new_ver)
            return True

    async def reset(self, user_id: int) -> bool:
        """Reset state machine to IDLE with empty context."""
        return await self.set_state(user_id, "IDLE", {}, clear_context=True)
