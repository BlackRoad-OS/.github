"""
Session Registry - Track active sessions in the mesh.

Maintains a registry of all active AI/agent sessions with their metadata,
status, and capabilities. Enables session discovery and coordination.
"""

import os
import json
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum


class SessionStatus(Enum):
    """Session status states."""
    ACTIVE = "active"
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    OFFLINE = "offline"


@dataclass
class Session:
    """Represents an active session in the mesh."""
    
    session_id: str
    agent_name: str                    # e.g., "Cece", "Agent-1"
    agent_type: str                    # e.g., "Claude", "GPT-4", "Custom"
    status: SessionStatus = SessionStatus.ACTIVE
    started_at: str = ""
    last_ping: str = ""
    human_user: Optional[str] = None   # e.g., "Alexa"
    location: str = "BlackRoad-OS/.github"
    capabilities: List[str] = field(default_factory=list)
    current_task: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if not self.started_at:
            self.started_at = datetime.utcnow().isoformat()
        if not self.last_ping:
            self.last_ping = datetime.utcnow().isoformat()
    
    def ping(self):
        """Update last ping timestamp."""
        self.last_ping = datetime.utcnow().isoformat()
    
    def is_stale(self, timeout_seconds: int = 300) -> bool:
        """Check if session is stale (no ping in timeout period)."""
        last_ping_dt = datetime.fromisoformat(self.last_ping.replace('Z', '+00:00'))
        return datetime.utcnow() - last_ping_dt > timedelta(seconds=timeout_seconds)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """Create from dictionary."""
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = SessionStatus(data['status'])
        return cls(**data)


class SessionRegistry:
    """
    Registry of active sessions.
    
    Tracks all AI/agent sessions currently active in the mesh,
    enabling discovery, collaboration, and coordination.
    
    Usage:
        registry = SessionRegistry()
        
        # Register a new session
        session = registry.register(
            session_id="cece-001",
            agent_name="Cece",
            agent_type="Claude",
            human_user="Alexa"
        )
        
        # List all sessions
        sessions = registry.list_sessions()
        
        # Ping to keep alive
        registry.ping("cece-001")
        
        # Update status
        registry.update_status("cece-001", SessionStatus.WORKING)
        
        # Find sessions by criteria
        active = registry.find_sessions(status=SessionStatus.ACTIVE)
    """
    
    def __init__(self, registry_path: Optional[Path] = None):
        """
        Initialize the session registry.
        
        Args:
            registry_path: Path to store registry data (auto-detected if None)
        """
        if registry_path:
            self.registry_path = Path(registry_path)
        else:
            # Default to bridge directory
            bridge_root = Path(__file__).parent.parent.parent.parent
            self.registry_path = bridge_root / ".sessions"
        
        self.registry_path.mkdir(exist_ok=True)
        self.sessions_file = self.registry_path / "active_sessions.json"
        
        self._sessions: Dict[str, Session] = {}
        self._load()
    
    def _load(self):
        """Load sessions from disk."""
        if not self.sessions_file.exists():
            return
        
        try:
            with open(self.sessions_file, 'r') as f:
                data = json.load(f)
            
            self._sessions = {
                sid: Session.from_dict(sdata)
                for sid, sdata in data.get('sessions', {}).items()
            }
            
            # Clean up stale sessions
            self._cleanup_stale()
            
        except Exception as e:
            print(f"Warning: Could not load session registry: {e}")
    
    def _save(self):
        """Save sessions to disk."""
        try:
            data = {
                'sessions': {
                    sid: session.to_dict()
                    for sid, session in self._sessions.items()
                },
                'updated_at': datetime.utcnow().isoformat(),
            }
            
            with open(self.sessions_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save session registry: {e}")
    
    def _cleanup_stale(self, timeout_seconds: int = 300):
        """Remove stale sessions."""
        stale = [
            sid for sid, session in self._sessions.items()
            if session.is_stale(timeout_seconds)
        ]
        
        for sid in stale:
            self._sessions[sid].status = SessionStatus.OFFLINE
            # Don't delete, just mark offline for historical tracking
    
    def register(
        self,
        session_id: str,
        agent_name: str,
        agent_type: str,
        human_user: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """
        Register a new session.
        
        Args:
            session_id: Unique session identifier
            agent_name: Name of the agent (e.g., "Cece")
            agent_type: Type of agent (e.g., "Claude", "GPT-4")
            human_user: Human user associated with session
            capabilities: List of capabilities this session supports
            metadata: Additional metadata
        
        Returns:
            The registered Session object
        """
        session = Session(
            session_id=session_id,
            agent_name=agent_name,
            agent_type=agent_type,
            human_user=human_user,
            capabilities=capabilities or [],
            metadata=metadata or {},
        )
        
        self._sessions[session_id] = session
        self._save()
        
        return session
    
    def unregister(self, session_id: str) -> bool:
        """
        Unregister a session.
        
        Args:
            session_id: Session to unregister
        
        Returns:
            True if unregistered, False if not found
        """
        if session_id in self._sessions:
            self._sessions[session_id].status = SessionStatus.OFFLINE
            self._save()
            return True
        return False
    
    def ping(self, session_id: str) -> bool:
        """
        Ping a session to keep it alive.
        
        Args:
            session_id: Session to ping
        
        Returns:
            True if pinged, False if not found
        """
        if session_id in self._sessions:
            self._sessions[session_id].ping()
            self._save()
            return True
        return False
    
    def get(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        return self._sessions.get(session_id)
    
    def update_status(
        self,
        session_id: str,
        status: SessionStatus,
        current_task: Optional[str] = None
    ) -> bool:
        """
        Update session status.
        
        Args:
            session_id: Session to update
            status: New status
            current_task: Current task description
        
        Returns:
            True if updated, False if not found
        """
        if session_id in self._sessions:
            self._sessions[session_id].status = status
            if current_task is not None:
                self._sessions[session_id].current_task = current_task
            self._sessions[session_id].ping()
            self._save()
            return True
        return False
    
    def list_sessions(
        self,
        include_offline: bool = False
    ) -> List[Session]:
        """
        List all sessions.
        
        Args:
            include_offline: Include offline sessions
        
        Returns:
            List of Session objects
        """
        self._cleanup_stale()
        
        sessions = list(self._sessions.values())
        
        if not include_offline:
            sessions = [s for s in sessions if s.status != SessionStatus.OFFLINE]
        
        return sessions
    
    def find_sessions(
        self,
        status: Optional[SessionStatus] = None,
        agent_type: Optional[str] = None,
        human_user: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> List[Session]:
        """
        Find sessions matching criteria.
        
        Args:
            status: Filter by status
            agent_type: Filter by agent type
            human_user: Filter by human user
            capability: Filter by capability
        
        Returns:
            List of matching sessions
        """
        self._cleanup_stale()
        
        results = list(self._sessions.values())
        
        if status:
            results = [s for s in results if s.status == status]
        
        if agent_type:
            results = [s for s in results if s.agent_type == agent_type]
        
        if human_user:
            results = [s for s in results if s.human_user == human_user]
        
        if capability:
            results = [s for s in results if capability in s.capabilities]
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        self._cleanup_stale()
        
        all_sessions = list(self._sessions.values())
        active = [s for s in all_sessions if s.status != SessionStatus.OFFLINE]
        
        stats = {
            'total_sessions': len(self._sessions),
            'active_sessions': len(active),
            'by_status': {},
            'by_agent_type': {},
            'by_user': {},
        }
        
        for session in all_sessions:
            # Count by status
            status_key = session.status.value
            stats['by_status'][status_key] = stats['by_status'].get(status_key, 0) + 1
            
            # Count by agent type
            stats['by_agent_type'][session.agent_type] = \
                stats['by_agent_type'].get(session.agent_type, 0) + 1
            
            # Count by user
            if session.human_user:
                stats['by_user'][session.human_user] = \
                    stats['by_user'].get(session.human_user, 0) + 1
        
        return stats
    
    def clear_offline(self):
        """Remove offline sessions from registry."""
        self._sessions = {
            sid: session
            for sid, session in self._sessions.items()
            if session.status != SessionStatus.OFFLINE
        }
        self._save()
