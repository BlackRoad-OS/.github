"""
Tests for the dispatcher Registry.

The registry loads routes/registry.yaml and provides org, service,
and endpoint lookups plus pattern-based routing rules.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dispatcher.registry import Registry, Org, Service, RoutingRule


class TestRegistryLoading:
    """Verify the registry loads correctly from YAML."""

    def setup_method(self):
        self.reg = Registry()

    def test_loads_15_orgs(self):
        orgs = self.reg.list_orgs()
        assert len(orgs) == 15

    def test_all_orgs_have_codes(self):
        expected_codes = {
            "OS", "AI", "CLD", "HW", "LAB", "SEC", "FND",
            "MED", "INT", "EDU", "GOV", "ARC", "STU", "VEN", "BBX",
        }
        loaded_codes = {org.code for org in self.reg.list_orgs()}
        assert expected_codes == loaded_codes

    def test_org_has_required_fields(self):
        org = self.reg.get_org("OS")
        assert org is not None
        assert org.name
        assert org.code == "OS"
        assert org.status
        assert org.description

    def test_rules_loaded(self):
        assert len(self.reg.rules) > 0

    def test_rules_sorted_by_priority(self):
        priorities = [r.priority for r in self.reg.rules]
        assert priorities == sorted(priorities, reverse=True)


class TestRegistryLookup:
    """Verify get_org, get_service, and get_endpoint methods."""

    def setup_method(self):
        self.reg = Registry()

    def test_get_org_valid(self):
        org = self.reg.get_org("FND")
        assert org is not None
        assert isinstance(org, Org)

    def test_get_org_invalid_returns_none(self):
        org = self.reg.get_org("DOESNOTEXIST")
        assert org is None

    def test_get_service_valid(self):
        # FND org should have a salesforce service
        org = self.reg.get_org("FND")
        assert org is not None
        service = org.default_service()
        assert service is not None
        assert isinstance(service, Service)

    def test_get_endpoint_known_org(self):
        endpoint = self.reg.get_endpoint("OS")
        assert endpoint is not None
        assert isinstance(endpoint, str)

    def test_get_endpoint_unknown_org_returns_none(self):
        result = self.reg.get_endpoint("ZZZNOPE")
        assert result is None

    def test_org_default_service_returns_service(self):
        org = self.reg.get_org("AI")
        assert org is not None
        svc = org.default_service()
        assert svc is not None

    def test_org_empty_services_returns_none(self):
        org = Org(
            name="Empty Org",
            code="EMP",
            status="planned",
            description="",
            github="",
            primary_node="",
            services={},
            repos=[],
        )
        assert org.default_service() is None
        assert org.get_service("anything") is None


class TestRegistryMatching:
    """Verify pattern-based routing rules."""

    def setup_method(self):
        self.reg = Registry()

    def test_match_returns_tuple(self):
        result = self.reg.match("sync salesforce contacts")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_match_salesforce_to_fnd(self):
        org_code, _ = self.reg.match("sync salesforce contacts")
        assert org_code == "FND"

    def test_match_unknown_falls_back(self):
        org_code, _ = self.reg.match("xyzzy completely unknown query")
        # Should return some fallback, not crash
        assert org_code is not None

    def test_routing_rule_matches(self):
        rule = RoutingRule(pattern=r"salesforce", org="FND", service="salesforce", priority=10)
        assert rule.matches("sync salesforce contacts")
        assert not rule.matches("deploy cloudflare worker")

    def test_routing_rule_case_insensitive(self):
        rule = RoutingRule(pattern=r"salesforce", org="FND", service="salesforce", priority=10)
        assert rule.matches("SALESFORCE SYNC")
        assert rule.matches("Salesforce Lead")
