"""
AI Provider Failover - Configuration
Default provider configs, priorities, and thresholds.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProviderConfig:
    """Configuration for a single AI provider."""
    name: str
    provider_type: str  # "claude", "openai", "llama", "custom"
    api_base: str
    api_key_env: str  # Environment variable name for API key
    model: str
    priority: int  # Lower = higher priority
    max_tokens_default: int = 1024
    timeout_seconds: float = 30.0
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    # Circuit breaker settings
    failure_threshold: int = 3
    recovery_timeout: float = 60.0
    half_open_max_calls: int = 1
    # Rate limits
    requests_per_minute: int = 60
    tokens_per_minute: int = 100_000
    # Tags for routing decisions
    tags: list = field(default_factory=list)

    @property
    def api_key(self) -> Optional[str]:
        return os.environ.get(self.api_key_env)


# ── Default Provider Chain ──────────────────────────────────────────

CLAUDE_CONFIG = ProviderConfig(
    name="claude-primary",
    provider_type="claude",
    api_base="https://api.anthropic.com/v1",
    api_key_env="ANTHROPIC_API_KEY",
    model="claude-sonnet-4-20250514",
    priority=1,
    max_tokens_default=1024,
    timeout_seconds=30.0,
    cost_per_1k_input=0.003,
    cost_per_1k_output=0.015,
    failure_threshold=3,
    recovery_timeout=60.0,
    requests_per_minute=60,
    tokens_per_minute=100_000,
    tags=["primary", "reasoning", "code", "analysis"],
)

GPT_CONFIG = ProviderConfig(
    name="gpt-secondary",
    provider_type="openai",
    api_base="https://api.openai.com/v1",
    api_key_env="OPENAI_API_KEY",
    model="gpt-4o",
    priority=2,
    max_tokens_default=1024,
    timeout_seconds=30.0,
    cost_per_1k_input=0.005,
    cost_per_1k_output=0.015,
    failure_threshold=3,
    recovery_timeout=60.0,
    requests_per_minute=60,
    tokens_per_minute=100_000,
    tags=["secondary", "general", "code"],
)

LLAMA_LOCAL_CONFIG = ProviderConfig(
    name="llama-local",
    provider_type="llama",
    api_base="http://octavia.local:11434/api",  # Ollama on Pi
    api_key_env="LLAMA_API_KEY",  # May be empty for local
    model="llama3:8b",
    priority=3,
    max_tokens_default=512,
    timeout_seconds=60.0,  # Local inference can be slower
    cost_per_1k_input=0.0,  # Free - own hardware
    cost_per_1k_output=0.0,
    failure_threshold=5,  # More lenient for local
    recovery_timeout=30.0,
    requests_per_minute=10,  # Pi is slower
    tokens_per_minute=10_000,
    tags=["local", "fallback", "private", "free"],
)

# ── The Chain ───────────────────────────────────────────────────────

DEFAULT_PROVIDERS = [CLAUDE_CONFIG, GPT_CONFIG, LLAMA_LOCAL_CONFIG]

# ── Router Settings ─────────────────────────────────────────────────

ROUTER_CONFIG = {
    "max_retries": 3,
    "retry_base_delay": 1.0,  # seconds
    "retry_max_delay": 16.0,
    "queue_max_size": 100,
    "queue_drain_interval": 5.0,  # seconds
    "health_check_interval": 30.0,  # seconds
    "log_level": "INFO",
}
