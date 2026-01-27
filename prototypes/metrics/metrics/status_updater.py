#!/usr/bin/env python3
"""
Status Updater - Keep .STATUS file current with live metrics.

Automatically updates the .STATUS beacon with real metrics.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from .counter import Counter
from .health import HealthChecker


class StatusUpdater:
    """
    Update .STATUS file with live metrics.

    Examples:
        >>> updater = StatusUpdater()
        >>> updater.update()  # Updates .STATUS with current metrics
    """

    def __init__(self, root_path: Optional[str] = None):
        """Initialize updater."""
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.status_file = self.root_path / '.STATUS'
        self.counter = Counter(self.root_path)
        self.health = HealthChecker(self.root_path)

    def generate(self) -> str:
        """Generate .STATUS content with live metrics."""
        metrics = self.counter.count_all()
        health = self.health.check_all()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        today = datetime.now().strftime("%Y-%m-%d")

        # Build org status lines
        org_status_lines = []
        orgs_dir = self.root_path / 'orgs'
        org_codes = ["OS", "AI", "CLD", "LAB", "SEC", "FND", "MED", "HW", "INT", "EDU", "GOV", "ARC", "STU", "VEN", "BBX"]
        org_names = {
            "OS": "BlackRoad-OS",
            "AI": "BlackRoad-AI",
            "CLD": "BlackRoad-Cloud",
            "LAB": "BlackRoad-Labs",
            "SEC": "BlackRoad-Security",
            "FND": "BlackRoad-Foundation",
            "MED": "BlackRoad-Media",
            "HW": "BlackRoad-Hardware",
            "INT": "BlackRoad-Interactive",
            "EDU": "BlackRoad-Education",
            "GOV": "BlackRoad-Gov",
            "ARC": "BlackRoad-Archive",
            "STU": "BlackRoad-Studio",
            "VEN": "BlackRoad-Ventures",
            "BBX": "Blackbox-Enterprises"
        }

        for code in org_codes:
            name = org_names.get(code, f"BlackRoad-{code}")
            org_dir = orgs_dir / name
            if code == "OS":
                status = "✔️ active"
                comment = "# The Bridge (you're here)"
            elif org_dir.exists():
                status = "📋 blueprint"
                comment = ""
            else:
                status = "💤 pending"
                comment = ""

            line = f"{code}:  {status:15} {comment}"
            org_status_lines.append(line)

        content = f"""# BLACKROAD STATUS BEACON
# Quick-read state file. Auto-generated with live metrics.

state: ACTIVE
updated: {today}
generated: {now}
session: LIVE

# ═══════════════════════════════════════
# LIVE METRICS
# ═══════════════════════════════════════

files: {metrics.total_files}
lines: {metrics.total_lines:,}
commits: {metrics.total_commits}
commits_today: {metrics.commits_today}

# ═══════════════════════════════════════
# HEALTH STATUS
# ═══════════════════════════════════════

overall: {health.overall.value} {health.overall.name}
healthy: {health.healthy_count}/{health.total_count}

# ═══════════════════════════════════════
# ORG STATUS
# ═══════════════════════════════════════

orgs_blueprinted: {metrics.orgs_blueprinted}/{metrics.orgs_total}
repos_defined: {metrics.repos_defined}

{chr(10).join(org_status_lines)}

# ═══════════════════════════════════════
# COMPONENTS
# ═══════════════════════════════════════

"""
        # Add component status
        for comp in health.components:
            content += f"{comp.name.lower()}: {comp.status.value} {comp.message}\n"

        content += """
# ═══════════════════════════════════════
# QUICK COMMANDS
# ═══════════════════════════════════════

# To view dashboard:
#   python -m metrics.dashboard
#
# To watch live:
#   python -m metrics.dashboard --watch
#
# To get JSON:
#   python -m metrics.dashboard --json

# ═══════════════════════════════════════
# EOF
"""
        return content

    def update(self) -> bool:
        """Update .STATUS file with current metrics."""
        try:
            content = self.generate()
            self.status_file.write_text(content)
            return True
        except Exception as e:
            print(f"Error updating .STATUS: {e}")
            return False

    def preview(self) -> str:
        """Preview what would be written to .STATUS."""
        return self.generate()


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Update .STATUS with live metrics")
    parser.add_argument("--preview", "-p", action="store_true", help="Preview without writing")
    parser.add_argument("--path", type=str, default=None, help="Root path")

    args = parser.parse_args()

    updater = StatusUpdater(args.path)

    if args.preview:
        print(updater.preview())
    else:
        if updater.update():
            print("✔️ .STATUS updated with live metrics")
        else:
            print("❌ Failed to update .STATUS")


if __name__ == "__main__":
    main()
