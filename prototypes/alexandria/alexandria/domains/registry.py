"""
Domain Registry - The categories of the Library.

Each domain is a realm of knowledge with:
- Description and philosophy
- Recommended models
- Templates for creation
- What agents can explore vs. what is immutable
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class DomainType(Enum):
    """Types of domains."""
    SCIENCE = "science"         # Math, physics, chemistry, biology
    CREATIVE = "creative"       # Art, music, writing, design
    TECHNICAL = "technical"     # Code, engineering, architecture
    BUSINESS = "business"       # Marketing, finance, operations
    LANGUAGE = "language"       # Translation, linguistics, communication
    WORLD = "world"             # 3D, games, simulations, VR
    RESEARCH = "research"       # Papers, analysis, synthesis
    PERSONAL = "personal"       # Notes, journals, self-expression


@dataclass
class Domain:
    """A domain of knowledge."""
    name: str
    code: str                   # Short code (MATH, PHY, ART, etc.)
    type: DomainType
    description: str
    philosophy: str             # The guiding principle
    recommended_models: List[str]  # Model names from catalog
    templates: List[str]        # Template names
    explore_paths: List[str]    # Where agents CAN explore
    immutable_paths: List[str]  # What agents CANNOT change
    tools: List[str]            # Available tools
    tags: List[str] = field(default_factory=list)


# =============================================================================
# THE DOMAIN REGISTRY
# =============================================================================

DOMAINS: List[Domain] = [
    # =========================================================================
    # SCIENCE DOMAINS
    # =========================================================================
    Domain(
        name="Mathematics",
        code="MATH",
        type=DomainType.SCIENCE,
        description="Numbers, proofs, equations, and the language of the universe.",
        philosophy="Mathematical truths are discovered, not invented. Respect the axioms.",
        recommended_models=[
            "deepseek-r1:8b",
            "mathstral:7b",
            "wizard-math:7b",
            "qwen2.5:7b",
        ],
        templates=["proof", "equation", "theorem", "problem-set"],
        explore_paths=[
            "work/math/**",
            "notebooks/math/**",
            "scratch/calculations/**",
        ],
        immutable_paths=[
            "templates/math/**",      # The templates themselves
            "axioms/**",              # Foundational axioms
            "constants/**",           # Mathematical constants
        ],
        tools=["wolfram", "sympy", "latex", "graphing"],
        tags=["proofs", "algebra", "calculus", "statistics", "geometry"],
    ),
    Domain(
        name="Physics",
        code="PHY",
        type=DomainType.SCIENCE,
        description="The laws governing matter, energy, space, and time.",
        philosophy="Nature doesn't care about our models. Observe, hypothesize, test.",
        recommended_models=[
            "deepseek-r1:32b",
            "deepseek-r1:8b",
            "llama3.1:70b",
        ],
        templates=["experiment", "simulation", "derivation", "lab-report"],
        explore_paths=[
            "work/physics/**",
            "simulations/**",
            "experiments/**",
        ],
        immutable_paths=[
            "templates/physics/**",
            "constants/physical/**",  # Speed of light, etc.
            "laws/**",                # Newton's laws, etc.
        ],
        tools=["simulation", "plotting", "units", "latex"],
        tags=["mechanics", "quantum", "relativity", "thermodynamics"],
    ),
    Domain(
        name="Chemistry",
        code="CHEM",
        type=DomainType.SCIENCE,
        description="The study of matter and its transformations.",
        philosophy="Everything is made of atoms. Understand the bonds.",
        recommended_models=[
            "deepseek-r1:8b",
            "llama3.1:8b",
        ],
        templates=["reaction", "molecule", "lab-protocol", "safety-sheet"],
        explore_paths=[
            "work/chemistry/**",
            "molecules/**",
            "reactions/**",
        ],
        immutable_paths=[
            "templates/chemistry/**",
            "periodic-table/**",
            "safety-data/**",
        ],
        tools=["molecule-viewer", "reaction-balancer", "periodic-table"],
        tags=["organic", "inorganic", "biochemistry", "reactions"],
    ),
    Domain(
        name="Biology",
        code="BIO",
        type=DomainType.SCIENCE,
        description="The study of life and living organisms.",
        philosophy="Life finds a way. Complexity emerges from simple rules.",
        recommended_models=[
            "llama3.1:8b",
            "meditron:7b",
        ],
        templates=["species", "pathway", "experiment", "observation"],
        explore_paths=[
            "work/biology/**",
            "observations/**",
            "data/**",
        ],
        immutable_paths=[
            "templates/biology/**",
            "taxonomy/**",
            "pathways/canonical/**",
        ],
        tools=["sequence-viewer", "pathway-mapper", "taxonomy-browser"],
        tags=["genetics", "ecology", "evolution", "cell-biology"],
    ),

    # =========================================================================
    # CREATIVE DOMAINS
    # =========================================================================
    Domain(
        name="Visual Art",
        code="ART",
        type=DomainType.CREATIVE,
        description="Drawing, painting, design, and visual expression.",
        philosophy="Art is not what you see, but what you make others see.",
        recommended_models=[
            "llava:13b",
            "mistral:7b",
            "gemma2:9b",
        ],
        templates=["canvas", "composition", "color-palette", "style-guide"],
        explore_paths=[
            "work/art/**",
            "sketches/**",
            "projects/**",
        ],
        immutable_paths=[
            "templates/art/**",       # The blank canvas template
            "styles/canonical/**",    # Classic style definitions
            "color-theory/**",        # Color fundamentals
        ],
        tools=["image-gen", "color-picker", "composition-grid"],
        tags=["drawing", "painting", "digital", "illustration", "design"],
    ),
    Domain(
        name="Music",
        code="MUS",
        type=DomainType.CREATIVE,
        description="Composition, sound, rhythm, and auditory expression.",
        philosophy="Music is the space between the notes.",
        recommended_models=[
            "mistral:7b",
            "mistral-nemo:12b",
        ],
        templates=["song", "composition", "chord-progression", "arrangement"],
        explore_paths=[
            "work/music/**",
            "compositions/**",
            "samples/**",
        ],
        immutable_paths=[
            "templates/music/**",
            "theory/scales/**",
            "theory/chords/**",
        ],
        tools=["midi", "audio-gen", "notation", "chord-analyzer"],
        tags=["composition", "production", "theory", "instruments"],
    ),
    Domain(
        name="Writing",
        code="WRIT",
        type=DomainType.CREATIVE,
        description="Stories, essays, poetry, and written expression.",
        philosophy="Write drunk, edit sober. First drafts are for discovery.",
        recommended_models=[
            "mistral-nemo:12b",
            "mistral:7b",
            "gemma2:9b",
            "neural-chat:7b",
        ],
        templates=["story", "essay", "poem", "script", "article", "novel-chapter"],
        explore_paths=[
            "work/writing/**",
            "drafts/**",
            "journals/**",
        ],
        immutable_paths=[
            "templates/writing/**",
            "style-guides/**",
            "grammar-rules/**",
        ],
        tools=["grammar-check", "word-count", "outline", "character-sheet"],
        tags=["fiction", "non-fiction", "poetry", "scripts", "blogs"],
    ),
    Domain(
        name="Design",
        code="DES",
        type=DomainType.CREATIVE,
        description="UI, UX, product design, and human-centered creation.",
        philosophy="Good design is invisible. Users don't notice it working.",
        recommended_models=[
            "llava:13b",
            "mistral:7b",
            "claude-3-5-sonnet",
        ],
        templates=["wireframe", "component", "design-system", "user-flow"],
        explore_paths=[
            "work/design/**",
            "mockups/**",
            "prototypes/**",
        ],
        immutable_paths=[
            "templates/design/**",
            "design-systems/core/**",
            "accessibility-guidelines/**",
        ],
        tools=["figma-export", "color-contrast", "spacing-calc"],
        tags=["ui", "ux", "product", "graphic", "branding"],
    ),

    # =========================================================================
    # TECHNICAL DOMAINS
    # =========================================================================
    Domain(
        name="Programming",
        code="CODE",
        type=DomainType.TECHNICAL,
        description="Software development, algorithms, and systems.",
        philosophy="Code is read more than written. Clarity over cleverness.",
        recommended_models=[
            "deepseek-coder-v2:16b",
            "codellama:34b",
            "codellama:7b",
            "starcoder2:7b",
        ],
        templates=["function", "class", "module", "api", "test", "cli"],
        explore_paths=[
            "src/**",
            "work/code/**",
            "experiments/**",
        ],
        immutable_paths=[
            "templates/code/**",
            "architecture/core/**",
            "standards/**",
        ],
        tools=["lsp", "debugger", "profiler", "git"],
        tags=["python", "javascript", "rust", "go", "systems"],
    ),
    Domain(
        name="Infrastructure",
        code="INFRA",
        type=DomainType.TECHNICAL,
        description="Cloud, servers, networks, and operations.",
        philosophy="Everything fails. Design for failure.",
        recommended_models=[
            "codellama:7b",
            "llama3.1:8b",
        ],
        templates=["terraform", "dockerfile", "k8s-manifest", "ci-pipeline"],
        explore_paths=[
            "infra/**",
            "deployments/**",
            "configs/**",
        ],
        immutable_paths=[
            "templates/infra/**",
            "security-policies/**",
            "network-topology/**",
        ],
        tools=["terraform", "docker", "kubectl", "ssh"],
        tags=["cloud", "devops", "networking", "security"],
    ),
    Domain(
        name="Data",
        code="DATA",
        type=DomainType.TECHNICAL,
        description="Databases, analytics, ML, and data engineering.",
        philosophy="Data is the new oil. But raw oil is useless.",
        recommended_models=[
            "sqlcoder:7b",
            "deepseek-coder-v2:16b",
            "qwen2.5:7b",
        ],
        templates=["schema", "query", "pipeline", "notebook", "model"],
        explore_paths=[
            "data/**",
            "notebooks/**",
            "models/**",
        ],
        immutable_paths=[
            "templates/data/**",
            "schemas/canonical/**",
            "privacy-rules/**",
        ],
        tools=["sql", "pandas", "spark", "jupyter"],
        tags=["sql", "analytics", "ml", "etl", "visualization"],
    ),

    # =========================================================================
    # BUSINESS DOMAINS
    # =========================================================================
    Domain(
        name="Marketing",
        code="MKT",
        type=DomainType.BUSINESS,
        description="Brand, campaigns, copy, and customer acquisition.",
        philosophy="Marketing is telling a story that spreads.",
        recommended_models=[
            "mistral:7b",
            "mistral-nemo:12b",
            "gemma2:9b",
        ],
        templates=["campaign", "ad-copy", "email", "landing-page", "social-post"],
        explore_paths=[
            "work/marketing/**",
            "campaigns/**",
            "content/**",
        ],
        immutable_paths=[
            "templates/marketing/**",
            "brand-guidelines/**",
            "compliance/**",
        ],
        tools=["analytics", "ab-test", "seo-checker"],
        tags=["content", "ads", "social", "email", "seo"],
    ),
    Domain(
        name="Finance",
        code="FIN",
        type=DomainType.BUSINESS,
        description="Accounting, investments, and financial planning.",
        philosophy="Cash flow is king. Revenue is vanity, profit is sanity.",
        recommended_models=[
            "deepseek-r1:8b",
            "qwen2.5:7b",
            "llama3.1:8b",
        ],
        templates=["budget", "forecast", "invoice", "report", "model"],
        explore_paths=[
            "work/finance/**",
            "reports/**",
            "projections/**",
        ],
        immutable_paths=[
            "templates/finance/**",
            "accounting-standards/**",
            "tax-rules/**",
        ],
        tools=["spreadsheet", "calculator", "chart"],
        tags=["accounting", "budgeting", "investing", "analysis"],
    ),
    Domain(
        name="Strategy",
        code="STRAT",
        type=DomainType.BUSINESS,
        description="Business planning, operations, and decision-making.",
        philosophy="Strategy is choosing what not to do.",
        recommended_models=[
            "llama3.1:70b",
            "deepseek-r1:8b",
            "claude-3-5-sonnet",
        ],
        templates=["business-plan", "okr", "swot", "roadmap", "decision-doc"],
        explore_paths=[
            "work/strategy/**",
            "plans/**",
            "decisions/**",
        ],
        immutable_paths=[
            "templates/strategy/**",
            "mission/**",
            "values/**",
        ],
        tools=["diagram", "timeline", "priority-matrix"],
        tags=["planning", "ops", "decisions", "leadership"],
    ),

    # =========================================================================
    # LANGUAGE DOMAINS
    # =========================================================================
    Domain(
        name="Translation",
        code="TRANS",
        type=DomainType.LANGUAGE,
        description="Converting meaning across languages.",
        philosophy="Translation is not about words, but meaning.",
        recommended_models=[
            "aya:8b",
            "qwen2.5:14b",
        ],
        templates=["translation", "glossary", "localization"],
        explore_paths=[
            "work/translation/**",
            "translations/**",
        ],
        immutable_paths=[
            "templates/translation/**",
            "glossaries/official/**",
        ],
        tools=["dictionary", "grammar-check", "cultural-notes"],
        tags=["multilingual", "localization", "interpretation"],
    ),
    Domain(
        name="Communication",
        code="COMM",
        type=DomainType.LANGUAGE,
        description="Emails, presentations, and effective communication.",
        philosophy="The single biggest problem in communication is the illusion that it has taken place.",
        recommended_models=[
            "mistral:7b",
            "gemma2:9b",
            "llama3.1:8b",
        ],
        templates=["email", "presentation", "memo", "proposal"],
        explore_paths=[
            "work/comms/**",
            "drafts/**",
        ],
        immutable_paths=[
            "templates/comms/**",
            "tone-guidelines/**",
        ],
        tools=["grammar-check", "tone-analyzer", "slide-maker"],
        tags=["email", "presentations", "writing", "speaking"],
    ),

    # =========================================================================
    # WORLD DOMAINS
    # =========================================================================
    Domain(
        name="3D & Games",
        code="3D",
        type=DomainType.WORLD,
        description="3D modeling, game development, and virtual worlds.",
        philosophy="Every pixel is a decision. Make it count.",
        recommended_models=[
            "codellama:7b",
            "llava:13b",
        ],
        templates=["scene", "model", "shader", "game-object", "level"],
        explore_paths=[
            "work/3d/**",
            "assets/**",
            "levels/**",
        ],
        immutable_paths=[
            "templates/3d/**",
            "core-shaders/**",
            "physics-engine/**",
        ],
        tools=["blender", "unity", "godot", "shader-editor"],
        tags=["modeling", "animation", "games", "vr", "ar"],
    ),
    Domain(
        name="Simulation",
        code="SIM",
        type=DomainType.WORLD,
        description="Simulating systems, behaviors, and scenarios.",
        philosophy="All models are wrong, but some are useful.",
        recommended_models=[
            "deepseek-r1:8b",
            "codellama:7b",
        ],
        templates=["simulation", "agent", "scenario", "experiment"],
        explore_paths=[
            "work/simulation/**",
            "scenarios/**",
            "results/**",
        ],
        immutable_paths=[
            "templates/simulation/**",
            "physics-rules/**",
        ],
        tools=["simulator", "visualizer", "analyzer"],
        tags=["physics", "agents", "scenarios", "forecasting"],
    ),

    # =========================================================================
    # RESEARCH DOMAINS
    # =========================================================================
    Domain(
        name="Research",
        code="RES",
        type=DomainType.RESEARCH,
        description="Academic research, papers, and knowledge synthesis.",
        philosophy="Standing on the shoulders of giants. Cite your sources.",
        recommended_models=[
            "llama3.1:70b",
            "deepseek-r1:32b",
            "claude-3-5-sonnet",
        ],
        templates=["paper", "literature-review", "hypothesis", "methodology"],
        explore_paths=[
            "work/research/**",
            "papers/**",
            "notes/**",
        ],
        immutable_paths=[
            "templates/research/**",
            "citation-styles/**",
            "ethics-guidelines/**",
        ],
        tools=["citation-manager", "literature-search", "latex"],
        tags=["papers", "citations", "analysis", "synthesis"],
    ),

    # =========================================================================
    # PERSONAL DOMAINS
    # =========================================================================
    Domain(
        name="Personal",
        code="PERS",
        type=DomainType.PERSONAL,
        description="Journals, notes, self-expression, and personal growth.",
        philosophy="Know thyself. The unexamined life is not worth living.",
        recommended_models=[
            "mistral:7b",
            "neural-chat:7b",
            "llama3.2:3b",
        ],
        templates=["journal", "note", "reflection", "goal", "habit"],
        explore_paths=[
            "personal/**",
            "journals/**",
            "notes/**",
        ],
        immutable_paths=[
            "templates/personal/**",
        ],
        tools=["note-taking", "calendar", "habit-tracker"],
        tags=["journals", "notes", "goals", "reflection"],
    ),
]


class DomainRegistry:
    """
    The registry of all knowledge domains.

    Provides lookup, search, and navigation.
    """

    def __init__(self):
        """Initialize the registry."""
        self.domains = {d.code: d for d in DOMAINS}
        self._by_name = {d.name.lower(): d for d in DOMAINS}
        self._by_type: Dict[DomainType, List[Domain]] = {}
        self._index()

    def _index(self):
        """Build indexes."""
        for domain in DOMAINS:
            if domain.type not in self._by_type:
                self._by_type[domain.type] = []
            self._by_type[domain.type].append(domain)

    def get(self, code: str) -> Optional[Domain]:
        """Get domain by code."""
        return self.domains.get(code.upper())

    def get_by_name(self, name: str) -> Optional[Domain]:
        """Get domain by name."""
        return self._by_name.get(name.lower())

    def for_type(self, domain_type: DomainType) -> List[Domain]:
        """Get domains of a type."""
        return self._by_type.get(domain_type, [])

    def search(self, query: str) -> List[Domain]:
        """Search domains."""
        query = query.lower()
        return [
            d for d in DOMAINS
            if query in d.name.lower()
            or query in d.description.lower()
            or any(query in t for t in d.tags)
        ]

    def list_all(self) -> List[Domain]:
        """List all domains."""
        return DOMAINS

    def can_explore(self, domain_code: str, path: str) -> bool:
        """Check if a path is explorable in a domain."""
        domain = self.get(domain_code)
        if not domain:
            return False

        # Check against immutable paths first
        for immutable in domain.immutable_paths:
            if self._path_matches(path, immutable):
                return False

        # Check against explore paths
        for explore in domain.explore_paths:
            if self._path_matches(path, explore):
                return True

        return False

    def is_immutable(self, domain_code: str, path: str) -> bool:
        """Check if a path is immutable (template) in a domain."""
        domain = self.get(domain_code)
        if not domain:
            return True  # Unknown = immutable for safety

        for immutable in domain.immutable_paths:
            if self._path_matches(path, immutable):
                return True

        return False

    def _path_matches(self, path: str, pattern: str) -> bool:
        """Check if path matches pattern (supports ** glob)."""
        import fnmatch

        # Handle ** (matches any depth)
        if "**" in pattern:
            pattern = pattern.replace("**", "*")
            return fnmatch.fnmatch(path, pattern) or path.startswith(pattern.rstrip("/*"))

        return fnmatch.fnmatch(path, pattern)

    def stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_domains": len(DOMAINS),
            "by_type": {
                t.value: len(self._by_type.get(t, []))
                for t in DomainType
            },
        }
