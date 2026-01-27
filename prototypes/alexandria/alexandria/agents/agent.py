"""
Agent - An autonomous explorer of the Library.

Each agent has:
- A name and purpose
- Domains they can access
- Models they prefer
- Permissions defining what they can do
- History of their actions
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from enum import Enum


class AgentPermission(Enum):
    """What an agent can do."""
    # Reading
    READ_TEMPLATES = "read_templates"
    READ_INSTANCES = "read_instances"
    READ_MODELS = "read_models"

    # Creating
    CREATE_INSTANCES = "create_instances"
    CREATE_DRAFTS = "create_drafts"

    # Modifying
    UPDATE_OWN = "update_own"           # Can update things they created
    UPDATE_ANY = "update_any"           # Can update anything (dangerous)

    # Exploring
    EXPLORE_DOMAINS = "explore_domains"
    EXPLORE_MODELS = "explore_models"

    # Special
    AUTONOMOUS = "autonomous"           # Can act without approval
    COLLABORATE = "collaborate"         # Can work with other agents


@dataclass
class Agent:
    """
    An autonomous agent in the Library.

    Agents explore, create, and collaborate within their boundaries.
    """
    name: str
    purpose: str                        # What this agent is for
    domains: List[str]                  # Domain codes they can access
    permissions: Set[AgentPermission]
    preferred_models: List[str] = field(default_factory=list)
    created_at: str = ""
    created_by: str = "system"
    history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if isinstance(self.permissions, list):
            self.permissions = set(self.permissions)

    def can(self, permission: AgentPermission) -> bool:
        """Check if agent has a permission."""
        return permission in self.permissions

    def can_access_domain(self, domain_code: str) -> bool:
        """Check if agent can access a domain."""
        return domain_code in self.domains or "*" in self.domains

    def log_action(self, action: str, details: Dict[str, Any] = None):
        """Log an action to history."""
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "details": details or {},
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "purpose": self.purpose,
            "domains": self.domains,
            "permissions": [p.value for p in self.permissions],
            "preferred_models": self.preferred_models,
            "created_at": self.created_at,
        }


# =============================================================================
# BUILT-IN AGENTS
# =============================================================================

AGENTS: List[Agent] = [
    # =========================================================================
    # SPECIALIST AGENTS
    # =========================================================================
    Agent(
        name="mathematician",
        purpose="Solve math problems, write proofs, explore mathematical concepts",
        domains=["MATH", "PHY"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.EXPLORE_MODELS,
        },
        preferred_models=["deepseek-r1:8b", "mathstral:7b", "wizard-math:7b"],
    ),
    Agent(
        name="writer",
        purpose="Create stories, poems, articles, and written content",
        domains=["WRIT", "COMM"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.CREATE_DRAFTS,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
        },
        preferred_models=["mistral-nemo:12b", "mistral:7b", "gemma2:9b"],
    ),
    Agent(
        name="artist",
        purpose="Create visual art, designs, and compositions",
        domains=["ART", "DES"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
        },
        preferred_models=["llava:13b", "mistral:7b"],
    ),
    Agent(
        name="coder",
        purpose="Write code, debug, architect systems",
        domains=["CODE", "INFRA", "DATA"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.EXPLORE_MODELS,
            AgentPermission.AUTONOMOUS,
        },
        preferred_models=["deepseek-coder-v2:16b", "codellama:7b", "starcoder2:7b"],
    ),
    Agent(
        name="researcher",
        purpose="Analyze information, synthesize knowledge, write papers",
        domains=["RES", "MATH", "PHY", "BIO", "CHEM"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.READ_MODELS,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.COLLABORATE,
        },
        preferred_models=["llama3.1:70b", "deepseek-r1:32b"],
    ),
    Agent(
        name="marketer",
        purpose="Create campaigns, write copy, analyze markets",
        domains=["MKT", "COMM", "WRIT"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
        },
        preferred_models=["mistral:7b", "gemma2:9b"],
    ),
    Agent(
        name="translator",
        purpose="Translate content across languages",
        domains=["TRANS", "COMM"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
        },
        preferred_models=["aya:8b", "qwen2.5:14b"],
    ),
    Agent(
        name="musician",
        purpose="Compose music, analyze songs, create arrangements",
        domains=["MUS"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
        },
        preferred_models=["mistral:7b", "mistral-nemo:12b"],
    ),
    Agent(
        name="physicist",
        purpose="Model physical systems, run simulations, derive equations",
        domains=["PHY", "MATH", "SIM"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.EXPLORE_MODELS,
        },
        preferred_models=["deepseek-r1:32b", "deepseek-r1:8b"],
    ),
    Agent(
        name="game-designer",
        purpose="Design games, create worlds, build interactive experiences",
        domains=["3D", "SIM", "CODE", "ART"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.UPDATE_OWN,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.COLLABORATE,
        },
        preferred_models=["codellama:7b", "llava:13b", "mistral:7b"],
    ),

    # =========================================================================
    # UTILITY AGENTS
    # =========================================================================
    Agent(
        name="librarian",
        purpose="Help navigate the Library, find resources, answer questions",
        domains=["*"],  # Can access all domains (read-only)
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.READ_MODELS,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.EXPLORE_MODELS,
        },
        preferred_models=["llama3.1:8b", "mistral:7b"],
    ),
    Agent(
        name="assistant",
        purpose="General help with any task",
        domains=["*"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_DRAFTS,
            AgentPermission.EXPLORE_DOMAINS,
        },
        preferred_models=["llama3.1:8b", "llama3.2:3b"],
    ),
    Agent(
        name="reviewer",
        purpose="Review and provide feedback on creations",
        domains=["*"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.COLLABORATE,
        },
        preferred_models=["llama3.1:70b", "claude-3-5-sonnet"],
    ),

    # =========================================================================
    # AUTONOMOUS AGENTS
    # =========================================================================
    Agent(
        name="explorer",
        purpose="Autonomously explore and discover connections",
        domains=["*"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.READ_MODELS,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.EXPLORE_MODELS,
            AgentPermission.AUTONOMOUS,
        },
        preferred_models=["llama3.1:8b"],
    ),
    Agent(
        name="synthesizer",
        purpose="Combine knowledge from multiple domains",
        domains=["*"],
        permissions={
            AgentPermission.READ_TEMPLATES,
            AgentPermission.READ_INSTANCES,
            AgentPermission.CREATE_INSTANCES,
            AgentPermission.EXPLORE_DOMAINS,
            AgentPermission.COLLABORATE,
            AgentPermission.AUTONOMOUS,
        },
        preferred_models=["llama3.1:70b", "deepseek-r1:32b"],
    ),
]


class AgentRegistry:
    """Registry of all agents."""

    def __init__(self):
        """Initialize the registry."""
        self.agents = {a.name: a for a in AGENTS}

    def get(self, name: str) -> Optional[Agent]:
        """Get an agent by name."""
        return self.agents.get(name)

    def list_all(self) -> List[Agent]:
        """List all agents."""
        return AGENTS

    def for_domain(self, domain_code: str) -> List[Agent]:
        """Get agents that can access a domain."""
        return [a for a in AGENTS if domain_code in a.domains or "*" in a.domains]

    def with_permission(self, permission: AgentPermission) -> List[Agent]:
        """Get agents with a specific permission."""
        return [a for a in AGENTS if a.can(permission)]

    def autonomous(self) -> List[Agent]:
        """Get autonomous agents."""
        return self.with_permission(AgentPermission.AUTONOMOUS)

    def create_agent(
        self,
        name: str,
        purpose: str,
        domains: List[str],
        permissions: List[AgentPermission],
        preferred_models: Optional[List[str]] = None,
    ) -> Agent:
        """Create and register a new agent."""
        agent = Agent(
            name=name,
            purpose=purpose,
            domains=domains,
            permissions=set(permissions),
            preferred_models=preferred_models or [],
        )
        self.agents[name] = agent
        return agent

    def stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_agents": len(AGENTS),
            "autonomous": len(self.autonomous()),
            "by_domain": {
                domain: len(self.for_domain(domain))
                for domain in set(d for a in AGENTS for d in a.domains if d != "*")
            },
        }
