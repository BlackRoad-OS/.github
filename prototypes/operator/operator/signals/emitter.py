"""
Signal Emitter - Morse code for the mesh.

Emits signals that can be received by other orgs and nodes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Callable, Dict, Any
from enum import Enum
import json


class SignalType(Enum):
    """Signal types."""
    COMPLETE = "✔️"
    IN_PROGRESS = "⏳"
    FAILED = "❌"
    WARNING = "⚠️"
    BROADCAST = "📡"
    TARGETED = "🎯"
    SYNC = "🔄"
    UPSTREAM = "⬆️"
    DOWNSTREAM = "⬇️"
    HEARTBEAT = "💓"
    CRITICAL = "🔴"
    IMPORTANT = "🟡"
    NORMAL = "🟢"
    LOW = "⚪"


@dataclass
class Signal:
    """A signal in the mesh."""
    type: SignalType
    source: str
    target: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Format as signal string."""
        return f"{self.type.value} {self.source} → {self.target} : {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.type.value,
            "source": self.source,
            "target": self.target,
            "message": self.message,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def parse(cls, signal_str: str) -> "Signal":
        """Parse a signal string."""
        # Format: "✔️ OS → AI : message"
        parts = signal_str.split(" → ")
        if len(parts) != 2:
            raise ValueError(f"Invalid signal format: {signal_str}")

        type_source = parts[0].strip()
        target_message = parts[1].strip()

        # Extract type (emoji) and source
        for st in SignalType:
            if type_source.startswith(st.value):
                signal_type = st
                source = type_source[len(st.value):].strip()
                break
        else:
            signal_type = SignalType.NORMAL
            source = type_source

        # Extract target and message
        if " : " in target_message:
            target, message = target_message.split(" : ", 1)
        else:
            target = target_message
            message = ""

        return cls(
            type=signal_type,
            source=source,
            target=target.strip(),
            message=message.strip()
        )


class SignalEmitter:
    """
    Emit signals to the mesh.

    Examples:
        >>> emitter = SignalEmitter()
        >>> emitter.emit_complete("OS", "AI", "Query routed")
        Signal(✔️ OS → AI : Query routed)

        >>> emitter.broadcast("OS", "System update")
        Signal(📡 OS → ALL : System update)
    """

    def __init__(
        self,
        default_source: str = "OS",
        handlers: Optional[List[Callable[[Signal], None]]] = None
    ):
        """
        Initialize the emitter.

        Args:
            default_source: Default source for signals
            handlers: List of callback functions for signals
        """
        self.default_source = default_source
        self.handlers = handlers or []
        self._history: List[Signal] = []

    def add_handler(self, handler: Callable[[Signal], None]):
        """Add a signal handler."""
        self.handlers.append(handler)

    def emit(
        self,
        signal_type: SignalType,
        target: str,
        message: str,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Signal:
        """
        Emit a signal.

        Args:
            signal_type: Type of signal
            target: Target org/node code
            message: Signal message
            source: Source (uses default if None)
            metadata: Optional metadata dict

        Returns:
            The emitted Signal
        """
        signal = Signal(
            type=signal_type,
            source=source or self.default_source,
            target=target,
            message=message,
            metadata=metadata or {}
        )

        # Store in history
        self._history.append(signal)
        if len(self._history) > 1000:
            self._history = self._history[-500:]

        # Call handlers
        for handler in self.handlers:
            try:
                handler(signal)
            except Exception as e:
                print(f"Signal handler error: {e}")

        return signal

    # Convenience methods

    def emit_complete(self, source: str, target: str, message: str) -> Signal:
        """Emit a completion signal."""
        return self.emit(SignalType.COMPLETE, target, message, source)

    def emit_failed(self, source: str, target: str, message: str) -> Signal:
        """Emit a failure signal."""
        return self.emit(SignalType.FAILED, target, message, source)

    def emit_progress(self, source: str, target: str, message: str) -> Signal:
        """Emit a progress signal."""
        return self.emit(SignalType.IN_PROGRESS, target, message, source)

    def emit_warning(self, source: str, target: str, message: str) -> Signal:
        """Emit a warning signal."""
        return self.emit(SignalType.WARNING, target, message, source)

    def route(self, target: str, message: str, source: Optional[str] = None) -> Signal:
        """Emit a routing signal."""
        return self.emit(SignalType.TARGETED, target, message, source)

    def broadcast(self, source: str, message: str) -> Signal:
        """Broadcast to all."""
        return self.emit(SignalType.BROADCAST, "ALL", message, source)

    def heartbeat(self, source: str, status: str = "healthy") -> Signal:
        """Emit a heartbeat."""
        return self.emit(
            SignalType.HEARTBEAT,
            "OS",
            f"status={status}",
            source
        )

    def critical(self, source: str, target: str, message: str) -> Signal:
        """Emit a critical alert."""
        return self.emit(SignalType.CRITICAL, target, message, source)

    @property
    def history(self) -> List[Signal]:
        """Get signal history."""
        return self._history.copy()

    def recent(self, n: int = 10) -> List[Signal]:
        """Get n most recent signals."""
        return self._history[-n:]

    def format_history(self, n: int = 10) -> str:
        """Format recent history as string."""
        lines = []
        for signal in self.recent(n):
            lines.append(f"{signal.timestamp} {signal}")
        return "\n".join(lines)


# Default emitter instance
_default_emitter = SignalEmitter()


def emit(signal_type: SignalType, target: str, message: str, **kwargs) -> Signal:
    """Emit using default emitter."""
    return _default_emitter.emit(signal_type, target, message, **kwargs)


def broadcast(message: str, source: str = "OS") -> Signal:
    """Broadcast using default emitter."""
    return _default_emitter.broadcast(source, message)


def route_signal(target: str, message: str, source: str = "OS") -> Signal:
    """Route using default emitter."""
    return _default_emitter.route(target, message, source)
