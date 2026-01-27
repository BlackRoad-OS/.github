"""
Browser - Core explorer functionality.

Navigate the BlackRoad ecosystem programmatically.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class Repo:
    """A repository definition."""
    name: str
    description: str
    priority: str = "P1"
    status: str = "planned"


@dataclass
class Org:
    """An organization."""
    name: str
    code: str
    description: str
    repos: List[Repo] = field(default_factory=list)
    signals: List[str] = field(default_factory=list)
    readme_content: str = ""
    path: Optional[Path] = None

    @property
    def repo_count(self) -> int:
        return len(self.repos)


# Org registry with codes and full names
ORG_REGISTRY = {
    "OS": ("BlackRoad-OS", "The Bridge - core infrastructure"),
    "AI": ("BlackRoad-AI", "Intelligence routing"),
    "CLD": ("BlackRoad-Cloud", "Edge compute, Cloudflare"),
    "HW": ("BlackRoad-Hardware", "Pi cluster, IoT, Hailo"),
    "LAB": ("BlackRoad-Labs", "Experiments, R&D"),
    "SEC": ("BlackRoad-Security", "Auth, secrets, audit"),
    "FND": ("BlackRoad-Foundation", "Salesforce, CRM, billing"),
    "MED": ("BlackRoad-Media", "Blog, docs, brand"),
    "INT": ("BlackRoad-Interactive", "Metaverse, 3D, games"),
    "EDU": ("BlackRoad-Education", "Learning, tutorials"),
    "GOV": ("BlackRoad-Gov", "Governance, voting"),
    "ARC": ("BlackRoad-Archive", "Storage, backups"),
    "STU": ("BlackRoad-Studio", "Design system, UI"),
    "VEN": ("BlackRoad-Ventures", "Marketplace, commerce"),
    "BBX": ("Blackbox-Enterprises", "Enterprise solutions"),
}


class Explorer:
    """
    Explore the BlackRoad ecosystem.

    Examples:
        >>> exp = Explorer()
        >>> orgs = exp.list_orgs()
        >>> for org in orgs:
        ...     print(f"{org.code}: {org.name}")

        >>> ai = exp.get_org("AI")
        >>> print(ai.description)
        >>> for repo in ai.repos:
        ...     print(f"  - {repo.name}")
    """

    def __init__(self, root_path: Optional[str] = None):
        """Initialize explorer."""
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.orgs_path = self.root_path / "orgs"
        self._orgs_cache: Dict[str, Org] = {}

    def list_orgs(self) -> List[Org]:
        """List all organizations."""
        orgs = []
        for code, (name, desc) in ORG_REGISTRY.items():
            org = self.get_org(code)
            if org:
                orgs.append(org)
            else:
                orgs.append(Org(name=name, code=code, description=desc))
        return orgs

    def get_org(self, code: str) -> Optional[Org]:
        """Get organization by code."""
        code = code.upper()

        if code in self._orgs_cache:
            return self._orgs_cache[code]

        if code not in ORG_REGISTRY:
            return None

        name, desc = ORG_REGISTRY[code]
        org_path = self.orgs_path / name

        if not org_path.exists():
            return Org(name=name, code=code, description=desc)

        # Load org data
        org = Org(
            name=name,
            code=code,
            description=desc,
            path=org_path
        )

        # Load README
        readme_path = org_path / "README.md"
        if readme_path.exists():
            org.readme_content = readme_path.read_text()

        # Load repos from REPOS.md
        repos_path = org_path / "REPOS.md"
        if repos_path.exists():
            org.repos = self._parse_repos(repos_path)

        # Load signals
        signals_path = org_path / "SIGNALS.md"
        if signals_path.exists():
            org.signals = self._parse_signals(signals_path)

        self._orgs_cache[code] = org
        return org

    def _parse_repos(self, repos_path: Path) -> List[Repo]:
        """Parse REPOS.md to extract repo definitions."""
        repos = []
        content = repos_path.read_text()

        # Find repo headers (### name)
        pattern = r'###\s+\d*\.?\s*`?(\w+)`?\s*\n+\*\*(?:Status|Purpose):\*\*\s*([^\n]+)'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for name, desc in matches:
            repos.append(Repo(name=name.strip('`'), description=desc.strip()))

        # Fallback: just find ### headers
        if not repos:
            header_pattern = r'###\s+\d*\.?\s*`?([^`\n]+)`?'
            for match in re.finditer(header_pattern, content):
                name = match.group(1).strip()
                if name and not name.startswith('('):
                    repos.append(Repo(name=name, description=""))

        return repos

    def _parse_signals(self, signals_path: Path) -> List[str]:
        """Parse SIGNALS.md to extract signal types."""
        signals = []
        content = signals_path.read_text()

        # Find signal patterns (emoji followed by description)
        signal_emojis = ['✔️', '❌', '⏳', '📡', '🎯', '🔄', '⬆️', '⬇️', '💓', '🔴', '🟡', '🟢']
        for emoji in signal_emojis:
            if emoji in content:
                signals.append(emoji)

        return signals

    def search(self, term: str) -> List[Dict]:
        """Search across all orgs."""
        results = []
        term_lower = term.lower()

        for code in ORG_REGISTRY:
            org = self.get_org(code)
            if not org:
                continue

            # Search in org name/description
            if term_lower in org.name.lower() or term_lower in org.description.lower():
                results.append({
                    "type": "org",
                    "org": org.code,
                    "name": org.name,
                    "match": org.description
                })

            # Search in repos
            for repo in org.repos:
                if term_lower in repo.name.lower() or term_lower in repo.description.lower():
                    results.append({
                        "type": "repo",
                        "org": org.code,
                        "name": repo.name,
                        "match": repo.description
                    })

            # Search in README
            if org.readme_content and term_lower in org.readme_content.lower():
                results.append({
                    "type": "content",
                    "org": org.code,
                    "name": f"{org.name}/README.md",
                    "match": "Found in README"
                })

        return results

    def format_org(self, code: str) -> str:
        """Format org details as string."""
        org = self.get_org(code)
        if not org:
            return f"Org '{code}' not found"

        lines = [
            "═" * 50,
            f"  {org.name} [{org.code}]",
            f"  {org.description}",
            "═" * 50,
            "",
        ]

        if org.repos:
            lines.append("  Repos:")
            for repo in org.repos:
                lines.append(f"    • {repo.name:15} {repo.description[:40]}")
            lines.append("")

        if org.signals:
            lines.append(f"  Signals: {' '.join(org.signals)}")
            lines.append("")

        if org.path:
            lines.append(f"  Path: {org.path}")

        return "\n".join(lines)

    def format_list(self) -> str:
        """Format org list as string."""
        lines = [
            "🌉 BlackRoad Organizations",
            "═" * 50,
            ""
        ]

        for i, (code, (name, desc)) in enumerate(ORG_REGISTRY.items(), 1):
            org = self.get_org(code)
            repo_count = org.repo_count if org else 0
            status = "✔️" if org and org.path else "📋"
            lines.append(f"  {i:2}. [{code:3}] {name:25} {status} ({repo_count} repos)")

        return "\n".join(lines)

    def tree(self) -> str:
        """Generate directory tree."""
        lines = ["BlackRoad-OS/.github/", "│"]

        # Core files
        core_files = [".STATUS", "INDEX.md", "MEMORY.md", "SIGNALS.md", "STREAMS.md", "REPO_MAP.md"]
        for f in core_files:
            if (self.root_path / f).exists():
                lines.append(f"├── {f}")

        # Orgs
        lines.append("├── orgs/")
        if self.orgs_path.exists():
            org_dirs = sorted([d.name for d in self.orgs_path.iterdir() if d.is_dir()])
            for i, org_dir in enumerate(org_dirs):
                prefix = "│   └──" if i == len(org_dirs) - 1 else "│   ├──"
                lines.append(f"{prefix} {org_dir}/")

        # Prototypes
        proto_path = self.root_path / "prototypes"
        if proto_path.exists():
            lines.append("├── prototypes/")
            proto_dirs = sorted([d.name for d in proto_path.iterdir() if d.is_dir()])
            for i, proto_dir in enumerate(proto_dirs):
                prefix = "│   └──" if i == len(proto_dirs) - 1 else "│   ├──"
                lines.append(f"{prefix} {proto_dir}/")

        # Profile
        lines.append("└── profile/")
        lines.append("    └── README.md")

        return "\n".join(lines)
