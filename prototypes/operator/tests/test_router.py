"""
Tests for the Operator router (end-to-end routing).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from routing.core.router import Operator, RouteResult, route


class TestOperatorRouting:
    """Verify end-to-end routing through the Operator."""

    def setup_method(self):
        self.op = Operator()

    def test_route_returns_result(self):
        result = self.op.route("What is the weather?")
        assert isinstance(result, RouteResult)

    def test_route_destination_not_none(self):
        result = self.op.route("sync salesforce contacts")
        assert result.destination is not None

    def test_route_salesforce_to_foundation(self):
        result = self.op.route("sync salesforce contacts")
        assert result.org_code == "FND"

    def test_route_ai_question(self):
        result = self.op.route("What language model should I use?")
        assert result.org_code == "AI"

    def test_route_deploy_to_cloud(self):
        result = self.op.route("deploy the cloudflare worker")
        assert result.org_code == "CLD"

    def test_route_signal_emitted(self):
        result = self.op.route("security audit required")
        assert "→" in result.signal
        assert "OS" in result.signal

    def test_route_has_timestamp(self):
        result = self.op.route("test query")
        assert result.timestamp
        assert "Z" in result.timestamp

    def test_route_confidence_in_range(self):
        result = self.op.route("create a new lead in salesforce")
        assert 0.0 <= result.confidence <= 1.0

    def test_route_batch(self):
        queries = ["salesforce sync", "deploy worker", "AI question"]
        results = self.op.route_batch(queries)
        assert len(results) == 3
        assert all(isinstance(r, RouteResult) for r in results)

    def test_stats_accumulate(self):
        op = Operator()
        op.route("salesforce query one")
        op.route("another query two")
        stats = op.stats
        assert stats["total"] == 2
        assert stats["avg_confidence"] > 0

    def test_stats_empty(self):
        op = Operator()
        stats = op.stats
        assert stats["total"] == 0

    def test_history_bounded(self):
        op = Operator()
        for i in range(1100):
            op.route(f"query number {i}")
        # History should be trimmed (max 1000, trims to 500)
        assert len(op._history) <= 1000

    def test_explain_returns_string(self):
        explanation = self.op.explain("sync salesforce contacts")
        assert isinstance(explanation, str)
        assert "Destination" in explanation
        assert "Confidence" in explanation

    def test_signal_callback_called(self):
        received = []
        op = Operator(signal_callback=lambda sig, res: received.append(sig))
        op.route("test query with callback")
        assert len(received) == 1
        assert "OS" in received[0]

    def test_route_to_dict(self):
        result = self.op.route("What is the weather?")
        d = result.to_dict()
        assert "destination" in d
        assert "org" in d
        assert "org_code" in d
        assert "confidence" in d
        assert "timestamp" in d

    def test_convenience_function(self):
        result = route("salesforce crm sync")
        assert isinstance(result, RouteResult)
        assert result.org_code == "FND"
