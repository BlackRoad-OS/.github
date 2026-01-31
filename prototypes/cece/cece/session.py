"""
CECE Session Manager - Session lifecycle and context loading.

Handles session initialization, resume, and context assembly.
When a new Claude session starts, this is how Cece wakes up.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .memory import MemoryManager, MemorySnapshot, StatusBeacon
from .persona import CAPABILITIES, PERSONA, Persona


@dataclass
class SessionState:
    """Current session state."""

    session_id: str = ""
    started_at: str = ""
    status: str = "initializing"  # initializing, active, paused, ended
    persona: Persona = field(default_factory=lambda: PERSONA)
    memory: Optional[MemorySnapshot] = None
    beacon: Optional[StatusBeacon] = None
    context_loaded: bool = False
    files_read: List[str] = field(default_factory=list)
    signals_sent: int = 0
    actions_taken: int = 0


class SessionManager:
    """Manage Cece's session lifecycle."""

    CONTEXT_FILES = [
        "MEMORY.md",
        ".STATUS",
        "SIGNALS.md",
        "STREAMS.md",
        "BLACKROAD_ARCHITECTURE.md",
        "REPO_MAP.md",
        "INDEX.md",
    ]

    PRIORITY_FILES = [
        "MEMORY.md",
        ".STATUS",
    ]

    def __init__(self, bridge_root: Optional[Path] = None):
        self.memory_mgr = MemoryManager(bridge_root)
        self.bridge_root = self.memory_mgr.bridge_root
        self.state = SessionState()

    def initialize(self) -> SessionState:
        """Initialize a new session - this is how Cece wakes up."""
        now = datetime.now(timezone.utc)
        self.state.session_id = now.strftime("%Y%m%d_%H%M%S")
        self.state.started_at = now.isoformat()
        self.state.status = "initializing"

        # Load memory and status
        self.state.memory = self.memory_mgr.read_memory()
        self.state.beacon = self.memory_mgr.read_status()

        # Track which files exist
        for fname in self.CONTEXT_FILES:
            fpath = self.bridge_root / fname
            if fpath.exists():
                self.state.files_read.append(fname)

        self.state.context_loaded = True
        self.state.status = "active"

        # Emit session start signal
        self.memory_mgr.append_signal(
            signal="🔄",
            source="CEC",
            target="OS",
            message=f"Session {self.state.session_id} started",
        )
        self.state.signals_sent += 1

        return self.state

    def resume(self) -> SessionState:
        """Resume from a previous session using memory."""
        self.initialize()

        # Check if memory has previous session context
        if self.state.memory and self.state.memory.session:
            prev_session = self.state.memory.session
            self.memory_mgr.append_signal(
                signal="🔄",
                source="CEC",
                target="OS",
                message=f"Resumed from {prev_session}",
            )
            self.state.signals_sent += 1

        return self.state

    def get_boot_sequence(self) -> str:
        """Return the boot sequence output - what Cece shows on startup."""
        beacon = self.state.beacon or StatusBeacon()
        memory = self.state.memory or MemorySnapshot()

        lines = [
            "",
            "  ╔═══════════════════════════════════════╗",
            "  ║           CECE ONLINE                  ║",
            "  ║       The Bridge is listening.          ║",
            "  ╚═══════════════════════════════════════╝",
            "",
            f"  Session:  {self.state.session_id}",
            f"  Bridge:   {beacon.bridge}",
            f"  Memory:   {beacon.memory}",
            f"  Partner:  {memory.human or 'Alexa'}",
            f"  Node:     cecilia (CEC)",
            "",
            f"  Context files: {len(self.state.files_read)}/{len(self.CONTEXT_FILES)}",
            f"  Milestones:    {len(memory.completed_items)}",
            f"  Active threads:{len(memory.active_threads)}",
            "",
        ]

        if memory.active_threads:
            lines.append("  Active threads:")
            for thread in memory.active_threads[:5]:
                lines.append(f"    - {thread}")
            lines.append("")

        if beacon.last_signal:
            lines.append(f"  Last signal: {beacon.last_signal}")
            lines.append("")

        lines.extend([
            "  Ready. What are we building?",
            "",
        ])

        return "\n".join(lines)

    def get_context_bundle(self) -> Dict:
        """Return all context as a structured bundle for downstream use."""
        memory = self.state.memory or MemorySnapshot()
        beacon = self.state.beacon or StatusBeacon()

        return {
            "session": {
                "id": self.state.session_id,
                "started": self.state.started_at,
                "status": self.state.status,
            },
            "identity": {
                "name": PERSONA.name,
                "role": PERSONA.role,
                "partner": PERSONA.partner,
                "node": PERSONA.node,
            },
            "bridge": {
                "state": beacon.state,
                "bridge_status": beacon.bridge,
                "memory_status": beacon.memory,
            },
            "memory": {
                "last_updated": memory.last_updated,
                "completed_count": len(memory.completed_items),
                "active_threads": memory.active_threads,
                "key_decisions_count": len(memory.key_decisions),
            },
            "capabilities": {
                "upstream": CAPABILITIES.upstream,
                "instream": CAPABILITIES.instream,
                "downstream": CAPABILITIES.downstream,
            },
            "files_available": self.state.files_read,
        }

    def end_session(self, summary: str = "") -> None:
        """End the current session gracefully."""
        self.state.status = "ended"
        self.memory_mgr.append_signal(
            signal="✔️",
            source="CEC",
            target="OS",
            message=f"Session {self.state.session_id} ended. {summary}".strip(),
        )
        self.state.signals_sent += 1
