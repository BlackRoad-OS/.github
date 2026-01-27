"""
Anthropic Provider - Claude 3.5 Sonnet, Claude 3 Opus, and more.

The thoughtful alternative. Great for reasoning and code.
"""

import os
import time
from typing import Optional, AsyncIterator, Dict, Any, List

from .base import (
    Provider,
    ProviderConfig,
    ProviderStatus,
    ModelCapability,
    CompletionRequest,
    CompletionResponse,
    Message,
)


# Model configurations
ANTHROPIC_MODELS = {
    "claude-sonnet-4-20250514": {
        "cost_input": 0.003,      # $3 per 1M tokens
        "cost_output": 0.015,     # $15 per 1M tokens
        "max_tokens": 200000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "claude-opus-4-20250514": {
        "cost_input": 0.015,      # $15 per 1M tokens
        "cost_output": 0.075,     # $75 per 1M tokens
        "max_tokens": 200000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "claude-3-5-sonnet-20241022": {
        "cost_input": 0.003,
        "cost_output": 0.015,
        "max_tokens": 200000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "claude-3-5-haiku-20241022": {
        "cost_input": 0.0008,     # $0.80 per 1M tokens
        "cost_output": 0.004,     # $4 per 1M tokens
        "max_tokens": 200000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "claude-3-opus-20240229": {
        "cost_input": 0.015,
        "cost_output": 0.075,
        "max_tokens": 200000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE, ModelCapability.VISION],
    },
    "claude-3-haiku-20240307": {
        "cost_input": 0.00025,
        "cost_output": 0.00125,
        "max_tokens": 200000,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
}


def default_config() -> ProviderConfig:
    """Default Anthropic configuration."""
    return ProviderConfig(
        name="anthropic",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        base_url="https://api.anthropic.com",
        default_model="claude-3-5-haiku-20241022",
        timeout=60,
        max_retries=3,
        cost_per_1k_input=0.0008,   # haiku default
        cost_per_1k_output=0.004,
        avg_latency_ms=600,
        max_tokens=200000,
        capabilities=[
            ModelCapability.CHAT,
            ModelCapability.CODE,
            ModelCapability.VISION,
        ],
    )


class AnthropicProvider(Provider):
    """
    Anthropic API provider.

    Supports:
    - Claude Sonnet 4, Claude Opus 4
    - Claude 3.5 Sonnet, Claude 3.5 Haiku
    - Claude 3 Opus, Claude 3 Haiku

    Usage:
        provider = AnthropicProvider()
        response = await provider.complete(request)
    """

    def __init__(self, config: Optional[ProviderConfig] = None):
        super().__init__(config or default_config())
        self._client = None

    @property
    def client(self):
        """Lazy-load the Anthropic client."""
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
                self._client = AsyncAnthropic(
                    api_key=self.config.api_key,
                    timeout=self.config.timeout,
                    max_retries=self.config.max_retries,
                )
            except ImportError:
                raise ImportError("anthropic package required: pip install anthropic")
        return self._client

    def _format_messages(self, messages: List[Message]) -> tuple:
        """
        Convert our Message format to Anthropic format.

        Returns (system_prompt, messages_list)
        """
        system_prompt = None
        formatted = []

        for msg in messages:
            if msg.role == "system":
                system_prompt = msg.content
                continue

            entry: Dict[str, Any] = {
                "role": msg.role,
            }

            # Handle vision (images)
            if msg.images:
                content = []
                for img in msg.images:
                    if img.startswith("http"):
                        # Anthropic requires base64 for images
                        # In production, you'd fetch and encode
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": img,
                            }
                        })
                    else:
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": img,
                            }
                        })
                content.append({"type": "text", "text": msg.content})
                entry["content"] = content
            else:
                entry["content"] = msg.content

            formatted.append(entry)

        return system_prompt, formatted

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Generate a chat completion."""
        model = request.model or self.config.default_model
        start_time = time.time()

        system_prompt, messages = self._format_messages(request.messages)

        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            if request.stop:
                kwargs["stop_sequences"] = request.stop

            response = await self.client.messages.create(**kwargs)

            latency_ms = int((time.time() - start_time) * 1000)

            # Extract usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # Calculate cost based on model
            model_info = ANTHROPIC_MODELS.get(model, {})
            cost_input = model_info.get("cost_input", self.config.cost_per_1k_input)
            cost_output = model_info.get("cost_output", self.config.cost_per_1k_output)
            cost = (input_tokens / 1000 * cost_input) + (output_tokens / 1000 * cost_output)

            # Extract content
            content = ""
            for block in response.content:
                if hasattr(block, "text"):
                    content += block.text

            self.record_success()

            return CompletionResponse(
                content=content,
                model=model,
                provider=self.name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                cost=cost,
                latency_ms=latency_ms,
                finish_reason=response.stop_reason,
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

        system_prompt, messages = self._format_messages(request.messages)

        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            if request.stop:
                kwargs["stop_sequences"] = request.stop

            async with self.client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield text

            self.record_success()

        except Exception as e:
            self.record_error()
            raise

    async def health_check(self) -> ProviderStatus:
        """Check if Anthropic is reachable."""
        try:
            # Quick completion test
            await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "hi"}],
            )
            self._status = ProviderStatus.HEALTHY
        except Exception:
            self._status = ProviderStatus.UNAVAILABLE

        return self._status
