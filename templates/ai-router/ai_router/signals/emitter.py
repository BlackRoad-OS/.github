"""
Signal Emitter - Broadcast AI routing events.

Signals flow through the BlackRoad mesh:
AI → OS → wherever they need to go.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Callable, Dict, Any
from enum import Enum


class SignalType(Enum):
    """Types of AI signals."""
    INFERENCE_START = "inference_start"
    INFERENCE_COMPLETE = "inference_complete"
    INFERENCE_FAILED = "inference_failed"
    FALLBACK_TRIGGERED = "fallback_triggered"
    PROVIDER_HEALTHY = "provider_healthy"
    PROVIDER_DEGRADED = "provider_degraded"
    PROVIDER_DOWN = "provider_down"
    COST_ALERT = "cost_alert"
    LATENCY_ALERT = "latency_alert"


@dataclass
class Signal:
    """A signal to emit."""
    type: SignalType
    source: str = "AI"
    target: str = "OS"
    data: Optional[Dict[str, Any]] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def format(self) -> str:
        """Format as BlackRoad signal string."""
        emoji = self._get_emoji()
        data_str = ", ".join(f"{k}={v}" for k, v in (self.data or {}).items())
        return f"{emoji} {self.source} → {self.target} : {self.type.value}, {data_str}"

    def _get_emoji(self) -> str:
        """Get emoji for signal type."""
        emoji_map = {
            SignalType.INFERENCE_START: "🧠",
            SignalType.INFERENCE_COMPLETE: "✅",
            SignalType.INFERENCE_FAILED: "❌",
            SignalType.FALLBACK_TRIGGERED: "🔄",
            SignalType.PROVIDER_HEALTHY: "🟢",
            SignalType.PROVIDER_DEGRADED: "🟡",
            SignalType.PROVIDER_DOWN: "🔴",
            SignalType.COST_ALERT: "💰",
            SignalType.LATENCY_ALERT: "⏱️",
        }
        return emoji_map.get(self.type, "📡")


class SignalEmitter:
    """
    Emit signals for AI routing events.

    Usage:
        emitter = SignalEmitter()

        # Emit completion signal
        emitter.inference_complete(
            provider="anthropic",
            model="claude-3.5-sonnet",
            latency_ms=450,
            cost=0.003
        )

        # Add handler
        emitter.on_signal(lambda s: send_to_webhook(s))
    """

    def __init__(self):
        self.handlers: List[Callable[[Signal], None]] = []
        self._history: List[Signal] = []

    def on_signal(self, handler: Callable[[Signal], None]):
        """Register a signal handler."""
        self.handlers.append(handler)

    def emit(self, signal: Signal):
        """Emit a signal to all handlers."""
        self._history.append(signal)

        # Print for visibility
        print(f"  {signal.format()}")

        # Call handlers
        for handler in self.handlers:
            try:
                handler(signal)
            except Exception as e:
                print(f"  ⚠️ Signal handler error: {e}")

    def inference_start(
        self,
        provider: str,
        model: str,
    ):
        """Signal that inference is starting."""
        self.emit(Signal(
            type=SignalType.INFERENCE_START,
            data={"provider": provider, "model": model}
        ))

    def inference_complete(
        self,
        provider: str,
        model: str,
        latency_ms: int,
        cost: float,
        tokens: int = 0,
    ):
        """Signal that inference completed successfully."""
        self.emit(Signal(
            type=SignalType.INFERENCE_COMPLETE,
            data={
                "provider": provider,
                "model": model,
                "latency_ms": latency_ms,
                "cost": f"${cost:.4f}",
                "tokens": tokens,
            }
        ))

    def inference_failed(
        self,
        provider: str,
        model: str,
        error: str,
    ):
        """Signal that inference failed."""
        self.emit(Signal(
            type=SignalType.INFERENCE_FAILED,
            data={
                "provider": provider,
                "model": model,
                "error": error[:50],  # Truncate error
            }
        ))

    def fallback_triggered(
        self,
        from_provider: str,
        to_provider: str,
        reason: str,
    ):
        """Signal that a fallback was triggered."""
        self.emit(Signal(
            type=SignalType.FALLBACK_TRIGGERED,
            data={
                "from": from_provider,
                "to": to_provider,
                "reason": reason,
            }
        ))

    def provider_status(
        self,
        provider: str,
        status: str,  # healthy, degraded, down
    ):
        """Signal provider status change."""
        type_map = {
            "healthy": SignalType.PROVIDER_HEALTHY,
            "degraded": SignalType.PROVIDER_DEGRADED,
            "down": SignalType.PROVIDER_DOWN,
        }
        self.emit(Signal(
            type=type_map.get(status, SignalType.PROVIDER_DEGRADED),
            data={"provider": provider, "status": status}
        ))

    def cost_alert(
        self,
        total_cost: float,
        period: str,
        threshold: float,
    ):
        """Signal that cost threshold was exceeded."""
        self.emit(Signal(
            type=SignalType.COST_ALERT,
            data={
                "total_cost": f"${total_cost:.2f}",
                "period": period,
                "threshold": f"${threshold:.2f}",
            }
        ))

    def latency_alert(
        self,
        provider: str,
        latency_ms: int,
        threshold_ms: int,
    ):
        """Signal that latency threshold was exceeded."""
        self.emit(Signal(
            type=SignalType.LATENCY_ALERT,
            data={
                "provider": provider,
                "latency_ms": latency_ms,
                "threshold_ms": threshold_ms,
            }
        ))

    @property
    def history(self) -> List[Signal]:
        """Get signal history."""
        return self._history.copy()

    def clear_history(self):
        """Clear signal history."""
        self._history = []
