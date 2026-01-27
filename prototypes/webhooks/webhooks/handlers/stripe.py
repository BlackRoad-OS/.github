"""Stripe webhook handler."""

import hmac
import hashlib
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class StripeHandler(WebhookHandler):
    """
    Handle Stripe webhooks.

    Events:
    - payment_intent.succeeded: Payment received
    - payment_intent.payment_failed: Payment failed
    - customer.subscription.created: New subscription
    - customer.subscription.deleted: Subscription cancelled
    - invoice.paid: Invoice paid
    """

    name = "stripe"
    target_org = "FND"

    # Event to signal type mapping
    EVENT_MAP = {
        "payment_intent.succeeded": SignalType.PAYMENT_RECEIVED,
        "payment_intent.payment_failed": SignalType.PAYMENT_FAILED,
        "charge.succeeded": SignalType.PAYMENT_RECEIVED,
        "charge.failed": SignalType.PAYMENT_FAILED,
        "customer.subscription.created": SignalType.SUBSCRIPTION_CREATED,
        "customer.subscription.deleted": SignalType.SUBSCRIPTION_CANCELLED,
        "customer.subscription.updated": SignalType.RECORD_UPDATED,
        "invoice.paid": SignalType.INVOICE_PAID,
        "invoice.payment_failed": SignalType.PAYMENT_FAILED,
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for Stripe webhook headers."""
        return self.get_header(headers, "Stripe-Signature") is not None

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify Stripe webhook signature."""
        if not secret:
            return True

        sig_header = self.get_header(headers, "Stripe-Signature")
        if not sig_header:
            return False

        # Parse signature header
        elements = dict(item.split("=") for item in sig_header.split(","))
        timestamp = elements.get("t", "")
        signature = elements.get("v1", "")

        # Compute expected signature
        payload = f"{timestamp}.{body.decode()}"
        expected = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse Stripe webhook into Signal."""
        event_type = body.get("type", "unknown")
        signal_type = self.EVENT_MAP.get(event_type, SignalType.CUSTOM)

        # Extract data from event object
        obj = body.get("data", {}).get("object", {})

        data = {
            "event": event_type,
            "id": obj.get("id", ""),
        }

        # Payment events
        if "payment" in event_type or "charge" in event_type:
            data.update({
                "amount": obj.get("amount", 0) / 100,  # Convert cents to dollars
                "currency": obj.get("currency", "usd").upper(),
                "customer": obj.get("customer", ""),
                "status": obj.get("status", ""),
            })

        # Subscription events
        elif "subscription" in event_type:
            data.update({
                "customer": obj.get("customer", ""),
                "status": obj.get("status", ""),
                "plan": obj.get("plan", {}).get("id", ""),
                "amount": obj.get("plan", {}).get("amount", 0) / 100,
            })

        # Invoice events
        elif "invoice" in event_type:
            data.update({
                "customer": obj.get("customer", ""),
                "amount": obj.get("amount_paid", 0) / 100,
                "status": obj.get("status", ""),
            })

        return Signal(
            type=signal_type,
            source=self.name,
            target=self.target_org,
            data=data,
            raw=body,
        )
