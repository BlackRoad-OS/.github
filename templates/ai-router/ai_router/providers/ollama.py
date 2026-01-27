"""
Ollama Provider - Local LLMs on any hardware.

Run Llama, Mistral, CodeLlama, and more locally.
No API costs, full privacy, works offline.
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
    EmbeddingRequest,
    EmbeddingResponse,
    Message,
)


# Common Ollama models
OLLAMA_MODELS = {
    # General purpose
    "llama3.2": {
        "size": "3B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "llama3.1": {
        "size": "8B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "llama3.1:70b": {
        "size": "70B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "mistral": {
        "size": "7B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "mixtral": {
        "size": "8x7B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "gemma2": {
        "size": "9B",
        "capabilities": [ModelCapability.CHAT],
    },
    # Code specialized
    "codellama": {
        "size": "7B",
        "capabilities": [ModelCapability.CODE],
    },
    "deepseek-coder": {
        "size": "6.7B",
        "capabilities": [ModelCapability.CODE],
    },
    "qwen2.5-coder": {
        "size": "7B",
        "capabilities": [ModelCapability.CODE],
    },
    # Small/fast
    "phi3": {
        "size": "3.8B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "tinyllama": {
        "size": "1.1B",
        "capabilities": [ModelCapability.CHAT],
    },
    # Embeddings
    "nomic-embed-text": {
        "size": "137M",
        "dimensions": 768,
        "capabilities": [ModelCapability.EMBEDDING],
    },
    "mxbai-embed-large": {
        "size": "335M",
        "dimensions": 1024,
        "capabilities": [ModelCapability.EMBEDDING],
    },
    # Vision
    "llava": {
        "size": "7B",
        "capabilities": [ModelCapability.CHAT, ModelCapability.VISION],
    },
}


def default_config() -> ProviderConfig:
    """Default Ollama configuration."""
    return ProviderConfig(
        name="ollama",
        api_key=None,  # No API key needed
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        default_model="llama3.2",
        timeout=120,  # Local models can be slow to start
        max_retries=2,
        cost_per_1k_input=0.0,   # FREE - local inference
        cost_per_1k_output=0.0,
        avg_latency_ms=500,
        max_tokens=4096,
        capabilities=[
            ModelCapability.CHAT,
            ModelCapability.CODE,
            ModelCapability.EMBEDDING,
            ModelCapability.VISION,
        ],
    )


class OllamaProvider(Provider):
    """
    Ollama local LLM provider.

    Runs models locally via Ollama. Free, private, offline-capable.

    Supports:
    - Llama 3.2, 3.1 (various sizes)
    - Mistral, Mixtral
    - CodeLlama, DeepSeek Coder
    - Phi-3, TinyLlama
    - Embeddings (nomic, mxbai)
    - Vision (LLaVA)

    Usage:
        provider = OllamaProvider()
        response = await provider.complete(request)

    Note: Requires Ollama installed and running.
    Install: https://ollama.ai
    """

    def __init__(self, config: Optional[ProviderConfig] = None):
        super().__init__(config or default_config())

    async def _call_api(
        self,
        endpoint: str,
        data: Dict[str, Any],
        stream: bool = False
    ) -> Any:
        """Call Ollama API."""
        import aiohttp

        url = f"{self.config.base_url}/{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            ) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"Ollama API error: {response.status} - {text}")

                if stream:
                    return response
                return await response.json()

    def _format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Convert messages to Ollama format."""
        formatted = []
        for msg in messages:
            entry = {
                "role": msg.role,
                "content": msg.content,
            }

            # Handle images for vision models
            if msg.images:
                entry["images"] = msg.images

            formatted.append(entry)

        return formatted

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Generate a chat completion."""
        model = request.model or self.config.default_model
        start_time = time.time()

        try:
            result = await self._call_api("api/chat", {
                "model": model,
                "messages": self._format_messages(request.messages),
                "stream": False,
                "options": {
                    "num_predict": request.max_tokens,
                    "temperature": request.temperature,
                    "stop": request.stop,
                }
            })

            latency_ms = int((time.time() - start_time) * 1000)

            # Extract tokens from response
            input_tokens = result.get("prompt_eval_count", 0)
            output_tokens = result.get("eval_count", 0)

            self.record_success()

            return CompletionResponse(
                content=result.get("message", {}).get("content", ""),
                model=model,
                provider=self.name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                cost=0.0,  # Free - local inference
                latency_ms=latency_ms,
                finish_reason=result.get("done_reason", "stop"),
                raw_response=result,
            )

        except Exception as e:
            self.record_error()
            raise

    async def complete_stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[str]:
        """Stream a chat completion."""
        model = request.model or self.config.default_model

        import aiohttp
        import json

        url = f"{self.config.base_url}/api/chat"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "model": model,
                        "messages": self._format_messages(request.messages),
                        "stream": True,
                        "options": {
                            "num_predict": request.max_tokens,
                            "temperature": request.temperature,
                            "stop": request.stop,
                        }
                    },
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                ) as response:
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line)
                                content = data.get("message", {}).get("content", "")
                                if content:
                                    yield content
                                if data.get("done"):
                                    break
                            except json.JSONDecodeError:
                                continue

            self.record_success()

        except Exception as e:
            self.record_error()
            raise

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings."""
        model = request.model or "nomic-embed-text"
        start_time = time.time()

        try:
            # Ollama embeds one text at a time
            embeddings = []
            for text in request.texts:
                result = await self._call_api("api/embeddings", {
                    "model": model,
                    "prompt": text,
                })
                embeddings.append(result.get("embedding", []))

            latency_ms = int((time.time() - start_time) * 1000)

            model_info = OLLAMA_MODELS.get(model, {})

            self.record_success()

            return EmbeddingResponse(
                embeddings=embeddings,
                model=model,
                provider=self.name,
                dimensions=model_info.get("dimensions", len(embeddings[0]) if embeddings else 0),
                total_tokens=0,  # Ollama doesn't report tokens for embeddings
                cost=0.0,
                latency_ms=latency_ms,
            )

        except Exception as e:
            self.record_error()
            raise

    async def health_check(self) -> ProviderStatus:
        """Check if Ollama is running."""
        try:
            import aiohttp

            url = f"{self.config.base_url}/api/tags"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        self._status = ProviderStatus.HEALTHY
                    else:
                        self._status = ProviderStatus.DEGRADED
        except Exception:
            self._status = ProviderStatus.UNAVAILABLE

        return self._status

    async def list_models(self) -> List[str]:
        """List available models."""
        try:
            import aiohttp

            url = f"{self.config.base_url}/api/tags"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    async def pull_model(self, model: str) -> bool:
        """Pull/download a model."""
        try:
            await self._call_api("api/pull", {"name": model})
            return True
        except Exception:
            return False
