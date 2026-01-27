"""
Base webhook handler interface.

All handlers implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..signal import Signal


class WebhookHandler(ABC):
    """Base class for webhook handlers."""

    name: str = "base"
    target_org: str = "OS"  # Default target org

    @abstractmethod
    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check if this handler can process the webhook."""
        pass

    @abstractmethod
    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse webhook into a Signal."""
        pass

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify webhook signature. Override in subclass."""
        return True  # Default: no verification

    def get_header(self, headers: Dict[str, str], name: str) -> Optional[str]:
        """Get header value (case-insensitive)."""
        name_lower = name.lower()
        for key, value in headers.items():
            if key.lower() == name_lower:
                return value
        return None
