"""
Base Provider - Abstract interface for all AI providers.

All providers implement this interface, making them interchangeable.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, AsyncIterator
from datetime import datetime


class ModelCapability(Enum):
    """What a model can do."""
    CHAT = "chat"                    # Conversational
    COMPLETION = "completion"        # Text completion
    CODE = "code"                    # Code generation
    VISION = "vision"                # Image understanding
    EMBEDDING = "embedding"          # Vector embeddings
    SPEECH_TO_TEXT = "speech_to_text"  # Audio transcription
    TEXT_TO_SPEECH = "text_to_speech"  # Voice synthesis
    IMAGE_GEN = "image_generation"   # Image creation


class ProviderStatus(Enum):
    """Provider health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


@dataclass
class ProviderConfig:
    """Configuration for a provider."""
    name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    enabled: bool = True

    # Cost tracking
    cost_per_1k_input: float = 0.0    # $ per 1000 input tokens
    cost_per_1k_output: float = 0.0   # $ per 1000 output tokens

    # Performance
    avg_latency_ms: int = 500         # Expected latency
    max_tokens: int = 4096            # Max context

    # Capabilities
    capabilities: List[ModelCapability] = field(default_factory=list)

    # Extra config
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """A message in a conversation."""
    role: str           # system, user, assistant
    content: str
    name: Optional[str] = None
    images: Optional[List[str]] = None  # Base64 or URLs for vision


@dataclass
class CompletionRequest:
    """Request for completion/chat."""
    messages: List[Message]
    model: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    stop: Optional[List[str]] = None
    stream: bool = False

    # Provider hints
    prefer_speed: bool = False
    prefer_quality: bool = False
    max_cost: Optional[float] = None  # Max $ to spend


@dataclass
class CompletionResponse:
    """Response from completion/chat."""
    content: str
    model: str
    provider: str

    # Usage
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    # Cost
    cost: float = 0.0

    # Timing
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Metadata
    finish_reason: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingRequest:
    """Request for embeddings."""
    texts: List[str]
    model: Optional[str] = None


@dataclass
class EmbeddingResponse:
    """Response with embeddings."""
    embeddings: List[List[float]]
    model: str
    provider: str
    dimensions: int
    total_tokens: int = 0
    cost: float = 0.0
    latency_ms: int = 0


class Provider(ABC):
    """
    Abstract base class for AI providers.

    All providers must implement:
    - complete(): Chat/completion
    - embed(): Generate embeddings (if supported)
    - health_check(): Check if provider is available
    """

    def __init__(self, config: ProviderConfig):
        self.config = config
        self.name = config.name
        self._status = ProviderStatus.UNKNOWN
        self._last_check: Optional[datetime] = None
        self._error_count = 0

    @property
    def status(self) -> ProviderStatus:
        """Current provider status."""
        return self._status

    @property
    def is_available(self) -> bool:
        """Is provider currently available?"""
        return self._status in (ProviderStatus.HEALTHY, ProviderStatus.DEGRADED)

    @property
    def capabilities(self) -> List[ModelCapability]:
        """What this provider can do."""
        return self.config.capabilities

    def supports(self, capability: ModelCapability) -> bool:
        """Check if provider supports a capability."""
        return capability in self.capabilities

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """
        Generate a completion/chat response.

        Args:
            request: The completion request

        Returns:
            CompletionResponse with generated text
        """
        pass

    @abstractmethod
    async def complete_stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[str]:
        """
        Stream a completion response.

        Args:
            request: The completion request

        Yields:
            Text chunks as they arrive
        """
        pass

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """
        Generate embeddings for text.

        Args:
            request: The embedding request

        Returns:
            EmbeddingResponse with vectors
        """
        raise NotImplementedError(f"{self.name} does not support embeddings")

    @abstractmethod
    async def health_check(self) -> ProviderStatus:
        """
        Check if provider is healthy.

        Returns:
            Current provider status
        """
        pass

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model: Optional[str] = None
    ) -> float:
        """Calculate cost for token usage."""
        input_cost = (input_tokens / 1000) * self.config.cost_per_1k_input
        output_cost = (output_tokens / 1000) * self.config.cost_per_1k_output
        return input_cost + output_cost

    def record_error(self):
        """Record an error for health tracking."""
        self._error_count += 1
        if self._error_count >= 3:
            self._status = ProviderStatus.DEGRADED
        if self._error_count >= 5:
            self._status = ProviderStatus.UNAVAILABLE

    def record_success(self):
        """Record a success, reset error count."""
        self._error_count = max(0, self._error_count - 1)
        if self._error_count == 0:
            self._status = ProviderStatus.HEALTHY

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, status={self.status.value})"
