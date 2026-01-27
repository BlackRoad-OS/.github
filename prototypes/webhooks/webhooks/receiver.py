"""
WebhookReceiver - The central webhook processing system.

Receives webhooks from all providers, converts them to signals,
and dispatches them to the appropriate org.
"""

import json
from typing import Dict, Any, Optional, List, Type
from datetime import datetime
from dataclasses import dataclass, field

from .signal import Signal, SignalType
from .handlers import (
    WebhookHandler,
    GitHubHandler,
    StripeHandler,
    SalesforceHandler,
    CloudflareHandler,
    SlackHandler,
    GoogleHandler,
    FigmaHandler,
)


@dataclass
class WebhookResult:
    """Result of processing a webhook."""
    success: bool
    signal: Optional[Signal] = None
    handler: str = ""
    error: Optional[str] = None
    verified: bool = False
    processing_time_ms: int = 0
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "signal": self.signal.to_dict() if self.signal else None,
            "handler": self.handler,
            "error": self.error,
            "verified": self.verified,
            "processing_time_ms": self.processing_time_ms,
            "timestamp": self.timestamp,
        }


class WebhookReceiver:
    """
    Central webhook receiver for the BlackRoad mesh.

    Routes incoming webhooks to the appropriate handler,
    verifies signatures, parses payloads, and emits signals.

    Usage:
        receiver = WebhookReceiver()

        # Process a webhook
        result = receiver.process(
            headers={"X-GitHub-Event": "push", ...},
            body=b'{"action": "push", ...}',
        )

        if result.success:
            print(f"Signal: {result.signal.format()}")
            # -> 📥 GITHUB → OS : push, repo=BlackRoad-OS/.github
    """

    # Default handler classes
    DEFAULT_HANDLERS: List[Type[WebhookHandler]] = [
        GitHubHandler,
        StripeHandler,
        SalesforceHandler,
        CloudflareHandler,
        SlackHandler,
        GoogleHandler,
        FigmaHandler,
    ]

    def __init__(
        self,
        secrets: Optional[Dict[str, str]] = None,
        handlers: Optional[List[WebhookHandler]] = None,
    ):
        """
        Initialize the receiver.

        Args:
            secrets: Dict of provider -> secret for verification
            handlers: Custom handlers (uses defaults if None)
        """
        self.secrets = secrets or {}
        self.handlers = handlers or [h() for h in self.DEFAULT_HANDLERS]
        self._history: List[WebhookResult] = []

    def process(
        self,
        headers: Dict[str, str],
        body: bytes,
        provider_hint: Optional[str] = None,
    ) -> WebhookResult:
        """
        Process an incoming webhook.

        Args:
            headers: HTTP headers
            body: Raw request body (bytes)
            provider_hint: Optional hint for which provider sent this

        Returns:
            WebhookResult with signal or error
        """
        start_time = datetime.now()

        # Parse body to dict
        try:
            body_dict = json.loads(body.decode())
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return WebhookResult(
                success=False,
                error=f"Invalid JSON body: {str(e)}",
            )

        # Find handler
        handler = self._find_handler(headers, body_dict, provider_hint)
        if not handler:
            return WebhookResult(
                success=False,
                error="No handler found for this webhook",
            )

        # Verify signature
        secret = self.secrets.get(handler.name)
        verified = handler.verify(headers, body, secret)

        if secret and not verified:
            return WebhookResult(
                success=False,
                handler=handler.name,
                verified=False,
                error="Signature verification failed",
            )

        # Parse webhook to signal
        try:
            signal = handler.parse(headers, body_dict)
        except Exception as e:
            return WebhookResult(
                success=False,
                handler=handler.name,
                verified=verified,
                error=f"Failed to parse webhook: {str(e)}",
            )

        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        result = WebhookResult(
            success=True,
            signal=signal,
            handler=handler.name,
            verified=verified,
            processing_time_ms=processing_time,
        )

        # Track history
        self._history.append(result)

        return result

    def _find_handler(
        self,
        headers: Dict[str, str],
        body: Dict[str, Any],
        provider_hint: Optional[str] = None,
    ) -> Optional[WebhookHandler]:
        """Find the appropriate handler for this webhook."""
        # If provider hint given, try that first
        if provider_hint:
            for handler in self.handlers:
                if handler.name == provider_hint:
                    return handler

        # Try each handler
        for handler in self.handlers:
            if handler.can_handle(headers, body):
                return handler

        return None

    def register_handler(self, handler: WebhookHandler) -> None:
        """Register a custom handler."""
        self.handlers.append(handler)

    def set_secret(self, provider: str, secret: str) -> None:
        """Set the secret for a provider."""
        self.secrets[provider] = secret

    @property
    def stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        if not self._history:
            return {
                "total": 0,
                "success_rate": 0,
                "by_handler": {},
                "by_signal_type": {},
            }

        successful = [r for r in self._history if r.success]
        by_handler: Dict[str, int] = {}
        by_signal: Dict[str, int] = {}

        for r in self._history:
            by_handler[r.handler] = by_handler.get(r.handler, 0) + 1
            if r.signal:
                sig_type = r.signal.type.value
                by_signal[sig_type] = by_signal.get(sig_type, 0) + 1

        return {
            "total": len(self._history),
            "success_rate": len(successful) / len(self._history),
            "avg_processing_ms": sum(r.processing_time_ms for r in self._history) / len(self._history),
            "by_handler": by_handler,
            "by_signal_type": by_signal,
        }

    def recent_signals(self, limit: int = 10) -> List[Signal]:
        """Get recent processed signals."""
        signals = [r.signal for r in self._history if r.signal]
        return signals[-limit:]


# Convenience function for simple webhook processing
def process_webhook(
    headers: Dict[str, str],
    body: bytes,
    secrets: Optional[Dict[str, str]] = None,
) -> WebhookResult:
    """
    Process a webhook (stateless convenience function).

    Args:
        headers: HTTP headers
        body: Raw request body
        secrets: Optional secrets for verification

    Returns:
        WebhookResult
    """
    receiver = WebhookReceiver(secrets=secrets)
    return receiver.process(headers, body)
