"""
Template Engine - Create without breaking foundations.

Templates are immutable constitutions.
Instances are mutable creations.

The House vs A House:
- THE house template defines what a house IS
- A house instance is what you CREATE from the template
- You can paint YOUR house any color
- You cannot change what a HOUSE fundamentally is
"""

from .engine import TemplateEngine, Template, Instance

__all__ = ["TemplateEngine", "Template", "Instance"]
