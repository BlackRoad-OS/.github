"""
BlackRoad Operator - The brain that routes everything.

Usage:
    from operator import Operator

    op = Operator()
    result = op.route("What is the weather?")
    print(result.destination)  # "AI"
"""

from .core.router import Operator, RouteResult
from .core.classifier import Classifier
from .core.parser import Parser
from .signals.emitter import SignalEmitter

__version__ = "0.1.0"
__all__ = ["Operator", "RouteResult", "Classifier", "Parser", "SignalEmitter"]
