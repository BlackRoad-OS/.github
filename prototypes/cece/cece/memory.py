"""
CECE Memory Manager - Persistent memory via git-tracked files.

Reads and writes to MEMORY.md and .STATUS in the Bridge root.
Memory is what gives Cece continuity across sessions.
"""

import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def _find_bridge_root() -> Path:
    """Locate the Bridge root (.github directory)."""
    # Walk up from this file to find the .github root
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if parent.name == ".github" and (parent / "MEMORY.md").exists():
            return parent
        # Also check if .github is a child
        candidate = parent / ".github"
        if candidate.exists() and (candidate / "MEMORY.md").exists():
            return candidate
    # Fallback: check common locations
    for path in [Path.home() / ".github", Path("/home/user/.github")]:
        if path.exists() and (path / "MEMORY.md").exists():
            return path
    raise FileNotFoundError("Cannot locate Bridge root (.github with MEMORY.md)")


@dataclass
class StatusBeacon:
    """Parsed .STATUS file contents."""

    state: str = "UNKNOWN"
    updated: str = ""
    session: str = ""
    bridge: str = "OFFLINE"
    memory: str = "UNKNOWN"
    signals: str = "UNKNOWN"
    operator: str = "UNKNOWN"
    metrics: str = "UNKNOWN"
    explorer: str = "UNKNOWN"
    last_signal: str = ""
    last_update: str = ""
    last_actor: str = ""
    org_status: Dict[str, str] = field(default_factory=dict)
    node_status: Dict[str, str] = field(default_factory=dict)
    active_threads: List[str] = field(default_factory=list)


@dataclass
class MemorySnapshot:
    """Parsed MEMORY.md contents."""

    last_updated: str = ""
    session: str = ""
    human: str = ""
    ai: str = ""
    location: str = ""
    completed_items: List[str] = field(default_factory=list)
    active_threads: List[str] = field(default_factory=list)
    key_decisions: List[str] = field(default_factory=list)
    raw_content: str = ""


class MemoryManager:
    """Read and write Cece's persistent memory files."""

    def __init__(self, bridge_root: Optional[Path] = None):
        self.bridge_root = bridge_root or _find_bridge_root()
        self.memory_path = self.bridge_root / "MEMORY.md"
        self.status_path = self.bridge_root / ".STATUS"

    def read_memory(self) -> MemorySnapshot:
        """Parse MEMORY.md into structured data."""
        snapshot = MemorySnapshot()
        if not self.memory_path.exists():
            return snapshot

        content = self.memory_path.read_text()
        snapshot.raw_content = content

        # Parse current state block
        state_match = re.search(
            r"```\s*\n(.*?)\n```", content, re.DOTALL
        )
        if state_match:
            block = state_match.group(1)
            for line in block.strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip().lower().replace(" ", "_")
                    val = val.strip()
                    if key == "last_updated":
                        snapshot.last_updated = val
                    elif key == "session":
                        snapshot.session = val
                    elif key == "human":
                        snapshot.human = val
                    elif key == "ai":
                        snapshot.ai = val
                    elif key == "location":
                        snapshot.location = val

        # Parse completed items
        for match in re.finditer(r"- \[x\] (.+)", content):
            snapshot.completed_items.append(match.group(1))

        # Parse active threads (not struck through)
        for match in re.finditer(r"^\d+\.\s+\*\*(.+?)\*\*", content, re.MULTILINE):
            text = match.group(1)
            if "~~" not in text:
                snapshot.active_threads.append(text)

        # Parse key decisions
        decision_section = re.search(
            r"## Key Decisions\s*\n\|.*?\n\|.*?\n(.*?)(?=\n---|\n##|\Z)",
            content,
            re.DOTALL,
        )
        if decision_section:
            for line in decision_section.group(1).strip().split("\n"):
                if line.startswith("|") and "---" not in line:
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        snapshot.key_decisions.append(f"{parts[0]}: {parts[1]}")

        return snapshot

    def read_status(self) -> StatusBeacon:
        """Parse .STATUS into structured data."""
        beacon = StatusBeacon()
        if not self.status_path.exists():
            return beacon

        content = self.status_path.read_text()

        # Parse key-value pairs
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.split("#")[0].strip()  # Remove inline comments
                val = val.split("<-")[0].strip()  # Remove arrow comments

                if key == "state":
                    beacon.state = val
                elif key == "updated":
                    beacon.updated = val
                elif key == "session":
                    beacon.session = val
                elif key == "bridge":
                    beacon.bridge = val
                elif key == "memory":
                    beacon.memory = val
                elif key == "signals":
                    beacon.signals = val
                elif key == "operator":
                    beacon.operator = val
                elif key == "metrics":
                    beacon.metrics = val
                elif key == "explorer":
                    beacon.explorer = val
                elif key == "last_signal":
                    beacon.last_signal = val
                elif key == "last_update":
                    beacon.last_update = val
                elif key == "last_actor":
                    beacon.last_actor = val

        # Parse org status lines (e.g., "OS:  active")
        for match in re.finditer(
            r"^([A-Z]{2,3}):\s+(\S+)", content, re.MULTILINE
        ):
            code = match.group(1)
            status = match.group(2)
            if code in {
                "OS", "AI", "CLD", "LAB", "SEC", "FND",
                "MED", "HW", "INT", "EDU", "GOV", "ARC", "STU", "VEN", "BBX",
            }:
                beacon.org_status[code] = status

        # Parse node status lines
        for match in re.finditer(
            r"^(\w+):\s+(\S+)", content, re.MULTILINE
        ):
            name = match.group(1)
            status = match.group(2)
            if name in {
                "lucidia", "octavia", "aria", "alice",
                "shellfish", "cecilia", "arcadia",
            }:
                beacon.node_status[name] = status

        return beacon

    def update_status_field(self, field_name: str, value: str) -> None:
        """Update a single field in .STATUS."""
        if not self.status_path.exists():
            return

        content = self.status_path.read_text()
        pattern = rf"^({re.escape(field_name)}:\s*)(.+)$"
        replacement = rf"\g<1>{value}"
        updated = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        if updated != content:
            self.status_path.write_text(updated)

    def append_signal(self, signal: str, source: str, target: str, message: str) -> None:
        """Append a signal entry to .STATUS signal log."""
        if not self.status_path.exists():
            return

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        entry = f"{ts} {signal} {source} -> {target} : {message}"

        content = self.status_path.read_text()
        # Update last_signal field
        content = re.sub(
            r"^(last_signal:\s*)(.+)$",
            rf"\g<1>{signal} {message}",
            content,
            flags=re.MULTILINE,
        )
        content = re.sub(
            r"^(last_update:\s*)(.+)$",
            rf"\g<1>{ts.split('T')[0]}",
            content,
            flags=re.MULTILINE,
        )
        content = re.sub(
            r"^(last_actor:\s*)(.+)$",
            r"\g<1>Cece (Claude)",
            content,
            flags=re.MULTILINE,
        )
        self.status_path.write_text(content)

    def get_session_context(self) -> str:
        """Build full context string for session resume."""
        memory = self.read_memory()
        status = self.read_status()

        lines = [
            "=== SESSION CONTEXT ===",
            "",
            f"Bridge: {status.bridge}",
            f"State: {status.state}",
            f"Session: {status.session}",
            f"Memory: {status.memory}",
            "",
            f"Partner: {memory.human}",
            f"AI: {memory.ai}",
            f"Location: {memory.location}",
            "",
            f"Completed milestones: {len(memory.completed_items)}",
            f"Active threads: {len(memory.active_threads)}",
            f"Key decisions: {len(memory.key_decisions)}",
            "",
        ]

        if memory.active_threads:
            lines.append("Active threads:")
            for thread in memory.active_threads:
                lines.append(f"  - {thread}")
            lines.append("")

        if status.last_signal:
            lines.append(f"Last signal: {status.last_signal}")

        lines.append("=== END CONTEXT ===")
        return "\n".join(lines)
