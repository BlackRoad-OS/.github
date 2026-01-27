"""
Routing Strategies - How to pick the right provider.

Different strategies for different needs:
- CostOptimized: Cheapest option first (local > cloud)
- LatencyOptimized: Fastest option first
- QualityOptimized: Best model first
- LocalFirst: Always try local before cloud
- CloudFirst: Always try cloud (for quality)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from ..providers.base import (
    Provider,
    ProviderStatus,
    ModelCapability,
    CompletionRequest,
)


@dataclass
class ProviderScore:
    """Score for a provider based on strategy."""
    provider: Provider
    score: float
    reason: str


class RoutingStrategy(ABC):
    """Base class for routing strategies."""

    name: str = "base"

    @abstractmethod
    def rank_providers(
        self,
        providers: List[Provider],
        request: CompletionRequest,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> List[ProviderScore]:
        """
        Rank providers by preference.

        Args:
            providers: Available providers
            request: The request being made
            capability: Required capability

        Returns:
            List of ProviderScore, highest score first
        """
        pass

    def filter_available(self, providers: List[Provider]) -> List[Provider]:
        """Filter to only available providers."""
        return [p for p in providers if p.is_available]

    def filter_capable(
        self,
        providers: List[Provider],
        capability: ModelCapability
    ) -> List[Provider]:
        """Filter to providers with required capability."""
        return [p for p in providers if p.supports(capability)]


class CostOptimized(RoutingStrategy):
    """
    Minimize cost. Prefers free local options.

    Priority:
    1. Hailo (free, on-device)
    2. Ollama (free, local)
    3. Cheapest cloud (GPT-4o-mini, Claude Haiku)
    """

    name = "cost_optimized"

    def rank_providers(
        self,
        providers: List[Provider],
        request: CompletionRequest,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> List[ProviderScore]:
        available = self.filter_available(providers)
        capable = self.filter_capable(available, capability)

        scores = []
        for p in capable:
            # Lower cost = higher score
            # Free providers get max score
            if p.config.cost_per_1k_output == 0:
                score = 1000.0
                reason = "Free (local inference)"
            else:
                # Invert cost: lower cost = higher score
                avg_cost = (p.config.cost_per_1k_input + p.config.cost_per_1k_output) / 2
                score = 1.0 / (avg_cost + 0.0001)  # Avoid div by zero
                reason = f"${avg_cost:.4f}/1k tokens"

            scores.append(ProviderScore(provider=p, score=score, reason=reason))

        # Sort by score descending
        return sorted(scores, key=lambda x: x.score, reverse=True)


class LatencyOptimized(RoutingStrategy):
    """
    Minimize latency. Fastest response wins.

    Priority:
    1. Hailo (on-device, ~100ms)
    2. Ollama (local, ~500ms)
    3. Fastest cloud
    """

    name = "latency_optimized"

    def rank_providers(
        self,
        providers: List[Provider],
        request: CompletionRequest,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> List[ProviderScore]:
        available = self.filter_available(providers)
        capable = self.filter_capable(available, capability)

        scores = []
        for p in capable:
            # Lower latency = higher score
            latency = p.config.avg_latency_ms
            score = 10000.0 / (latency + 1)  # Invert
            reason = f"~{latency}ms avg latency"

            scores.append(ProviderScore(provider=p, score=score, reason=reason))

        return sorted(scores, key=lambda x: x.score, reverse=True)


class QualityOptimized(RoutingStrategy):
    """
    Maximize quality. Best model wins.

    Priority:
    1. Claude Opus / GPT-4o
    2. Claude Sonnet / GPT-4-turbo
    3. Smaller models
    """

    name = "quality_optimized"

    # Quality rankings (higher = better)
    QUALITY_RANKS = {
        "openai": {
            "gpt-4o": 95,
            "gpt-4-turbo": 90,
            "gpt-4o-mini": 75,
            "gpt-3.5-turbo": 60,
        },
        "anthropic": {
            "claude-opus-4-20250514": 98,
            "claude-sonnet-4-20250514": 92,
            "claude-3-5-sonnet-20241022": 90,
            "claude-3-opus-20240229": 88,
            "claude-3-5-haiku-20241022": 70,
            "claude-3-haiku-20240307": 65,
        },
        "ollama": {
            "llama3.1:70b": 80,
            "mixtral": 75,
            "llama3.1": 70,
            "llama3.2": 65,
            "mistral": 60,
            "phi3": 55,
            "tinyllama": 40,
        },
        "hailo": {
            "llama-7b-q4": 50,
            "phi-2-q4": 45,
            "tinyllama-1b-q4": 35,
        },
    }

    def rank_providers(
        self,
        providers: List[Provider],
        request: CompletionRequest,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> List[ProviderScore]:
        available = self.filter_available(providers)
        capable = self.filter_capable(available, capability)

        scores = []
        for p in capable:
            model = request.model or p.config.default_model
            provider_ranks = self.QUALITY_RANKS.get(p.name, {})
            quality = provider_ranks.get(model, 50)  # Default to 50
            reason = f"Quality rank: {quality}/100"

            scores.append(ProviderScore(provider=p, score=quality, reason=reason))

        return sorted(scores, key=lambda x: x.score, reverse=True)


class LocalFirst(RoutingStrategy):
    """
    Always try local before cloud.

    Priority:
    1. Hailo (hardware accelerated)
    2. Ollama (local CPU/GPU)
    3. Cloud providers (fallback)
    """

    name = "local_first"

    def rank_providers(
        self,
        providers: List[Provider],
        request: CompletionRequest,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> List[ProviderScore]:
        available = self.filter_available(providers)
        capable = self.filter_capable(available, capability)

        scores = []
        for p in capable:
            if p.name == "hailo":
                score = 1000.0
                reason = "Local: Hailo hardware accelerator"
            elif p.name == "ollama":
                score = 900.0
                reason = "Local: Ollama"
            else:
                score = 100.0
                reason = f"Cloud: {p.name}"

            scores.append(ProviderScore(provider=p, score=score, reason=reason))

        return sorted(scores, key=lambda x: x.score, reverse=True)


class CloudFirst(RoutingStrategy):
    """
    Always try cloud first for maximum quality.

    Priority:
    1. Anthropic (Claude)
    2. OpenAI (GPT)
    3. Local (fallback)
    """

    name = "cloud_first"

    def rank_providers(
        self,
        providers: List[Provider],
        request: CompletionRequest,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> List[ProviderScore]:
        available = self.filter_available(providers)
        capable = self.filter_capable(available, capability)

        scores = []
        for p in capable:
            if p.name == "anthropic":
                score = 1000.0
                reason = "Cloud: Anthropic (Claude)"
            elif p.name == "openai":
                score = 900.0
                reason = "Cloud: OpenAI (GPT)"
            else:
                score = 100.0
                reason = f"Local fallback: {p.name}"

            scores.append(ProviderScore(provider=p, score=score, reason=reason))

        return sorted(scores, key=lambda x: x.score, reverse=True)


# Strategy registry
STRATEGIES: Dict[str, RoutingStrategy] = {
    "cost": CostOptimized(),
    "latency": LatencyOptimized(),
    "quality": QualityOptimized(),
    "local_first": LocalFirst(),
    "cloud_first": CloudFirst(),
}


def get_strategy(name: str) -> RoutingStrategy:
    """Get a strategy by name."""
    if name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(STRATEGIES.keys())}")
    return STRATEGIES[name]
