"""Price model for Stripe billing."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


# BlackRoad pricing tiers
BLACKROAD_PRICES = {
    "blackroad_basic": {
        "name": "BlackRoad Basic",
        "amount": 100,  # $1.00/month
        "currency": "usd",
        "interval": "month",
        "features": ["API access", "1 workspace"],
    },
    "blackroad_pro": {
        "name": "BlackRoad Pro",
        "amount": 500,  # $5.00/month
        "currency": "usd",
        "interval": "month",
        "features": ["API access", "10 workspaces", "Priority support"],
    },
    "blackroad_enterprise": {
        "name": "BlackRoad Enterprise",
        "amount": None,  # Custom pricing
        "currency": "usd",
        "interval": "month",
        "features": ["Everything", "SLA", "Dedicated support"],
    },
}


@dataclass
class Price:
    """Represents a Stripe price."""
    id: str
    product_id: str
    amount: Optional[int]  # cents, None for custom
    currency: str = "usd"
    interval: str = "month"
    active: bool = True

    @property
    def amount_dollars(self) -> Optional[float]:
        return self.amount / 100 if self.amount is not None else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "amount": self.amount,
            "currency": self.currency,
            "interval": self.interval,
            "active": self.active,
            "amount_dollars": self.amount_dollars,
        }

    @classmethod
    def from_stripe(cls, data: Dict[str, Any]) -> "Price":
        """Create from Stripe API response."""
        return cls(
            id=data["id"],
            product_id=data.get("product", ""),
            amount=data.get("unit_amount"),
            currency=data.get("currency", "usd"),
            interval=data.get("recurring", {}).get("interval", "month")
            if data.get("recurring") else "one_time",
            active=data.get("active", True),
        )
