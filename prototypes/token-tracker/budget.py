"""
Budget Management
Track spending against budgets and emit alerts at thresholds.
"""

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BudgetAlert:
    """A budget alert event."""
    timestamp: float
    level: str  # "warning", "critical", "exceeded"
    message: str
    spent: float
    limit: float
    percent: float

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "spent": round(self.spent, 4),
            "limit": round(self.limit, 2),
            "percent": round(self.percent, 1),
        }


class BudgetManager:
    """
    Manages spending budgets with multi-level alerts.

    Thresholds:
    - 50%: Info
    - 75%: Warning
    - 90%: Critical
    - 100%: Exceeded (can trigger auto-fallback to free providers)
    """

    def __init__(self):
        self._daily_limit: float = 50.0  # Default $50/day
        self._monthly_limit: float = 500.0  # Default $500/month
        self._alert_thresholds = [
            (0.50, "info", "50% of budget used"),
            (0.75, "warning", "75% of budget used - consider rate limiting"),
            (0.90, "critical", "90% of budget used - switching to low-cost providers"),
            (1.00, "exceeded", "Budget exceeded - routing to free providers only"),
        ]
        self._triggered: set = set()  # Track which thresholds fired
        self._daily_reset: Optional[float] = None

    def set_daily_limit(self, amount: float) -> None:
        """Set daily spending limit."""
        self._daily_limit = amount

    def set_monthly_limit(self, amount: float) -> None:
        """Set monthly spending limit."""
        self._monthly_limit = amount

    def check(self, total_spent: float) -> Optional[BudgetAlert]:
        """
        Check spending against budget. Returns alert if threshold crossed.
        """
        if self._daily_limit <= 0:
            return None

        percent = total_spent / self._daily_limit

        for threshold, level, message in self._alert_thresholds:
            if percent >= threshold and threshold not in self._triggered:
                self._triggered.add(threshold)
                return BudgetAlert(
                    timestamp=time.time(),
                    level=level,
                    message=message,
                    spent=total_spent,
                    limit=self._daily_limit,
                    percent=percent * 100,
                )

        return None

    def is_over_budget(self, total_spent: float) -> bool:
        """Check if spending exceeds the daily limit."""
        return total_spent >= self._daily_limit

    def should_use_free_only(self, total_spent: float) -> bool:
        """Check if we should restrict to free providers (>90% budget)."""
        if self._daily_limit <= 0:
            return False
        return (total_spent / self._daily_limit) >= 0.90

    def reset_daily(self) -> None:
        """Reset daily tracking."""
        self._triggered.clear()
        self._daily_reset = time.time()

    def status(self) -> dict:
        """Current budget status."""
        return {
            "daily_limit": self._daily_limit,
            "monthly_limit": self._monthly_limit,
            "limit": self._daily_limit,  # Alias
            "spent": 0.0,  # Caller fills this
            "percent_used": 0.0,
            "thresholds_triggered": list(self._triggered),
        }
