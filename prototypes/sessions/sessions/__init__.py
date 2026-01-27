"""
BlackRoad Session Management - Collaboration & Memory.

Enables multiple AI/agent sessions to discover, communicate, and share state.
"""

from .registry import SessionRegistry, Session, SessionStatus
from .collaboration import CollaborationHub, Message, MessageType
from .memory import SharedMemory, MemoryEntry

__all__ = [
    "SessionRegistry",
    "Session",
    "SessionStatus",
    "CollaborationHub",
    "Message",
    "MessageType",
    "SharedMemory",
    "MemoryEntry",
]

__version__ = "0.1.0"
