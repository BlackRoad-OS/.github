"""Invoice model for Stripe billing."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Invoice:
    """Represents a Stripe invoice."""
    id: str
    customer_id: str
    subscription_id: Optional[str] = None
    status: str = "draft"  # draft, open, paid, void, uncollectible
    amount_due: int = 0    # cents
    amount_paid: int = 0   # cents
    currency: str = "usd"
    created: str = ""

    def __post_init__(self):
        if not self.created:
            self.created = datetime.utcnow().isoformat()

    @property
    def is_paid(self) -> bool:
        return self.status == "paid"

    @property
    def amount_due_dollars(self) -> float:
        return self.amount_due / 100

    @property
    def amount_paid_dollars(self) -> float:
        return self.amount_paid / 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "subscription_id": self.subscription_id,
            "status": self.status,
            "amount_due": self.amount_due,
            "amount_paid": self.amount_paid,
            "currency": self.currency,
            "is_paid": self.is_paid,
            "created": self.created,
        }

    @classmethod
    def from_stripe(cls, data: Dict[str, Any]) -> "Invoice":
        """Create from Stripe API response."""
        return cls(
            id=data["id"],
            customer_id=data.get("customer", ""),
            subscription_id=data.get("subscription"),
            status=data.get("status", "draft"),
            amount_due=data.get("amount_due", 0),
            amount_paid=data.get("amount_paid", 0),
            currency=data.get("currency", "usd"),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Invoice":
        return cls(
            id=data["id"],
            customer_id=data["customer_id"],
            subscription_id=data.get("subscription_id"),
            status=data.get("status", "draft"),
            amount_due=data.get("amount_due", 0),
            amount_paid=data.get("amount_paid", 0),
            currency=data.get("currency", "usd"),
            created=data.get("created", ""),
        )
