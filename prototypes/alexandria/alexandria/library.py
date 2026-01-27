"""
The Library of Alexandria - The central hub.

Everything comes together here:
- Models for every domain
- Domains for every category
- Templates for every creation
- Agents for every task

Usage:
    from alexandria import Library

    lib = Library()

    # Find models for math
    models = lib.models.for_domain("mathematics")

    # Get a template
    template = lib.templates.get_template("proof")

    # Create from template (safe - template unchanged)
    proof, errors = lib.create("proof", {
        "theorem": "There are infinitely many primes",
        "given": "Assume finite primes p1...pn",
        "method": "contradiction",
        "steps": ["Consider N = p1*p2*...*pn + 1", ...],
        "conclusion": "QED"
    }, agent="mathematician")

    # Explore with an agent
    results = lib.explore("What models are good for physics?", agent="physicist")
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from .models import ModelCatalog, Model
from .domains import DomainRegistry, Domain
from .templates import TemplateEngine, Template, Instance
from .agents import AgentRegistry, Agent, AgentPermission


class Library:
    """
    The Library of Alexandria.

    The central hub for:
    - 30+ specialized AI models
    - 15+ knowledge domains
    - 20+ creation templates
    - 15+ autonomous agents

    All with clear boundaries:
    - Templates are immutable (the constitution)
    - Instances are mutable (your creations)
    - Agents have permissions (their boundaries)
    - Domains have paths (where they can go)
    """

    def __init__(self):
        """Initialize the Library."""
        self.models = ModelCatalog()
        self.domains = DomainRegistry()
        self.templates = TemplateEngine()
        self.agents = AgentRegistry()

        self._action_log: List[Dict[str, Any]] = []

    # =========================================================================
    # Creation (with guardrails)
    # =========================================================================

    def create(
        self,
        template_name: str,
        data: Dict[str, Any],
        agent: str = "assistant",
    ) -> Tuple[Optional[Instance], List[str]]:
        """
        Create an instance from a template.

        The template is NEVER modified.
        A new instance is created.

        Args:
            template_name: Name of the template
            data: Data for the instance
            agent: Agent doing the creation

        Returns:
            (instance, errors)
        """
        # Get agent
        agent_obj = self.agents.get(agent)
        if not agent_obj:
            return (None, [f"Unknown agent: {agent}"])

        # Check permission
        if not agent_obj.can(AgentPermission.CREATE_INSTANCES):
            return (None, [f"Agent {agent} cannot create instances"])

        # Get template
        template = self.templates.get_template(template_name)
        if not template:
            return (None, [f"Unknown template: {template_name}"])

        # Check domain access
        if not agent_obj.can_access_domain(template.domain):
            return (None, [f"Agent {agent} cannot access domain {template.domain}"])

        # Create instance
        instance, errors = self.templates.create(
            template_name=template_name,
            data=data,
            created_by=agent,
        )

        if instance:
            # Log action
            self._log_action(
                agent=agent,
                action="create",
                template=template_name,
                instance_id=instance.id,
            )
            agent_obj.log_action("create", {"template": template_name, "instance": instance.id})

        return (instance, errors)

    def update(
        self,
        instance_id: str,
        changes: Dict[str, Any],
        agent: str = "assistant",
    ) -> Tuple[bool, List[str]]:
        """
        Update an instance.

        Args:
            instance_id: ID of the instance
            changes: Changes to apply
            agent: Agent doing the update

        Returns:
            (success, errors)
        """
        # Get agent
        agent_obj = self.agents.get(agent)
        if not agent_obj:
            return (False, [f"Unknown agent: {agent}"])

        # Get instance
        instance = self.templates.get_instance(instance_id)
        if not instance:
            return (False, ["Instance not found"])

        # Check permission
        if instance.created_by == agent:
            if not agent_obj.can(AgentPermission.UPDATE_OWN):
                return (False, ["Agent cannot update own instances"])
        else:
            if not agent_obj.can(AgentPermission.UPDATE_ANY):
                return (False, ["Agent cannot update others' instances"])

        # Update
        success, errors = self.templates.update_instance(
            instance_id=instance_id,
            changes=changes,
            by=agent,
        )

        if success:
            self._log_action(
                agent=agent,
                action="update",
                instance_id=instance_id,
                changes=changes,
            )
            agent_obj.log_action("update", {"instance": instance_id})

        return (success, errors)

    # =========================================================================
    # Exploration
    # =========================================================================

    def explore(
        self,
        query: str,
        agent: str = "explorer",
        domain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Explore the Library.

        Args:
            query: What to explore
            agent: Agent doing the exploration
            domain: Limit to a domain

        Returns:
            Exploration results
        """
        agent_obj = self.agents.get(agent)
        if not agent_obj:
            return {"error": f"Unknown agent: {agent}"}

        if not agent_obj.can(AgentPermission.EXPLORE_DOMAINS):
            return {"error": "Agent cannot explore"}

        results = {
            "query": query,
            "agent": agent,
            "timestamp": datetime.utcnow().isoformat(),
            "models": [],
            "domains": [],
            "templates": [],
        }

        query_lower = query.lower()

        # Search models
        if "model" in query_lower or agent_obj.can(AgentPermission.EXPLORE_MODELS):
            results["models"] = [
                {"name": m.name, "description": m.description, "domains": m.domains}
                for m in self.models.search(query=query)[:5]
            ]

        # Search domains
        matching_domains = self.domains.search(query)
        if domain:
            matching_domains = [d for d in matching_domains if d.code == domain]

        results["domains"] = [
            {"code": d.code, "name": d.name, "description": d.description}
            for d in matching_domains[:5]
        ]

        # Search templates
        results["templates"] = [
            {"name": t.name, "description": t.description, "domain": t.domain}
            for t in self.templates.list_templates()
            if query_lower in t.name.lower() or query_lower in t.description.lower()
        ][:5]

        # Log exploration
        agent_obj.log_action("explore", {"query": query})

        return results

    def recommend_model(
        self,
        task: str,
        agent: Optional[str] = None,
        local_only: bool = True,
        max_memory_gb: float = 8.0,
    ) -> List[Model]:
        """
        Recommend models for a task.

        Args:
            task: What you want to do
            agent: Optional agent (uses their preferences)
            local_only: Only local/Ollama models
            max_memory_gb: Maximum memory

        Returns:
            List of recommended models
        """
        # If agent specified, consider their preferences
        if agent:
            agent_obj = self.agents.get(agent)
            if agent_obj and agent_obj.preferred_models:
                # Return agent's preferred models that fit constraints
                preferred = []
                for name in agent_obj.preferred_models:
                    model = self.models.get(name)
                    if model and model.memory_gb <= max_memory_gb:
                        if not local_only or model.provider in ("ollama", "local", "hailo"):
                            preferred.append(model)
                if preferred:
                    return preferred

        # Fall back to general recommendation
        return self.models.recommend(task, local_only=local_only, max_memory_gb=max_memory_gb)

    # =========================================================================
    # Access Control
    # =========================================================================

    def can_modify(self, path: str, agent: str) -> bool:
        """
        Check if an agent can modify a path.

        Templates and immutable paths cannot be modified.

        Args:
            path: The path to check
            agent: The agent trying to modify

        Returns:
            True if allowed
        """
        agent_obj = self.agents.get(agent)
        if not agent_obj:
            return False

        # Check against all domains
        for domain in self.domains.list_all():
            if agent_obj.can_access_domain(domain.code):
                if self.domains.is_immutable(domain.code, path):
                    return False  # Immutable path
                if self.domains.can_explore(domain.code, path):
                    return True

        return False

    def is_immutable(self, path: str) -> bool:
        """
        Check if a path is immutable (template/constitution).

        Args:
            path: The path to check

        Returns:
            True if immutable
        """
        # Templates directory is always immutable
        if path.startswith("templates/"):
            return True

        # Check against all domains
        for domain in self.domains.list_all():
            if self.domains.is_immutable(domain.code, path):
                return True

        return False

    # =========================================================================
    # Utilities
    # =========================================================================

    def _log_action(self, agent: str, action: str, **kwargs):
        """Log an action."""
        self._action_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "action": action,
            **kwargs,
        })

    def stats(self) -> Dict[str, Any]:
        """Get Library statistics."""
        return {
            "models": self.models.stats(),
            "domains": self.domains.stats(),
            "templates": self.templates.stats(),
            "agents": self.agents.stats(),
            "actions_logged": len(self._action_log),
        }

    def summary(self) -> str:
        """Get a human-readable summary."""
        stats = self.stats()
        return f"""
Alexandria Library
==================

Models:     {stats['models']['total_models']} ({stats['models']['local_models']} local)
Domains:    {stats['domains']['total_domains']}
Templates:  {stats['templates']['total_templates']}
Agents:     {stats['agents']['total_agents']} ({stats['agents']['autonomous']} autonomous)

Domains by Type:
{chr(10).join(f"  - {t}: {c}" for t, c in stats['domains']['by_type'].items())}

Ready to explore!
"""
