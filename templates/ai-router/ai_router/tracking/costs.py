"""
Cost Tracking - Know exactly what you're spending.

Track every token, every dollar, every provider.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class UsageRecord:
    """A single usage record."""
    timestamp: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    latency_ms: int
    success: bool


@dataclass
class CostReport:
    """Aggregated cost report."""
    period_start: str
    period_end: str
    total_cost: float
    total_tokens: int
    total_requests: int
    success_rate: float
    by_provider: Dict[str, Dict[str, Any]]
    by_model: Dict[str, Dict[str, Any]]
    avg_latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "period_start": self.period_start,
            "period_end": self.period_end,
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "total_requests": self.total_requests,
            "success_rate": self.success_rate,
            "by_provider": self.by_provider,
            "by_model": self.by_model,
            "avg_latency_ms": self.avg_latency_ms,
        }

    def summary(self) -> str:
        """Human-readable summary."""
        lines = [
            f"Cost Report: {self.period_start} to {self.period_end}",
            "=" * 50,
            f"Total Cost:     ${self.total_cost:.4f}",
            f"Total Tokens:   {self.total_tokens:,}",
            f"Total Requests: {self.total_requests}",
            f"Success Rate:   {self.success_rate:.1%}",
            f"Avg Latency:    {self.avg_latency_ms:.0f}ms",
            "",
            "By Provider:",
        ]

        for provider, stats in self.by_provider.items():
            lines.append(f"  {provider}: ${stats['cost']:.4f} ({stats['requests']} requests)")

        lines.append("")
        lines.append("By Model:")
        for model, stats in self.by_model.items():
            lines.append(f"  {model}: ${stats['cost']:.4f} ({stats['tokens']:,} tokens)")

        return "\n".join(lines)


class CostTracker:
    """
    Track costs across all AI usage.

    Features:
    - Per-request tracking
    - Aggregated reports
    - Budget alerts
    - Persistent storage

    Usage:
        tracker = CostTracker()

        # Record usage
        tracker.record(response)

        # Get report
        report = tracker.report(period="day")
        print(report.summary())

        # Check budget
        if tracker.total_cost > budget:
            alert()
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the cost tracker.

        Args:
            storage_path: Path to persist usage data
        """
        self.records: List[UsageRecord] = []
        self.storage_path = Path(storage_path) if storage_path else None

        if self.storage_path and self.storage_path.exists():
            self._load()

    def record(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        latency_ms: int,
        success: bool = True,
    ):
        """Record a usage event."""
        record = UsageRecord(
            timestamp=datetime.utcnow().isoformat(),
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost=cost,
            latency_ms=latency_ms,
            success=success,
        )
        self.records.append(record)

        # Persist
        if self.storage_path:
            self._save()

    def record_response(self, response: Any):
        """Record from a CompletionResponse."""
        self.record(
            provider=response.provider,
            model=response.model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            cost=response.cost,
            latency_ms=response.latency_ms,
            success=True,
        )

    @property
    def total_cost(self) -> float:
        """Total cost across all records."""
        return sum(r.cost for r in self.records)

    @property
    def total_tokens(self) -> int:
        """Total tokens used."""
        return sum(r.total_tokens for r in self.records)

    def report(
        self,
        period: str = "all",
        provider: Optional[str] = None,
    ) -> CostReport:
        """
        Generate a cost report.

        Args:
            period: "hour", "day", "week", "month", "all"
            provider: Filter to specific provider

        Returns:
            CostReport with aggregated data
        """
        # Filter by time
        now = datetime.utcnow()
        if period == "hour":
            cutoff = now - timedelta(hours=1)
        elif period == "day":
            cutoff = now - timedelta(days=1)
        elif period == "week":
            cutoff = now - timedelta(weeks=1)
        elif period == "month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = datetime.min

        filtered = [
            r for r in self.records
            if datetime.fromisoformat(r.timestamp) >= cutoff
        ]

        # Filter by provider
        if provider:
            filtered = [r for r in filtered if r.provider == provider]

        if not filtered:
            return CostReport(
                period_start=cutoff.isoformat(),
                period_end=now.isoformat(),
                total_cost=0,
                total_tokens=0,
                total_requests=0,
                success_rate=0,
                by_provider={},
                by_model={},
                avg_latency_ms=0,
            )

        # Aggregate
        by_provider: Dict[str, Dict[str, Any]] = {}
        by_model: Dict[str, Dict[str, Any]] = {}
        total_latency = 0
        successful = 0

        for r in filtered:
            # By provider
            if r.provider not in by_provider:
                by_provider[r.provider] = {"cost": 0, "tokens": 0, "requests": 0}
            by_provider[r.provider]["cost"] += r.cost
            by_provider[r.provider]["tokens"] += r.total_tokens
            by_provider[r.provider]["requests"] += 1

            # By model
            if r.model not in by_model:
                by_model[r.model] = {"cost": 0, "tokens": 0, "requests": 0}
            by_model[r.model]["cost"] += r.cost
            by_model[r.model]["tokens"] += r.total_tokens
            by_model[r.model]["requests"] += 1

            total_latency += r.latency_ms
            if r.success:
                successful += 1

        return CostReport(
            period_start=cutoff.isoformat(),
            period_end=now.isoformat(),
            total_cost=sum(r.cost for r in filtered),
            total_tokens=sum(r.total_tokens for r in filtered),
            total_requests=len(filtered),
            success_rate=successful / len(filtered) if filtered else 0,
            by_provider=by_provider,
            by_model=by_model,
            avg_latency_ms=total_latency / len(filtered) if filtered else 0,
        )

    def _save(self):
        """Save records to disk."""
        if not self.storage_path:
            return

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(
                [vars(r) for r in self.records],
                f,
                indent=2
            )

    def _load(self):
        """Load records from disk."""
        if not self.storage_path or not self.storage_path.exists():
            return

        with open(self.storage_path) as f:
            data = json.load(f)
            self.records = [UsageRecord(**r) for r in data]

    def clear(self):
        """Clear all records."""
        self.records = []
        if self.storage_path and self.storage_path.exists():
            self.storage_path.unlink()
