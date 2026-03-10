"""
Tests for the request classifier.

The classifier is the routing brain — it maps any query to one of
15 organizations by matching patterns and keywords.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from routing.core.classifier import Classifier, Classification


class TestClassifierBasicRouting:
    """Verify that unambiguous queries route to the correct org."""

    def setup_method(self):
        self.clf = Classifier()

    def test_ai_question(self):
        r = self.clf.classify("What is the weather forecast today?")
        assert r.category == "ai"
        assert r.org_code == "AI"

    def test_crm_salesforce(self):
        r = self.clf.classify("sync salesforce contacts")
        assert r.category == "crm"
        assert r.org_code == "FND"

    def test_crm_lead(self):
        r = self.clf.classify("create a new lead in the pipeline")
        assert r.category == "crm"
        assert r.org_code == "FND"

    def test_security_audit(self):
        r = self.clf.classify("run a security audit on the secrets vault")
        assert r.category == "security"
        assert r.org_code == "SEC"

    def test_infrastructure_deploy(self):
        r = self.clf.classify("deploy the cloudflare worker to edge")
        assert r.category == "infrastructure"
        assert r.org_code == "CLD"

    def test_hardware_pi(self):
        r = self.clf.classify("check the raspberry pi lucidia node")
        assert r.category == "hardware"
        assert r.org_code == "HW"

    def test_education_docs(self):
        r = self.clf.classify("write a tutorial and documentation guide")
        assert r.category == "education"
        assert r.org_code == "EDU"

    def test_governance_vote(self):
        r = self.clf.classify("submit a governance proposal and vote")
        assert r.category == "governance"
        assert r.org_code == "GOV"

    def test_design_ui(self):
        r = self.clf.classify("update the brand color theme in the UI design")
        assert r.category == "design"
        assert r.org_code == "STU"

    def test_experiment_lab(self):
        r = self.clf.classify("run an experiment in the sandbox prototype")
        assert r.category == "experiment"
        assert r.org_code == "LAB"

    def test_storage_backup(self):
        r = self.clf.classify("backup and archive the file data")
        assert r.category == "storage"
        assert r.org_code == "ARC"

    def test_metaverse_game(self):
        r = self.clf.classify("build a 3d game world in the metaverse")
        assert r.category == "metaverse"
        assert r.org_code == "INT"

    def test_media_content(self):
        r = self.clf.classify("publish a new blog post article")
        assert r.category == "media"
        assert r.org_code == "MED"

    def test_enterprise_compliance(self):
        r = self.clf.classify("implement SOC2 and GDPR enterprise compliance")
        assert r.category == "enterprise"
        assert r.org_code == "BBX"

    def test_commerce_marketplace(self):
        r = self.clf.classify("list a product on the marketplace for sale")
        assert r.category == "commerce"
        assert r.org_code == "VEN"


class TestClassifierEdgeCases:
    """Verify classifier behavior on edge and boundary inputs."""

    def setup_method(self):
        self.clf = Classifier()

    def test_empty_query_defaults_to_ai(self):
        r = self.clf.classify("")
        assert r.category == "ai"
        assert r.org_code == "AI"
        assert r.confidence == 0.5

    def test_nonsense_defaults_to_ai(self):
        r = self.clf.classify("xyzzy plugh frobnicate")
        assert r.category == "ai"
        assert r.org_code == "AI"

    def test_returns_classification_object(self):
        r = self.clf.classify("What is Python?")
        assert isinstance(r, Classification)
        assert isinstance(r.matched_patterns, list)
        assert 0.0 <= r.confidence <= 1.0

    def test_confidence_capped_at_one(self):
        # Throw a query with many pattern matches
        r = self.clf.classify(
            "explain how to summarize and analyze ai llm model questions"
        )
        assert r.confidence <= 1.0

    def test_matched_patterns_not_empty_on_match(self):
        r = self.clf.classify("salesforce crm customer lead")
        assert len(r.matched_patterns) > 0

    def test_case_insensitive(self):
        lower = self.clf.classify("SALESFORCE CRM")
        upper = self.clf.classify("salesforce crm")
        assert lower.org_code == upper.org_code

    def test_batch_classify(self):
        queries = ["sync salesforce", "run experiment", "deploy worker"]
        results = self.clf.classify_batch(queries)
        assert len(results) == 3
        assert all(isinstance(r, Classification) for r in results)

    def test_custom_rules(self):
        custom_rules = [
            {
                "category": "custom_test",
                "org_code": "TST",
                "patterns": [r"\bfrobnicator\b"],
                "keywords": [],
            }
        ]
        clf = Classifier(rules=custom_rules)
        r = clf.classify("activate the frobnicator")
        assert r.category == "custom_test"
        assert r.org_code == "TST"
