"""
Rate Limiter - Token bucket rate limiting for the dispatcher.

Prevents service abuse by limiting requests per client/org/global.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class TokenBucket:
    """
    Token bucket for rate limiting.

    Tokens refill at a steady rate. Each request consumes one token.
    When the bucket is empty, requests are rejected.
    """
    capacity: int
    refill_rate: float  # tokens per second
    tokens: float = 0.0
    last_refill: float = 0.0

    def __post_init__(self):
        if self.tokens == 0.0:
            self.tokens = float(self.capacity)
        if self.last_refill == 0.0:
            self.last_refill = time.monotonic()

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self) -> bool:
        """
        Try to consume one token.

        Returns:
            True if the request is allowed, False if rate limited.
        """
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False

    @property
    def remaining(self) -> int:
        """Number of tokens remaining (after refill)."""
        self._refill()
        return int(self.tokens)

    @property
    def retry_after(self) -> float:
        """Seconds until the next token is available."""
        self._refill()
        if self.tokens >= 1.0:
            return 0.0
        deficit = 1.0 - self.tokens
        return deficit / self.refill_rate


class RateLimiter:
    """
    Rate limiter for the dispatcher.

    Supports per-key limiting (e.g., per org code, per client IP)
    and a global limit across all requests.

    Usage:
        limiter = RateLimiter(
            global_rate=100,        # 100 requests/second globally
            per_key_rate=20,        # 20 requests/second per org
            per_key_capacity=50,    # burst up to 50 per org
        )

        # Check before dispatching
        allowed, info = limiter.check("FND")
        if not allowed:
            print(f"Rate limited. Retry after {info['retry_after']:.1f}s")
    """

    def __init__(
        self,
        global_rate: float = 100.0,
        global_capacity: int = 200,
        per_key_rate: float = 20.0,
        per_key_capacity: int = 50,
        enabled: bool = True,
    ):
        """
        Initialize the rate limiter.

        Args:
            global_rate: Max requests/second across all keys
            global_capacity: Max burst size globally
            per_key_rate: Max requests/second per key (org code, client, etc.)
            per_key_capacity: Max burst size per key
            enabled: Whether rate limiting is active
        """
        self.enabled = enabled
        self.per_key_rate = per_key_rate
        self.per_key_capacity = per_key_capacity

        self._global_bucket = TokenBucket(
            capacity=global_capacity,
            refill_rate=global_rate,
        )
        self._key_buckets: Dict[str, TokenBucket] = {}

    def _get_bucket(self, key: str) -> TokenBucket:
        """Get or create a bucket for a key."""
        if key not in self._key_buckets:
            self._key_buckets[key] = TokenBucket(
                capacity=self.per_key_capacity,
                refill_rate=self.per_key_rate,
            )
        return self._key_buckets[key]

    def check(self, key: Optional[str] = None) -> tuple:
        """
        Check if a request is allowed.

        Args:
            key: Rate limit key (e.g., org code). If None, only global limit applies.

        Returns:
            (allowed: bool, info: dict) where info contains:
                - remaining: tokens left
                - retry_after: seconds to wait (0 if allowed)
                - limited_by: "global" or "key" or None
        """
        if not self.enabled:
            return (True, {"remaining": -1, "retry_after": 0.0, "limited_by": None})

        # Check global limit
        if not self._global_bucket.consume():
            return (False, {
                "remaining": 0,
                "retry_after": self._global_bucket.retry_after,
                "limited_by": "global",
            })

        # Check per-key limit
        if key:
            bucket = self._get_bucket(key)
            if not bucket.consume():
                # Refund the global token since we're rejecting
                self._global_bucket.tokens = min(
                    self._global_bucket.capacity,
                    self._global_bucket.tokens + 1.0,
                )
                return (False, {
                    "remaining": 0,
                    "retry_after": bucket.retry_after,
                    "limited_by": "key",
                    "key": key,
                })

        # Determine remaining (use per-key if available, else global)
        if key:
            remaining = self._get_bucket(key).remaining
        else:
            remaining = self._global_bucket.remaining

        return (True, {
            "remaining": remaining,
            "retry_after": 0.0,
            "limited_by": None,
        })

    def status(self) -> Dict:
        """
        Get rate limiter status.

        Returns:
            Dict with global and per-key stats.
        """
        return {
            "enabled": self.enabled,
            "global": {
                "remaining": self._global_bucket.remaining,
                "capacity": self._global_bucket.capacity,
                "rate": self._global_bucket.refill_rate,
            },
            "keys": {
                key: {
                    "remaining": bucket.remaining,
                    "capacity": bucket.capacity,
                    "rate": bucket.refill_rate,
                }
                for key, bucket in self._key_buckets.items()
            },
        }

    def reset(self, key: Optional[str] = None):
        """
        Reset rate limits.

        Args:
            key: Reset a specific key. If None, reset everything.
        """
        if key:
            if key in self._key_buckets:
                del self._key_buckets[key]
        else:
            self._key_buckets.clear()
            self._global_bucket.tokens = float(self._global_bucket.capacity)
            self._global_bucket.last_refill = time.monotonic()
