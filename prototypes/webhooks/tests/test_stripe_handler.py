"""
Tests for the Stripe webhook handler.

Covers: signature verification, event parsing, signal generation,
and the full webhook → signal pipeline for all Stripe event types.
"""

import json
import hmac
import hashlib
import time
import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webhooks.handlers.stripe import StripeHandler
from webhooks.signal import Signal, SignalType


class TestStripeHandlerCanHandle:
    """Test StripeHandler.can_handle()."""

    def setup_method(self):
        self.handler = StripeHandler()

    def test_recognizes_stripe_signature_header(self):
        headers = {"Stripe-Signature": "t=123,v1=abc"}
        assert self.handler.can_handle(headers, {}) is True

    def test_recognizes_case_insensitive_header(self):
        headers = {"stripe-signature": "t=123,v1=abc"}
        assert self.handler.can_handle(headers, {}) is True

    def test_rejects_missing_signature(self):
        headers = {"Content-Type": "application/json"}
        assert self.handler.can_handle(headers, {}) is False

    def test_rejects_empty_headers(self):
        assert self.handler.can_handle({}, {}) is False

    def test_rejects_github_headers(self):
        headers = {"X-GitHub-Event": "push"}
        assert self.handler.can_handle(headers, {}) is False


class TestStripeHandlerVerify:
    """Test StripeHandler.verify() signature verification."""

    def setup_method(self):
        self.handler = StripeHandler()
        self.secret = "whsec_test_secret_key_12345"

    def _make_signature(self, payload: str, secret: str, timestamp: str = None) -> str:
        """Generate a valid Stripe signature."""
        if timestamp is None:
            timestamp = str(int(time.time()))
        signed_payload = f"{timestamp}.{payload}"
        sig = hmac.HMAC(
            secret.encode(),
            signed_payload.encode(),
            hashlib.sha256,
        ).hexdigest()
        return f"t={timestamp},v1={sig}"

    def test_valid_signature_passes(self):
        payload = '{"type": "payment_intent.succeeded"}'
        sig = self._make_signature(payload, self.secret)
        headers = {"Stripe-Signature": sig}
        assert self.handler.verify(headers, payload.encode(), self.secret) is True

    def test_invalid_signature_fails(self):
        payload = '{"type": "payment_intent.succeeded"}'
        headers = {"Stripe-Signature": "t=123,v1=invalid_signature_here"}
        assert self.handler.verify(headers, payload.encode(), self.secret) is False

    def test_no_secret_passes_without_verification(self):
        payload = b'{"type": "test"}'
        headers = {"Stripe-Signature": "t=123,v1=whatever"}
        assert self.handler.verify(headers, payload, None) is True

    def test_empty_secret_passes_without_verification(self):
        payload = b'{"type": "test"}'
        headers = {"Stripe-Signature": "t=123,v1=whatever"}
        assert self.handler.verify(headers, payload, "") is True

    def test_missing_signature_header_fails(self):
        payload = b'{"type": "test"}'
        headers = {}
        assert self.handler.verify(headers, payload, self.secret) is False

    def test_tampered_payload_fails(self):
        original = '{"amount": 1000}'
        sig = self._make_signature(original, self.secret)
        tampered = '{"amount": 9999}'
        headers = {"Stripe-Signature": sig}
        assert self.handler.verify(headers, tampered.encode(), self.secret) is False

    def test_wrong_secret_fails(self):
        payload = '{"type": "test"}'
        sig = self._make_signature(payload, self.secret)
        headers = {"Stripe-Signature": sig}
        assert self.handler.verify(headers, payload.encode(), "wrong_secret") is False


class TestStripeHandlerParse:
    """Test StripeHandler.parse() event parsing."""

    def setup_method(self):
        self.handler = StripeHandler()

    def test_payment_intent_succeeded(self):
        body = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_test123",
                    "amount": 10000,
                    "currency": "usd",
                    "customer": "cus_abc",
                    "status": "succeeded",
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.PAYMENT_RECEIVED
        assert signal.source == "stripe"
        assert signal.target == "FND"
        assert signal.data["amount"] == 100.0  # $100.00
        assert signal.data["currency"] == "USD"
        assert signal.data["customer"] == "cus_abc"
        assert signal.data["event"] == "payment_intent.succeeded"

    def test_payment_intent_failed(self):
        body = {
            "type": "payment_intent.payment_failed",
            "data": {
                "object": {
                    "id": "pi_fail",
                    "amount": 500,
                    "currency": "usd",
                    "customer": "cus_xyz",
                    "status": "requires_payment_method",
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.PAYMENT_FAILED
        assert signal.data["amount"] == 5.0
        assert signal.data["status"] == "requires_payment_method"

    def test_subscription_created(self):
        body = {
            "type": "customer.subscription.created",
            "data": {
                "object": {
                    "id": "sub_test",
                    "customer": "cus_123",
                    "status": "active",
                    "plan": {"id": "price_basic", "amount": 100},
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.SUBSCRIPTION_CREATED
        assert signal.data["customer"] == "cus_123"
        assert signal.data["plan"] == "price_basic"
        assert signal.data["amount"] == 1.0  # $1.00

    def test_subscription_deleted(self):
        body = {
            "type": "customer.subscription.deleted",
            "data": {
                "object": {
                    "id": "sub_cancel",
                    "customer": "cus_456",
                    "status": "canceled",
                    "plan": {"id": "price_pro", "amount": 500},
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.SUBSCRIPTION_CANCELLED
        assert signal.data["status"] == "canceled"

    def test_invoice_paid(self):
        body = {
            "type": "invoice.paid",
            "data": {
                "object": {
                    "id": "in_paid",
                    "customer": "cus_789",
                    "amount_paid": 100,
                    "status": "paid",
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.INVOICE_PAID
        assert signal.data["amount"] == 1.0
        assert signal.data["status"] == "paid"

    def test_invoice_payment_failed(self):
        body = {
            "type": "invoice.payment_failed",
            "data": {
                "object": {
                    "id": "in_fail",
                    "customer": "cus_fail",
                    "amount_paid": 0,
                    "status": "open",
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.PAYMENT_FAILED

    def test_charge_succeeded(self):
        body = {
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": "ch_ok",
                    "amount": 2500,
                    "currency": "eur",
                    "customer": "cus_eu",
                    "status": "succeeded",
                }
            }
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.PAYMENT_RECEIVED
        assert signal.data["amount"] == 25.0
        assert signal.data["currency"] == "EUR"

    def test_unknown_event_maps_to_custom(self):
        body = {
            "type": "some.unknown.event",
            "data": {"object": {"id": "unknown"}}
        }
        signal = self.handler.parse({}, body)
        assert signal.type == SignalType.CUSTOM
        assert signal.data["event"] == "some.unknown.event"

    def test_signal_has_correct_target_org(self):
        body = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_1", "amount": 0, "currency": "usd"}}
        }
        signal = self.handler.parse({}, body)
        assert signal.target == "FND"

    def test_signal_has_id_and_timestamp(self):
        body = {
            "type": "invoice.paid",
            "data": {"object": {"id": "in_1", "amount_paid": 0, "status": "paid"}}
        }
        signal = self.handler.parse({}, body)
        assert len(signal.id) == 12
        assert signal.timestamp != ""

    def test_signal_raw_contains_original_body(self):
        body = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_raw", "amount": 100, "currency": "usd"}}
        }
        signal = self.handler.parse({}, body)
        assert signal.raw == body

    def test_signal_format_string(self):
        body = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_fmt", "amount": 5000, "currency": "usd", "customer": "cus_1"}}
        }
        signal = self.handler.parse({}, body)
        formatted = signal.format()
        assert "STRIPE" in formatted
        assert "FND" in formatted
        assert "payment_received" in formatted


class TestStripeHandlerEventMap:
    """Test that all expected Stripe events are mapped."""

    def test_all_payment_events_mapped(self):
        handler = StripeHandler()
        payment_events = [
            "payment_intent.succeeded",
            "payment_intent.payment_failed",
            "charge.succeeded",
            "charge.failed",
        ]
        for event in payment_events:
            assert event in handler.EVENT_MAP

    def test_all_subscription_events_mapped(self):
        handler = StripeHandler()
        sub_events = [
            "customer.subscription.created",
            "customer.subscription.deleted",
            "customer.subscription.updated",
        ]
        for event in sub_events:
            assert event in handler.EVENT_MAP

    def test_all_invoice_events_mapped(self):
        handler = StripeHandler()
        invoice_events = [
            "invoice.paid",
            "invoice.payment_failed",
        ]
        for event in invoice_events:
            assert event in handler.EVENT_MAP

    def test_handler_name_is_stripe(self):
        handler = StripeHandler()
        assert handler.name == "stripe"

    def test_handler_target_is_fnd(self):
        handler = StripeHandler()
        assert handler.target_org == "FND"
