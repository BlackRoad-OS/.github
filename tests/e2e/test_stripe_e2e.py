"""
End-to-end tests for the full Stripe integration pipeline.

Tests the complete flow:
  Stripe webhook → WebhookReceiver → StripeHandler → Signal → routing → FND org

Also tests the stripe-billing service client and webhook handler.
"""

import json
import hmac
import hashlib
import time
import sys
import os
import pytest

# Add prototypes and templates to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "prototypes", "webhooks"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "templates", "stripe-billing"))

from webhooks.receiver import WebhookReceiver, process_webhook
from webhooks.signal import Signal, SignalType
from webhooks.handlers.stripe import StripeHandler

from stripe_billing.client import StripeClient, BillingMetrics
from stripe_billing.models.customer import Customer
from stripe_billing.models.subscription import Subscription
from stripe_billing.models.invoice import Invoice
from stripe_billing.models.price import Price, BLACKROAD_PRICES
from stripe_billing.webhooks.handler import StripeWebhookHandler, WebhookEvent


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

WEBHOOK_SECRET = "whsec_e2e_test_secret_key_blackroad"


def _sign_stripe_payload(payload_str: str, secret: str = WEBHOOK_SECRET) -> str:
    """Generate a valid Stripe-Signature header."""
    timestamp = str(int(time.time()))
    signed = f"{timestamp}.{payload_str}"
    sig = hmac.HMAC(secret.encode(), signed.encode(), hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={sig}"


def _make_stripe_event(event_type: str, obj: dict) -> dict:
    """Build a Stripe event object."""
    return {
        "id": f"evt_e2e_{event_type.replace('.', '_')}",
        "type": event_type,
        "data": {"object": obj},
        "created": int(time.time()),
    }


# ═══════════════════════════════════════════════════════════════════
# E2E: STRIPE WEBHOOK → SIGNAL PIPELINE
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.e2e
@pytest.mark.stripe
class TestStripeWebhookToSignalE2E:
    """Full pipeline: Stripe webhook → verified → parsed → Signal → routed to FND."""

    def test_payment_e2e_with_signature_verification(self):
        """Simulate a real Stripe payment webhook with signature verification."""
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})

        event = _make_stripe_event("payment_intent.succeeded", {
            "id": "pi_e2e_001",
            "amount": 10000,  # $100.00
            "currency": "usd",
            "customer": "cus_e2e_001",
            "status": "succeeded",
        })
        payload_str = json.dumps(event)
        sig = _sign_stripe_payload(payload_str)

        result = receiver.process(
            headers={"Stripe-Signature": sig},
            body=payload_str.encode(),
        )

        assert result.success is True
        assert result.verified is True
        assert result.handler == "stripe"
        assert result.signal.type == SignalType.PAYMENT_RECEIVED
        assert result.signal.source == "stripe"
        assert result.signal.target == "FND"
        assert result.signal.data["amount"] == 100.0
        assert result.signal.data["currency"] == "USD"
        assert result.signal.data["customer"] == "cus_e2e_001"

        # Verify the signal formats correctly for the mesh
        formatted = result.signal.format()
        assert "STRIPE" in formatted
        assert "FND" in formatted
        assert "payment_received" in formatted

    def test_subscription_lifecycle_e2e(self):
        """Test full subscription lifecycle: create → update → cancel."""
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})

        # 1. Subscription created
        create_event = _make_stripe_event("customer.subscription.created", {
            "id": "sub_e2e_lifecycle",
            "customer": "cus_e2e_lifecycle",
            "status": "active",
            "plan": {"id": "price_blackroad_basic", "amount": 100},
        })
        payload = json.dumps(create_event)
        result = receiver.process(
            {"Stripe-Signature": _sign_stripe_payload(payload)},
            payload.encode(),
        )
        assert result.success is True
        assert result.signal.type == SignalType.SUBSCRIPTION_CREATED
        assert result.signal.data["plan"] == "price_blackroad_basic"

        # 2. Subscription updated
        update_event = _make_stripe_event("customer.subscription.updated", {
            "id": "sub_e2e_lifecycle",
            "customer": "cus_e2e_lifecycle",
            "status": "active",
            "plan": {"id": "price_blackroad_pro", "amount": 500},
        })
        payload = json.dumps(update_event)
        result = receiver.process(
            {"Stripe-Signature": _sign_stripe_payload(payload)},
            payload.encode(),
        )
        assert result.success is True
        assert result.signal.type == SignalType.RECORD_UPDATED

        # 3. Subscription cancelled
        cancel_event = _make_stripe_event("customer.subscription.deleted", {
            "id": "sub_e2e_lifecycle",
            "customer": "cus_e2e_lifecycle",
            "status": "canceled",
            "plan": {"id": "price_blackroad_pro", "amount": 500},
        })
        payload = json.dumps(cancel_event)
        result = receiver.process(
            {"Stripe-Signature": _sign_stripe_payload(payload)},
            payload.encode(),
        )
        assert result.success is True
        assert result.signal.type == SignalType.SUBSCRIPTION_CANCELLED

        # Verify all 3 events tracked
        assert receiver.stats["total"] == 3
        assert receiver.stats["success_rate"] == 1.0

    def test_failed_payment_triggers_alert_signal(self):
        """Payment failure should produce a PAYMENT_FAILED signal routed to FND."""
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})

        event = _make_stripe_event("payment_intent.payment_failed", {
            "id": "pi_e2e_fail",
            "amount": 500,
            "currency": "usd",
            "customer": "cus_e2e_fail",
            "status": "requires_payment_method",
        })
        payload = json.dumps(event)
        result = receiver.process(
            {"Stripe-Signature": _sign_stripe_payload(payload)},
            payload.encode(),
        )

        assert result.success is True
        assert result.signal.type == SignalType.PAYMENT_FAILED
        assert result.signal.target == "FND"
        assert result.signal.data["status"] == "requires_payment_method"

    def test_tampered_webhook_rejected(self):
        """Webhook with tampered payload should be rejected."""
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})

        original = json.dumps(_make_stripe_event("payment_intent.succeeded", {
            "id": "pi_real", "amount": 100, "currency": "usd",
        }))
        sig = _sign_stripe_payload(original)

        # Tamper with the payload
        tampered = json.dumps(_make_stripe_event("payment_intent.succeeded", {
            "id": "pi_real", "amount": 999999, "currency": "usd",
        }))

        result = receiver.process(
            {"Stripe-Signature": sig},
            tampered.encode(),
        )
        assert result.success is False
        assert result.verified is False

    def test_signal_serialization_round_trip(self):
        """Signal from Stripe webhook should survive serialization round-trip."""
        receiver = WebhookReceiver()
        event = _make_stripe_event("invoice.paid", {
            "id": "in_rt", "customer": "cus_rt", "amount_paid": 100, "status": "paid",
        })
        result = receiver.process(
            {"Stripe-Signature": "t=0,v1=test"},
            json.dumps(event).encode(),
        )

        # Serialize and deserialize
        signal_dict = result.signal.to_dict()
        restored = Signal.from_dict(signal_dict)

        assert restored.type == result.signal.type
        assert restored.source == result.signal.source
        assert restored.target == result.signal.target
        assert restored.data == result.signal.data
        assert restored.id == result.signal.id


# ═══════════════════════════════════════════════════════════════════
# E2E: STRIPE BILLING CLIENT
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.e2e
@pytest.mark.stripe
class TestStripeBillingClientE2E:
    """Test the full billing client workflow."""

    def test_customer_lifecycle(self):
        """Create customer → create subscription → pay invoice → check metrics."""
        client = StripeClient(test_mode=True)

        # Create customer
        customer = client.create_customer(
            email="test@blackroad.ai",
            name="Test User",
            metadata={"blackroad_id": "usr_001"},
        )
        assert customer.id.startswith("cus_test_")
        assert customer.email == "test@blackroad.ai"
        assert customer.metadata["blackroad_id"] == "usr_001"

        # Verify customer retrieval
        retrieved = client.get_customer(customer.id)
        assert retrieved is not None
        assert retrieved.email == customer.email

        # Create subscription
        sub = client.create_subscription(customer.id, "price_blackroad_basic")
        assert sub is not None
        assert sub.is_active
        assert sub.customer_id == customer.id
        assert sub.price_id == "price_blackroad_basic"

        # Create and pay invoice
        invoice = client.create_invoice(customer.id, 100, sub.id)
        assert invoice is not None
        assert invoice.status == "open"

        paid = client.pay_invoice(invoice.id)
        assert paid is not None
        assert paid.is_paid
        assert paid.amount_paid == 100

        # Check metrics
        metrics = client.get_metrics()
        assert metrics.total_customers == 1
        assert metrics.active_subscriptions == 1
        assert metrics.total_revenue_cents == 100

        # Check events were emitted
        events = client.events
        event_types = [e["type"] for e in events]
        assert "customer.created" in event_types
        assert "customer.subscription.created" in event_types
        assert "invoice.paid" in event_types

    def test_subscription_cancellation(self):
        """Test subscription cancel at period end vs immediate."""
        client = StripeClient(test_mode=True)
        customer = client.create_customer(email="cancel@test.com")
        sub = client.create_subscription(customer.id, "price_blackroad_pro")

        # Cancel at period end
        updated = client.cancel_subscription(sub.id, at_period_end=True)
        assert updated.cancel_at_period_end is True
        assert updated.is_active  # Still active until period end

        # Immediate cancel
        sub2 = client.create_subscription(customer.id, "price_blackroad_basic")
        canceled = client.cancel_subscription(sub2.id, at_period_end=False)
        assert canceled.status == "canceled"
        assert not canceled.is_active

    def test_multiple_customers_metrics(self):
        """Test metrics with multiple customers and subscriptions."""
        client = StripeClient(test_mode=True)

        for i in range(5):
            customer = client.create_customer(email=f"user{i}@blackroad.ai")
            client.create_subscription(customer.id, "price_blackroad_basic")
            inv = client.create_invoice(customer.id, 100)
            client.pay_invoice(inv.id)

        metrics = client.get_metrics()
        assert metrics.total_customers == 5
        assert metrics.active_subscriptions == 5
        assert metrics.total_revenue_cents == 500
        assert metrics.total_revenue_dollars == 5.0

    def test_nonexistent_customer_returns_none(self):
        client = StripeClient(test_mode=True)
        assert client.get_customer("cus_nonexistent") is None
        assert client.create_subscription("cus_nonexistent", "price_x") is None
        assert client.create_invoice("cus_nonexistent", 100) is None

    def test_nonexistent_subscription_returns_none(self):
        client = StripeClient(test_mode=True)
        assert client.get_subscription("sub_nonexistent") is None
        assert client.cancel_subscription("sub_nonexistent") is None

    def test_nonexistent_invoice_returns_none(self):
        client = StripeClient(test_mode=True)
        assert client.get_invoice("in_nonexistent") is None
        assert client.pay_invoice("in_nonexistent") is None


# ═══════════════════════════════════════════════════════════════════
# E2E: STRIPE BILLING WEBHOOK HANDLER
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.e2e
@pytest.mark.stripe
class TestStripeBillingWebhookHandlerE2E:
    """Test the billing service webhook handler processing events."""

    def test_payment_succeeded_event(self):
        handler = StripeWebhookHandler()
        event = _make_stripe_event("payment_intent.succeeded", {
            "id": "pi_bh_001",
            "amount": 10000,
            "customer": "cus_bh_001",
        })
        result = handler.process_event(event)
        assert result.success is True
        assert "payment_received" in result.signal
        assert "$100.00" in result.signal
        assert "cus_bh_001" in result.signal

    def test_payment_failed_event(self):
        handler = StripeWebhookHandler()
        event = _make_stripe_event("payment_intent.payment_failed", {
            "id": "pi_bh_fail",
            "amount": 500,
            "customer": "cus_bh_fail",
        })
        result = handler.process_event(event)
        assert result.success is True
        assert "payment_failed" in result.signal

    def test_customer_created_event(self):
        handler = StripeWebhookHandler()
        event = _make_stripe_event("customer.created", {
            "id": "cus_bh_new",
            "email": "new@blackroad.ai",
            "name": "New Customer",
            "created": int(time.time()),
        })
        result = handler.process_event(event)
        assert result.success is True
        assert "customer_created" in result.signal
        assert "cus_bh_new" in result.signal
        # Customer should be synced to client store
        assert handler.client.get_customer("cus_bh_new") is not None

    def test_subscription_created_syncs_to_store(self):
        handler = StripeWebhookHandler()
        event = _make_stripe_event("customer.subscription.created", {
            "id": "sub_bh_sync",
            "customer": "cus_sync",
            "status": "active",
            "plan": {"id": "price_basic"},
            "items": {"data": [{"price": {"id": "price_basic"}}]},
        })
        result = handler.process_event(event)
        assert result.success is True
        assert "subscription_created" in result.signal
        assert handler.client.get_subscription("sub_bh_sync") is not None

    def test_subscription_deleted_marks_canceled(self):
        handler = StripeWebhookHandler()
        # First create
        handler.process_event(_make_stripe_event("customer.subscription.created", {
            "id": "sub_bh_cancel",
            "customer": "cus_cancel",
            "status": "active",
            "plan": {"id": "price_basic"},
            "items": {"data": [{"price": {"id": "price_basic"}}]},
        }))
        # Then delete
        result = handler.process_event(_make_stripe_event("customer.subscription.deleted", {
            "id": "sub_bh_cancel",
            "customer": "cus_cancel",
            "status": "canceled",
        }))
        assert result.success is True
        assert "subscription_cancelled" in result.signal
        sub = handler.client.get_subscription("sub_bh_cancel")
        assert sub is not None
        assert sub.status == "canceled"

    def test_invoice_paid_event(self):
        handler = StripeWebhookHandler()
        event = _make_stripe_event("invoice.paid", {
            "id": "in_bh_paid",
            "customer": "cus_paid",
            "amount_paid": 100,
        })
        result = handler.process_event(event)
        assert result.success is True
        assert "invoice_paid" in result.signal
        assert "$1.00" in result.signal

    def test_unknown_event_still_succeeds(self):
        handler = StripeWebhookHandler()
        event = _make_stripe_event("some.random.event", {"id": "obj_random"})
        result = handler.process_event(event)
        assert result.success is True
        assert "stripe_event" in result.signal

    def test_handler_stats(self):
        handler = StripeWebhookHandler()
        handler.process_event(_make_stripe_event("payment_intent.succeeded", {
            "id": "pi_s1", "amount": 100, "customer": "c",
        }))
        handler.process_event(_make_stripe_event("invoice.paid", {
            "id": "in_s1", "customer": "c", "amount_paid": 100,
        }))
        stats = handler.stats
        assert stats["total"] == 2
        assert stats["success_rate"] == 1.0
        assert "payment_intent.succeeded" in stats["by_type"]
        assert "invoice.paid" in stats["by_type"]


# ═══════════════════════════════════════════════════════════════════
# E2E: WEBHOOK SIGNATURE VERIFICATION
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.e2e
@pytest.mark.stripe
class TestStripeSignatureVerificationE2E:
    """Test Stripe webhook signature verification end-to-end."""

    def test_client_verify_valid_signature(self):
        client = StripeClient(webhook_secret=WEBHOOK_SECRET, test_mode=True)
        payload = b'{"type":"test.event","data":{"object":{"id":"obj_1"}}}'
        sig = _sign_stripe_payload(payload.decode())
        assert client.verify_webhook_signature(payload, sig) is True

    def test_client_verify_invalid_signature(self):
        client = StripeClient(webhook_secret=WEBHOOK_SECRET, test_mode=True)
        payload = b'{"type":"test"}'
        assert client.verify_webhook_signature(payload, "t=0,v1=bad") is False

    def test_client_construct_event_valid(self):
        client = StripeClient(webhook_secret=WEBHOOK_SECRET, test_mode=True)
        event_data = {"type": "payment_intent.succeeded", "data": {"object": {"id": "pi_c"}}}
        payload = json.dumps(event_data).encode()
        sig = _sign_stripe_payload(payload.decode())

        event = client.construct_event(payload, sig)
        assert event is not None
        assert event["type"] == "payment_intent.succeeded"

    def test_client_construct_event_invalid(self):
        client = StripeClient(webhook_secret=WEBHOOK_SECRET, test_mode=True)
        payload = b'{"type":"test"}'
        event = client.construct_event(payload, "t=0,v1=invalid")
        assert event is None

    def test_handler_verify_matches_client_verify(self):
        """Both the webhook handler and billing client should agree on signatures."""
        handler = StripeHandler()
        client = StripeClient(webhook_secret=WEBHOOK_SECRET, test_mode=True)

        payload = b'{"type":"charge.succeeded","data":{"object":{"id":"ch_v"}}}'
        sig_header = _sign_stripe_payload(payload.decode())

        handler_result = handler.verify(
            {"Stripe-Signature": sig_header},
            payload,
            WEBHOOK_SECRET,
        )
        client_result = client.verify_webhook_signature(payload, sig_header)

        assert handler_result == client_result == True


# ═══════════════════════════════════════════════════════════════════
# E2E: FULL PIPELINE (WEBHOOK → RECEIVER → BILLING SERVICE)
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.e2e
@pytest.mark.stripe
class TestFullStripeIntegrationE2E:
    """
    Test the complete integration pipeline:
    Stripe webhook → WebhookReceiver → Signal → StripeWebhookHandler → billing actions
    """

    def test_full_payment_pipeline(self):
        """
        Simulate: Stripe sends payment_intent.succeeded webhook
        → WebhookReceiver verifies and creates Signal
        → StripeWebhookHandler processes event
        → Signal routed to FND org
        """
        # Step 1: Receive webhook
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})
        event = _make_stripe_event("payment_intent.succeeded", {
            "id": "pi_full_001",
            "amount": 100,  # $1.00
            "currency": "usd",
            "customer": "cus_full_001",
            "status": "succeeded",
        })
        payload = json.dumps(event)
        sig = _sign_stripe_payload(payload)

        webhook_result = receiver.process(
            {"Stripe-Signature": sig},
            payload.encode(),
        )

        # Verify webhook processing
        assert webhook_result.success is True
        assert webhook_result.verified is True
        assert webhook_result.signal.target == "FND"  # Routed to Foundation org

        # Step 2: Billing service processes the event
        billing_handler = StripeWebhookHandler()
        billing_result = billing_handler.process_event(event)

        assert billing_result.success is True
        assert "payment_received" in billing_result.signal
        assert "cus_full_001" in billing_result.signal

        # Step 3: Verify the signal can be serialized for mesh routing
        signal_dict = webhook_result.signal.to_dict()
        assert signal_dict["target"] == "FND"
        assert signal_dict["source"] == "stripe"
        assert signal_dict["type"] == "payment_received"

    def test_full_subscription_onboarding_pipeline(self):
        """
        Simulate full customer onboarding:
        1. customer.created webhook
        2. customer.subscription.created webhook
        3. invoice.paid webhook
        4. Verify billing metrics
        """
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})
        billing_handler = StripeWebhookHandler()
        signals_emitted = []

        # 1. Customer created
        events = [
            _make_stripe_event("customer.created", {
                "id": "cus_onboard",
                "email": "onboard@blackroad.ai",
                "name": "Onboarding Test",
                "created": int(time.time()),
            }),
            _make_stripe_event("customer.subscription.created", {
                "id": "sub_onboard",
                "customer": "cus_onboard",
                "status": "active",
                "plan": {"id": "price_blackroad_basic", "amount": 100},
                "items": {"data": [{"price": {"id": "price_blackroad_basic"}}]},
            }),
            _make_stripe_event("invoice.paid", {
                "id": "in_onboard",
                "customer": "cus_onboard",
                "amount_paid": 100,
                "status": "paid",
            }),
        ]

        for event in events:
            payload = json.dumps(event)
            sig = _sign_stripe_payload(payload)

            # Process through webhook receiver
            webhook_result = receiver.process(
                {"Stripe-Signature": sig},
                payload.encode(),
            )
            assert webhook_result.success is True
            assert webhook_result.verified is True
            signals_emitted.append(webhook_result.signal)

            # Process through billing handler
            billing_result = billing_handler.process_event(event)
            assert billing_result.success is True

        # Verify all signals routed to FND
        for signal in signals_emitted:
            assert signal.target == "FND"

        # Verify signal types in order
        assert signals_emitted[0].type == SignalType.CUSTOM  # customer.created not in handler EVENT_MAP
        assert signals_emitted[1].type == SignalType.SUBSCRIPTION_CREATED
        assert signals_emitted[2].type == SignalType.INVOICE_PAID

        # Verify billing state
        assert billing_handler.client.get_customer("cus_onboard") is not None
        assert billing_handler.client.get_subscription("sub_onboard") is not None

        # Verify receiver stats
        stats = receiver.stats
        assert stats["total"] == 3
        assert stats["success_rate"] == 1.0

    def test_rejected_webhook_never_reaches_billing(self):
        """Tampered webhook should be rejected before reaching billing service."""
        receiver = WebhookReceiver(secrets={"stripe": WEBHOOK_SECRET})

        event = _make_stripe_event("payment_intent.succeeded", {
            "id": "pi_reject",
            "amount": 999999,
            "currency": "usd",
        })
        payload = json.dumps(event)
        # Sign with wrong key
        bad_sig = _sign_stripe_payload(payload, secret="wrong_secret")

        result = receiver.process(
            {"Stripe-Signature": bad_sig},
            payload.encode(),
        )

        # Should fail verification — event never processed
        assert result.success is False
        assert result.signal is None


# ═══════════════════════════════════════════════════════════════════
# E2E: DATA MODEL TESTS
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.e2e
@pytest.mark.stripe
class TestStripeDataModelsE2E:
    """Test Stripe billing data models."""

    def test_customer_round_trip(self):
        customer = Customer(
            id="cus_rt",
            email="rt@test.com",
            name="Round Trip",
            metadata={"tier": "pro"},
        )
        d = customer.to_dict()
        restored = Customer.from_dict(d)
        assert restored.id == customer.id
        assert restored.email == customer.email
        assert restored.name == customer.name
        assert restored.metadata == customer.metadata

    def test_subscription_active_states(self):
        active = Subscription(id="s1", customer_id="c1", status="active")
        trialing = Subscription(id="s2", customer_id="c1", status="trialing")
        canceled = Subscription(id="s3", customer_id="c1", status="canceled")
        past_due = Subscription(id="s4", customer_id="c1", status="past_due")

        assert active.is_active is True
        assert trialing.is_active is True
        assert canceled.is_active is False
        assert past_due.is_active is False

    def test_invoice_amounts(self):
        invoice = Invoice(
            id="in_amt",
            customer_id="c1",
            amount_due=2500,
            amount_paid=2500,
            status="paid",
        )
        assert invoice.amount_due_dollars == 25.0
        assert invoice.amount_paid_dollars == 25.0
        assert invoice.is_paid is True

    def test_price_model(self):
        price = Price(
            id="price_1",
            product_id="prod_1",
            amount=100,
            currency="usd",
            interval="month",
        )
        assert price.amount_dollars == 1.0
        d = price.to_dict()
        assert d["amount"] == 100
        assert d["amount_dollars"] == 1.0

    def test_enterprise_price_null_amount(self):
        price = Price(
            id="price_ent",
            product_id="prod_ent",
            amount=None,
        )
        assert price.amount_dollars is None

    def test_blackroad_prices_defined(self):
        assert "blackroad_basic" in BLACKROAD_PRICES
        assert "blackroad_pro" in BLACKROAD_PRICES
        assert "blackroad_enterprise" in BLACKROAD_PRICES
        assert BLACKROAD_PRICES["blackroad_basic"]["amount"] == 100
        assert BLACKROAD_PRICES["blackroad_pro"]["amount"] == 500
        assert BLACKROAD_PRICES["blackroad_enterprise"]["amount"] is None

    def test_billing_metrics(self):
        metrics = BillingMetrics(
            total_customers=10,
            active_subscriptions=8,
            mrr_cents=800,
            total_revenue_cents=5000,
        )
        assert metrics.mrr_dollars == 8.0
        assert metrics.total_revenue_dollars == 50.0
        d = metrics.to_dict()
        assert d["mrr_dollars"] == 8.0
