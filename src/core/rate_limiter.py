"""
Fable-Omega High-Precision In-Memory Sliding Window & Token Bucket Rate Limiter
Prevents Telegram Bot API FloodWait (429) errors without third-party broker dependencies.
"""

from __future__ import annotations

import asyncio
import time


class TokenBucketRateLimiter:
    """Zero-dependency asynchronous rate limiter enforcing 30 req/s global and 1 req/s per-peer."""

    def __init__(
        self,
        global_rate: float = 30.0,
        global_capacity: float = 30.0,
        peer_rate: float = 1.0,
        peer_capacity: float = 3.0
    ) -> None:
        self.global_rate = global_rate
        self.global_capacity = global_capacity
        self.peer_rate = peer_rate
        self.peer_capacity = peer_capacity

        self._global_tokens = global_capacity
        self._global_last_time = time.perf_counter()
        
        self._peer_tokens: dict[int, float] = {}
        self._peer_last_time: dict[int, float] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, peer_id: int | None = None, bypass: bool = False) -> None:
        """Asynchronously block until rate permit is available unless bypassed for tests."""
        if bypass:
            return
        while True:
            async with self._lock:
                now = time.perf_counter()

                # Global bucket replenishment
                elapsed_global = now - self._global_last_time
                self._global_tokens = min(self.global_capacity, self._global_tokens + (elapsed_global * self.global_rate))
                self._global_last_time = now

                # Peer bucket replenishment
                peer_available = True
                peer_wait = 0.0
                if peer_id is not None:
                    last_peer_time = self._peer_last_time.get(peer_id, now)
                    curr_peer_tokens = self._peer_tokens.get(peer_id, self.peer_capacity)
                    
                    elapsed_peer = now - last_peer_time
                    curr_peer_tokens = min(self.peer_capacity, curr_peer_tokens + (elapsed_peer * self.peer_rate))
                    
                    if curr_peer_tokens < 1.0:
                        peer_available = False
                        peer_wait = (1.0 - curr_peer_tokens) / self.peer_rate

                    self._peer_tokens[peer_id] = curr_peer_tokens
                    self._peer_last_time[peer_id] = now

                # Global check
                global_available = self._global_tokens >= 1.0
                global_wait = (1.0 - self._global_tokens) / self.global_rate if not global_available else 0.0

                if global_available and peer_available:
                    self._global_tokens -= 1.0
                    if peer_id is not None:
                        self._peer_tokens[peer_id] -= 1.0
                    return

            wait_delay = max(global_wait, peer_wait, 0.02)
            await asyncio.sleep(wait_delay)


# Global Rate Limiter Singleton
RATE_LIMITER = TokenBucketRateLimiter()
