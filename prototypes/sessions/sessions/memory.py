"""
Shared Memory - Cross-session memory space.

Provides a shared memory space where sessions can store and retrieve
data, enabling state sharing and coordination across multiple sessions.
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class MemoryType(Enum):
    """Types of memory entries."""
    STATE = "state"                    # Session state
    FACT = "fact"                      # Learned fact
    DECISION = "decision"              # Decision made
    TASK = "task"                      # Task info
    CONTEXT = "context"                # Context/background
    NOTE = "note"                      # General note
    CONFIG = "config"                  # Configuration


@dataclass
class MemoryEntry:
    """A shared memory entry."""
    
    entry_id: str
    type: MemoryType
    key: str                          # Memory key (e.g., "current_task", "last_decision")
    value: Any
    session_id: str                   # Session that created this
    timestamp: str
    ttl: Optional[int] = None         # Time to live in seconds (None = forever)
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize defaults."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
    
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if not self.ttl:
            return False
        
        created = datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
        age_seconds = (datetime.utcnow() - created).total_seconds()
        
        return age_seconds > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['type'] = self.type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from dictionary."""
        if 'type' in data and isinstance(data['type'], str):
            data['type'] = MemoryType(data['type'])
        return cls(**data)


class SharedMemory:
    """
    Shared memory space for cross-session coordination.
    
    Provides a key-value store where sessions can store and retrieve
    information, enabling state sharing and collaboration.
    
    Usage:
        memory = SharedMemory()
        
        # Store a value
        memory.set(
            session_id="session-1",
            key="current_task",
            value="Building collaboration system",
            type=MemoryType.STATE
        )
        
        # Get a value
        value = memory.get("current_task")
        
        # Get all values for a key pattern
        tasks = memory.search(key_pattern="task_*")
        
        # Get all entries from a session
        entries = memory.get_by_session("session-1")
        
        # Query with tags
        entries = memory.get_by_tags(["python", "code-review"])
    """
    
    def __init__(self, memory_path: Optional[Path] = None):
        """
        Initialize shared memory.
        
        Args:
            memory_path: Path to store memory data
        """
        if memory_path:
            self.memory_path = Path(memory_path)
        else:
            # Default to bridge directory
            bridge_root = Path(__file__).parent.parent.parent.parent
            self.memory_path = bridge_root / ".sessions" / "shared_memory"
        
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.memory_path / "memory.json"
        
        self._entries: Dict[str, MemoryEntry] = {}
        self._index_by_key: Dict[str, List[str]] = {}
        self._index_by_session: Dict[str, List[str]] = {}
        self._index_by_tag: Dict[str, List[str]] = {}
        
        self._load()
    
    def _load(self):
        """Load memory from disk."""
        if not self.memory_file.exists():
            return
        
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
            
            self._entries = {
                eid: MemoryEntry.from_dict(edata)
                for eid, edata in data.get('entries', {}).items()
            }
            
            self._rebuild_indices()
            self._cleanup_expired()
            
        except Exception as e:
            print(f"Warning: Could not load shared memory: {e}")
    
    def _save(self):
        """Save memory to disk."""
        try:
            data = {
                'entries': {
                    eid: entry.to_dict()
                    for eid, entry in self._entries.items()
                },
                'updated_at': datetime.utcnow().isoformat(),
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save shared memory: {e}")
    
    def _rebuild_indices(self):
        """Rebuild all indices."""
        self._index_by_key.clear()
        self._index_by_session.clear()
        self._index_by_tag.clear()
        
        for entry_id, entry in self._entries.items():
            # Index by key
            if entry.key not in self._index_by_key:
                self._index_by_key[entry.key] = []
            self._index_by_key[entry.key].append(entry_id)
            
            # Index by session
            if entry.session_id not in self._index_by_session:
                self._index_by_session[entry.session_id] = []
            self._index_by_session[entry.session_id].append(entry_id)
            
            # Index by tags
            for tag in entry.tags:
                if tag not in self._index_by_tag:
                    self._index_by_tag[tag] = []
                self._index_by_tag[tag].append(entry_id)
    
    def _cleanup_expired(self):
        """Remove expired entries."""
        expired = [
            eid for eid, entry in self._entries.items()
            if entry.is_expired()
        ]
        
        for eid in expired:
            del self._entries[eid]
        
        if expired:
            self._rebuild_indices()
    
    def set(
        self,
        session_id: str,
        key: str,
        value: Any,
        type: MemoryType = MemoryType.STATE,
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryEntry:
        """
        Store a value in shared memory.
        
        Args:
            session_id: Session storing the value
            key: Memory key
            value: Value to store
            type: Type of memory entry
            ttl: Time to live in seconds (None = forever)
            tags: Tags for searching
            metadata: Additional metadata
        
        Returns:
            The created MemoryEntry
        """
        import uuid
        
        entry = MemoryEntry(
            entry_id=str(uuid.uuid4()),
            type=type,
            key=key,
            value=value,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat(),
            ttl=ttl,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        self._entries[entry.entry_id] = entry
        
        # Update indices
        if key not in self._index_by_key:
            self._index_by_key[key] = []
        self._index_by_key[key].append(entry.entry_id)
        
        if session_id not in self._index_by_session:
            self._index_by_session[session_id] = []
        self._index_by_session[session_id].append(entry.entry_id)
        
        for tag in entry.tags:
            if tag not in self._index_by_tag:
                self._index_by_tag[tag] = []
            self._index_by_tag[tag].append(entry.entry_id)
        
        self._save()
        
        return entry
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the most recent value for a key.
        
        Args:
            key: Memory key
            default: Default if not found
        
        Returns:
            The value or default
        """
        self._cleanup_expired()
        
        entry_ids = self._index_by_key.get(key, [])
        
        if not entry_ids:
            return default
        
        # Get most recent entry
        entries = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        
        if not entries:
            return default
        
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries[0].value
    
    def get_entry(self, key: str) -> Optional[MemoryEntry]:
        """
        Get the most recent entry for a key.
        
        Args:
            key: Memory key
        
        Returns:
            The MemoryEntry or None
        """
        self._cleanup_expired()
        
        entry_ids = self._index_by_key.get(key, [])
        
        if not entry_ids:
            return None
        
        # Get most recent entry
        entries = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        
        if not entries:
            return None
        
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries[0]
    
    def get_all(self, key: str) -> List[MemoryEntry]:
        """
        Get all entries for a key.
        
        Args:
            key: Memory key
        
        Returns:
            List of MemoryEntry objects
        """
        self._cleanup_expired()
        
        entry_ids = self._index_by_key.get(key, [])
        entries = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries
    
    def get_by_session(self, session_id: str) -> List[MemoryEntry]:
        """
        Get all entries from a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            List of MemoryEntry objects
        """
        self._cleanup_expired()
        
        entry_ids = self._index_by_session.get(session_id, [])
        entries = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries
    
    def get_by_tags(self, tags: List[str], match_all: bool = False) -> List[MemoryEntry]:
        """
        Get entries by tags.
        
        Args:
            tags: Tags to search for
            match_all: If True, entry must have all tags; if False, any tag
        
        Returns:
            List of MemoryEntry objects
        """
        self._cleanup_expired()
        
        if not tags:
            return []
        
        # Get entry IDs for each tag
        entry_sets = [set(self._index_by_tag.get(tag, [])) for tag in tags]
        
        if match_all:
            # Intersection - must have all tags
            entry_ids = set.intersection(*entry_sets) if entry_sets else set()
        else:
            # Union - any tag
            entry_ids = set.union(*entry_sets) if entry_sets else set()
        
        entries = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries
    
    def search(self, key_pattern: str) -> List[MemoryEntry]:
        """
        Search entries by key pattern.
        
        Args:
            key_pattern: Pattern to match (supports * wildcard)
        
        Returns:
            List of matching MemoryEntry objects
        """
        self._cleanup_expired()
        
        import fnmatch
        
        matching_keys = [
            key for key in self._index_by_key.keys()
            if fnmatch.fnmatch(key, key_pattern)
        ]
        
        entries = []
        for key in matching_keys:
            entries.extend(self.get_all(key))
        
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return entries
    
    def delete(self, key: str, session_id: Optional[str] = None) -> int:
        """
        Delete entries for a key.
        
        Args:
            key: Memory key
            session_id: Only delete from this session (optional)
        
        Returns:
            Number of entries deleted
        """
        entry_ids = self._index_by_key.get(key, [])
        
        to_delete = []
        for eid in entry_ids:
            if eid in self._entries:
                if session_id is None or self._entries[eid].session_id == session_id:
                    to_delete.append(eid)
        
        for eid in to_delete:
            del self._entries[eid]
        
        if to_delete:
            self._rebuild_indices()
            self._save()
        
        return len(to_delete)
    
    def clear(self, session_id: Optional[str] = None):
        """
        Clear memory entries.
        
        Args:
            session_id: Only clear from this session (optional)
        """
        if session_id:
            entry_ids = self._index_by_session.get(session_id, [])
            for eid in entry_ids:
                if eid in self._entries:
                    del self._entries[eid]
        else:
            self._entries.clear()
        
        self._rebuild_indices()
        self._save()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        self._cleanup_expired()
        
        return {
            'total_entries': len(self._entries),
            'by_type': {
                mem_type.value: len([e for e in self._entries.values() if e.type == mem_type])
                for mem_type in MemoryType
            },
            'unique_keys': len(self._index_by_key),
            'unique_sessions': len(self._index_by_session),
            'unique_tags': len(self._index_by_tag),
        }
