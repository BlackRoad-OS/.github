"""
Circuit Breaker Pattern
Prevents cascading failures by tracking error rates and temporarily
disabling unhealthy providers.

States:
  CLOSED   -> Normal operation, requests flow through
  OPEN     -> Provider failing, requests blocked
  HALF_OPEN -> Testing if provider recovered
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class CircuitState(Enum):
    CLOSED = "closed"       # Healthy - requests flow
    OPEN = "open"           # Failing - requests blocked
    HALF_OPEN = "half_open" # Testing recovery


@dataclass
class CircuitStats:
    """Tracks circuit breaker statistics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    state_changes: int = 0
    total_open_time: float = 0.0
    last_state_change: Optional[float] = None


class CircuitBreaker:
    """
    Circuit breaker for an AI provider.

    CLOSED: All good. Count failures.
    OPEN: Too many failures. Block requests. Wait for recovery timeout.
    HALF_OPEN: Recovery timeout passed. Allow limited test requests.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 3,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 1,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._half_open_calls = 0
        self._opened_at: Optional[float] = None
        self.stats = CircuitStats()

    @property
    def state(self) -> CircuitState:
        """Get current state, auto-transitioning OPEN -> HALF_OPEN if cooldown passed."""
        if self._state == CircuitState.OPEN and self._opened_at:
            elapsed = time.time() - self._opened_at
            if elapsed >= self.recovery_timeout:
                self._transition(CircuitState.HALF_OPEN)
        return self._state

    @property
    def is_available(self) -> bool:
        """Can we send a request through this circuit?"""
        state = self.state
        if state == CircuitState.CLOSED:
            return True
        if state == CircuitState.HALF_OPEN:
            return self._half_open_calls < self.half_open_max_calls
        return False  # OPEN

    def record_success(self, latency: float = 0.0) -> None:
        """Record a successful request."""
        self.stats.total_requests += 1
        self.stats.successful_requests += 1
        self.stats.consecutive_successes += 1
        self.stats.consecutive_failures = 0
        self.stats.last_success_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            # Recovery confirmed - close the circuit
            self._transition(CircuitState.CLOSED)

    def record_failure(self, error: Optional[str] = None) -> None:
        """Record a failed request."""
        now = time.time()
        self.stats.total_requests += 1
        self.stats.failed_requests += 1
        self.stats.consecutive_failures += 1
        self.stats.consecutive_successes = 0
        self.stats.last_failure_time = now

        if self._state == CircuitState.HALF_OPEN:
            # Recovery failed - reopen
            self._transition(CircuitState.OPEN)
        elif self._state == CircuitState.CLOSED:
            if self.stats.consecutive_failures >= self.failure_threshold:
                self._transition(CircuitState.OPEN)

    def reset(self) -> None:
        """Manually reset circuit to closed state."""
        self._transition(CircuitState.CLOSED)
        self.stats.consecutive_failures = 0
        self.stats.consecutive_successes = 0

    def _transition(self, new_state: CircuitState) -> None:
        """Transition to a new state."""
        now = time.time()
        old_state = self._state

        if old_state == CircuitState.OPEN and self._opened_at:
            self.stats.total_open_time += now - self._opened_at

        self._state = new_state
        self.stats.state_changes += 1
        self.stats.last_state_change = now

        if new_state == CircuitState.OPEN:
            self._opened_at = now
            self._half_open_calls = 0
        elif new_state == CircuitState.HALF_OPEN:
            self._half_open_calls = 0
        elif new_state == CircuitState.CLOSED:
            self._opened_at = None
            self._half_open_calls = 0
            self.stats.consecutive_failures = 0

    def to_dict(self) -> dict:
        """Serialize state for monitoring."""
        return {
            "name": self.name,
            "state": self.state.value,
            "consecutive_failures": self.stats.consecutive_failures,
            "total_requests": self.stats.total_requests,
            "success_rate": (
                self.stats.successful_requests / self.stats.total_requests
                if self.stats.total_requests > 0
                else 1.0
            ),
            "total_open_time": round(self.stats.total_open_time, 2),
            "is_available": self.is_available,
        }

    def __repr__(self) -> str:
        return (
            f"CircuitBreaker({self.name}, state={self.state.value}, "
            f"failures={self.stats.consecutive_failures}/{self.failure_threshold})"
        )
