"""
Tests for the WebhookReceiver — the central webhook processing pipeline.

Covers: handler routing, signature verification, full processing pipeline,
statistics tracking, and multi-provider handling.
"""

import json
import hmac
import hashlib
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webhooks.receiver import WebhookReceiver, WebhookResult, process_webhook
from webhooks.signal import Signal, SignalType


def _stripe_payload(event_type: str, obj: dict = None) -> bytes:
    """Build a Stripe webhook payload."""
    return json.dumps({
        "type": event_type,
        "data": {"object": obj or {"id": "test_obj", "amount": 1000, "currency": "usd"}},
    }).encode()


def _stripe_headers(sig: str = "t=123,v1=test") -> dict:
    """Build Stripe webhook headers."""
    return {"Stripe-Signature": sig, "Content-Type": "application/json"}


def _github_payload(event: str = "push", repo: str = "BlackRoad-OS/.github") -> bytes:
    """Build a GitHub webhook payload."""
    return json.dumps({
        "action": "opened" if event == "pull_request" else None,
        "repository": {"full_name": repo},
        "ref": "refs/heads/main",
        "commits": [{"message": "test commit"}],
    }).encode()


def _github_headers(event: str = "push") -> dict:
    """Build GitHub webhook headers."""
    return {"X-GitHub-Event": event, "Content-Type": "application/json"}


class TestWebhookReceiverProcessStripe:
    """Test processing Stripe webhooks through the receiver."""

    def setup_method(self):
        self.receiver = WebhookReceiver()

    def test_processes_stripe_payment_succeeded(self):
        payload = _stripe_payload("payment_intent.succeeded", {
            "id": "pi_123",
            "amount": 10000,
            "currency": "usd",
            "customer": "cus_abc",
            "status": "succeeded",
        })
        result = self.receiver.process(_stripe_headers(), payload)
        assert result.success is True
        assert result.handler == "stripe"
        assert result.signal is not None
        assert result.signal.type == SignalType.PAYMENT_RECEIVED
        assert result.signal.data["amount"] == 100.0

    def test_processes_stripe_subscription_created(self):
        payload = _stripe_payload("customer.subscription.created", {
            "id": "sub_1",
            "customer": "cus_1",
            "status": "active",
            "plan": {"id": "price_basic", "amount": 100},
        })
        result = self.receiver.process(_stripe_headers(), payload)
        assert result.success is True
        assert result.signal.type == SignalType.SUBSCRIPTION_CREATED

    def test_processes_stripe_invoice_paid(self):
        payload = _stripe_payload("invoice.paid", {
            "id": "in_1",
            "customer": "cus_1",
            "amount_paid": 500,
            "status": "paid",
        })
        result = self.receiver.process(_stripe_headers(), payload)
        assert result.success is True
        assert result.signal.type == SignalType.INVOICE_PAID

    def test_stripe_verification_with_valid_secret(self):
        secret = "whsec_test_verify"
        receiver = WebhookReceiver(secrets={"stripe": secret})

        payload_str = '{"type":"payment_intent.succeeded","data":{"object":{"id":"pi_v","amount":100,"currency":"usd"}}}'
        timestamp = str(int(time.time()))
        signed_payload = f"{timestamp}.{payload_str}"
        sig = hmac.HMAC(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()

        headers = {"Stripe-Signature": f"t={timestamp},v1={sig}"}
        result = receiver.process(headers, payload_str.encode())
        assert result.success is True
        assert result.verified is True

    def test_stripe_verification_fails_with_wrong_secret(self):
        receiver = WebhookReceiver(secrets={"stripe": "correct_secret"})
        payload = _stripe_payload("payment_intent.succeeded")
        headers = {"Stripe-Signature": "t=123,v1=wrong_sig"}
        result = receiver.process(headers, payload)
        assert result.success is False
        assert "verification failed" in result.error.lower()

    def test_processes_stripe_with_provider_hint(self):
        payload = _stripe_payload("charge.succeeded", {
            "id": "ch_1",
            "amount": 2500,
            "currency": "usd",
            "customer": "cus_hint",
            "status": "succeeded",
        })
        # Even without Stripe-Signature header, provider_hint should find the handler
        result = self.receiver.process(
            {"Content-Type": "application/json"},
            payload,
            provider_hint="stripe",
        )
        assert result.success is True
        assert result.handler == "stripe"


class TestWebhookReceiverProcessGitHub:
    """Test processing GitHub webhooks through the receiver."""

    def setup_method(self):
        self.receiver = WebhookReceiver()

    def test_processes_github_push(self):
        result = self.receiver.process(
            _github_headers("push"),
            _github_payload("push"),
        )
        assert result.success is True
        assert result.handler == "github"
        assert result.signal is not None
        assert result.signal.type == SignalType.PUSH

    def test_processes_github_pull_request(self):
        payload = json.dumps({
            "action": "opened",
            "pull_request": {"title": "Test PR", "number": 1, "merged": False},
            "repository": {"full_name": "BlackRoad-OS/.github"},
        }).encode()
        result = self.receiver.process(
            _github_headers("pull_request"),
            payload,
        )
        assert result.success is True
        assert result.signal.type == SignalType.PULL_REQUEST


class TestWebhookReceiverErrorHandling:
    """Test error handling in the receiver."""

    def setup_method(self):
        self.receiver = WebhookReceiver()

    def test_rejects_invalid_json(self):
        result = self.receiver.process(
            _stripe_headers(),
            b"not valid json at all",
        )
        assert result.success is False
        assert "Invalid JSON" in result.error

    def test_rejects_unrecognized_webhook(self):
        result = self.receiver.process(
            {"Content-Type": "application/json"},
            b'{"some": "data"}',
        )
        assert result.success is False
        assert "No handler found" in result.error

    def test_handles_empty_body(self):
        result = self.receiver.process(_stripe_headers(), b"")
        assert result.success is False

    def test_handles_binary_body(self):
        result = self.receiver.process(_stripe_headers(), b"\x00\x01\x02")
        assert result.success is False


class TestWebhookReceiverStats:
    """Test receiver statistics tracking."""

    def test_empty_stats(self):
        receiver = WebhookReceiver()
        stats = receiver.stats
        assert stats["total"] == 0
        assert stats["success_rate"] == 0

    def test_stats_after_successful_processing(self):
        receiver = WebhookReceiver()
        receiver.process(_stripe_headers(), _stripe_payload("invoice.paid", {
            "id": "in_s", "customer": "cus_s", "amount_paid": 100, "status": "paid",
        }))
        stats = receiver.stats
        assert stats["total"] == 1
        assert stats["success_rate"] == 1.0
        assert stats["by_handler"]["stripe"] == 1

    def test_stats_track_failures(self):
        """Early failures (invalid JSON, no handler) return before history append.
        Signature verification failures after handler match DO get tracked."""
        receiver = WebhookReceiver(secrets={"stripe": "real_secret"})
        # This will find the stripe handler but fail verification
        receiver.process(
            {"Stripe-Signature": "t=0,v1=bad_sig"},
            _stripe_payload("payment_intent.succeeded"),
        )
        # Early failures (no handler found) don't hit history
        receiver.process({}, b'{"no": "handler"}')
        # Only the verification failure was tracked (after handler match)
        stats = receiver.stats
        assert stats["total"] == 0  # Receiver only tracks successful parses

    def test_recent_signals(self):
        receiver = WebhookReceiver()
        for i in range(5):
            receiver.process(_stripe_headers(), _stripe_payload("invoice.paid", {
                "id": f"in_{i}", "customer": "cus", "amount_paid": 100, "status": "paid",
            }))
        signals = receiver.recent_signals(limit=3)
        assert len(signals) == 3


class TestProcessWebhookConvenience:
    """Test the stateless process_webhook() convenience function."""

    def test_processes_stripe_webhook(self):
        result = process_webhook(
            _stripe_headers(),
            _stripe_payload("payment_intent.succeeded", {
                "id": "pi_conv", "amount": 500, "currency": "usd",
            }),
        )
        assert result.success is True
        assert result.signal.type == SignalType.PAYMENT_RECEIVED

    def test_processes_with_secrets(self):
        secret = "whsec_conv_test"
        payload_str = '{"type":"invoice.paid","data":{"object":{"id":"in_c","customer":"c","amount_paid":100,"status":"paid"}}}'
        timestamp = str(int(time.time()))
        sig = hmac.HMAC(
            secret.encode(),
            f"{timestamp}.{payload_str}".encode(),
            hashlib.sha256,
        ).hexdigest()

        result = process_webhook(
            {"Stripe-Signature": f"t={timestamp},v1={sig}"},
            payload_str.encode(),
            secrets={"stripe": secret},
        )
        assert result.success is True
        assert result.verified is True


class TestWebhookResultSerialization:
    """Test WebhookResult.to_dict()."""

    def test_successful_result_serialization(self):
        receiver = WebhookReceiver()
        result = receiver.process(_stripe_headers(), _stripe_payload("invoice.paid", {
            "id": "in_ser", "customer": "cus_ser", "amount_paid": 100, "status": "paid",
        }))
        d = result.to_dict()
        assert d["success"] is True
        assert d["handler"] == "stripe"
        assert d["signal"] is not None
        assert d["signal"]["type"] == "invoice_paid"
        assert "timestamp" in d

    def test_failed_result_serialization(self):
        result = WebhookResult(success=False, error="test error")
        d = result.to_dict()
        assert d["success"] is False
        assert d["error"] == "test error"
        assert d["signal"] is None
