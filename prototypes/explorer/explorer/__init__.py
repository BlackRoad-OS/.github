"""
BlackRoad Explorer - Navigate the ecosystem from CLI.

Usage:
    from explorer import Explorer

    exp = Explorer()
    exp.list_orgs()
    exp.show_org("AI")
"""

from .browser import Explorer, Org, Repo

__version__ = "0.1.0"
__all__ = ["Explorer", "Org", "Repo"]
