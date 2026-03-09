"""
AI Provider Abstraction
Unified interface for different AI providers (Claude, OpenAI, Llama/Ollama).
Each provider tracks its own health, latency, and cost metrics.
"""

import time
import json
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from circuit_breaker import CircuitBreaker
from config import ProviderConfig


@dataclass
class ProviderMetrics:
    """Runtime metrics for a provider."""
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    total_latency: float = 0.0
    latency_samples: list = field(default_factory=list)

    @property
    def avg_latency(self) -> float:
        if not self.latency_samples:
            return 0.0
        # Use last 20 samples for rolling average
        recent = self.latency_samples[-20:]
        return sum(recent) / len(recent)

    @property
    def p95_latency(self) -> float:
        if not self.latency_samples:
            return 0.0
        recent = sorted(self.latency_samples[-100:])
        idx = int(len(recent) * 0.95)
        return recent[min(idx, len(recent) - 1)]


class AIProvider:
    """
    Wraps an AI provider with health tracking, circuit breaking,
    and unified request interface.
    """

    def __init__(self, config: ProviderConfig):
        self.config = config
        self.circuit = CircuitBreaker(
            name=config.name,
            failure_threshold=config.failure_threshold,
            recovery_timeout=config.recovery_timeout,
            half_open_max_calls=config.half_open_max_calls,
        )
        self.metrics = ProviderMetrics()
        self._last_health_check: Optional[float] = None
        self._healthy = True

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def priority(self) -> int:
        return self.config.priority

    @property
    def is_available(self) -> bool:
        return self.circuit.is_available and self._healthy

    def score(self) -> float:
        """
        Calculate a routing score. Lower is better.
        Factors: priority, latency, cost, reliability.
        """
        priority_weight = self.config.priority * 10
        latency_weight = self.metrics.avg_latency * 2
        cost_weight = (self.config.cost_per_1k_input + self.config.cost_per_1k_output) * 100

        reliability = 1.0
        if self.metrics.total_requests > 0:
            success_rate = (
                self.circuit.stats.successful_requests / self.metrics.total_requests
            )
            reliability = (1 - success_rate) * 50  # Penalty for failures

        return priority_weight + latency_weight + cost_weight + reliability

    async def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
    ) -> dict:
        """
        Send a completion request to this provider.
        Returns: {"text": str, "input_tokens": int, "output_tokens": int, "latency": float}
        """
        max_tokens = max_tokens or self.config.max_tokens_default
        start = time.time()

        try:
            if self.config.provider_type == "claude":
                result = await self._complete_claude(prompt, system, max_tokens, temperature)
            elif self.config.provider_type == "openai":
                result = await self._complete_openai(prompt, system, max_tokens, temperature)
            elif self.config.provider_type == "llama":
                result = await self._complete_llama(prompt, system, max_tokens, temperature)
            else:
                raise ValueError(f"Unknown provider type: {self.config.provider_type}")

            latency = time.time() - start
            result["latency"] = latency

            # Track metrics
            self.metrics.total_requests += 1
            self.metrics.total_input_tokens += result.get("input_tokens", 0)
            self.metrics.total_output_tokens += result.get("output_tokens", 0)
            self.metrics.total_latency += latency
            self.metrics.latency_samples.append(latency)
            self.metrics.total_cost += self._calculate_cost(
                result.get("input_tokens", 0),
                result.get("output_tokens", 0),
            )

            self.circuit.record_success(latency)
            return result

        except Exception as e:
            latency = time.time() - start
            self.metrics.total_requests += 1
            self.circuit.record_failure(str(e))
            raise ProviderError(self.name, str(e), latency) from e

    async def _complete_claude(
        self, prompt: str, system: Optional[str], max_tokens: int, temperature: float
    ) -> dict:
        """Call Anthropic Claude API."""
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config.api_key or "",
            "anthropic-version": "2023-06-01",
        }
        body = {
            "model": self.config.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system

        data = await self._http_post(
            f"{self.config.api_base}/messages", headers, body
        )
        return {
            "text": data["content"][0]["text"],
            "input_tokens": data["usage"]["input_tokens"],
            "output_tokens": data["usage"]["output_tokens"],
            "model": data.get("model", self.config.model),
            "provider": self.name,
        }

    async def _complete_openai(
        self, prompt: str, system: Optional[str], max_tokens: int, temperature: float
    ) -> dict:
        """Call OpenAI API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key or ''}",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body = {
            "model": self.config.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        data = await self._http_post(
            f"{self.config.api_base}/chat/completions", headers, body
        )
        return {
            "text": data["choices"][0]["message"]["content"],
            "input_tokens": data["usage"]["prompt_tokens"],
            "output_tokens": data["usage"]["completion_tokens"],
            "model": data.get("model", self.config.model),
            "provider": self.name,
        }

    async def _complete_llama(
        self, prompt: str, system: Optional[str], max_tokens: int, temperature: float
    ) -> dict:
        """Call Ollama API (local Llama)."""
        headers = {"Content-Type": "application/json"}
        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        body = {
            "model": self.config.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        data = await self._http_post(
            f"{self.config.api_base}/generate", headers, body
        )
        return {
            "text": data.get("response", ""),
            "input_tokens": data.get("prompt_eval_count", 0),
            "output_tokens": data.get("eval_count", 0),
            "model": data.get("model", self.config.model),
            "provider": self.name,
        }

    async def _http_post(self, url: str, headers: dict, body: dict) -> dict:
        """Make an async HTTP POST request."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_post, url, headers, body)

    def _sync_post(self, url: str, headers: dict, body: dict) -> dict:
        """Synchronous HTTP POST."""
        req = Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(req, timeout=self.config.timeout_seconds) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise ProviderError(
                self.name,
                f"HTTP {e.code}: {error_body[:200]}",
            ) from e
        except URLError as e:
            raise ProviderError(self.name, f"Connection error: {e.reason}") from e

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a request."""
        input_cost = (input_tokens / 1000) * self.config.cost_per_1k_input
        output_cost = (output_tokens / 1000) * self.config.cost_per_1k_output
        return input_cost + output_cost

    async def health_check(self) -> bool:
        """Quick health check - send a minimal request."""
        try:
            result = await self.complete(
                prompt="Say OK",
                max_tokens=5,
                temperature=0.0,
            )
            self._healthy = bool(result.get("text"))
        except Exception:
            self._healthy = False
        self._last_health_check = time.time()
        return self._healthy

    def to_dict(self) -> dict:
        """Serialize provider state for monitoring."""
        return {
            "name": self.name,
            "type": self.config.provider_type,
            "model": self.config.model,
            "priority": self.priority,
            "available": self.is_available,
            "healthy": self._healthy,
            "score": round(self.score(), 2),
            "circuit": self.circuit.to_dict(),
            "metrics": {
                "total_requests": self.metrics.total_requests,
                "total_input_tokens": self.metrics.total_input_tokens,
                "total_output_tokens": self.metrics.total_output_tokens,
                "total_cost": round(self.metrics.total_cost, 4),
                "avg_latency": round(self.metrics.avg_latency, 3),
                "p95_latency": round(self.metrics.p95_latency, 3),
            },
        }


class ProviderError(Exception):
    """Raised when a provider request fails."""

    def __init__(self, provider: str, message: str, latency: float = 0.0):
        self.provider = provider
        self.latency = latency
        super().__init__(f"[{provider}] {message}")
