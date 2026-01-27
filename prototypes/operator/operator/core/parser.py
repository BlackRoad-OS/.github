"""
Parser - Understands any input format.

Converts various input types into a normalized Request object.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import json


class InputType(Enum):
    """Types of input the parser can handle."""
    TEXT = "text"
    HTTP = "http"
    WEBHOOK = "webhook"
    SIGNAL = "signal"
    CLI = "cli"


@dataclass
class Request:
    """Normalized request object."""
    raw: str
    input_type: InputType
    query: str
    context: Dict[str, Any]
    metadata: Dict[str, Any]

    def __repr__(self):
        return f"Request(type={self.input_type.value}, query='{self.query[:50]}...')"


class Parser:
    """
    Parse any input into a normalized Request.

    Examples:
        >>> parser = Parser()
        >>> req = parser.parse("What is the weather?")
        >>> req.query
        'What is the weather?'
        >>> req.input_type
        <InputType.TEXT: 'text'>
    """

    def parse(
        self,
        input_data: Any,
        input_type: Optional[InputType] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Request:
        """
        Parse input into a Request object.

        Args:
            input_data: The raw input (string, dict, etc.)
            input_type: Optional type hint
            context: Optional context dict

        Returns:
            Normalized Request object
        """
        context = context or {}
        metadata = {}

        # Auto-detect input type if not provided
        if input_type is None:
            input_type = self._detect_type(input_data)

        # Parse based on type
        if input_type == InputType.TEXT:
            query = str(input_data).strip()
            raw = query

        elif input_type == InputType.HTTP:
            raw, query, metadata = self._parse_http(input_data)

        elif input_type == InputType.WEBHOOK:
            raw, query, metadata = self._parse_webhook(input_data)

        elif input_type == InputType.SIGNAL:
            raw, query, metadata = self._parse_signal(input_data)

        elif input_type == InputType.CLI:
            raw, query = self._parse_cli(input_data)

        else:
            query = str(input_data)
            raw = query

        return Request(
            raw=raw,
            input_type=input_type,
            query=query,
            context=context,
            metadata=metadata
        )

    def _detect_type(self, input_data: Any) -> InputType:
        """Auto-detect the input type."""
        if isinstance(input_data, str):
            # Check if it looks like a signal
            if any(s in input_data for s in ["→", "✔️", "❌", "📡", "🎯"]):
                return InputType.SIGNAL
            return InputType.TEXT

        if isinstance(input_data, dict):
            # Check for HTTP-like structure
            if "method" in input_data or "headers" in input_data:
                return InputType.HTTP
            # Check for webhook-like structure
            if "event" in input_data or "payload" in input_data:
                return InputType.WEBHOOK

        return InputType.TEXT

    def _parse_http(self, data: Dict) -> tuple:
        """Parse HTTP request."""
        raw = json.dumps(data)
        query = data.get("body", data.get("query", ""))
        metadata = {
            "method": data.get("method", "GET"),
            "path": data.get("path", "/"),
            "headers": data.get("headers", {})
        }
        return raw, query, metadata

    def _parse_webhook(self, data: Dict) -> tuple:
        """Parse webhook payload."""
        raw = json.dumps(data)
        event = data.get("event", "unknown")
        payload = data.get("payload", data)
        query = f"webhook:{event}"
        metadata = {
            "event": event,
            "payload": payload,
            "source": data.get("source", "unknown")
        }
        return raw, query, metadata

    def _parse_signal(self, data: str) -> tuple:
        """Parse a signal string."""
        raw = data
        # Signal format: "✔️ OS → AI : message"
        parts = data.split(":")
        if len(parts) >= 2:
            query = parts[1].strip()
        else:
            query = data
        metadata = {"signal": data}
        return raw, query, metadata

    def _parse_cli(self, data: Any) -> tuple:
        """Parse CLI input."""
        if isinstance(data, list):
            query = " ".join(data)
        else:
            query = str(data)
        return query, query
