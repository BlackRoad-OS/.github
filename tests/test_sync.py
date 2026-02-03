#!/usr/bin/env python3
"""
Test suite for sync functionality
Tests that updates are properly dispatched to target orgs
"""

import json
import os
import sys
import yaml
from pathlib import Path


class TestSyncToOrgs:
    """Test sync-to-orgs workflow functionality"""

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.errors = []

    def error(self, msg):
        """Record an error"""
        self.errors.append(msg)
        print(f"❌ {msg}")

    def success(self, msg):
        """Record success"""
        print(f"✓ {msg}")

    def test_workflow_exists(self):
        """Test that sync-to-orgs workflow file exists"""
        workflow_path = self.root / ".github/workflows/sync-to-orgs.yml"
        if not workflow_path.exists():
            self.error("sync-to-orgs.yml workflow not found")
            return False

        self.success("sync-to-orgs.yml workflow exists")
        return True

    def test_workflow_valid_yaml(self):
        """Test that workflow is valid YAML"""
        workflow_path = self.root / ".github/workflows/sync-to-orgs.yml"

        try:
            with open(workflow_path) as f:
                workflow = yaml.safe_load(f)

            assert "name" in workflow, "Missing 'name' field"
            # 'on' gets parsed as True by PyYAML, so check for True or 'on'
            assert True in workflow or "on" in workflow, "Missing 'on' field"
            assert "jobs" in workflow, "Missing 'jobs' field"

            self.success("Workflow YAML is valid")
            return True
        except Exception as e:
            self.error(f"Invalid workflow YAML: {e}")
            return False

    def test_workflow_triggers(self):
        """Test that workflow has correct triggers"""
        workflow_path = self.root / ".github/workflows/sync-to-orgs.yml"

        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)

        # 'on' gets parsed as True by PyYAML
        triggers = workflow.get(True, workflow.get("on", {}))

        # Should trigger on push to main
        if "push" in triggers:
            branches = triggers["push"].get("branches", [])
            if "main" in branches:
                self.success("Workflow triggers on push to main")
            else:
                self.error("Workflow does not trigger on push to main")

        # Should have manual dispatch
        if "workflow_dispatch" in triggers:
            self.success("Workflow has manual dispatch")
        else:
            self.error("Workflow missing workflow_dispatch")

    def test_registry_loads(self):
        """Test that registry.yaml loads successfully"""
        registry_path = self.root / "routes/registry.yaml"

        if not registry_path.exists():
            self.error("routes/registry.yaml not found")
            return False

        try:
            with open(registry_path) as f:
                registry = yaml.safe_load(f)

            assert "orgs" in registry, "Missing 'orgs' in registry"
            assert "rules" in registry, "Missing 'rules' in registry"

            orgs = registry["orgs"]
            self.success(f"Registry loads with {len(orgs)} orgs")
            return True
        except Exception as e:
            self.error(f"Failed to load registry: {e}")
            return False

    def test_active_orgs(self):
        """Test that active orgs are properly configured"""
        registry_path = self.root / "routes/registry.yaml"

        with open(registry_path) as f:
            registry = yaml.safe_load(f)

        active_orgs = []
        for code, org in registry["orgs"].items():
            if org.get("status") == "active":
                active_orgs.append(code)

                # Validate org structure
                if "name" not in org:
                    self.error(f"Org {code} missing 'name'")
                if "github" not in org:
                    self.error(f"Org {code} missing 'github'")
                if "repos" not in org:
                    self.error(f"Org {code} missing 'repos'")

        if active_orgs:
            self.success(f"Found {len(active_orgs)} active orgs: {', '.join(active_orgs)}")
        else:
            self.error("No active orgs found in registry")

    def test_org_repos_valid(self):
        """Test that org repos have valid structure"""
        registry_path = self.root / "routes/registry.yaml"

        with open(registry_path) as f:
            registry = yaml.safe_load(f)

        total_repos = 0
        for code, org in registry["orgs"].items():
            if org.get("status") != "active":
                continue

            repos = org.get("repos", [])
            for repo in repos:
                total_repos += 1

                if "name" not in repo:
                    self.error(f"Repo in {code} missing 'name'")
                if "url" not in repo:
                    self.error(f"Repo in {code} missing 'url'")
                if not repo.get("url", "").startswith("https://github.com/"):
                    self.error(f"Invalid repo URL in {code}: {repo.get('url')}")

        self.success(f"Validated {total_repos} repo configurations")

    def test_dispatch_payload_format(self):
        """Test that dispatch payload format is correct"""
        workflow_path = self.root / ".github/workflows/sync-to-orgs.yml"

        with open(workflow_path) as f:
            content = f.read()

        # Check for dispatch event structure
        required_fields = ["event_type", "client_payload"]
        for field in required_fields:
            if field in content:
                self.success(f"Dispatch includes '{field}'")
            else:
                self.error(f"Dispatch missing '{field}'")

    def test_auto_merge_workflow_exists(self):
        """Test that auto-merge workflow exists"""
        workflow_path = self.root / ".github/workflows/auto-merge.yml"
        if not workflow_path.exists():
            self.error("auto-merge.yml workflow not found")
            return False

        self.success("auto-merge.yml workflow exists")
        return True

    def test_auto_merge_triggers(self):
        """Test that auto-merge has correct triggers"""
        workflow_path = self.root / ".github/workflows/auto-merge.yml"

        if not workflow_path.exists():
            return

        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)

        # 'on' gets parsed as True by PyYAML
        triggers = workflow.get(True, workflow.get("on", {}))

        # Should trigger on workflow_run for CI
        if "workflow_run" in triggers:
            workflows = triggers["workflow_run"].get("workflows", [])
            if "CI" in workflows:
                self.success("Auto-merge triggers after CI workflow")
            else:
                self.error("Auto-merge does not trigger after CI")
        else:
            self.error("Auto-merge missing workflow_run trigger")

    def test_ci_workflow_valid(self):
        """Test that CI workflow is properly configured"""
        workflow_path = self.root / ".github/workflows/ci.yml"

        if not workflow_path.exists():
            self.error("ci.yml workflow not found")
            return False

        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)

        # Check for required jobs
        jobs = workflow.get("jobs", {})
        required_jobs = ["lint", "validate-config"]

        for job_name in required_jobs:
            if job_name in jobs:
                self.success(f"CI has '{job_name}' job")
            else:
                self.error(f"CI missing '{job_name}' job")

        return True

    def run_all(self):
        """Run all tests"""
        print("🧪 Running sync functionality tests...\n")

        tests = [
            self.test_workflow_exists,
            self.test_workflow_valid_yaml,
            self.test_workflow_triggers,
            self.test_registry_loads,
            self.test_active_orgs,
            self.test_org_repos_valid,
            self.test_dispatch_payload_format,
            self.test_auto_merge_workflow_exists,
            self.test_auto_merge_triggers,
            self.test_ci_workflow_valid,
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                self.error(f"Test {test.__name__} failed with exception: {e}")
            print()

        # Summary
        print("=" * 50)
        if self.errors:
            print(f"❌ Tests failed: {len(self.errors)} error(s)")
            for error in self.errors:
                print(f"  - {error}")
            return 1
        else:
            print("✓ All tests passed!")
            return 0


if __name__ == "__main__":
    tester = TestSyncToOrgs()
    sys.exit(tester.run_all())
