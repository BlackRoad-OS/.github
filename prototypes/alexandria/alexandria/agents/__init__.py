"""
Agent System - Autonomous explorers with boundaries.

Agents can:
- Explore domains
- Create instances from templates
- Use specialized models
- Collaborate with other agents

Agents cannot:
- Modify templates
- Access paths outside their domain
- Exceed their permissions
"""

from .agent import Agent, AgentPermission, AgentRegistry

__all__ = ["Agent", "AgentPermission", "AgentRegistry"]
