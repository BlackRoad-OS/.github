"""
Router - The brain that routes to brains.

This is the core of BlackRoad's AI routing.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any, AsyncIterator, Union

from ..providers.base import (
    Provider,
    ProviderStatus,
    ModelCapability,
    CompletionRequest,
    CompletionResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    Message,
)
from ..providers.openai import OpenAIProvider
from ..providers.anthropic import AnthropicProvider
from ..providers.hailo import HailoProvider
from ..providers.ollama import OllamaProvider
from .strategy import RoutingStrategy, CostOptimized, get_strategy


@dataclass
class Route:
    """A route taken by a request."""
    provider: str
    model: str
    success: bool
    latency_ms: int
    cost: float
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RouteResult:
    """Result of a routed request."""
    response: Optional[CompletionResponse]
    routes_tried: List[Route]
    final_provider: str
    total_latency_ms: int
    total_cost: float
    success: bool
    error: Optional[str] = None

    @property
    def content(self) -> str:
        """Get response content."""
        return self.response.content if self.response else ""

    def signal(self) -> str:
        """Generate a signal for this route."""
        if self.success:
            return f"🧠 AI → OS : inference_complete, provider={self.final_provider}, latency={self.total_latency_ms}ms, cost=${self.total_cost:.4f}"
        else:
            return f"❌ AI → OS : inference_failed, tried={len(self.routes_tried)}, error={self.error}"


class Router:
    """
    The AI Router - Route to intelligence, don't build it.

    Features:
    - Multiple providers (OpenAI, Anthropic, Hailo, Ollama)
    - Automatic fallback on failure
    - Cost tracking
    - Strategy-based routing (cost, latency, quality)
    - Signal emission

    Usage:
        router = Router()

        # Simple completion
        response = await router.complete("What is 2+2?")

        # With specific provider
        response = await router.complete("Write code", provider="anthropic")

        # With fallback chain
        response = await router.complete("Analyze", chain=["hailo", "ollama", "openai"])

        # With strategy
        router = Router(strategy="cost")  # Always pick cheapest
    """

    def __init__(
        self,
        providers: Optional[List[Provider]] = None,
        strategy: Union[str, RoutingStrategy] = "cost",
        signal_callback: Optional[callable] = None,
    ):
        """
        Initialize the router.

        Args:
            providers: List of providers (auto-configured if None)
            strategy: Routing strategy (name or instance)
            signal_callback: Function to call when signals are emitted
        """
        self.providers: Dict[str, Provider] = {}
        self._setup_providers(providers)

        if isinstance(strategy, str):
            self.strategy = get_strategy(strategy)
        else:
            self.strategy = strategy

        self.signal_callback = signal_callback
        self._history: List[RouteResult] = []

    def _setup_providers(self, providers: Optional[List[Provider]]):
        """Set up providers."""
        if providers:
            for p in providers:
                self.providers[p.name] = p
        else:
            # Auto-configure default providers
            self.providers = {
                "openai": OpenAIProvider(),
                "anthropic": AnthropicProvider(),
                "hailo": HailoProvider(),
                "ollama": OllamaProvider(),
            }

    def get_provider(self, name: str) -> Optional[Provider]:
        """Get a provider by name."""
        return self.providers.get(name)

    async def health_check_all(self) -> Dict[str, ProviderStatus]:
        """Check health of all providers."""
        results = {}
        for name, provider in self.providers.items():
            try:
                status = await asyncio.wait_for(
                    provider.health_check(),
                    timeout=5.0
                )
                results[name] = status
            except asyncio.TimeoutError:
                results[name] = ProviderStatus.UNAVAILABLE
            except Exception:
                results[name] = ProviderStatus.UNAVAILABLE
        return results

    async def complete(
        self,
        prompt: Union[str, List[Message]],
        *,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        chain: Optional[List[str]] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        stream: bool = False,
        capability: ModelCapability = ModelCapability.CHAT,
    ) -> RouteResult:
        """
        Complete a prompt using the best available provider.

        Args:
            prompt: Text prompt or list of messages
            model: Specific model to use
            provider: Specific provider to use
            chain: Fallback chain of providers
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stream: Whether to stream response
            capability: Required capability

        Returns:
            RouteResult with response and routing info
        """
        # Build request
        if isinstance(prompt, str):
            messages = [Message(role="user", content=prompt)]
        else:
            messages = prompt

        request = CompletionRequest(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
        )

        # Determine provider order
        if provider:
            # Specific provider requested
            provider_order = [provider]
        elif chain:
            # Explicit chain provided
            provider_order = chain
        else:
            # Use strategy to rank providers
            ranked = self.strategy.rank_providers(
                list(self.providers.values()),
                request,
                capability,
            )
            provider_order = [score.provider.name for score in ranked]

        # Try providers in order
        routes_tried = []
        last_error = None
        start_time = datetime.now()

        for provider_name in provider_order:
            p = self.providers.get(provider_name)
            if not p:
                continue

            route_start = datetime.now()
            try:
                response = await p.complete(request)

                route = Route(
                    provider=provider_name,
                    model=response.model,
                    success=True,
                    latency_ms=response.latency_ms,
                    cost=response.cost,
                )
                routes_tried.append(route)

                total_latency = int((datetime.now() - start_time).total_seconds() * 1000)
                total_cost = sum(r.cost for r in routes_tried)

                result = RouteResult(
                    response=response,
                    routes_tried=routes_tried,
                    final_provider=provider_name,
                    total_latency_ms=total_latency,
                    total_cost=total_cost,
                    success=True,
                )

                # Emit signal
                self._emit_signal(result.signal())

                # Track history
                self._history.append(result)

                return result

            except Exception as e:
                last_error = str(e)
                latency = int((datetime.now() - route_start).total_seconds() * 1000)
                route = Route(
                    provider=provider_name,
                    model=model or p.config.default_model,
                    success=False,
                    latency_ms=latency,
                    cost=0.0,
                    error=last_error,
                )
                routes_tried.append(route)
                continue

        # All providers failed
        total_latency = int((datetime.now() - start_time).total_seconds() * 1000)
        result = RouteResult(
            response=None,
            routes_tried=routes_tried,
            final_provider="none",
            total_latency_ms=total_latency,
            total_cost=0.0,
            success=False,
            error=last_error,
        )

        self._emit_signal(result.signal())
        self._history.append(result)

        return result

    async def complete_stream(
        self,
        prompt: Union[str, List[Message]],
        *,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """Stream a completion."""
        if isinstance(prompt, str):
            messages = [Message(role="user", content=prompt)]
        else:
            messages = prompt

        request = CompletionRequest(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )

        # Get provider
        if provider:
            p = self.providers.get(provider)
        else:
            ranked = self.strategy.rank_providers(
                list(self.providers.values()),
                request,
                ModelCapability.CHAT,
            )
            p = ranked[0].provider if ranked else None

        if not p:
            raise ValueError("No provider available")

        async for chunk in p.complete_stream(request):
            yield chunk

    async def embed(
        self,
        texts: Union[str, List[str]],
        *,
        model: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> EmbeddingResponse:
        """Generate embeddings."""
        if isinstance(texts, str):
            texts = [texts]

        request = EmbeddingRequest(texts=texts, model=model)

        # Get provider with embedding capability
        if provider:
            p = self.providers.get(provider)
        else:
            for name in ["openai", "ollama", "hailo"]:
                p = self.providers.get(name)
                if p and p.supports(ModelCapability.EMBEDDING):
                    break

        if not p:
            raise ValueError("No embedding provider available")

        return await p.embed(request)

    def _emit_signal(self, signal: str):
        """Emit a signal."""
        if self.signal_callback:
            self.signal_callback(signal)
        # Also print for visibility
        print(f"  {signal}")

    @property
    def stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        if not self._history:
            return {"total": 0, "success_rate": 0, "by_provider": {}, "total_cost": 0}

        successful = [r for r in self._history if r.success]
        by_provider: Dict[str, int] = {}
        total_cost = 0.0

        for r in self._history:
            by_provider[r.final_provider] = by_provider.get(r.final_provider, 0) + 1
            total_cost += r.total_cost

        return {
            "total": len(self._history),
            "success_rate": len(successful) / len(self._history),
            "by_provider": by_provider,
            "total_cost": total_cost,
            "avg_latency_ms": sum(r.total_latency_ms for r in self._history) / len(self._history),
        }


# Convenience function
async def complete(prompt: str, **kwargs) -> RouteResult:
    """Quick completion with default router."""
    router = Router()
    return await router.complete(prompt, **kwargs)
