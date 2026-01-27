"""
OpenAI Provider - GPT-4, GPT-3.5, embeddings, and more.

The heavyweight champion of cloud AI.
"""

import os
import time
from typing import Optional, AsyncIterator, Dict, Any, List
from dataclasses import dataclass

from .base import (
    Provider,
    ProviderConfig,
    ProviderStatus,
    ModelCapability,
    CompletionRequest,
    CompletionResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    Message,
)


# Model configurations
OPENAI_MODELS = {
    # GPT-4 family
    "gpt-4o": {
        "cost_input": 0.005,      # $5 per 1M tokens
        "cost_output": 0.015,     # $15 per 1M tokens
        "max_tokens": 128000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "gpt-4o-mini": {
        "cost_input": 0.00015,    # $0.15 per 1M tokens
        "cost_output": 0.0006,    # $0.60 per 1M tokens
        "max_tokens": 128000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "gpt-4-turbo": {
        "cost_input": 0.01,
        "cost_output": 0.03,
        "max_tokens": 128000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    # GPT-3.5
    "gpt-3.5-turbo": {
        "cost_input": 0.0005,
        "cost_output": 0.0015,
        "max_tokens": 16385,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    # Embeddings
    "text-embedding-3-small": {
        "cost_input": 0.00002,
        "cost_output": 0.0,
        "max_tokens": 8191,
        "dimensions": 1536,
        "capabilities": [ModelCapability.EMBEDDING],
    },
    "text-embedding-3-large": {
        "cost_input": 0.00013,
        "cost_output": 0.0,
        "max_tokens": 8191,
        "dimensions": 3072,
        "capabilities": [ModelCapability.EMBEDDING],
    },
}


def default_config() -> ProviderConfig:
    """Default OpenAI configuration."""
    return ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.openai.com/v1",
        default_model="gpt-4o-mini",
        timeout=60,
        max_retries=3,
        cost_per_1k_input=0.00015,   # gpt-4o-mini default
        cost_per_1k_output=0.0006,
        avg_latency_ms=800,
        max_tokens=128000,
        capabilities=[
            ModelCapability.CHAT,
            ModelCapability.CODE,
            ModelCapability.VISION,
            ModelCapability.EMBEDDING,
        ],
    )


class OpenAIProvider(Provider):
    """
    OpenAI API provider.

    Supports:
    - GPT-4o, GPT-4o-mini, GPT-4-turbo
    - GPT-3.5-turbo
    - text-embedding-3-small/large

    Usage:
        provider = OpenAIProvider()
        response = await provider.complete(request)
    """

    def __init__(self, config: Optional[ProviderConfig] = None):
        super().__init__(config or default_config())
        self._client = None

    @property
    def client(self):
        """Lazy-load the OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.base_url,
                    timeout=self.config.timeout,
                    max_retries=self.config.max_retries,
                )
            except ImportError:
                raise ImportError("openai package required: pip install openai")
        return self._client

    def _format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Convert our Message format to OpenAI format."""
        formatted = []
        for msg in messages:
            entry: Dict[str, Any] = {
                "role": msg.role,
            }

            # Handle vision (images)
            if msg.images:
                content = [{"type": "text", "text": msg.content}]
                for img in msg.images:
                    if img.startswith("http"):
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": img}
                        })
                    else:
                        # Assume base64
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img}"}
                        })
                entry["content"] = content
            else:
                entry["content"] = msg.content

            if msg.name:
                entry["name"] = msg.name

            formatted.append(entry)

        return formatted

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Generate a chat completion."""
        model = request.model or self.config.default_model
        start_time = time.time()

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=self._format_messages(request.messages),
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stop=request.stop,
                stream=False,
            )

            latency_ms = int((time.time() - start_time) * 1000)

            # Extract usage
            usage = response.usage
            input_tokens = usage.prompt_tokens if usage else 0
            output_tokens = usage.completion_tokens if usage else 0

            # Calculate cost based on model
            model_info = OPENAI_MODELS.get(model, {})
            cost_input = model_info.get("cost_input", self.config.cost_per_1k_input)
            cost_output = model_info.get("cost_output", self.config.cost_per_1k_output)
            cost = (input_tokens / 1000 * cost_input) + (output_tokens / 1000 * cost_output)

            self.record_success()

            return CompletionResponse(
                content=response.choices[0].message.content or "",
                model=model,
                provider=self.name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                cost=cost,
                latency_ms=latency_ms,
                finish_reason=response.choices[0].finish_reason,
                raw_response=response.model_dump(),
            )

        except Exception as e:
            self.record_error()
            raise

    async def complete_stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[str]:
        """Stream a chat completion."""
        model = request.model or self.config.default_model

        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=self._format_messages(request.messages),
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stop=request.stop,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            self.record_success()

        except Exception as e:
            self.record_error()
            raise

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings."""
        model = request.model or "text-embedding-3-small"
        start_time = time.time()

        try:
            response = await self.client.embeddings.create(
                model=model,
                input=request.texts,
            )

            latency_ms = int((time.time() - start_time) * 1000)

            # Extract embeddings
            embeddings = [item.embedding for item in response.data]
            dimensions = len(embeddings[0]) if embeddings else 0
            total_tokens = response.usage.total_tokens if response.usage else 0

            # Calculate cost
            model_info = OPENAI_MODELS.get(model, {})
            cost_input = model_info.get("cost_input", 0.00002)
            cost = total_tokens / 1000 * cost_input

            self.record_success()

            return EmbeddingResponse(
                embeddings=embeddings,
                model=model,
                provider=self.name,
                dimensions=dimensions,
                total_tokens=total_tokens,
                cost=cost,
                latency_ms=latency_ms,
            )

        except Exception as e:
            self.record_error()
            raise

    async def health_check(self) -> ProviderStatus:
        """Check if OpenAI is reachable."""
        try:
            # Simple models list call
            await self.client.models.list()
            self._status = ProviderStatus.HEALTHY
        except Exception:
            self._status = ProviderStatus.UNAVAILABLE

        return self._status
