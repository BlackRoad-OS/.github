"""
Router - The main Operator that ties everything together.

This is the brain of BlackRoad.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime

from .parser import Parser, Request, InputType
from .classifier import Classifier, Classification


# Org registry
ORGS = {
    "OS": {"name": "BlackRoad-OS", "description": "Core infrastructure"},
    "AI": {"name": "BlackRoad-AI", "description": "Intelligence routing"},
    "CLD": {"name": "BlackRoad-Cloud", "description": "Edge compute"},
    "HW": {"name": "BlackRoad-Hardware", "description": "Hardware & IoT"},
    "LAB": {"name": "BlackRoad-Labs", "description": "Experiments"},
    "SEC": {"name": "BlackRoad-Security", "description": "Security"},
    "FND": {"name": "BlackRoad-Foundation", "description": "CRM & billing"},
    "MED": {"name": "BlackRoad-Media", "description": "Content"},
    "INT": {"name": "BlackRoad-Interactive", "description": "Metaverse"},
    "EDU": {"name": "BlackRoad-Education", "description": "Learning"},
    "GOV": {"name": "BlackRoad-Gov", "description": "Governance"},
    "ARC": {"name": "BlackRoad-Archive", "description": "Storage"},
    "STU": {"name": "BlackRoad-Studio", "description": "Design"},
    "VEN": {"name": "BlackRoad-Ventures", "description": "Commerce"},
    "BBX": {"name": "Blackbox-Enterprises", "description": "Enterprise"},
}


@dataclass
class RouteResult:
    """Result of routing a request."""
    destination: str
    org: str
    org_code: str
    confidence: float
    classification: Classification
    request: Request
    timestamp: str
    signal: str

    def __repr__(self):
        return f"RouteResult(→ {self.org} [{self.org_code}], conf={self.confidence:.2f})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "destination": self.destination,
            "org": self.org,
            "org_code": self.org_code,
            "confidence": self.confidence,
            "category": self.classification.category,
            "query": self.request.query,
            "timestamp": self.timestamp,
            "signal": self.signal
        }


class Operator:
    """
    The main Operator - routes requests to the right destination.

    Examples:
        >>> op = Operator()
        >>> result = op.route("What is the weather?")
        >>> print(result.org)
        'BlackRoad-AI'

        >>> result = op.route("Update customer record")
        >>> print(result.org)
        'BlackRoad-Foundation'
    """

    def __init__(
        self,
        parser: Optional[Parser] = None,
        classifier: Optional[Classifier] = None,
        signal_callback: Optional[callable] = None
    ):
        """
        Initialize the Operator.

        Args:
            parser: Custom parser (uses default if None)
            classifier: Custom classifier (uses default if None)
            signal_callback: Function to call when signals are emitted
        """
        self.parser = parser or Parser()
        self.classifier = classifier or Classifier()
        self.signal_callback = signal_callback
        self._route_count = 0
        self._history: List[RouteResult] = []

    def route(
        self,
        input_data: Any,
        input_type: Optional[InputType] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> RouteResult:
        """
        Route a request to the appropriate destination.

        Args:
            input_data: The input to route (string, dict, etc.)
            input_type: Optional input type hint
            context: Optional context dictionary

        Returns:
            RouteResult with destination, confidence, and signal
        """
        # Parse the input
        request = self.parser.parse(input_data, input_type, context)

        # Classify the request
        classification = self.classifier.classify(request.query)

        # Get org info
        org_code = classification.org_code
        org_info = ORGS.get(org_code, ORGS["AI"])

        # Generate timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Generate signal
        signal = f"🎯 OS → {org_code} : {classification.category}"

        # Create result
        result = RouteResult(
            destination=classification.category,
            org=org_info["name"],
            org_code=org_code,
            confidence=classification.confidence,
            classification=classification,
            request=request,
            timestamp=timestamp,
            signal=signal
        )

        # Emit signal if callback provided
        if self.signal_callback:
            self.signal_callback(signal, result)

        # Track history
        self._route_count += 1
        self._history.append(result)

        # Keep history bounded
        if len(self._history) > 1000:
            self._history = self._history[-500:]

        return result

    def route_batch(
        self,
        inputs: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> List[RouteResult]:
        """Route multiple inputs."""
        return [self.route(inp, context=context) for inp in inputs]

    @property
    def stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        if not self._history:
            return {"total": 0, "by_org": {}, "avg_confidence": 0}

        by_org: Dict[str, int] = {}
        total_conf = 0.0

        for result in self._history:
            by_org[result.org_code] = by_org.get(result.org_code, 0) + 1
            total_conf += result.confidence

        return {
            "total": self._route_count,
            "by_org": by_org,
            "avg_confidence": total_conf / len(self._history)
        }

    def explain(self, input_data: Any) -> str:
        """
        Explain how a request would be routed.

        Returns a human-readable explanation.
        """
        result = self.route(input_data)

        lines = [
            f"Query: {result.request.query}",
            f"",
            f"Classification:",
            f"  Category: {result.classification.category}",
            f"  Confidence: {result.confidence:.1%}",
            f"  Matched: {', '.join(result.classification.matched_patterns)}",
            f"",
            f"Destination:",
            f"  Org: {result.org}",
            f"  Code: {result.org_code}",
            f"  Description: {ORGS[result.org_code]['description']}",
            f"",
            f"Signal: {result.signal}",
        ]

        return "\n".join(lines)


# Convenience function
def route(query: str, **kwargs) -> RouteResult:
    """Quick route function."""
    return Operator().route(query, **kwargs)
