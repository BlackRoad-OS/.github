"""
Prompt Template Model
Templates with variable substitution, provider overrides, and metadata.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PromptTemplate:
    """
    A reusable prompt template with variable placeholders.

    Variables use {{variable_name}} syntax.
    Provider overrides allow customizing prompts per AI provider.
    """

    id: str
    name: str
    description: str
    system_prompt: str
    user_prompt: str
    version: str = "1.0"
    category: str = "general"
    tags: list = field(default_factory=list)
    variables: list = field(default_factory=list)  # Expected variable names
    defaults: dict = field(default_factory=dict)  # Default values for variables
    provider_overrides: dict = field(default_factory=dict)  # {provider: {system:, user:}}
    created_at: float = field(default_factory=time.time)
    usage_count: int = 0
    last_used: Optional[float] = None

    def render(
        self,
        variables: Optional[dict] = None,
        provider: Optional[str] = None,
    ) -> dict:
        """
        Render the template with given variables.

        Args:
            variables: Dict of variable values to substitute
            provider: If specified, use provider-specific overrides

        Returns:
            {"system": str, "user": str} with variables resolved
        """
        vars_merged = {**self.defaults, **(variables or {})}

        # Select base prompts (with provider override if available)
        if provider and provider in self.provider_overrides:
            override = self.provider_overrides[provider]
            system = override.get("system_prompt", self.system_prompt)
            user = override.get("user_prompt", self.user_prompt)
        else:
            system = self.system_prompt
            user = self.user_prompt

        # Substitute variables
        system = self._substitute(system, vars_merged)
        user = self._substitute(user, vars_merged)

        # Track usage
        self.usage_count += 1
        self.last_used = time.time()

        return {"system": system, "user": user}

    def _substitute(self, text: str, variables: dict) -> str:
        """Replace {{var}} placeholders with values."""
        def replacer(match):
            key = match.group(1).strip()
            if key in variables:
                return str(variables[key])
            return match.group(0)  # Leave unresolved

        return re.sub(r"\{\{(\s*\w+\s*)\}\}", replacer, text)

    def validate(self, variables: dict) -> list[str]:
        """Check if all required variables are provided."""
        missing = []
        for var in self.variables:
            if var not in variables and var not in self.defaults:
                missing.append(var)
        return missing

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "tags": self.tags,
            "variables": self.variables,
            "usage_count": self.usage_count,
        }
