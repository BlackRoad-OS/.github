#!/usr/bin/env python3
"""
Dashboard - Real-time KPIs at a glance.

The nerve center for BlackRoad monitoring.
"""

import os
import sys
import time
import argparse
from datetime import datetime
from typing import Optional
from pathlib import Path

from .counter import Counter, CodeMetrics
from .health import HealthChecker, HealthStatus, Status


class Dashboard:
    """
    Real-time dashboard for BlackRoad KPIs.

    Examples:
        >>> dashboard = Dashboard()
        >>> dashboard.show()  # One-time display

        >>> dashboard.watch(interval=5)  # Live updates
    """

    def __init__(self, root_path: Optional[str] = None):
        """Initialize dashboard."""
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.counter = Counter(self.root_path)
        self.health = HealthChecker(self.root_path)

    def show(self, compact: bool = False) -> str:
        """Generate dashboard display."""
        metrics = self.counter.count_all()
        health = self.health.check_all()

        if compact:
            return self._compact_view(metrics, health)
        return self._full_view(metrics, health)

    def _full_view(self, metrics: CodeMetrics, health: HealthStatus) -> str:
        """Full dashboard view."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate percentages
        org_pct = (metrics.orgs_blueprinted / metrics.orgs_total) * 100

        lines = [
            "╔══════════════════════════════════════════════════════════════════╗",
            "║              🌉 BLACKROAD BRIDGE DASHBOARD 🌉                     ║",
            f"║                     {now}                        ║",
            "╠══════════════════════════════════════════════════════════════════╣",
            "║                                                                  ║",
            f"║  HEALTH: {health.overall.value} {health.overall.name:8}     COMPONENTS: {health.healthy_count}/{health.total_count} healthy        ║",
            "║                                                                  ║",
            "╠══════════════════════════════════════════════════════════════════╣",
            "║   CODE METRICS        │   ORG STATUS         │   SYSTEM          ║",
            "║  ─────────────────────┼──────────────────────┼─────────────────  ║",
        ]

        # Main metrics row
        lines.append(
            f"║   Files:    {metrics.total_files:>6,}   │   Blueprints: {metrics.orgs_blueprinted:>2}/{metrics.orgs_total:<2}   │   Bridge: {health.overall.value}      ║"
        )
        lines.append(
            f"║   Lines:    {metrics.total_lines:>6,}   │   Progress:  {org_pct:>3.0f}%    │   Git:    {self._git_status(health)}      ║"
        )
        lines.append(
            f"║   Commits:  {metrics.total_commits:>6,}   │   Repos:     {metrics.repos_defined:>3}     │   Files:  {self._files_status(health)}      ║"
        )

        lines.extend([
            "║                       │                      │                   ║",
            "╠══════════════════════════════════════════════════════════════════╣",
            "║   BREAKDOWN BY TYPE                                              ║",
            "║  ─────────────────────────────────────────────────────────────   ║",
        ])

        # Top 5 file types
        sorted_ext = sorted(
            metrics.lines_by_ext.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        type_line = "║   "
        for ext, lines_count in sorted_ext:
            name = self.counter.CODE_EXTENSIONS.get(ext, ext or '?')[:6]
            type_line += f"{name}: {lines_count:,}  "
        type_line = type_line.ljust(67) + "║"
        lines.append(type_line)

        lines.extend([
            "║                                                                  ║",
            "╠══════════════════════════════════════════════════════════════════╣",
            "║   COMPONENTS                                                     ║",
            "║  ─────────────────────────────────────────────────────────────   ║",
        ])

        # Component status
        for comp in health.components:
            comp_line = f"║   {comp.status.value} {comp.name:12} {comp.message[:45]}"
            lines.append(comp_line.ljust(67) + "║")

        lines.extend([
            "║                                                                  ║",
            "╠══════════════════════════════════════════════════════════════════╣",
            "║   QUICK STATS                                                    ║",
            "║  ─────────────────────────────────────────────────────────────   ║",
        ])

        # Quick stats
        commits_today = metrics.commits_today
        lines.append(
            f"║   Today: {commits_today} commits   │   Session active   │   All systems go     ║"
        )

        lines.extend([
            "║                                                                  ║",
            "╚══════════════════════════════════════════════════════════════════╝",
        ])

        return "\n".join(lines)

    def _compact_view(self, metrics: CodeMetrics, health: HealthStatus) -> str:
        """Compact one-line view."""
        return (
            f"{health.overall.value} "
            f"Files:{metrics.total_files} "
            f"Lines:{metrics.total_lines:,} "
            f"Commits:{metrics.total_commits} "
            f"Orgs:{metrics.orgs_blueprinted}/{metrics.orgs_total} "
            f"Health:{health.healthy_count}/{health.total_count}"
        )

    def _git_status(self, health: HealthStatus) -> str:
        """Get git status emoji."""
        for c in health.components:
            if c.name == "Git":
                return c.status.value
        return "❓"

    def _files_status(self, health: HealthStatus) -> str:
        """Get files status emoji."""
        for c in health.components:
            if c.name == "Files":
                return c.status.value
        return "❓"

    def watch(self, interval: int = 5):
        """Watch mode - updates every interval seconds."""
        try:
            while True:
                # Clear screen
                os.system('clear' if os.name != 'nt' else 'cls')

                # Show dashboard
                print(self.show())
                print(f"\n  Refreshing every {interval}s... (Ctrl+C to exit)")

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard closed.")

    def json(self) -> dict:
        """Return dashboard data as JSON-serializable dict."""
        metrics = self.counter.count_all()
        health = self.health.check_all()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics.to_dict(),
            "health": health.to_dict()
        }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="BlackRoad Dashboard")

    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch mode (live updates)"
    )

    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="Update interval in seconds (default: 5)"
    )

    parser.add_argument(
        "--compact", "-c",
        action="store_true",
        help="Compact one-line output"
    )

    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )

    parser.add_argument(
        "--path", "-p",
        type=str,
        default=None,
        help="Root path to analyze"
    )

    args = parser.parse_args()

    dashboard = Dashboard(args.path)

    if args.json:
        import json
        print(json.dumps(dashboard.json(), indent=2))
    elif args.watch:
        dashboard.watch(args.interval)
    elif args.compact:
        print(dashboard.show(compact=True))
    else:
        print(dashboard.show())


if __name__ == "__main__":
    main()
