"""
Registry - Load and manage the routing registry.

The registry contains all orgs, services, and endpoints.
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import yaml


@dataclass
class Service:
    """A service within an org."""
    name: str
    description: str
    type: str                      # internal, external
    endpoint: str
    health: Optional[str] = None
    provider: Optional[str] = None  # salesforce, stripe, etc.
    fallback: Optional[str] = None
    nodes: List[str] = field(default_factory=list)
    auth: Optional[str] = None


@dataclass
class Repo:
    """A repository within an org."""
    name: str
    description: str
    url: str


@dataclass
class Org:
    """An organization in the BlackRoad ecosystem."""
    name: str
    code: str
    status: str                    # active, planned
    description: str
    github: str
    primary_node: str
    services: Dict[str, Service] = field(default_factory=dict)
    repos: List[Repo] = field(default_factory=list)

    def get_service(self, name: str) -> Optional[Service]:
        """Get a service by name."""
        return self.services.get(name)

    def default_service(self) -> Optional[Service]:
        """Get the default service for this org."""
        if self.services:
            return list(self.services.values())[0]
        return None


@dataclass
class RoutingRule:
    """A routing rule for pattern matching."""
    pattern: str
    org: str
    service: str
    priority: int = 0

    def matches(self, text: str) -> bool:
        """Check if text matches this rule."""
        return bool(re.search(self.pattern, text.lower()))


class Registry:
    """
    The routing registry - knows where everything lives.

    Usage:
        registry = Registry()

        # Get an org
        org = registry.get_org("FND")

        # Get a service
        service = registry.get_service("FND", "salesforce")

        # Find by pattern
        org, service = registry.match("sync salesforce")
    """

    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize the registry.

        Args:
            registry_path: Path to registry.yaml
        """
        self.orgs: Dict[str, Org] = {}
        self.rules: List[RoutingRule] = []
        self.defaults: Dict[str, Any] = {}

        # Find registry file
        if registry_path:
            self.registry_path = Path(registry_path)
        else:
            # Look in standard locations
            candidates = [
                Path(__file__).parent.parent.parent.parent / "routes" / "registry.yaml",
                Path.cwd() / "routes" / "registry.yaml",
                Path.cwd() / "registry.yaml",
            ]
            for p in candidates:
                if p.exists():
                    self.registry_path = p
                    break
            else:
                self.registry_path = candidates[0]

        self._load()

    def _load(self):
        """Load the registry from YAML."""
        if not self.registry_path.exists():
            print(f"Warning: Registry not found at {self.registry_path}")
            return

        with open(self.registry_path) as f:
            data = yaml.safe_load(f)

        # Load orgs
        for code, org_data in data.get("orgs", {}).items():
            services = {}
            for svc_name, svc_data in org_data.get("services", {}).items():
                services[svc_name] = Service(
                    name=svc_name,
                    description=svc_data.get("description", ""),
                    type=svc_data.get("type", "internal"),
                    endpoint=svc_data.get("endpoint", ""),
                    health=svc_data.get("health"),
                    provider=svc_data.get("provider"),
                    fallback=svc_data.get("fallback"),
                    nodes=svc_data.get("nodes", []),
                    auth=svc_data.get("auth"),
                )

            repos = []
            for repo_data in org_data.get("repos", []):
                repos.append(Repo(
                    name=repo_data.get("name", ""),
                    description=repo_data.get("description", ""),
                    url=repo_data.get("url", ""),
                ))

            self.orgs[code] = Org(
                name=org_data.get("name", ""),
                code=code,
                status=org_data.get("status", "planned"),
                description=org_data.get("description", ""),
                github=org_data.get("github", ""),
                primary_node=org_data.get("primary_node", ""),
                services=services,
                repos=repos,
            )

        # Load rules
        for rule_data in data.get("rules", []):
            self.rules.append(RoutingRule(
                pattern=rule_data.get("pattern", ""),
                org=rule_data.get("org", "AI"),
                service=rule_data.get("service", ""),
                priority=rule_data.get("priority", 0),
            ))

        # Sort rules by priority (highest first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

        # Load defaults
        self.defaults = data.get("defaults", {})

    def get_org(self, code: str) -> Optional[Org]:
        """Get an org by code."""
        return self.orgs.get(code)

    def get_service(self, org_code: str, service_name: str) -> Optional[Service]:
        """Get a service by org code and service name."""
        org = self.orgs.get(org_code)
        if org:
            return org.get_service(service_name)
        return None

    def get_endpoint(self, org_code: str, service_name: Optional[str] = None) -> Optional[str]:
        """Get the endpoint URL for a service."""
        org = self.orgs.get(org_code)
        if not org:
            return None

        if service_name:
            service = org.get_service(service_name)
        else:
            # Use default service
            default_svc_name = self.defaults.get("default_services", {}).get(org_code)
            if default_svc_name:
                service = org.get_service(default_svc_name)
            else:
                service = org.default_service()

        return service.endpoint if service else None

    def match(self, text: str) -> tuple:
        """
        Match text against routing rules.

        Returns:
            (org_code, service_name) or (fallback_org, None)
        """
        # Check rules
        for rule in self.rules:
            if rule.matches(text):
                return (rule.org, rule.service)

        # Return fallback
        fallback = self.defaults.get("fallback_org", "AI")
        return (fallback, None)

    def list_orgs(self) -> List[Org]:
        """List all orgs."""
        return list(self.orgs.values())

    def list_services(self, org_code: Optional[str] = None) -> List[tuple]:
        """
        List all services.

        Returns list of (org_code, service_name, service) tuples.
        """
        results = []
        orgs = [self.orgs[org_code]] if org_code else self.orgs.values()

        for org in orgs:
            for name, service in org.services.items():
                results.append((org.code, name, service))

        return results

    def to_dict(self) -> Dict[str, Any]:
        """Export registry as dict."""
        return {
            "orgs": {
                code: {
                    "name": org.name,
                    "status": org.status,
                    "services": list(org.services.keys()),
                    "repos": [r.name for r in org.repos],
                }
                for code, org in self.orgs.items()
            },
            "rules": len(self.rules),
        }
