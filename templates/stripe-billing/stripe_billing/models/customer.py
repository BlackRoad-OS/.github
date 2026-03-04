"""Customer model for Stripe billing."""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime


@dataclass
class Customer:
    """Represents a Stripe customer."""
    id: str
    email: str
    name: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    created: str = ""

    def __post_init__(self):
        if not self.created:
            self.created = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "metadata": self.metadata,
            "created": self.created,
        }

    @classmethod
    def from_stripe(cls, data: Dict[str, Any]) -> "Customer":
        """Create from Stripe API response."""
        return cls(
            id=data["id"],
            email=data.get("email", ""),
            name=data.get("name"),
            metadata=data.get("metadata", {}),
            created=datetime.fromtimestamp(data.get("created", 0)).isoformat()
            if isinstance(data.get("created"), (int, float))
            else str(data.get("created", "")),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        return cls(
            id=data["id"],
            email=data["email"],
            name=data.get("name"),
            metadata=data.get("metadata", {}),
            created=data.get("created", ""),
        )
