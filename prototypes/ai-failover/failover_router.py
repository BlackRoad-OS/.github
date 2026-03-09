"""
Failover Router
Routes AI requests through a priority-ordered chain of providers.
If the primary fails, automatically cascades to the next available provider.
"""

import time
import asyncio
import json
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from config import ProviderConfig, ROUTER_CONFIG
from provider import AIProvider, ProviderError
from circuit_breaker import CircuitState


@dataclass
class RouteResult:
    """Result of a routed request."""
    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    latency: float
    cost: float
    attempts: int
    failed_providers: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "provider": self.provider,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "latency": round(self.latency, 3),
            "cost": round(self.cost, 6),
            "attempts": self.attempts,
            "failed_providers": self.failed_providers,
        }


@dataclass
class QueuedRequest:
    """A request waiting in the retry queue."""
    prompt: str
    system: Optional[str]
    max_tokens: int
    temperature: float
    created_at: float
    attempts: int = 0


class FailoverRouter:
    """
    Routes requests through a chain of AI providers with automatic failover.

    Usage:
        router = FailoverRouter(provider_configs)
        result = await router.route("What is BlackRoad?")
        print(result.text)
        print(f"Served by: {result.provider}")
    """

    def __init__(self, provider_configs: list[ProviderConfig]):
        # Sort by priority (lower = higher priority)
        sorted_configs = sorted(provider_configs, key=lambda c: c.priority)
        self.providers = [AIProvider(cfg) for cfg in sorted_configs]
        self.queue: deque[QueuedRequest] = deque(
            maxlen=ROUTER_CONFIG["queue_max_size"]
        )
        self._route_log: list[dict] = []
        self._total_routes = 0
        self._total_failovers = 0

    async def route(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        preferred_provider: Optional[str] = None,
        required_tags: Optional[list[str]] = None,
    ) -> RouteResult:
        """
        Route a request through the failover chain.

        Args:
            prompt: The user prompt
            system: Optional system prompt
            max_tokens: Max tokens for response
            temperature: Sampling temperature
            preferred_provider: Name of preferred provider (skips priority order)
            required_tags: Only use providers with ALL of these tags

        Returns:
            RouteResult with response and metadata

        Raises:
            AllProvidersFailedError: If no provider could handle the request
        """
        start = time.time()
        self._total_routes += 1

        # Build candidate list
        candidates = self._select_candidates(preferred_provider, required_tags)

        if not candidates:
            raise AllProvidersFailedError(
                "No available providers matching criteria",
                tried=[],
            )

        # Try each candidate in order
        failed = []
        attempts = 0

        for provider in candidates:
            if not provider.is_available:
                failed.append({
                    "provider": provider.name,
                    "reason": f"circuit_{provider.circuit.state.value}",
                })
                continue

            attempts += 1
            try:
                result = await provider.complete(
                    prompt=prompt,
                    system=system,
                    max_tokens=max_tokens or provider.config.max_tokens_default,
                    temperature=temperature,
                )

                route_result = RouteResult(
                    text=result["text"],
                    provider=result["provider"],
                    model=result["model"],
                    input_tokens=result["input_tokens"],
                    output_tokens=result["output_tokens"],
                    latency=time.time() - start,
                    cost=provider._calculate_cost(
                        result["input_tokens"], result["output_tokens"]
                    ),
                    attempts=attempts,
                    failed_providers=[f["provider"] for f in failed],
                )

                if failed:
                    self._total_failovers += 1

                self._log_route(route_result)
                return route_result

            except ProviderError as e:
                failed.append({
                    "provider": provider.name,
                    "reason": str(e),
                    "latency": e.latency,
                })
                continue

        # All providers failed
        raise AllProvidersFailedError(
            f"All {len(candidates)} providers failed",
            tried=failed,
        )

    def _select_candidates(
        self,
        preferred: Optional[str],
        required_tags: Optional[list[str]],
    ) -> list[AIProvider]:
        """Select and order candidate providers."""
        candidates = list(self.providers)

        # Filter by tags if specified
        if required_tags:
            candidates = [
                p for p in candidates
                if all(tag in p.config.tags for tag in required_tags)
            ]

        # Move preferred provider to front
        if preferred:
            pref = [p for p in candidates if p.name == preferred]
            rest = [p for p in candidates if p.name != preferred]
            candidates = pref + rest

        return candidates

    def _log_route(self, result: RouteResult) -> None:
        """Log a routing decision."""
        entry = {
            "timestamp": time.time(),
            "provider": result.provider,
            "model": result.model,
            "latency": result.latency,
            "attempts": result.attempts,
            "failed_providers": result.failed_providers,
            "tokens": result.input_tokens + result.output_tokens,
            "cost": result.cost,
        }
        self._route_log.append(entry)
        # Keep last 1000 entries
        if len(self._route_log) > 1000:
            self._route_log = self._route_log[-1000:]

    async def health_check_all(self) -> dict:
        """Run health checks on all providers concurrently."""
        tasks = [p.health_check() for p in self.providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            p.name: r if isinstance(r, bool) else False
            for p, r in zip(self.providers, results)
        }

    def status(self) -> dict:
        """Get router status and all provider states."""
        available = [p for p in self.providers if p.is_available]
        return {
            "total_routes": self._total_routes,
            "total_failovers": self._total_failovers,
            "failover_rate": (
                self._total_failovers / self._total_routes
                if self._total_routes > 0
                else 0.0
            ),
            "available_providers": len(available),
            "total_providers": len(self.providers),
            "queue_size": len(self.queue),
            "providers": [p.to_dict() for p in self.providers],
            "recent_routes": self._route_log[-10:],
        }

    def status_summary(self) -> str:
        """Human-readable status summary."""
        s = self.status()
        lines = [
            "╔══════════════════════════════════════╗",
            "║     AI FAILOVER ROUTER STATUS        ║",
            "╠══════════════════════════════════════╣",
            f"║  Routes: {s['total_routes']:<8} Failovers: {s['total_failovers']:<6}║",
            f"║  Available: {s['available_providers']}/{s['total_providers']} providers"
            + " " * (14 - len(str(s['available_providers'])) - len(str(s['total_providers'])))
            + "║",
            "╠══════════════════════════════════════╣",
        ]

        for p in s["providers"]:
            state_icon = {
                "closed": "[OK]",
                "open": "[!!]",
                "half_open": "[??]",
            }.get(p["circuit"]["state"], "[--]")

            lines.append(
                f"║  {state_icon} {p['name'][:20]:<20} "
                f"P{p['priority']} "
                f"${p['metrics']['total_cost']:.2f}"
                + " ║"
            )

        lines.append("╚══════════════════════════════════════╝")
        return "\n".join(lines)


class AllProvidersFailedError(Exception):
    """All providers in the chain failed."""

    def __init__(self, message: str, tried: list[dict]):
        self.tried = tried
        super().__init__(message)


# ── CLI Demo ────────────────────────────────────────────────────────

async def demo():
    """Demo the failover router."""
    from config import DEFAULT_PROVIDERS

    print("BlackRoad AI Failover Router")
    print("=" * 40)

    router = FailoverRouter(DEFAULT_PROVIDERS)
    print(router.status_summary())
    print()
    print("Provider chain loaded:")
    for p in router.providers:
        print(f"  {p.priority}. {p.name} ({p.config.model})")

    print()
    print("To route a request:")
    print('  result = await router.route("Your prompt here")')
    print()
    print("The router will try each provider in priority order.")
    print("If one fails, it cascades to the next automatically.")


if __name__ == "__main__":
    asyncio.run(demo())
