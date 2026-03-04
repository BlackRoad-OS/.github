"""
Stripe client wrapper for BlackRoad billing.

Wraps Stripe API operations and emits signals to the BlackRoad mesh.
Routes through FND org on lucidia:8092.
"""

import os
import json
import hmac
import hashlib
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from .models.customer import Customer
from .models.subscription import Subscription
from .models.invoice import Invoice
from .models.price import Price, BLACKROAD_PRICES


@dataclass
class BillingMetrics:
    """Billing KPIs."""
    total_customers: int = 0
    active_subscriptions: int = 0
    mrr_cents: int = 0  # Monthly recurring revenue in cents
    total_revenue_cents: int = 0

    @property
    def mrr_dollars(self) -> float:
        return self.mrr_cents / 100

    @property
    def total_revenue_dollars(self) -> float:
        return self.total_revenue_cents / 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_customers": self.total_customers,
            "active_subscriptions": self.active_subscriptions,
            "mrr_cents": self.mrr_cents,
            "mrr_dollars": self.mrr_dollars,
            "total_revenue_cents": self.total_revenue_cents,
            "total_revenue_dollars": self.total_revenue_dollars,
        }


class StripeClient:
    """
    BlackRoad Stripe client.

    Manages customers, subscriptions, invoices, and webhook verification.
    Designed to run on lucidia:8092 and emit signals to the mesh.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        test_mode: bool = False,
    ):
        self.api_key = api_key or os.environ.get("STRIPE_API_KEY", "")
        self.webhook_secret = webhook_secret or os.environ.get("STRIPE_WEBHOOK_SECRET", "")
        self.test_mode = test_mode

        # In-memory stores for test mode
        self._customers: Dict[str, Customer] = {}
        self._subscriptions: Dict[str, Subscription] = {}
        self._invoices: Dict[str, Invoice] = {}
        self._events: List[Dict[str, Any]] = []

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature_header: str,
        secret: Optional[str] = None,
    ) -> bool:
        """
        Verify Stripe webhook signature (v1).

        Args:
            payload: Raw request body bytes
            signature_header: Stripe-Signature header value
            secret: Webhook endpoint secret (uses self.webhook_secret if not provided)

        Returns:
            True if signature is valid
        """
        signing_secret = secret or self.webhook_secret
        if not signing_secret:
            return False

        try:
            elements = {}
            for item in signature_header.split(","):
                key, value = item.split("=", 1)
                elements[key.strip()] = value.strip()

            timestamp = elements.get("t", "")
            signature = elements.get("v1", "")

            if not timestamp or not signature:
                return False

            signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
            expected = hmac.HMAC(
                signing_secret.encode("utf-8"),
                signed_payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            return hmac.compare_digest(signature, expected)
        except Exception:
            return False

    def construct_event(
        self,
        payload: bytes,
        signature_header: str,
        secret: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Verify signature and construct event object.

        Returns:
            Parsed event dict if valid, None if verification fails
        """
        if not self.verify_webhook_signature(payload, signature_header, secret):
            return None

        try:
            return json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    # ─── Customer operations ──────────────────────────────────────

    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Customer:
        """Create a new customer."""
        customer_id = f"cus_{'test_' if self.test_mode else ''}{_generate_id()}"
        customer = Customer(
            id=customer_id,
            email=email,
            name=name,
            metadata=metadata or {},
        )
        self._customers[customer_id] = customer
        self._emit_event("customer.created", customer.to_dict())
        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        return self._customers.get(customer_id)

    def list_customers(self) -> List[Customer]:
        """List all customers."""
        return list(self._customers.values())

    # ─── Subscription operations ──────────────────────────────────

    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
    ) -> Optional[Subscription]:
        """Create a subscription for a customer."""
        customer = self._customers.get(customer_id)
        if not customer:
            return None

        sub_id = f"sub_{'test_' if self.test_mode else ''}{_generate_id()}"
        subscription = Subscription(
            id=sub_id,
            customer_id=customer_id,
            status="active",
            price_id=price_id,
        )
        self._subscriptions[sub_id] = subscription
        self._emit_event("customer.subscription.created", {
            "id": sub_id,
            "customer": customer_id,
            "status": "active",
            "plan": {"id": price_id},
        })
        return subscription

    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True,
    ) -> Optional[Subscription]:
        """Cancel a subscription."""
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            return None

        if at_period_end:
            sub.cancel_at_period_end = True
        else:
            sub.status = "canceled"

        event_type = "customer.subscription.updated" if at_period_end else "customer.subscription.deleted"
        self._emit_event(event_type, sub.to_dict())
        return sub

    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get subscription by ID."""
        return self._subscriptions.get(subscription_id)

    def list_subscriptions(self, customer_id: Optional[str] = None) -> List[Subscription]:
        """List subscriptions, optionally filtered by customer."""
        subs = list(self._subscriptions.values())
        if customer_id:
            subs = [s for s in subs if s.customer_id == customer_id]
        return subs

    # ─── Invoice operations ───────────────────────────────────────

    def create_invoice(
        self,
        customer_id: str,
        amount_cents: int,
        subscription_id: Optional[str] = None,
    ) -> Optional[Invoice]:
        """Create an invoice."""
        customer = self._customers.get(customer_id)
        if not customer:
            return None

        inv_id = f"in_{'test_' if self.test_mode else ''}{_generate_id()}"
        invoice = Invoice(
            id=inv_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
            status="open",
            amount_due=amount_cents,
        )
        self._invoices[inv_id] = invoice
        return invoice

    def pay_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """Mark an invoice as paid."""
        invoice = self._invoices.get(invoice_id)
        if not invoice:
            return None

        invoice.status = "paid"
        invoice.amount_paid = invoice.amount_due
        self._emit_event("invoice.paid", {
            "id": invoice.id,
            "customer": invoice.customer_id,
            "amount_paid": invoice.amount_paid,
            "status": "paid",
        })
        return invoice

    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """Get invoice by ID."""
        return self._invoices.get(invoice_id)

    # ─── Metrics ──────────────────────────────────────────────────

    def get_metrics(self) -> BillingMetrics:
        """Calculate billing metrics."""
        active_subs = [s for s in self._subscriptions.values() if s.is_active]
        paid_invoices = [i for i in self._invoices.values() if i.is_paid]

        # Calculate MRR from active subscriptions using price lookup
        mrr = 0
        for sub in active_subs:
            for tier_key, tier in BLACKROAD_PRICES.items():
                if tier["amount"] and sub.price_id and tier_key in sub.price_id:
                    mrr += tier["amount"]
                    break
            else:
                mrr += 100  # Default $1/month

        return BillingMetrics(
            total_customers=len(self._customers),
            active_subscriptions=len(active_subs),
            mrr_cents=mrr,
            total_revenue_cents=sum(i.amount_paid for i in paid_invoices),
        )

    # ─── Internal ─────────────────────────────────────────────────

    def _emit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Record an event (in production, this would emit a signal)."""
        event = {
            "type": event_type,
            "data": {"object": data},
            "created": int(datetime.utcnow().timestamp()),
        }
        self._events.append(event)

    @property
    def events(self) -> List[Dict[str, Any]]:
        """Get recorded events."""
        return list(self._events)


def _generate_id() -> str:
    """Generate a short random ID."""
    import hashlib
    import time
    content = f"{time.time()}{id(object())}"
    return hashlib.sha256(content.encode()).hexdigest()[:14]
