"""
BlackRoad AI Router

Route to intelligence, don't build it.

This module provides unified routing to multiple AI providers:
- OpenAI (GPT-4, GPT-3.5, embeddings)
- Anthropic (Claude 3.5, Claude 3)
- Local Hailo-8 (on-device inference)
- Ollama (local LLMs)

Usage:
    from ai_router import Router

    router = Router()
    response = router.complete("What is the meaning of life?")

    # With specific provider
    response = router.complete("Write code", provider="anthropic")

    # With fallback chain
    response = router.complete("Analyze image", chain=["hailo", "openai"])
"""

__version__ = "0.1.0"

from .routing.router import Router, Route, RouteResult
from .routing.strategy import RoutingStrategy, CostOptimized, LatencyOptimized, QualityOptimized
from .providers.base import Provider, ProviderConfig, ModelCapability
from .tracking.costs import CostTracker
from .signals.emitter import SignalEmitter

__all__ = [
    "Router",
    "Route",
    "RouteResult",
    "RoutingStrategy",
    "CostOptimized",
    "LatencyOptimized",
    "QualityOptimized",
    "Provider",
    "ProviderConfig",
    "ModelCapability",
    "CostTracker",
    "SignalEmitter",
]
