"""
CECE Coordinator - Cross-org coordination via signals.

Handles signal emission, org routing, and mesh coordination.
This is how Cece talks to the rest of the BlackRoad ecosystem.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .memory import MemoryManager


# Organization registry
ORGS = {
    "OS": {"name": "BlackRoad-OS", "focus": "Core infra (The Bridge)", "tier": 1},
    "AI": {"name": "BlackRoad-AI", "focus": "Models, routing", "tier": 1},
    "CLD": {"name": "BlackRoad-Cloud", "focus": "Cloud services", "tier": 1},
    "LAB": {"name": "BlackRoad-Labs", "focus": "Research", "tier": 2},
    "SEC": {"name": "BlackRoad-Security", "focus": "Security", "tier": 2},
    "HW": {"name": "BlackRoad-Hardware", "focus": "IoT, devices", "tier": 2},
    "FND": {"name": "BlackRoad-Foundation", "focus": "CRM, business", "tier": 3},
    "VEN": {"name": "BlackRoad-Ventures", "focus": "Commerce", "tier": 3},
    "BBX": {"name": "Blackbox-Enterprises", "focus": "Enterprise", "tier": 3},
    "MED": {"name": "BlackRoad-Media", "focus": "Content", "tier": 4},
    "STU": {"name": "BlackRoad-Studio", "focus": "Design", "tier": 4},
    "INT": {"name": "BlackRoad-Interactive", "focus": "Games, metaverse", "tier": 4},
    "EDU": {"name": "BlackRoad-Education", "focus": "Learning", "tier": 5},
    "GOV": {"name": "BlackRoad-Gov", "focus": "Governance", "tier": 5},
    "ARC": {"name": "BlackRoad-Archive", "focus": "Storage", "tier": 5},
}

# Node registry
NODES = {
    "LUC": {"name": "lucidia", "hardware": "Pi5 + Hailo-8", "role": "Salesforce, blockchain"},
    "OCT": {"name": "octavia", "hardware": "Pi5 + Hailo-8", "role": "AI inference (26 TOPS)"},
    "ARI": {"name": "aria", "hardware": "Pi5", "role": "Agent orchestration"},
    "ALI": {"name": "alice", "hardware": "Pi 400", "role": "K8s control plane, mesh root"},
    "SHL": {"name": "shellfish", "hardware": "Digital Ocean", "role": "Public gateway"},
    "CEC": {"name": "cecilia", "hardware": "Mac", "role": "Development environment"},
    "ARC": {"name": "arcadia", "hardware": "iPhone", "role": "Mobile interface"},
}

# Signal types
SIGNALS = {
    "complete": "✔️",
    "progress": "⏳",
    "blocked": "❌",
    "warning": "⚠️",
    "idle": "💤",
    "broadcast": "📡",
    "targeted": "🎯",
    "sync": "🔄",
    "upstream": "⬆️",
    "downstream": "⬇️",
    "critical": "🔴",
    "important": "🟡",
    "normal": "🟢",
    "low": "⚪",
}


@dataclass
class Signal:
    """A signal in the mesh."""

    timestamp: str
    signal_type: str
    signal_icon: str
    source: str
    target: str
    message: str

    def format(self) -> str:
        """Format as signal log entry."""
        return f"{self.timestamp} {self.signal_icon} {self.source} -> {self.target} : {self.message}"


@dataclass
class SignalLog:
    """In-memory signal log for current session."""

    entries: List[Signal] = field(default_factory=list)

    def append(self, signal: Signal) -> None:
        self.entries.append(signal)

    def recent(self, count: int = 10) -> List[Signal]:
        return self.entries[-count:]

    def format_log(self, count: int = 10) -> str:
        lines = []
        for sig in self.recent(count):
            lines.append(sig.format())
        return "\n".join(lines) if lines else "(no signals)"


class Coordinator:
    """Coordinate across orgs and nodes via signals."""

    def __init__(self, bridge_root: Optional[Path] = None):
        self.memory_mgr = MemoryManager(bridge_root)
        self.log = SignalLog()
        self.source = "CEC"  # Cece's node code

    def emit(
        self,
        signal_type: str,
        target: str,
        message: str,
        persist: bool = True,
    ) -> Signal:
        """Emit a signal to the mesh."""
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        icon = SIGNALS.get(signal_type, "🟢")

        signal = Signal(
            timestamp=ts,
            signal_type=signal_type,
            signal_icon=icon,
            source=self.source,
            target=target,
            message=message,
        )

        self.log.append(signal)

        if persist:
            self.memory_mgr.append_signal(icon, self.source, target, message)

        return signal

    def broadcast(self, message: str, priority: str = "normal") -> Signal:
        """Broadcast a signal to all orgs."""
        return self.emit("broadcast", "ALL", f"[{priority.upper()}] {message}")

    def target_org(self, org_code: str, message: str) -> Signal:
        """Send a targeted signal to a specific org."""
        if org_code not in ORGS:
            raise ValueError(f"Unknown org code: {org_code}. Valid: {list(ORGS.keys())}")
        return self.emit("targeted", org_code, message)

    def target_node(self, node_code: str, message: str) -> Signal:
        """Send a targeted signal to a specific node."""
        if node_code not in NODES:
            raise ValueError(f"Unknown node code: {node_code}. Valid: {list(NODES.keys())}")
        return self.emit("targeted", node_code, message)

    def complete(self, target: str, message: str) -> Signal:
        """Signal task completion."""
        return self.emit("complete", target, message)

    def progress(self, target: str, message: str) -> Signal:
        """Signal work in progress."""
        return self.emit("progress", target, message)

    def blocked(self, target: str, message: str) -> Signal:
        """Signal a blocker."""
        return self.emit("blocked", target, message)

    def route_request(self, request: str) -> Dict:
        """Route a request to the appropriate org based on keywords."""
        request_lower = request.lower()

        # Simple keyword-based routing
        routing_rules = {
            "AI": ["model", "inference", "prompt", "llm", "claude", "gpt", "ai"],
            "CLD": ["cloud", "deploy", "edge", "cloudflare", "worker", "cdn"],
            "HW": ["hardware", "pi", "hailo", "sensor", "node", "esp32"],
            "SEC": ["security", "auth", "vault", "key", "encrypt", "rbac"],
            "FND": ["salesforce", "stripe", "billing", "crm", "payment"],
            "MED": ["content", "blog", "social", "media", "publish"],
            "STU": ["design", "figma", "canva", "ui", "brand"],
            "INT": ["game", "metaverse", "unity", "3d", "avatar"],
            "EDU": ["learn", "course", "tutorial", "education"],
            "GOV": ["governance", "compliance", "policy", "civic"],
            "ARC": ["archive", "backup", "storage", "preserve"],
            "LAB": ["experiment", "research", "prototype", "test"],
            "VEN": ["invest", "venture", "commerce", "market"],
            "BBX": ["enterprise", "stealth", "classified"],
        }

        scores = {}
        for org_code, keywords in routing_rules.items():
            score = sum(1 for kw in keywords if kw in request_lower)
            if score > 0:
                scores[org_code] = score

        if not scores:
            return {
                "target": "OS",
                "confidence": 0.5,
                "reason": "No specific org matched, routing to OS (Bridge)",
            }

        best = max(scores, key=scores.get)
        total_keywords = len(routing_rules[best])
        confidence = min(scores[best] / max(total_keywords, 1), 1.0)

        return {
            "target": best,
            "confidence": round(confidence, 2),
            "reason": f"Matched {scores[best]} keywords for {ORGS[best]['name']}",
            "org": ORGS[best],
        }

    def get_org_info(self, code: str) -> Optional[Dict]:
        """Get info about an org by code."""
        return ORGS.get(code)

    def get_node_info(self, code: str) -> Optional[Dict]:
        """Get info about a node by code."""
        return NODES.get(code)

    def list_orgs(self, tier: Optional[int] = None) -> Dict[str, Dict]:
        """List all orgs, optionally filtered by tier."""
        if tier is None:
            return ORGS
        return {k: v for k, v in ORGS.items() if v["tier"] == tier}

    def list_nodes(self) -> Dict[str, Dict]:
        """List all nodes."""
        return NODES

    def mesh_status(self) -> str:
        """Return a formatted mesh status overview."""
        beacon = self.memory_mgr.read_status()
        lines = [
            "=== MESH STATUS ===",
            "",
            "Organizations:",
        ]
        for code, status in sorted(beacon.org_status.items()):
            org = ORGS.get(code, {})
            name = org.get("name", code)
            lines.append(f"  {code}: {status:15s} ({name})")

        lines.append("\nNodes:")
        for name, status in sorted(beacon.node_status.items()):
            node_info = next(
                (v for v in NODES.values() if v["name"] == name), {}
            )
            role = node_info.get("role", "")
            lines.append(f"  {name:12s} {status:15s} ({role})")

        lines.append(f"\nRecent signals ({len(self.log.entries)} this session):")
        lines.append(self.log.format_log(5))
        lines.append("\n=== END STATUS ===")
        return "\n".join(lines)
