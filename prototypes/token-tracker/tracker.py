"""
Token Usage Tracker
Tracks token consumption and costs per route, per provider, with
time-series aggregation and budget alerting.
"""

import time
import json
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional

from budget import BudgetManager, BudgetAlert


@dataclass
class UsageRecord:
    """A single usage record."""
    timestamp: float
    route: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency: float = 0.0
    metadata: dict = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class AggregateStats:
    """Aggregated usage statistics."""
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    total_latency: float = 0.0
    first_seen: Optional[float] = None
    last_seen: Optional[float] = None

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def avg_tokens_per_request(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_tokens / self.total_requests

    @property
    def avg_cost_per_request(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_cost / self.total_requests

    @property
    def avg_latency(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_latency / self.total_requests

    def record(self, rec: UsageRecord) -> None:
        self.total_requests += 1
        self.total_input_tokens += rec.input_tokens
        self.total_output_tokens += rec.output_tokens
        self.total_cost += rec.cost
        self.total_latency += rec.latency
        now = rec.timestamp
        if self.first_seen is None:
            self.first_seen = now
        self.last_seen = now

    def to_dict(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 6),
            "avg_tokens_per_request": round(self.avg_tokens_per_request, 1),
            "avg_cost_per_request": round(self.avg_cost_per_request, 6),
            "avg_latency": round(self.avg_latency, 3),
        }


# ── Default cost table ─────────────────────────────────────────────

COST_TABLE = {
    # provider_type: (cost_per_1k_input, cost_per_1k_output)
    "claude": (0.003, 0.015),
    "openai": (0.005, 0.015),
    "llama": (0.0, 0.0),  # Local = free
}


class TokenTracker:
    """
    Tracks all token usage across the BlackRoad routing engine.

    Features:
    - Per-route usage tracking
    - Per-provider usage tracking
    - Time-windowed aggregation (hourly, daily)
    - Budget management with alerts
    - Cost calculation
    """

    def __init__(self, budget_manager: Optional[BudgetManager] = None):
        self._records: list[UsageRecord] = []
        self._by_route: dict[str, AggregateStats] = defaultdict(AggregateStats)
        self._by_provider: dict[str, AggregateStats] = defaultdict(AggregateStats)
        self._by_model: dict[str, AggregateStats] = defaultdict(AggregateStats)
        self._global = AggregateStats()
        self._hourly: dict[str, AggregateStats] = defaultdict(AggregateStats)
        self.budget = budget_manager or BudgetManager()
        self._alerts: list[BudgetAlert] = []

    def record(
        self,
        route: str,
        provider: str,
        model: str = "",
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: Optional[float] = None,
        latency: float = 0.0,
        metadata: Optional[dict] = None,
    ) -> UsageRecord:
        """Record a token usage event."""
        # Auto-calculate cost if not provided
        if cost is None:
            provider_type = provider.split("-")[0] if "-" in provider else provider
            rates = COST_TABLE.get(provider_type, (0.0, 0.0))
            cost = (input_tokens / 1000) * rates[0] + (output_tokens / 1000) * rates[1]

        rec = UsageRecord(
            timestamp=time.time(),
            route=route,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            latency=latency,
            metadata=metadata or {},
        )

        # Store record
        self._records.append(rec)
        if len(self._records) > 10000:
            self._records = self._records[-10000:]

        # Update aggregates
        self._global.record(rec)
        self._by_route[route].record(rec)
        self._by_provider[provider].record(rec)
        self._by_model[model].record(rec)

        # Hourly bucket
        hour_key = time.strftime("%Y-%m-%d-%H", time.gmtime(rec.timestamp))
        self._hourly[hour_key].record(rec)

        # Check budgets
        alert = self.budget.check(self._global.total_cost)
        if alert:
            self._alerts.append(alert)

        return rec

    def get_route_stats(self, route: str) -> dict:
        """Get stats for a specific route."""
        if route in self._by_route:
            return self._by_route[route].to_dict()
        return {}

    def get_provider_stats(self, provider: str) -> dict:
        """Get stats for a specific provider."""
        if provider in self._by_provider:
            return self._by_provider[provider].to_dict()
        return {}

    def top_routes(self, n: int = 10) -> list[dict]:
        """Get top N routes by token usage."""
        routes = [
            {"route": k, **v.to_dict()}
            for k, v in self._by_route.items()
        ]
        return sorted(routes, key=lambda x: x["total_tokens"], reverse=True)[:n]

    def top_providers(self, n: int = 10) -> list[dict]:
        """Get top N providers by cost."""
        providers = [
            {"provider": k, **v.to_dict()}
            for k, v in self._by_provider.items()
        ]
        return sorted(providers, key=lambda x: x["total_cost"], reverse=True)[:n]

    def hourly_breakdown(self, last_n_hours: int = 24) -> list[dict]:
        """Get hourly usage for the last N hours."""
        keys = sorted(self._hourly.keys())[-last_n_hours:]
        return [
            {"hour": k, **self._hourly[k].to_dict()}
            for k in keys
        ]

    def summary(self) -> dict:
        """Full usage summary."""
        return {
            "global": self._global.to_dict(),
            "top_routes": self.top_routes(5),
            "top_providers": self.top_providers(5),
            "budget": self.budget.status(),
            "alerts": [a.to_dict() for a in self._alerts[-10:]],
            "hourly": self.hourly_breakdown(6),
        }

    def dashboard(self) -> str:
        """ASCII dashboard of token usage."""
        g = self._global
        lines = [
            "╔══════════════════════════════════════════╗",
            "║       TOKEN USAGE DASHBOARD              ║",
            "╠══════════════════════════════════════════╣",
            f"║  Requests:     {g.total_requests:<25}║",
            f"║  Input Tokens: {g.total_input_tokens:<25}║",
            f"║  Output Tokens:{g.total_output_tokens:<25}║",
            f"║  Total Tokens: {g.total_tokens:<25}║",
            f"║  Total Cost:   ${g.total_cost:<24.4f}║",
            f"║  Avg/Request:  {g.avg_tokens_per_request:<22.0f}tk ║",
            "╠══════════════════════════════════════════╣",
            "║  BY ROUTE                                ║",
        ]

        for r in self.top_routes(5):
            name = r["route"][:18]
            lines.append(
                f"║  {name:<18} {r['total_tokens']:>8}tk ${r['total_cost']:>7.4f} ║"
            )

        lines.extend([
            "╠══════════════════════════════════════════╣",
            "║  BY PROVIDER                             ║",
        ])

        for p in self.top_providers(5):
            name = p["provider"][:18]
            lines.append(
                f"║  {name:<18} {p['total_tokens']:>8}tk ${p['total_cost']:>7.4f} ║"
            )

        budget_status = self.budget.status()
        lines.extend([
            "╠══════════════════════════════════════════╣",
            f"║  Budget: ${budget_status['spent']:.2f} / ${budget_status['limit']:.2f}"
            f" ({budget_status['percent_used']:.0f}%)"
            + " " * 10 + "║",
            "╚══════════════════════════════════════════╝",
        ])

        return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    """Demo the token tracker."""
    print("BlackRoad Token Usage Tracker")
    print("=" * 40)

    tracker = TokenTracker()
    tracker.budget.set_daily_limit(10.0)  # $10/day

    # Simulate some usage
    routes = ["code_review", "summarize", "classify", "debug", "search"]
    providers = ["claude-primary", "gpt-secondary", "llama-local"]
    models = ["claude-sonnet-4-20250514", "gpt-4o", "llama3:8b"]

    import random
    for i in range(50):
        r = random.randint(0, len(routes) - 1)
        p = random.randint(0, len(providers) - 1)
        tracker.record(
            route=routes[r],
            provider=providers[p],
            model=models[p],
            input_tokens=random.randint(50, 500),
            output_tokens=random.randint(100, 1000),
            latency=random.uniform(0.5, 5.0),
        )

    print(tracker.dashboard())
    print(f"\n{json.dumps(tracker.summary(), indent=2)}")


if __name__ == "__main__":
    main()
