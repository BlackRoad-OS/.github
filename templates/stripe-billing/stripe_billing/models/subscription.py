"""Subscription model for Stripe billing."""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime


@dataclass
class Subscription:
    """Represents a Stripe subscription."""
    id: str
    customer_id: str
    status: str  # active, canceled, past_due, trialing, incomplete
    price_id: str = ""
    current_period_start: str = ""
    current_period_end: str = ""
    cancel_at_period_end: bool = False
    created: str = ""

    def __post_init__(self):
        if not self.created:
            self.created = datetime.utcnow().isoformat()

    @property
    def is_active(self) -> bool:
        return self.status in ("active", "trialing")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "status": self.status,
            "price_id": self.price_id,
            "current_period_start": self.current_period_start,
            "current_period_end": self.current_period_end,
            "cancel_at_period_end": self.cancel_at_period_end,
            "is_active": self.is_active,
            "created": self.created,
        }

    @classmethod
    def from_stripe(cls, data: Dict[str, Any]) -> "Subscription":
        """Create from Stripe API response."""
        items = data.get("items", {}).get("data", [])
        price_id = items[0]["price"]["id"] if items else ""

        return cls(
            id=data["id"],
            customer_id=data.get("customer", ""),
            status=data.get("status", "incomplete"),
            price_id=price_id,
            current_period_start=datetime.fromtimestamp(
                data.get("current_period_start", 0)
            ).isoformat() if data.get("current_period_start") else "",
            current_period_end=datetime.fromtimestamp(
                data.get("current_period_end", 0)
            ).isoformat() if data.get("current_period_end") else "",
            cancel_at_period_end=data.get("cancel_at_period_end", False),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Subscription":
        return cls(
            id=data["id"],
            customer_id=data["customer_id"],
            status=data["status"],
            price_id=data.get("price_id", ""),
            current_period_start=data.get("current_period_start", ""),
            current_period_end=data.get("current_period_end", ""),
            cancel_at_period_end=data.get("cancel_at_period_end", False),
            created=data.get("created", ""),
        )
