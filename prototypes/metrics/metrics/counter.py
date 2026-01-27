"""
Counter - Count files, lines, commits, everything.

Real-time code metrics for the BlackRoad ecosystem.
"""

import os
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class CodeMetrics:
    """Code metrics snapshot."""
    total_files: int = 0
    total_lines: int = 0
    total_commits: int = 0
    commits_today: int = 0

    # By type
    files_by_ext: Dict[str, int] = field(default_factory=dict)
    lines_by_ext: Dict[str, int] = field(default_factory=dict)

    # Orgs
    orgs_blueprinted: int = 0
    orgs_total: int = 15
    repos_defined: int = 0

    # Bridge specific
    bridge_files: int = 0
    bridge_lines: int = 0

    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return {
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "total_commits": self.total_commits,
            "commits_today": self.commits_today,
            "files_by_ext": self.files_by_ext,
            "lines_by_ext": self.lines_by_ext,
            "orgs_blueprinted": self.orgs_blueprinted,
            "orgs_total": self.orgs_total,
            "repos_defined": self.repos_defined,
            "bridge_files": self.bridge_files,
            "bridge_lines": self.bridge_lines,
            "timestamp": self.timestamp
        }


class Counter:
    """
    Count everything in the BlackRoad ecosystem.

    Examples:
        >>> counter = Counter()
        >>> metrics = counter.count_all()
        >>> print(f"Files: {metrics.total_files}")
        >>> print(f"Lines: {metrics.total_lines}")
    """

    # File extensions to count
    CODE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.md': 'Markdown',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.json': 'JSON',
        '.sh': 'Shell',
        '.rs': 'Rust',
        '.go': 'Go',
        '.html': 'HTML',
        '.css': 'CSS',
    }

    # Directories to skip
    SKIP_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'dist', 'build'}

    def __init__(self, root_path: Optional[str] = None):
        """Initialize counter with root path."""
        self.root_path = Path(root_path) if root_path else Path.cwd()

    def count_all(self) -> CodeMetrics:
        """Count all metrics."""
        metrics = CodeMetrics()

        # Count files and lines
        self._count_files(metrics)

        # Count commits
        self._count_commits(metrics)

        # Count orgs
        self._count_orgs(metrics)

        return metrics

    def _count_files(self, metrics: CodeMetrics):
        """Count files and lines of code."""
        for root, dirs, files in os.walk(self.root_path):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            for file in files:
                filepath = Path(root) / file
                ext = filepath.suffix.lower()

                # Count file
                metrics.total_files += 1
                metrics.files_by_ext[ext] = metrics.files_by_ext.get(ext, 0) + 1

                # Count lines for code files
                if ext in self.CODE_EXTENSIONS or ext in {'.txt', ''}:
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = sum(1 for _ in f)
                            metrics.total_lines += lines
                            metrics.lines_by_ext[ext] = metrics.lines_by_ext.get(ext, 0) + lines
                    except Exception:
                        pass

        # Bridge specific
        metrics.bridge_files = metrics.total_files
        metrics.bridge_lines = metrics.total_lines

    def _count_commits(self, metrics: CodeMetrics):
        """Count git commits."""
        try:
            # Total commits
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                metrics.total_commits = int(result.stdout.strip())

            # Commits today
            today = datetime.now().strftime('%Y-%m-%d')
            result = subprocess.run(
                ['git', 'log', '--oneline', f'--since={today}'],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                metrics.commits_today = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except Exception:
            pass

    def _count_orgs(self, metrics: CodeMetrics):
        """Count org blueprints."""
        orgs_dir = self.root_path / 'orgs'
        if orgs_dir.exists():
            # Count org directories (excluding README.md)
            orgs = [d for d in orgs_dir.iterdir() if d.is_dir()]
            metrics.orgs_blueprinted = len(orgs)

            # Count repos defined (from REPOS.md files)
            for org_dir in orgs:
                repos_file = org_dir / 'REPOS.md'
                if repos_file.exists():
                    try:
                        content = repos_file.read_text()
                        # Count lines that start with ### (repo headers)
                        metrics.repos_defined += content.count('### ')
                    except Exception:
                        pass

    def quick_count(self) -> Dict[str, int]:
        """Quick count of key metrics."""
        metrics = self.count_all()
        return {
            'files': metrics.total_files,
            'lines': metrics.total_lines,
            'commits': metrics.total_commits,
            'orgs': metrics.orgs_blueprinted,
            'repos': metrics.repos_defined
        }

    def format_summary(self) -> str:
        """Format a summary string."""
        metrics = self.count_all()

        lines = [
            "📊 Code Metrics",
            "─" * 30,
            f"  Files:      {metrics.total_files:,}",
            f"  Lines:      {metrics.total_lines:,}",
            f"  Commits:    {metrics.total_commits:,} ({metrics.commits_today} today)",
            "",
            "📁 By Extension",
            "─" * 30,
        ]

        # Top extensions by lines
        sorted_ext = sorted(
            metrics.lines_by_ext.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        for ext, count in sorted_ext:
            name = self.CODE_EXTENSIONS.get(ext, ext or 'other')
            lines.append(f"  {name:12} {count:,} lines")

        lines.extend([
            "",
            "🏢 Organizations",
            "─" * 30,
            f"  Blueprinted: {metrics.orgs_blueprinted}/{metrics.orgs_total}",
            f"  Repos Defined: {metrics.repos_defined}",
        ])

        return "\n".join(lines)


# CLI support
if __name__ == "__main__":
    counter = Counter()
    print(counter.format_summary())
