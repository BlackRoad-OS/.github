"""
Tests for WebhookReceiver.

Verifies that the receiver correctly identifies handlers, verifies
signatures, parses events, and emits signals.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from webhooks.receiver import WebhookReceiver, WebhookResult
from webhooks.signal import Signal, SignalType


def _body(payload: dict) -> bytes:
    """Encode a dict as JSON bytes."""
    return json.dumps(payload).encode()


class TestWebhookResultSerialization:
    """Verify WebhookResult.to_dict()."""

    def test_success_result_dict(self):
        signal = Signal(type=SignalType.PUSH, source="github", target="OS")
        result = WebhookResult(
            success=True, signal=signal, handler="github", verified=True,
            processing_time_ms=5
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["handler"] == "github"
        assert d["verified"] is True
        assert d["signal"] is not None
        assert d["processing_time_ms"] == 5

    def test_failure_result_dict(self):
        result = WebhookResult(success=False, error="bad json")
        d = result.to_dict()
        assert d["success"] is False
        assert d["signal"] is None
        assert d["error"] == "bad json"

    def test_timestamp_auto_set(self):
        result = WebhookResult(success=True)
        assert result.timestamp


class TestWebhookReceiverInvalidInput:
    """Verify receiver behavior on bad inputs."""

    def setup_method(self):
        self.receiver = WebhookReceiver()

    def test_invalid_json_returns_error(self):
        result = self.receiver.process(headers={}, body=b"not json")
        assert not result.success
        assert "Invalid JSON" in result.error

    def test_no_handler_returns_error(self):
        body = _body({"unknown_field": "value"})
        result = self.receiver.process(headers={}, body=body)
        assert not result.success
        assert "No handler" in result.error


class TestWebhookReceiverGitHub:
    """Verify GitHub webhook processing."""

    def setup_method(self):
        self.receiver = WebhookReceiver()

    def test_github_push_event(self):
        headers = {"X-GitHub-Event": "push"}
        payload = {
            "ref": "refs/heads/main",
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "pusher": {"name": "alexa"},
            "commits": [],
        }
        result = self.receiver.process(headers=headers, body=_body(payload))
        assert result.success
        assert result.handler == "github"
        assert result.signal is not None
        assert result.signal.type == SignalType.PUSH

    def test_github_pull_request_event(self):
        headers = {"X-GitHub-Event": "pull_request"}
        payload = {
            "action": "opened",
            "pull_request": {
                "number": 42,
                "title": "Test PR",
                "user": {"login": "alexa"},
                "head": {"sha": "abc123"},
            },
            "repository": {"full_name": "BlackRoad-OS/.github"},
        }
        result = self.receiver.process(headers=headers, body=_body(payload))
        assert result.success
        assert result.signal.type == SignalType.PULL_REQUEST

    def test_github_workflow_run_event(self):
        headers = {"X-GitHub-Event": "workflow_run"}
        payload = {
            "action": "completed",
            "workflow_run": {
                "id": 123,
                "name": "CI",
                "conclusion": "success",
                "head_sha": "abc123",
            },
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "sender": {"login": "github-actions[bot]"},
        }
        result = self.receiver.process(headers=headers, body=_body(payload))
        assert result.success
        assert result.signal.type == SignalType.WORKFLOW_RUN

    def test_github_provider_hint(self):
        headers = {"X-GitHub-Event": "push"}
        payload = {
            "ref": "refs/heads/main",
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "pusher": {"name": "alexa"},
            "commits": [],
        }
        result = self.receiver.process(
            headers=headers, body=_body(payload), provider_hint="github"
        )
        assert result.success


class TestWebhookReceiverStripe:
    """Verify Stripe webhook processing."""

    def setup_method(self):
        self.receiver = WebhookReceiver()

    def test_stripe_payment_intent_succeeded(self):
        headers = {"Stripe-Signature": "t=1234,v1=abc"}
        payload = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_123",
                    "amount": 10000,
                    "currency": "usd",
                    "customer": "cus_123",
                }
            },
        }
        result = self.receiver.process(headers=headers, body=_body(payload))
        assert result.success
        assert result.signal.type == SignalType.PAYMENT_RECEIVED


class TestWebhookReceiverStats:
    """Verify receiver statistics."""

    def test_stats_empty(self):
        receiver = WebhookReceiver()
        stats = receiver.stats
        assert stats["total"] == 0

    def test_stats_after_processing(self):
        receiver = WebhookReceiver()
        headers = {"X-GitHub-Event": "push"}
        payload = {
            "ref": "refs/heads/main",
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "pusher": {"name": "alexa"},
            "commits": [],
        }
        receiver.process(headers=headers, body=_body(payload))
        stats = receiver.stats
        assert stats["total"] == 1
        assert stats["success_rate"] == 1.0

    def test_history_is_appended(self):
        receiver = WebhookReceiver()
        headers = {"X-GitHub-Event": "push"}
        payload = {
            "ref": "refs/heads/main",
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "pusher": {"name": "alexa"},
            "commits": [],
        }
        receiver.process(headers=headers, body=_body(payload))
        assert len(receiver._history) == 1
