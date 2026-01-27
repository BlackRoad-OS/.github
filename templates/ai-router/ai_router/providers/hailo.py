"""
Hailo Provider - On-device AI inference with Hailo-8.

26 TOPS of edge AI power. No cloud, no latency, no cost per token.
Runs on lucidia, octavia, and alice.
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


# Hailo-optimized models
HAILO_MODELS = {
    # Vision models
    "yolov8n": {
        "type": "vision",
        "task": "object_detection",
        "input_size": (640, 640),
        "capabilities": [ModelCapability.VISION],
    },
    "yolov8s": {
        "type": "vision",
        "task": "object_detection",
        "input_size": (640, 640),
        "capabilities": [ModelCapability.VISION],
    },
    # LLMs (quantized for Hailo)
    "llama-7b-q4": {
        "type": "llm",
        "max_tokens": 2048,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "phi-2-q4": {
        "type": "llm",
        "max_tokens": 2048,
        "capabilities": [ModelCapability.CHAT, ModelCapability.CODE],
    },
    "tinyllama-1b-q4": {
        "type": "llm",
        "max_tokens": 2048,
        "capabilities": [ModelCapability.CHAT],
    },
    # Speech
    "whisper-tiny": {
        "type": "speech",
        "task": "transcription",
        "capabilities": [ModelCapability.SPEECH_TO_TEXT],
    },
    # Embeddings
    "all-minilm-l6": {
        "type": "embedding",
        "dimensions": 384,
        "capabilities": [ModelCapability.EMBEDDING],
    },
}


def default_config() -> ProviderConfig:
    """Default Hailo configuration."""
    return ProviderConfig(
        name="hailo",
        api_key=None,  # No API key needed - local device
        base_url=os.getenv("HAILO_API_URL", "http://localhost:5000"),
        default_model="tinyllama-1b-q4",
        timeout=30,
        max_retries=1,  # Local, no point retrying much
        cost_per_1k_input=0.0,   # FREE - it's local!
        cost_per_1k_output=0.0,
        avg_latency_ms=100,      # Fast - on device
        max_tokens=2048,
        capabilities=[
            ModelCapability.CHAT,
            ModelCapability.CODE,
            ModelCapability.VISION,
            ModelCapability.EMBEDDING,
            ModelCapability.SPEECH_TO_TEXT,
        ],
        extra={
            "device": os.getenv("HAILO_DEVICE", "/dev/hailo0"),
            "node": os.getenv("NODE_NAME", "unknown"),
        }
    )


class HailoProvider(Provider):
    """
    Hailo-8 on-device inference provider.

    Runs models directly on the Hailo-8 AI accelerator.
    No cloud, no API costs, minimal latency.

    Supports:
    - Object detection (YOLOv8)
    - LLMs (quantized Llama, Phi, TinyLlama)
    - Speech-to-text (Whisper)
    - Embeddings (MiniLM)

    Usage:
        provider = HailoProvider()
        response = await provider.complete(request)

    Note: Requires hailo-platform SDK and a Hailo-8 device.
    """

    def __init__(self, config: Optional[ProviderConfig] = None):
        super().__init__(config or default_config())
        self._runtime = None
        self._models: Dict[str, Any] = {}

    @property
    def device(self) -> str:
        """Hailo device path."""
        return self.config.extra.get("device", "/dev/hailo0")

    @property
    def node(self) -> str:
        """Which node this is running on."""
        return self.config.extra.get("node", "unknown")

    def _get_runtime(self):
        """Get or create Hailo runtime."""
        if self._runtime is None:
            try:
                # Try to import hailo_platform
                # This would be the actual Hailo SDK
                # For now, we'll use a mock/HTTP approach
                import aiohttp
                self._runtime = "http"  # Use HTTP API to Hailo service
            except ImportError:
                self._runtime = "mock"
        return self._runtime

    async def _call_hailo_api(
        self,
        endpoint: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call the local Hailo inference API."""
        import aiohttp

        url = f"{self.config.base_url}/{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            ) as response:
                if response.status != 200:
                    raise Exception(f"Hailo API error: {response.status}")
                return await response.json()

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Generate a completion using on-device LLM."""
        model = request.model or self.config.default_model
        start_time = time.time()

        # Check if model is available on Hailo
        if model not in HAILO_MODELS:
            raise ValueError(f"Model {model} not available on Hailo")

        model_info = HAILO_MODELS[model]
        if model_info["type"] != "llm":
            raise ValueError(f"Model {model} is not an LLM")

        try:
            # Format messages into prompt
            prompt = self._format_prompt(request.messages)

            # Call Hailo inference service
            result = await self._call_hailo_api("v1/completions", {
                "model": model,
                "prompt": prompt,
                "max_tokens": min(request.max_tokens, model_info.get("max_tokens", 2048)),
                "temperature": request.temperature,
                "stop": request.stop,
            })

            latency_ms = int((time.time() - start_time) * 1000)

            self.record_success()

            return CompletionResponse(
                content=result.get("text", ""),
                model=model,
                provider=f"{self.name}@{self.node}",
                input_tokens=result.get("input_tokens", 0),
                output_tokens=result.get("output_tokens", 0),
                total_tokens=result.get("total_tokens", 0),
                cost=0.0,  # Free! On-device inference
                latency_ms=latency_ms,
                finish_reason=result.get("finish_reason", "stop"),
                raw_response=result,
            )

        except Exception as e:
            self.record_error()
            raise

    async def complete_stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[str]:
        """Stream a completion from on-device LLM."""
        model = request.model or self.config.default_model

        try:
            prompt = self._format_prompt(request.messages)

            # Stream from Hailo service
            import aiohttp
            url = f"{self.config.base_url}/v1/completions/stream"

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "model": model,
                        "prompt": prompt,
                        "max_tokens": request.max_tokens,
                        "temperature": request.temperature,
                    }
                ) as response:
                    async for line in response.content:
                        text = line.decode().strip()
                        if text:
                            yield text

            self.record_success()

        except Exception as e:
            self.record_error()
            raise

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings using on-device model."""
        model = request.model or "all-minilm-l6"
        start_time = time.time()

        try:
            result = await self._call_hailo_api("v1/embeddings", {
                "model": model,
                "texts": request.texts,
            })

            latency_ms = int((time.time() - start_time) * 1000)

            model_info = HAILO_MODELS.get(model, {})

            self.record_success()

            return EmbeddingResponse(
                embeddings=result.get("embeddings", []),
                model=model,
                provider=f"{self.name}@{self.node}",
                dimensions=model_info.get("dimensions", 384),
                total_tokens=result.get("total_tokens", 0),
                cost=0.0,  # Free!
                latency_ms=latency_ms,
            )

        except Exception as e:
            self.record_error()
            raise

    async def detect_objects(
        self,
        image: bytes,
        model: str = "yolov8n",
        confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Run object detection on an image.

        Returns list of detections with bounding boxes.
        """
        import base64

        result = await self._call_hailo_api("v1/detect", {
            "model": model,
            "image": base64.b64encode(image).decode(),
            "confidence_threshold": confidence,
        })

        return result.get("detections", [])

    async def transcribe(
        self,
        audio: bytes,
        model: str = "whisper-tiny"
    ) -> str:
        """Transcribe audio to text."""
        import base64

        result = await self._call_hailo_api("v1/transcribe", {
            "model": model,
            "audio": base64.b64encode(audio).decode(),
        })

        return result.get("text", "")

    async def health_check(self) -> ProviderStatus:
        """Check if Hailo device is available."""
        try:
            # Check device exists
            if os.path.exists(self.device):
                # Try API ping
                result = await self._call_hailo_api("health", {})
                if result.get("status") == "ok":
                    self._status = ProviderStatus.HEALTHY
                else:
                    self._status = ProviderStatus.DEGRADED
            else:
                self._status = ProviderStatus.UNAVAILABLE
        except Exception:
            self._status = ProviderStatus.UNAVAILABLE

        return self._status

    def _format_prompt(self, messages: List[Message]) -> str:
        """Format messages into a single prompt for the LLM."""
        parts = []
        for msg in messages:
            if msg.role == "system":
                parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                parts.append(f"Assistant: {msg.content}")

        parts.append("Assistant:")
        return "\n\n".join(parts)
