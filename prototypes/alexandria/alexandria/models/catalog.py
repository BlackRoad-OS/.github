"""
Model Catalog - The collection of all available models.

Every model has:
- Name and provider (ollama, openai, anthropic, hailo)
- Domains it excels at
- Capabilities (reasoning, coding, creative, etc.)
- Resource requirements
- When to use it
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class ModelCapability(Enum):
    """What a model can do."""
    # Reasoning
    REASONING = "reasoning"
    LOGIC = "logic"
    MATH = "math"
    ANALYSIS = "analysis"

    # Creative
    CREATIVE = "creative"
    WRITING = "writing"
    POETRY = "poetry"
    STORYTELLING = "storytelling"

    # Technical
    CODING = "coding"
    ARCHITECTURE = "architecture"
    DEBUGGING = "debugging"

    # Language
    TRANSLATION = "translation"
    GRAMMAR = "grammar"
    SUMMARIZATION = "summarization"

    # Visual
    VISION = "vision"
    IMAGE_UNDERSTANDING = "image_understanding"
    DIAGRAM_READING = "diagram_reading"

    # Specialized
    SCIENCE = "science"
    RESEARCH = "research"
    LEGAL = "legal"
    MEDICAL = "medical"
    FINANCIAL = "financial"

    # Conversational
    CHAT = "chat"
    ROLEPLAY = "roleplay"
    INSTRUCTION = "instruction"

    # Fast/Efficient
    FAST = "fast"
    EMBEDDING = "embedding"


@dataclass
class Model:
    """A model in the catalog."""
    name: str
    provider: str  # ollama, openai, anthropic, hailo, local
    description: str
    capabilities: List[ModelCapability]
    domains: List[str]
    size: str  # 1B, 7B, 13B, 70B, etc.
    context_length: int = 4096
    quantization: Optional[str] = None  # q4_0, q8_0, fp16
    requires_gpu: bool = False
    memory_gb: float = 4.0
    speed: str = "medium"  # fast, medium, slow
    quality: str = "good"  # basic, good, excellent, sota
    use_when: str = ""
    avoid_when: str = ""
    tags: List[str] = field(default_factory=list)


# =============================================================================
# THE MODEL CATALOG
# =============================================================================

MODELS: List[Model] = [
    # =========================================================================
    # OLLAMA - General Purpose
    # =========================================================================
    Model(
        name="llama3.2:3b",
        provider="ollama",
        description="Fast, efficient general model. Great for quick tasks.",
        capabilities=[ModelCapability.CHAT, ModelCapability.INSTRUCTION, ModelCapability.FAST],
        domains=["general", "chat", "quick-tasks"],
        size="3B",
        context_length=128000,
        memory_gb=2.0,
        speed="fast",
        quality="good",
        use_when="Need quick responses, simple tasks, or running on limited hardware",
        avoid_when="Complex reasoning, long documents, or specialized domains",
        tags=["general", "fast", "lightweight"],
    ),
    Model(
        name="llama3.2:1b",
        provider="ollama",
        description="Ultra-light model for edge devices and quick lookups.",
        capabilities=[ModelCapability.CHAT, ModelCapability.FAST],
        domains=["general", "edge", "mobile"],
        size="1B",
        context_length=128000,
        memory_gb=1.0,
        speed="fast",
        quality="basic",
        use_when="Edge devices, Raspberry Pi, quick classifications",
        avoid_when="Anything requiring quality or reasoning",
        tags=["edge", "mobile", "pi"],
    ),
    Model(
        name="llama3.1:8b",
        provider="ollama",
        description="Balanced general model with good reasoning.",
        capabilities=[ModelCapability.CHAT, ModelCapability.REASONING, ModelCapability.INSTRUCTION],
        domains=["general", "reasoning", "coding"],
        size="8B",
        context_length=128000,
        memory_gb=5.0,
        speed="medium",
        quality="good",
        use_when="General tasks requiring decent reasoning",
        avoid_when="Very specialized domains or maximum quality needed",
        tags=["general", "balanced"],
    ),
    Model(
        name="llama3.1:70b",
        provider="ollama",
        description="Large, powerful model for complex reasoning.",
        capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS, ModelCapability.CODING],
        domains=["general", "reasoning", "research", "coding"],
        size="70B",
        context_length=128000,
        memory_gb=40.0,
        requires_gpu=True,
        speed="slow",
        quality="excellent",
        use_when="Complex reasoning, research, important decisions",
        avoid_when="Quick tasks, limited hardware",
        tags=["powerful", "reasoning"],
    ),

    # =========================================================================
    # OLLAMA - Mathematics & Logic
    # =========================================================================
    Model(
        name="deepseek-r1:8b",
        provider="ollama",
        description="Reasoning model with chain-of-thought. Great for math and logic.",
        capabilities=[ModelCapability.REASONING, ModelCapability.MATH, ModelCapability.LOGIC],
        domains=["mathematics", "logic", "proofs", "puzzles"],
        size="8B",
        context_length=64000,
        memory_gb=5.0,
        speed="medium",
        quality="excellent",
        use_when="Math problems, logical reasoning, step-by-step thinking",
        avoid_when="Creative writing, casual chat",
        tags=["math", "reasoning", "logic"],
    ),
    Model(
        name="deepseek-r1:32b",
        provider="ollama",
        description="Larger reasoning model for complex mathematical proofs.",
        capabilities=[ModelCapability.REASONING, ModelCapability.MATH, ModelCapability.LOGIC, ModelCapability.SCIENCE],
        domains=["mathematics", "physics", "proofs", "research"],
        size="32B",
        context_length=64000,
        memory_gb=20.0,
        requires_gpu=True,
        speed="slow",
        quality="excellent",
        use_when="Complex proofs, advanced math, physics problems",
        avoid_when="Simple tasks, no GPU available",
        tags=["math", "physics", "research"],
    ),
    Model(
        name="qwen2.5:7b",
        provider="ollama",
        description="Strong math and coding abilities from Alibaba.",
        capabilities=[ModelCapability.MATH, ModelCapability.CODING, ModelCapability.REASONING],
        domains=["mathematics", "coding", "analysis"],
        size="7B",
        context_length=32000,
        memory_gb=4.5,
        speed="medium",
        quality="good",
        use_when="Math problems, code generation, analysis",
        avoid_when="Creative writing",
        tags=["math", "coding", "qwen"],
    ),
    Model(
        name="mathstral:7b",
        provider="ollama",
        description="Mistral model fine-tuned specifically for mathematics.",
        capabilities=[ModelCapability.MATH, ModelCapability.REASONING],
        domains=["mathematics", "algebra", "calculus", "statistics"],
        size="7B",
        context_length=32000,
        memory_gb=4.5,
        speed="medium",
        quality="excellent",
        use_when="Pure math problems, equations, proofs",
        avoid_when="Non-math tasks",
        tags=["math", "specialized"],
    ),

    # =========================================================================
    # OLLAMA - Coding & Technical
    # =========================================================================
    Model(
        name="codellama:7b",
        provider="ollama",
        description="Meta's code-specialized Llama model.",
        capabilities=[ModelCapability.CODING, ModelCapability.DEBUGGING],
        domains=["coding", "programming", "debugging"],
        size="7B",
        context_length=16000,
        memory_gb=4.5,
        speed="medium",
        quality="good",
        use_when="Code generation, debugging, code review",
        avoid_when="Non-coding tasks",
        tags=["code", "programming"],
    ),
    Model(
        name="codellama:34b",
        provider="ollama",
        description="Larger CodeLlama for complex programming tasks.",
        capabilities=[ModelCapability.CODING, ModelCapability.ARCHITECTURE, ModelCapability.DEBUGGING],
        domains=["coding", "architecture", "systems"],
        size="34B",
        context_length=16000,
        memory_gb=20.0,
        requires_gpu=True,
        speed="slow",
        quality="excellent",
        use_when="Complex codebases, architecture decisions, difficult bugs",
        avoid_when="Simple code tasks, no GPU",
        tags=["code", "architecture"],
    ),
    Model(
        name="deepseek-coder-v2:16b",
        provider="ollama",
        description="DeepSeek's code model with excellent completion.",
        capabilities=[ModelCapability.CODING, ModelCapability.DEBUGGING, ModelCapability.REASONING],
        domains=["coding", "programming", "algorithms"],
        size="16B",
        context_length=128000,
        memory_gb=10.0,
        speed="medium",
        quality="excellent",
        use_when="Code generation with reasoning, long files",
        avoid_when="Non-code tasks",
        tags=["code", "deepseek"],
    ),
    Model(
        name="starcoder2:7b",
        provider="ollama",
        description="BigCode's StarCoder for multi-language support.",
        capabilities=[ModelCapability.CODING],
        domains=["coding", "multi-language"],
        size="7B",
        context_length=16000,
        memory_gb=4.5,
        speed="medium",
        quality="good",
        use_when="Code in various languages",
        avoid_when="Non-code tasks",
        tags=["code", "multi-language"],
    ),

    # =========================================================================
    # OLLAMA - Creative & Writing
    # =========================================================================
    Model(
        name="mistral:7b",
        provider="ollama",
        description="Excellent creative writing and storytelling.",
        capabilities=[ModelCapability.CREATIVE, ModelCapability.WRITING, ModelCapability.CHAT],
        domains=["writing", "creative", "stories", "marketing"],
        size="7B",
        context_length=32000,
        memory_gb=4.5,
        speed="medium",
        quality="good",
        use_when="Creative writing, stories, marketing copy",
        avoid_when="Technical or math tasks",
        tags=["creative", "writing"],
    ),
    Model(
        name="mistral-nemo:12b",
        provider="ollama",
        description="Larger Mistral with better coherence for long-form writing.",
        capabilities=[ModelCapability.CREATIVE, ModelCapability.WRITING, ModelCapability.STORYTELLING],
        domains=["writing", "novels", "scripts", "content"],
        size="12B",
        context_length=128000,
        memory_gb=8.0,
        speed="medium",
        quality="excellent",
        use_when="Long-form content, novels, detailed writing",
        avoid_when="Quick tasks",
        tags=["creative", "long-form"],
    ),
    Model(
        name="gemma2:9b",
        provider="ollama",
        description="Google's Gemma - great for creative and instructional content.",
        capabilities=[ModelCapability.CREATIVE, ModelCapability.INSTRUCTION, ModelCapability.WRITING],
        domains=["writing", "education", "explanations"],
        size="9B",
        context_length=8000,
        memory_gb=6.0,
        speed="medium",
        quality="good",
        use_when="Educational content, explanations, creative writing",
        avoid_when="Very long context",
        tags=["creative", "education", "google"],
    ),
    Model(
        name="neural-chat:7b",
        provider="ollama",
        description="Intel's conversational model, natural dialogue.",
        capabilities=[ModelCapability.CHAT, ModelCapability.ROLEPLAY, ModelCapability.CREATIVE],
        domains=["chat", "roleplay", "conversation"],
        size="7B",
        context_length=8000,
        memory_gb=4.5,
        speed="medium",
        quality="good",
        use_when="Natural conversations, roleplay, character chat",
        avoid_when="Technical tasks",
        tags=["chat", "roleplay"],
    ),

    # =========================================================================
    # OLLAMA - Language & Translation
    # =========================================================================
    Model(
        name="aya:8b",
        provider="ollama",
        description="Cohere's multilingual model - 100+ languages.",
        capabilities=[ModelCapability.TRANSLATION, ModelCapability.CHAT],
        domains=["language", "translation", "multilingual"],
        size="8B",
        context_length=8000,
        memory_gb=5.0,
        speed="medium",
        quality="excellent",
        use_when="Translation, multilingual content, non-English",
        avoid_when="English-only tasks",
        tags=["multilingual", "translation"],
    ),
    Model(
        name="qwen2.5:14b",
        provider="ollama",
        description="Excellent Chinese-English bilingual capabilities.",
        capabilities=[ModelCapability.TRANSLATION, ModelCapability.REASONING, ModelCapability.CODING],
        domains=["language", "chinese", "bilingual", "coding"],
        size="14B",
        context_length=32000,
        memory_gb=9.0,
        speed="medium",
        quality="excellent",
        use_when="Chinese content, bilingual tasks",
        avoid_when="Other languages",
        tags=["chinese", "bilingual"],
    ),

    # =========================================================================
    # OLLAMA - Vision & Multimodal
    # =========================================================================
    Model(
        name="llava:7b",
        provider="ollama",
        description="Vision-language model - understands images.",
        capabilities=[ModelCapability.VISION, ModelCapability.IMAGE_UNDERSTANDING],
        domains=["vision", "images", "multimodal"],
        size="7B",
        context_length=4096,
        memory_gb=5.0,
        speed="medium",
        quality="good",
        use_when="Image understanding, visual questions",
        avoid_when="Text-only tasks",
        tags=["vision", "multimodal"],
    ),
    Model(
        name="llava:13b",
        provider="ollama",
        description="Larger vision model for detailed image analysis.",
        capabilities=[ModelCapability.VISION, ModelCapability.IMAGE_UNDERSTANDING, ModelCapability.DIAGRAM_READING],
        domains=["vision", "diagrams", "charts", "art"],
        size="13B",
        context_length=4096,
        memory_gb=8.0,
        speed="medium",
        quality="excellent",
        use_when="Detailed image analysis, diagrams, charts",
        avoid_when="Text-only, quick tasks",
        tags=["vision", "detailed"],
    ),
    Model(
        name="moondream:1.8b",
        provider="ollama",
        description="Tiny vision model for edge devices.",
        capabilities=[ModelCapability.VISION, ModelCapability.FAST],
        domains=["vision", "edge", "mobile"],
        size="1.8B",
        context_length=2048,
        memory_gb=1.5,
        speed="fast",
        quality="basic",
        use_when="Quick image checks on limited hardware",
        avoid_when="Detailed analysis needed",
        tags=["vision", "edge", "tiny"],
    ),

    # =========================================================================
    # OLLAMA - Science & Research
    # =========================================================================
    Model(
        name="meditron:7b",
        provider="ollama",
        description="Medical/clinical knowledge model.",
        capabilities=[ModelCapability.MEDICAL, ModelCapability.SCIENCE],
        domains=["medical", "health", "clinical"],
        size="7B",
        context_length=4096,
        memory_gb=4.5,
        speed="medium",
        quality="good",
        use_when="Medical questions, health information (NOT diagnosis)",
        avoid_when="Non-medical, actual medical advice",
        tags=["medical", "specialized"],
    ),
    Model(
        name="sqlcoder:7b",
        provider="ollama",
        description="SQL query generation specialist.",
        capabilities=[ModelCapability.CODING],
        domains=["sql", "databases", "queries"],
        size="7B",
        context_length=8000,
        memory_gb=4.5,
        speed="medium",
        quality="excellent",
        use_when="SQL queries, database questions",
        avoid_when="Non-SQL tasks",
        tags=["sql", "database", "specialized"],
    ),

    # =========================================================================
    # OLLAMA - Embeddings & Fast
    # =========================================================================
    Model(
        name="nomic-embed-text",
        provider="ollama",
        description="Fast text embeddings for search and retrieval.",
        capabilities=[ModelCapability.EMBEDDING, ModelCapability.FAST],
        domains=["embeddings", "search", "similarity"],
        size="137M",
        context_length=8192,
        memory_gb=0.5,
        speed="fast",
        quality="good",
        use_when="Text embeddings, semantic search",
        avoid_when="Generation tasks",
        tags=["embedding", "search"],
    ),
    Model(
        name="all-minilm",
        provider="ollama",
        description="Tiny embedding model for quick similarity.",
        capabilities=[ModelCapability.EMBEDDING, ModelCapability.FAST],
        domains=["embeddings", "search"],
        size="23M",
        context_length=512,
        memory_gb=0.1,
        speed="fast",
        quality="basic",
        use_when="Quick embeddings, limited resources",
        avoid_when="Need high quality embeddings",
        tags=["embedding", "tiny"],
    ),
    Model(
        name="mxbai-embed-large",
        provider="ollama",
        description="High-quality embeddings from mixedbread.ai",
        capabilities=[ModelCapability.EMBEDDING],
        domains=["embeddings", "search", "rag"],
        size="335M",
        context_length=512,
        memory_gb=1.0,
        speed="fast",
        quality="excellent",
        use_when="High-quality RAG, semantic search",
        avoid_when="Generation",
        tags=["embedding", "rag"],
    ),

    # =========================================================================
    # OLLAMA - Specialized & Experimental
    # =========================================================================
    Model(
        name="phi3:mini",
        provider="ollama",
        description="Microsoft's efficient small model.",
        capabilities=[ModelCapability.REASONING, ModelCapability.FAST],
        domains=["general", "reasoning", "edge"],
        size="3.8B",
        context_length=4096,
        memory_gb=2.5,
        speed="fast",
        quality="good",
        use_when="Good reasoning on limited hardware",
        avoid_when="Very long context",
        tags=["efficient", "microsoft"],
    ),
    Model(
        name="tinyllama:1.1b",
        provider="ollama",
        description="Tiny model for experiments and edge.",
        capabilities=[ModelCapability.CHAT, ModelCapability.FAST],
        domains=["edge", "experiments", "testing"],
        size="1.1B",
        context_length=2048,
        memory_gb=0.8,
        speed="fast",
        quality="basic",
        use_when="Testing, experiments, Pi Zero",
        avoid_when="Production quality needed",
        tags=["tiny", "edge", "testing"],
    ),
    Model(
        name="wizard-math:7b",
        provider="ollama",
        description="Fine-tuned for mathematical reasoning.",
        capabilities=[ModelCapability.MATH, ModelCapability.REASONING],
        domains=["mathematics", "word-problems"],
        size="7B",
        context_length=4096,
        memory_gb=4.5,
        speed="medium",
        quality="excellent",
        use_when="Word problems, applied math",
        avoid_when="Pure proofs, non-math",
        tags=["math", "word-problems"],
    ),
    Model(
        name="stable-code:3b",
        provider="ollama",
        description="Stability AI's efficient code model.",
        capabilities=[ModelCapability.CODING, ModelCapability.FAST],
        domains=["coding", "autocomplete"],
        size="3B",
        context_length=16000,
        memory_gb=2.0,
        speed="fast",
        quality="good",
        use_when="Code completion, fast generation",
        avoid_when="Complex architecture",
        tags=["code", "fast"],
    ),

    # =========================================================================
    # CLOUD PROVIDERS (for comparison/fallback)
    # =========================================================================
    Model(
        name="gpt-4o",
        provider="openai",
        description="OpenAI's flagship multimodal model.",
        capabilities=[
            ModelCapability.REASONING, ModelCapability.CODING, ModelCapability.CREATIVE,
            ModelCapability.VISION, ModelCapability.ANALYSIS
        ],
        domains=["general", "coding", "vision", "research"],
        size="unknown",
        context_length=128000,
        memory_gb=0,  # Cloud
        speed="medium",
        quality="sota",
        use_when="Maximum quality needed, multimodal tasks",
        avoid_when="Cost-sensitive, privacy-sensitive",
        tags=["cloud", "premium", "multimodal"],
    ),
    Model(
        name="gpt-4o-mini",
        provider="openai",
        description="Fast, affordable OpenAI model.",
        capabilities=[ModelCapability.REASONING, ModelCapability.CODING, ModelCapability.FAST],
        domains=["general", "coding"],
        size="unknown",
        context_length=128000,
        memory_gb=0,
        speed="fast",
        quality="good",
        use_when="Good cloud model at lower cost",
        avoid_when="Need maximum quality",
        tags=["cloud", "affordable"],
    ),
    Model(
        name="claude-3-5-sonnet",
        provider="anthropic",
        description="Anthropic's balanced model with strong coding.",
        capabilities=[
            ModelCapability.REASONING, ModelCapability.CODING, ModelCapability.CREATIVE,
            ModelCapability.ANALYSIS
        ],
        domains=["general", "coding", "research", "writing"],
        size="unknown",
        context_length=200000,
        memory_gb=0,
        speed="medium",
        quality="excellent",
        use_when="Complex reasoning, long context, coding",
        avoid_when="Cost-sensitive",
        tags=["cloud", "anthropic"],
    ),
    Model(
        name="claude-3-5-haiku",
        provider="anthropic",
        description="Fast Anthropic model for quick tasks.",
        capabilities=[ModelCapability.REASONING, ModelCapability.FAST, ModelCapability.CODING],
        domains=["general", "coding"],
        size="unknown",
        context_length=200000,
        memory_gb=0,
        speed="fast",
        quality="good",
        use_when="Quick cloud responses, good balance",
        avoid_when="Maximum quality needed",
        tags=["cloud", "fast", "anthropic"],
    ),
]


class ModelCatalog:
    """
    The catalog of all available models.

    Provides search, filtering, and recommendations.
    """

    def __init__(self):
        """Initialize the catalog."""
        self.models = {m.name: m for m in MODELS}
        self._by_domain: Dict[str, List[Model]] = {}
        self._by_capability: Dict[ModelCapability, List[Model]] = {}
        self._index()

    def _index(self):
        """Build indexes for fast lookup."""
        for model in MODELS:
            # Index by domain
            for domain in model.domains:
                if domain not in self._by_domain:
                    self._by_domain[domain] = []
                self._by_domain[domain].append(model)

            # Index by capability
            for cap in model.capabilities:
                if cap not in self._by_capability:
                    self._by_capability[cap] = []
                self._by_capability[cap].append(model)

    def get(self, name: str) -> Optional[Model]:
        """Get a model by name."""
        return self.models.get(name)

    def for_domain(self, domain: str) -> List[Model]:
        """Get models for a domain."""
        return self._by_domain.get(domain, [])

    def for_capability(self, capability: ModelCapability) -> List[Model]:
        """Get models with a capability."""
        return self._by_capability.get(capability, [])

    def for_provider(self, provider: str) -> List[Model]:
        """Get models from a provider."""
        return [m for m in MODELS if m.provider == provider]

    def local_only(self) -> List[Model]:
        """Get only local/Ollama models."""
        return [m for m in MODELS if m.provider in ("ollama", "local", "hailo")]

    def fast(self) -> List[Model]:
        """Get fast models."""
        return [m for m in MODELS if m.speed == "fast"]

    def search(
        self,
        query: Optional[str] = None,
        domain: Optional[str] = None,
        capability: Optional[ModelCapability] = None,
        provider: Optional[str] = None,
        max_memory_gb: Optional[float] = None,
        local_only: bool = False,
    ) -> List[Model]:
        """Search for models matching criteria."""
        results = list(MODELS)

        if domain:
            results = [m for m in results if domain in m.domains]

        if capability:
            results = [m for m in results if capability in m.capabilities]

        if provider:
            results = [m for m in results if m.provider == provider]

        if max_memory_gb:
            results = [m for m in results if m.memory_gb <= max_memory_gb]

        if local_only:
            results = [m for m in results if m.provider in ("ollama", "local", "hailo")]

        if query:
            query = query.lower()
            results = [
                m for m in results
                if query in m.name.lower() or query in m.description.lower()
                or any(query in t for t in m.tags)
            ]

        return results

    def recommend(
        self,
        task: str,
        local_only: bool = True,
        max_memory_gb: float = 8.0,
    ) -> List[Model]:
        """Recommend models for a task."""
        # Map common tasks to domains/capabilities
        task_lower = task.lower()

        if any(w in task_lower for w in ["math", "equation", "calculate", "proof"]):
            return self.search(domain="mathematics", local_only=local_only, max_memory_gb=max_memory_gb)

        if any(w in task_lower for w in ["code", "program", "function", "bug", "debug"]):
            return self.search(capability=ModelCapability.CODING, local_only=local_only, max_memory_gb=max_memory_gb)

        if any(w in task_lower for w in ["write", "story", "creative", "poem", "blog"]):
            return self.search(capability=ModelCapability.CREATIVE, local_only=local_only, max_memory_gb=max_memory_gb)

        if any(w in task_lower for w in ["translate", "language", "spanish", "french", "chinese"]):
            return self.search(domain="language", local_only=local_only, max_memory_gb=max_memory_gb)

        if any(w in task_lower for w in ["image", "picture", "photo", "diagram", "chart"]):
            return self.search(capability=ModelCapability.VISION, local_only=local_only, max_memory_gb=max_memory_gb)

        if any(w in task_lower for w in ["reason", "think", "analyze", "logic"]):
            return self.search(capability=ModelCapability.REASONING, local_only=local_only, max_memory_gb=max_memory_gb)

        if any(w in task_lower for w in ["embed", "search", "similar"]):
            return self.search(capability=ModelCapability.EMBEDDING, local_only=local_only, max_memory_gb=max_memory_gb)

        # Default: general balanced models
        return self.search(domain="general", local_only=local_only, max_memory_gb=max_memory_gb)

    def list_all(self) -> List[Model]:
        """List all models."""
        return MODELS

    def list_domains(self) -> List[str]:
        """List all domains."""
        return list(self._by_domain.keys())

    def stats(self) -> Dict[str, Any]:
        """Get catalog statistics."""
        return {
            "total_models": len(MODELS),
            "by_provider": {
                provider: len(self.for_provider(provider))
                for provider in set(m.provider for m in MODELS)
            },
            "domains": len(self._by_domain),
            "capabilities": len(self._by_capability),
            "local_models": len(self.local_only()),
        }
