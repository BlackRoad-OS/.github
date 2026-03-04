"""
Tests for the Signal model.

Covers: creation, serialization, round-trip, formatting.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webhooks.signal import Signal, SignalType


class TestSignalCreation:
    """Test Signal construction."""

    def test_creates_with_required_fields(self):
        signal = Signal(
            type=SignalType.PAYMENT_RECEIVED,
            source="stripe",
            target="FND",
        )
        assert signal.type == SignalType.PAYMENT_RECEIVED
        assert signal.source == "stripe"
        assert signal.target == "FND"

    def test_generates_id_automatically(self):
        signal = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert len(signal.id) == 12

    def test_generates_timestamp_automatically(self):
        signal = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert signal.timestamp != ""
        assert "T" in signal.timestamp  # ISO format

    def test_uses_provided_id(self):
        signal = Signal(type=SignalType.PUSH, source="github", target="OS", id="custom_id")
        assert signal.id == "custom_id"

    def test_uses_provided_timestamp(self):
        signal = Signal(type=SignalType.PUSH, source="github", target="OS", timestamp="2025-01-01T00:00:00")
        assert signal.timestamp == "2025-01-01T00:00:00"

    def test_default_data_is_empty_dict(self):
        signal = Signal(type=SignalType.PING, source="test", target="OS")
        assert signal.data == {}

    def test_raw_defaults_to_none(self):
        signal = Signal(type=SignalType.PING, source="test", target="OS")
        assert signal.raw is None


class TestSignalSerialization:
    """Test Signal to_dict() and from_dict()."""

    def test_to_dict_contains_all_fields(self):
        signal = Signal(
            type=SignalType.PAYMENT_RECEIVED,
            source="stripe",
            target="FND",
            data={"amount": 100.0, "customer": "cus_1"},
        )
        d = signal.to_dict()
        assert d["type"] == "payment_received"
        assert d["source"] == "stripe"
        assert d["target"] == "FND"
        assert d["data"]["amount"] == 100.0
        assert "id" in d
        assert "timestamp" in d
        assert "formatted" in d

    def test_round_trip_preserves_data(self):
        original = Signal(
            type=SignalType.SUBSCRIPTION_CREATED,
            source="stripe",
            target="FND",
            data={"customer": "cus_test", "plan": "basic"},
        )
        d = original.to_dict()
        restored = Signal.from_dict(d)
        assert restored.type == original.type
        assert restored.source == original.source
        assert restored.target == original.target
        assert restored.data == original.data
        assert restored.id == original.id
        assert restored.timestamp == original.timestamp

    def test_from_dict_handles_minimal_data(self):
        d = {
            "type": "push",
            "source": "github",
            "target": "OS",
        }
        signal = Signal.from_dict(d)
        assert signal.type == SignalType.PUSH
        assert signal.data == {}


class TestSignalFormat:
    """Test Signal.format() output."""

    def test_payment_received_format(self):
        signal = Signal(
            type=SignalType.PAYMENT_RECEIVED,
            source="stripe",
            target="FND",
            data={"amount": 100.0, "customer": "cus_1"},
        )
        fmt = signal.format()
        assert "STRIPE" in fmt
        assert "FND" in fmt
        assert "payment_received" in fmt

    def test_push_format_has_emoji(self):
        signal = Signal(type=SignalType.PUSH, source="github", target="OS")
        fmt = signal.format()
        assert "GITHUB" in fmt
        assert "OS" in fmt

    def test_custom_type_gets_default_emoji(self):
        signal = Signal(type=SignalType.CUSTOM, source="unknown", target="OS")
        fmt = signal.format()
        assert "UNKNOWN" in fmt

    def test_format_truncates_data_to_three_items(self):
        signal = Signal(
            type=SignalType.PAYMENT_RECEIVED,
            source="stripe",
            target="FND",
            data={"a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
        )
        fmt = signal.format()
        # Should only show first 3 data items
        assert "d=" not in fmt
        assert "e=" not in fmt


class TestSignalTypes:
    """Test all Stripe-related signal types exist."""

    def test_stripe_signal_types_exist(self):
        assert SignalType.PAYMENT_RECEIVED.value == "payment_received"
        assert SignalType.PAYMENT_FAILED.value == "payment_failed"
        assert SignalType.SUBSCRIPTION_CREATED.value == "subscription_created"
        assert SignalType.SUBSCRIPTION_CANCELLED.value == "subscription_cancelled"
        assert SignalType.INVOICE_PAID.value == "invoice_paid"
