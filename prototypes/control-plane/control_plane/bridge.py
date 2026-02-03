"""
Bridge - The unified control plane for BlackRoad.

This module ties together all the prototypes:
- Operator (routing)
- Metrics (KPIs)
- Explorer (browsing)
- Status (beacon)
- Signals (coordination)
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

# Add prototypes to path
BRIDGE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(BRIDGE_ROOT / "prototypes" / "operator"))
sys.path.insert(0, str(BRIDGE_ROOT / "prototypes" / "metrics"))
sys.path.insert(0, str(BRIDGE_ROOT / "prototypes" / "explorer"))


@dataclass
class BridgeState:
    """Current state of the Bridge."""
    status: str
    session: str
    updated: datetime
    orgs_total: int
    orgs_active: int
    prototypes_ready: List[str]
    templates_ready: List[str]
    nodes_online: int
    nodes_total: int


class Bridge:
    """
    The Bridge - Central control plane for BlackRoad.

    This is the master interface that coordinates:
    - Routing requests to the right org (Operator)
    - Monitoring ecosystem health (Metrics)
    - Navigating the ecosystem (Explorer)
    - Emitting and receiving signals (Signals)
    """

    def __init__(self):
        self.root = BRIDGE_ROOT
        self._operator = None
        self._metrics = None
        self._explorer = None

    @property
    def operator(self):
        """Lazy load the Operator."""
        if self._operator is None:
            try:
                from routing.core.router import Operator
                self._operator = Operator()
            except ImportError:
                self._operator = None
        return self._operator

    @property
    def metrics(self):
        """Lazy load the Metrics counter."""
        if self._metrics is None:
            try:
                from metrics.counter import Counter
                self._metrics = Counter(str(self.root))
            except ImportError:
                self._metrics = None
        return self._metrics

    @property
    def explorer(self):
        """Lazy load the Explorer."""
        if self._explorer is None:
            try:
                from explorer.browser import Explorer
                self._explorer = Explorer(str(self.root))
            except ImportError:
                self._explorer = None
        return self._explorer

    def get_state(self) -> BridgeState:
        """Get the current state of the Bridge."""
        # Count orgs
        orgs_dir = self.root / "orgs"
        orgs = list(orgs_dir.iterdir()) if orgs_dir.exists() else []

        # Count prototypes
        proto_dir = self.root / "prototypes"
        prototypes = [p.name for p in proto_dir.iterdir() if p.is_dir()] if proto_dir.exists() else []

        # Count templates
        tmpl_dir = self.root / "templates"
        templates = [t.name for t in tmpl_dir.iterdir() if t.is_dir()] if tmpl_dir.exists() else []

        return BridgeState(
            status="ONLINE",
            session="SESSION_2",
            updated=datetime.now(),
            orgs_total=len(orgs),
            orgs_active=1,  # OS is active
            prototypes_ready=prototypes,
            templates_ready=templates,
            nodes_online=1,  # cecilia (dev)
            nodes_total=7
        )

    def route(self, query: str) -> Dict[str, Any]:
        """Route a query through the Operator."""
        if self.operator is None:
            return {"error": "Operator not available"}

        result = self.operator.route(query)
        return {
            "destination": result.destination,
            "org": result.org,
            "confidence": result.confidence,
            "category": result.classification.category,
            "signal": result.signal
        }

    def status(self) -> str:
        """Get a quick status readout."""
        state = self.get_state()

        lines = [
            "",
            "  BLACKROAD BRIDGE",
            "  " + "=" * 40,
            "",
            f"  Status:     {state.status}",
            f"  Session:    {state.session}",
            f"  Updated:    {state.updated.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"  Orgs:       {state.orgs_active}/{state.orgs_total} active",
            f"  Nodes:      {state.nodes_online}/{state.nodes_total} online",
            f"  Prototypes: {len(state.prototypes_ready)} ready",
            f"  Templates:  {len(state.templates_ready)} ready",
            "",
            "  " + "=" * 40,
            ""
        ]
        return "\n".join(lines)

    def dashboard(self) -> str:
        """Get the full metrics dashboard."""
        try:
            from metrics.dashboard import Dashboard
            dash = Dashboard(str(self.root))
            return dash.show()
        except ImportError:
            return "Metrics dashboard not available"

    def browse(self, path: str = "") -> str:
        """Browse the ecosystem."""
        if self.explorer is None:
            return "Explorer not available"
        
        # Explorer just has tree() method
        return self.explorer.tree()

    def signal(self, message: str, target: str = "OS") -> str:
        """Emit a signal."""
        # Use simple fallback format since SignalEmitter needs different args
        return f"📡 OS → {target} : {message}"

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search the ecosystem."""
        if self.explorer is None:
            return []

        results = self.explorer.search(query)
        # Results from search are already dicts
        return results

    def list_orgs(self) -> List[Dict[str, str]]:
        """List all organizations."""
        orgs_dir = self.root / "orgs"
        if not orgs_dir.exists():
            return []

        orgs = []
        for org_dir in sorted(orgs_dir.iterdir()):
            if org_dir.is_dir():
                readme = org_dir / "README.md"
                mission = "Unknown"
                if readme.exists():
                    with open(readme) as f:
                        for line in f:
                            if line.startswith(">"):
                                mission = line.strip("> \n")
                                break
                orgs.append({
                    "name": org_dir.name,
                    "mission": mission
                })
        return orgs

    def list_templates(self) -> List[Dict[str, str]]:
        """List all templates."""
        tmpl_dir = self.root / "templates"
        if not tmpl_dir.exists():
            return []

        templates = []
        for tmpl in sorted(tmpl_dir.iterdir()):
            if tmpl.is_dir():
                readme = tmpl / "README.md"
                desc = "No description"
                if readme.exists():
                    with open(readme) as f:
                        for line in f:
                            if line.startswith(">"):
                                desc = line.strip("> \n")
                                break
                templates.append({
                    "name": tmpl.name,
                    "description": desc
                })
        return templates


# Singleton instance
_bridge: Optional[Bridge] = None

def get_bridge() -> Bridge:
    """Get the singleton Bridge instance."""
    global _bridge
    if _bridge is None:
        _bridge = Bridge()
    return _bridge
