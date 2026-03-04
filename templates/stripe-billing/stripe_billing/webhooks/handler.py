"""
Stripe webhook handler for the billing service.

Runs on lucidia:8092 and processes incoming Stripe events,
converting them to BlackRoad signals routed through FND org.
"""

import json
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime

from ..client import StripeClient
from ..models.customer import Customer
from ..models.subscription import Subscription
from ..models.invoice import Invoice


@dataclass
class WebhookEvent:
    """Processed webhook event."""
    event_type: str
    object_id: str
    success: bool
    signal: str = ""
    error: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


class StripeWebhookHandler:
    """
    Handles incoming Stripe webhook events on the billing service.

    Maps Stripe events to BlackRoad signal actions:
    - payment_intent.succeeded → grant/extend access
    - customer.subscription.created → provision workspace
    - customer.subscription.deleted → revoke access
    - invoice.paid → record payment
    - invoice.payment_failed → alert + retry
    """

    # Event type to handler method mapping
    EVENT_HANDLERS = {
        "payment_intent.succeeded": "_handle_payment_succeeded",
        "payment_intent.payment_failed": "_handle_payment_failed",
        "customer.created": "_handle_customer_created",
        "customer.subscription.created": "_handle_subscription_created",
        "customer.subscription.updated": "_handle_subscription_updated",
        "customer.subscription.deleted": "_handle_subscription_deleted",
        "invoice.paid": "_handle_invoice_paid",
        "invoice.payment_failed": "_handle_invoice_payment_failed",
        "charge.succeeded": "_handle_payment_succeeded",
        "charge.failed": "_handle_payment_failed",
    }

    def __init__(self, client: Optional[StripeClient] = None):
        self.client = client or StripeClient(test_mode=True)
        self._history: List[WebhookEvent] = []

    def process_event(self, event: Dict[str, Any]) -> WebhookEvent:
        """
        Process a verified Stripe webhook event.

        Args:
            event: Parsed Stripe event object

        Returns:
            WebhookEvent with result
        """
        event_type = event.get("type", "unknown")
        obj = event.get("data", {}).get("object", {})
        object_id = obj.get("id", "unknown")

        handler_name = self.EVENT_HANDLERS.get(event_type)
        if not handler_name:
            result = WebhookEvent(
                event_type=event_type,
                object_id=object_id,
                success=True,
                signal=f"📡 FND → OS : stripe_event, type={event_type}",
            )
            self._history.append(result)
            return result

        handler = getattr(self, handler_name)
        try:
            signal = handler(obj)
            result = WebhookEvent(
                event_type=event_type,
                object_id=object_id,
                success=True,
                signal=signal,
            )
        except Exception as e:
            result = WebhookEvent(
                event_type=event_type,
                object_id=object_id,
                success=False,
                error=str(e),
            )

        self._history.append(result)
        return result

    def _handle_payment_succeeded(self, obj: Dict[str, Any]) -> str:
        amount = obj.get("amount", 0)
        customer = obj.get("customer", "unknown")
        return f"💰 FND → OS : payment_received, customer={customer}, amount=${amount / 100:.2f}"

    def _handle_payment_failed(self, obj: Dict[str, Any]) -> str:
        amount = obj.get("amount", 0)
        customer = obj.get("customer", "unknown")
        return f"❌ FND → OS : payment_failed, customer={customer}, amount=${amount / 100:.2f}"

    def _handle_customer_created(self, obj: Dict[str, Any]) -> str:
        email = obj.get("email", "unknown")
        customer_id = obj.get("id", "unknown")
        # Sync to local store
        self.client._customers[customer_id] = Customer.from_stripe(obj)
        return f"👤 FND → OS : customer_created, id={customer_id}, email={email}"

    def _handle_subscription_created(self, obj: Dict[str, Any]) -> str:
        sub_id = obj.get("id", "unknown")
        customer = obj.get("customer", "unknown")
        status = obj.get("status", "unknown")
        plan = obj.get("plan", {}).get("id", "unknown")
        # Sync to local store
        self.client._subscriptions[sub_id] = Subscription.from_stripe(obj)
        return f"📦 FND → OS : subscription_created, customer={customer}, plan={plan}, status={status}"

    def _handle_subscription_updated(self, obj: Dict[str, Any]) -> str:
        sub_id = obj.get("id", "unknown")
        customer = obj.get("customer", "unknown")
        status = obj.get("status", "unknown")
        if sub_id in self.client._subscriptions:
            self.client._subscriptions[sub_id].status = status
        return f"📦 FND → OS : subscription_updated, customer={customer}, status={status}"

    def _handle_subscription_deleted(self, obj: Dict[str, Any]) -> str:
        sub_id = obj.get("id", "unknown")
        customer = obj.get("customer", "unknown")
        if sub_id in self.client._subscriptions:
            self.client._subscriptions[sub_id].status = "canceled"
        return f"📦 FND → OS : subscription_cancelled, customer={customer}"

    def _handle_invoice_paid(self, obj: Dict[str, Any]) -> str:
        invoice_id = obj.get("id", "unknown")
        customer = obj.get("customer", "unknown")
        amount = obj.get("amount_paid", 0)
        return f"🧾 FND → OS : invoice_paid, customer={customer}, amount=${amount / 100:.2f}"

    def _handle_invoice_payment_failed(self, obj: Dict[str, Any]) -> str:
        invoice_id = obj.get("id", "unknown")
        customer = obj.get("customer", "unknown")
        amount = obj.get("amount_due", 0)
        return f"⚠️ FND → OS : payment_failed, customer={customer}, amount=${amount / 100:.2f}"

    @property
    def stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        if not self._history:
            return {"total": 0, "success_rate": 0, "by_type": {}}

        successful = [e for e in self._history if e.success]
        by_type: Dict[str, int] = {}
        for e in self._history:
            by_type[e.event_type] = by_type.get(e.event_type, 0) + 1

        return {
            "total": len(self._history),
            "success_rate": len(successful) / len(self._history),
            "by_type": by_type,
        }
