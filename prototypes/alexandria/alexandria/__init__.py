"""
Alexandria - The Library for Agents

A vast, explorable knowledge system where every agent can:
- Discover specialized models for any domain
- Explore templates for creation
- Learn from the collective intelligence
- Create without breaking foundations

Philosophy:
- Templates are constitutions, not constraints
- Agents can draw houses, but not change THE house template
- Every domain has its own language, models, and rules
- Knowledge flows across all devices and platforms

Domains:
- Mathematics: Proofs, computation, logic
- Physics: Simulations, mechanics, quantum
- Language: Translation, writing, poetry
- Art: Drawing, music, design
- Marketing: Copy, campaigns, analytics
- Worlds: 3D, games, simulations
- Code: Programming, architecture, systems
- Research: Papers, analysis, synthesis
- Business: Finance, operations, strategy

Usage:
    from alexandria import Library

    lib = Library()

    # Find models for a domain
    models = lib.models.for_domain("mathematics")

    # Get templates for creation
    template = lib.templates.get("house")

    # Create with guardrails
    result = lib.create("house", style="modern", agent="architect")
    # -> Creates instance, template unchanged
"""

__version__ = "0.1.0"

from .library import Library
from .models import ModelCatalog
from .domains import DomainRegistry
from .templates import TemplateEngine

__all__ = [
    "Library",
    "ModelCatalog",
    "DomainRegistry",
    "TemplateEngine",
]
