"""
Health Checker - Is everything alive?

Monitor the health of the BlackRoad ecosystem.
"""

import os
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum


class Status(Enum):
    """Health status levels."""
    HEALTHY = "🟢"
    WARNING = "🟡"
    CRITICAL = "🔴"
    OFFLINE = "⚪"
    UNKNOWN = "❓"


@dataclass
class ComponentHealth:
    """Health of a single component."""
    name: str
    status: Status
    message: str
    last_check: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metrics: Dict = field(default_factory=dict)

    def __str__(self):
        return f"{self.status.value} {self.name}: {self.message}"


@dataclass
class HealthStatus:
    """Overall health status."""
    overall: Status
    components: List[ComponentHealth]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def healthy_count(self) -> int:
        return sum(1 for c in self.components if c.status == Status.HEALTHY)

    @property
    def total_count(self) -> int:
        return len(self.components)

    def to_dict(self) -> Dict:
        return {
            "overall": self.overall.value,
            "healthy": self.healthy_count,
            "total": self.total_count,
            "components": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "message": c.message
                }
                for c in self.components
            ],
            "timestamp": self.timestamp
        }


class HealthChecker:
    """
    Check health of all BlackRoad components.

    Examples:
        >>> checker = HealthChecker()
        >>> health = checker.check_all()
        >>> print(health.overall)
        >>> for component in health.components:
        ...     print(component)
    """

    # Known nodes
    NODES = {
        "lucidia": {"role": "Salesforce/Blockchain", "type": "pi"},
        "octavia": {"role": "AI Routing", "type": "pi"},
        "aria": {"role": "Agents", "type": "pi"},
        "alice": {"role": "K8s Master", "type": "pi"},
        "shellfish": {"role": "Gateway", "type": "cloud"},
        "cecilia": {"role": "Dev", "type": "local"},
        "arcadia": {"role": "Mobile", "type": "mobile"},
    }

    # Orgs to check
    ORGS = [
        "OS", "AI", "CLD", "HW", "LAB", "SEC", "FND",
        "MED", "INT", "EDU", "GOV", "ARC", "STU", "VEN", "BBX"
    ]

    def __init__(self, root_path: Optional[str] = None):
        """Initialize health checker."""
        self.root_path = Path(root_path) if root_path else Path.cwd()

    def check_all(self) -> HealthStatus:
        """Check health of all components."""
        components = []

        # Check Bridge
        components.append(self._check_bridge())

        # Check Git
        components.append(self._check_git())

        # Check Orgs (blueprints)
        components.append(self._check_orgs())

        # Check Prototypes
        components.append(self._check_prototypes())

        # Check critical files
        components.append(self._check_critical_files())

        # Determine overall status
        statuses = [c.status for c in components]
        if Status.CRITICAL in statuses:
            overall = Status.CRITICAL
        elif Status.WARNING in statuses:
            overall = Status.WARNING
        elif all(s == Status.HEALTHY for s in statuses):
            overall = Status.HEALTHY
        else:
            overall = Status.WARNING

        return HealthStatus(overall=overall, components=components)

    def _check_bridge(self) -> ComponentHealth:
        """Check Bridge health."""
        critical_files = ['.STATUS', 'MEMORY.md', 'SIGNALS.md', 'STREAMS.md']
        missing = []

        for f in critical_files:
            if not (self.root_path / f).exists():
                missing.append(f)

        if not missing:
            return ComponentHealth(
                name="Bridge",
                status=Status.HEALTHY,
                message="All systems operational"
            )
        elif len(missing) < len(critical_files) // 2:
            return ComponentHealth(
                name="Bridge",
                status=Status.WARNING,
                message=f"Missing: {', '.join(missing)}"
            )
        else:
            return ComponentHealth(
                name="Bridge",
                status=Status.CRITICAL,
                message=f"Missing critical files: {', '.join(missing)}"
            )

    def _check_git(self) -> ComponentHealth:
        """Check Git health."""
        try:
            # Check if git repo
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return ComponentHealth(
                    name="Git",
                    status=Status.CRITICAL,
                    message="Not a git repository"
                )

            # Check for uncommitted changes
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

            # Check remote connectivity
            remote_result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )
            has_remote = 'origin' in remote_result.stdout

            if changes == 0 and has_remote:
                return ComponentHealth(
                    name="Git",
                    status=Status.HEALTHY,
                    message="Clean, remote configured"
                )
            elif changes > 0:
                return ComponentHealth(
                    name="Git",
                    status=Status.WARNING,
                    message=f"{changes} uncommitted changes",
                    metrics={"uncommitted": changes}
                )
            else:
                return ComponentHealth(
                    name="Git",
                    status=Status.WARNING,
                    message="No remote configured"
                )
        except Exception as e:
            return ComponentHealth(
                name="Git",
                status=Status.CRITICAL,
                message=f"Error: {str(e)}"
            )

    def _check_orgs(self) -> ComponentHealth:
        """Check org blueprints."""
        orgs_dir = self.root_path / 'orgs'

        if not orgs_dir.exists():
            return ComponentHealth(
                name="Orgs",
                status=Status.CRITICAL,
                message="orgs/ directory missing"
            )

        # Count blueprinted orgs
        orgs = [d.name for d in orgs_dir.iterdir() if d.is_dir()]
        count = len(orgs)

        if count >= 15:
            return ComponentHealth(
                name="Orgs",
                status=Status.HEALTHY,
                message=f"All {count} orgs blueprinted",
                metrics={"blueprinted": count}
            )
        elif count >= 10:
            return ComponentHealth(
                name="Orgs",
                status=Status.WARNING,
                message=f"{count}/15 orgs blueprinted",
                metrics={"blueprinted": count}
            )
        else:
            return ComponentHealth(
                name="Orgs",
                status=Status.CRITICAL,
                message=f"Only {count}/15 orgs blueprinted",
                metrics={"blueprinted": count}
            )

    def _check_prototypes(self) -> ComponentHealth:
        """Check prototype status."""
        proto_dir = self.root_path / 'prototypes'

        if not proto_dir.exists():
            return ComponentHealth(
                name="Prototypes",
                status=Status.WARNING,
                message="No prototypes yet"
            )

        protos = [d.name for d in proto_dir.iterdir() if d.is_dir()]

        if 'operator' in protos:
            return ComponentHealth(
                name="Prototypes",
                status=Status.HEALTHY,
                message=f"Operator + {len(protos)-1} others",
                metrics={"count": len(protos), "list": protos}
            )
        else:
            return ComponentHealth(
                name="Prototypes",
                status=Status.WARNING,
                message=f"{len(protos)} prototypes (no operator)",
                metrics={"count": len(protos)}
            )

    def _check_critical_files(self) -> ComponentHealth:
        """Check critical files exist and are recent."""
        files = {
            '.STATUS': 'Status beacon',
            'MEMORY.md': 'Memory',
            'BLACKROAD_ARCHITECTURE.md': 'Architecture'
        }

        issues = []
        for f, name in files.items():
            path = self.root_path / f
            if not path.exists():
                issues.append(f"{name} missing")
            else:
                # Check if modified recently (within 24h)
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if datetime.now() - mtime > timedelta(days=7):
                    issues.append(f"{name} stale")

        if not issues:
            return ComponentHealth(
                name="Files",
                status=Status.HEALTHY,
                message="All critical files present"
            )
        elif len(issues) == 1:
            return ComponentHealth(
                name="Files",
                status=Status.WARNING,
                message=issues[0]
            )
        else:
            return ComponentHealth(
                name="Files",
                status=Status.CRITICAL,
                message=f"{len(issues)} issues"
            )

    def format_report(self) -> str:
        """Generate health report."""
        health = self.check_all()

        lines = [
            f"🏥 Health Check - {health.timestamp[:19]}",
            "═" * 40,
            f"Overall: {health.overall.value} {health.overall.name}",
            f"Healthy: {health.healthy_count}/{health.total_count}",
            "",
            "Components:",
            "─" * 40,
        ]

        for c in health.components:
            lines.append(f"  {c.status.value} {c.name:12} {c.message}")

        return "\n".join(lines)


# CLI support
if __name__ == "__main__":
    checker = HealthChecker()
    print(checker.format_report())
