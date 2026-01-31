"""
Script to update .STATUS beacon with active sessions.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add sessions to path
sys.path.insert(0, str(Path(__file__).parent.parent / "prototypes" / "sessions"))

from sessions.registry import SessionRegistry
from sessions.collaboration import CollaborationHub
from sessions.memory import SharedMemory


def update_status_beacon():
    """Update .STATUS with current session information."""
    
    # Get bridge root
    bridge_root = Path(__file__).parent.parent
    status_file = bridge_root / ".STATUS"
    
    # Initialize session systems
    registry = SessionRegistry()
    hub = CollaborationHub(registry)
    memory = SharedMemory()
    
    # Get stats
    session_stats = registry.get_stats()
    collab_stats = hub.get_stats()
    memory_stats = memory.get_stats()
    
    # Get active sessions
    sessions = registry.list_sessions()
    
    # Read current status
    if status_file.exists():
        with open(status_file, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Find session section or create it
    session_section_start = -1
    session_section_end = -1
    
    for i, line in enumerate(lines):
        if "# ACTIVE SESSIONS" in line:
            session_section_start = i
        elif session_section_start >= 0 and line.startswith("# ═══"):
            session_section_end = i
            break
    
    # Build session section
    session_lines = [
        "# ═══════════════════════════════════════\n",
        "# ACTIVE SESSIONS ([COLLABORATION] + [MEMORY])\n",
        "# ═══════════════════════════════════════\n",
        "\n",
        f"total_sessions: {session_stats['total_sessions']}\n",
        f"active_sessions: {session_stats['active_sessions']}\n",
        f"collaboration_messages: {collab_stats['total_messages']}\n",
        f"shared_memory_entries: {memory_stats['total_entries']}\n",
        "\n",
    ]
    
    if sessions:
        session_lines.append("# Active session list:\n")
        for session in sessions[:10]:  # Limit to 10 most recent
            status_emoji = {
                "active": "🟢",
                "working": "⚙️",
                "idle": "⏸️",
                "waiting": "⏳",
                "offline": "⚪",
            }.get(session.status.value, "🔵")
            
            session_lines.append(
                f"# {status_emoji} {session.session_id}: {session.agent_name} ({session.agent_type})"
            )
            if session.current_task:
                session_lines.append(f" - {session.current_task}")
            session_lines.append("\n")
    else:
        session_lines.append("# No active sessions\n")
    
    session_lines.append("\n")
    
    # Update or append session section
    if session_section_start >= 0:
        # Replace existing section
        if session_section_end < 0:
            session_section_end = len(lines)
        lines = lines[:session_section_start] + session_lines + lines[session_section_end + 1:]
    else:
        # Append new section
        if lines and not lines[-1].endswith('\n'):
            lines.append('\n')
        lines.extend(session_lines)
    
    # Write back
    with open(status_file, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Updated .STATUS beacon with {session_stats['active_sessions']} active sessions")


if __name__ == "__main__":
    update_status_beacon()
