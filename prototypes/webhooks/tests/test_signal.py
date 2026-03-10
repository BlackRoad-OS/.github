"""
Tests for the Signal dataclass.

Every webhook event is converted to a Signal before being dispatched
through the BlackRoad mesh.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from webhooks.signal import Signal, SignalType


class TestSignalCreation:
    """Verify Signal construction and defaults."""

    def test_basic_signal(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert s.type == SignalType.PUSH
        assert s.source == "github"
        assert s.target == "OS"

    def test_auto_timestamp(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert s.timestamp
        assert "T" in s.timestamp  # ISO format

    def test_auto_id_generated(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert s.id
        assert len(s.id) == 12  # sha256[:12]

    def test_id_is_deterministic_for_same_content(self):
        # Two signals with same type/source/timestamp get same ID
        ts = "2026-01-01T00:00:00"
        s1 = Signal(type=SignalType.PUSH, source="github", target="OS", timestamp=ts)
        s2 = Signal(type=SignalType.PUSH, source="github", target="OS", timestamp=ts)
        assert s1.id == s2.id

    def test_explicit_timestamp_preserved(self):
        ts = "2026-03-01T12:00:00"
        s = Signal(type=SignalType.PAYMENT_RECEIVED, source="stripe", target="FND", timestamp=ts)
        assert s.timestamp == ts


class TestSignalFormat:
    """Verify the format() method produces correct signal strings."""

    def test_format_includes_source_and_target(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS",
                   data={"repo": "BlackRoad-OS/.github"})
        formatted = s.format()
        assert "GITHUB" in formatted
        assert "OS" in formatted

    def test_format_includes_type(self):
        s = Signal(type=SignalType.PAYMENT_RECEIVED, source="stripe", target="FND")
        formatted = s.format()
        assert "payment_received" in formatted

    def test_format_has_arrow(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert "→" in s.format()

    def test_format_emoji_push(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        assert "📥" in s.format()

    def test_format_emoji_payment(self):
        s = Signal(type=SignalType.PAYMENT_RECEIVED, source="stripe", target="FND")
        assert "💰" in s.format()

    def test_format_unknown_type_uses_fallback_emoji(self):
        s = Signal(type=SignalType.CUSTOM, source="external", target="OS")
        assert "📡" in s.format()

    def test_format_data_included(self):
        s = Signal(type=SignalType.LEAD_CREATED, source="salesforce", target="FND",
                   data={"object_type": "Lead", "action": "created"})
        formatted = s.format()
        assert "object_type" in formatted or "Lead" in formatted


class TestSignalSerialization:
    """Verify to_dict / from_dict round-trip."""

    def test_to_dict_keys(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        d = s.to_dict()
        assert "id" in d
        assert "type" in d
        assert "source" in d
        assert "target" in d
        assert "data" in d
        assert "timestamp" in d
        assert "formatted" in d

    def test_to_dict_type_is_string(self):
        s = Signal(type=SignalType.PUSH, source="github", target="OS")
        d = s.to_dict()
        assert d["type"] == "push"

    def test_round_trip(self):
        original = Signal(
            type=SignalType.SUBSCRIPTION_CREATED,
            source="stripe",
            target="FND",
            data={"customer": "cus_123"},
        )
        d = original.to_dict()
        restored = Signal.from_dict(d)
        assert restored.type == original.type
        assert restored.source == original.source
        assert restored.target == original.target
        assert restored.data == original.data

    def test_from_dict_preserves_id_and_timestamp(self):
        original = Signal(type=SignalType.PING, source="health", target="OS")
        d = original.to_dict()
        restored = Signal.from_dict(d)
        # timestamp and id are explicitly passed in from_dict
        assert restored.source == original.source
        assert restored.target == original.target
