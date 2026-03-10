"""
Tests for the Dispatcher core.

The dispatcher classifies requests, looks up endpoints,
and routes them to service clients (using MockServiceClient in tests).
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dispatcher.core import Dispatcher, DispatchResult


class TestDispatchResult:
    """Verify DispatchResult post-init behavior."""

    def test_success_signal_format(self):
        r = DispatchResult(
            success=True,
            org="BlackRoad-Foundation",
            org_code="FND",
            service="salesforce",
            endpoint="https://example.com",
            latency_ms=42,
        )
        assert "FND" in r.signal
        assert "dispatched" in r.signal
        assert "42ms" in r.signal

    def test_failure_signal_format(self):
        r = DispatchResult(
            success=False,
            org="BlackRoad-Foundation",
            org_code="FND",
            service="salesforce",
            endpoint="",
            error="connection refused",
        )
        assert "FND" in r.signal
        assert "dispatch_failed" in r.signal
        assert "connection refused" in r.signal

    def test_timestamp_auto_set(self):
        r = DispatchResult(
            success=True, org="OS", org_code="OS",
            service="operator", endpoint="http://localhost"
        )
        assert r.timestamp
        assert "T" in r.timestamp  # ISO format


class TestDispatcherMock:
    """Verify Dispatcher routing with MockServiceClient."""

    def _run(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    def setup_method(self):
        self.dispatcher = Dispatcher(mock=True)

    def test_dispatch_returns_result(self):
        result = self._run(self.dispatcher.dispatch("test query"))
        assert isinstance(result, DispatchResult)

    def test_dispatch_has_org_code(self):
        result = self._run(self.dispatcher.dispatch("test query"))
        assert result.org_code is not None
        assert len(result.org_code) >= 2

    def test_dispatch_salesforce_routes_to_fnd(self):
        result = self._run(self.dispatcher.dispatch("sync salesforce contacts"))
        assert result.org_code == "FND"

    def test_dispatch_records_latency(self):
        result = self._run(self.dispatcher.dispatch("test query"))
        assert result.latency_ms >= 0

    def test_dispatch_appends_to_history(self):
        d = Dispatcher(mock=True)
        self._run(d.dispatch("query one"))
        self._run(d.dispatch("query two"))
        assert len(d._history) == 2

    def test_dispatch_to_known_org(self):
        result = self._run(self.dispatcher.dispatch_to("OS"))
        assert result.org_code == "OS"

    def test_dispatch_to_unknown_org_returns_error(self):
        result = self._run(self.dispatcher.dispatch_to("ZZZNOPE"))
        assert not result.success
        assert result.error is not None

    def test_stats_empty(self):
        d = Dispatcher(mock=True)
        stats = d.stats
        assert stats["total"] == 0
        assert stats["success_rate"] == 0

    def test_stats_after_dispatch(self):
        d = Dispatcher(mock=True)
        self._run(d.dispatch("some query"))
        stats = d.stats
        assert stats["total"] == 1

    def test_list_routes(self):
        routes = self.dispatcher.list_routes()
        assert isinstance(routes, list)
        assert len(routes) > 0
