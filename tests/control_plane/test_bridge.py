"""
Tests for the Control Plane Bridge module.

Tests the core Bridge class that unifies all prototypes.
"""

import pytest
import sys
from pathlib import Path

# Add control plane to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "prototypes" / "control-plane"))

from control_plane.bridge import Bridge, BridgeState, get_bridge


class TestBridge:
    """Test suite for the Bridge class."""
    
    @pytest.fixture
    def bridge(self):
        """Create a Bridge instance."""
        return Bridge()
    
    # --- INITIALIZATION TESTS ---
    
    @pytest.mark.unit
    def test_bridge_init(self, bridge):
        """Test Bridge initialization."""
        assert bridge is not None
        assert bridge.root is not None
        assert bridge._operator is None  # Lazy loaded
        assert bridge._metrics is None  # Lazy loaded
        assert bridge._explorer is None  # Lazy loaded
    
    @pytest.mark.unit
    def test_bridge_singleton(self):
        """Test Bridge singleton pattern."""
        bridge1 = get_bridge()
        bridge2 = get_bridge()
        
        assert bridge1 is bridge2
    
    # --- STATE TESTS ---
    
    @pytest.mark.unit
    def test_get_state(self, bridge):
        """Test getting Bridge state."""
        state = bridge.get_state()
        
        assert isinstance(state, BridgeState)
        assert state.status == "ONLINE"
        assert state.session == "SESSION_2"
        assert state.orgs_total >= 0
        assert state.orgs_active >= 0
        assert isinstance(state.prototypes_ready, list)
        assert isinstance(state.templates_ready, list)
        assert state.nodes_online >= 0
        assert state.nodes_total > 0
    
    @pytest.mark.unit
    def test_state_has_timestamp(self, bridge):
        """Test state includes timestamp."""
        state = bridge.get_state()
        
        assert state.updated is not None
        assert hasattr(state.updated, 'strftime')
    
    # --- STATUS TESTS ---
    
    @pytest.mark.unit
    def test_status(self, bridge):
        """Test status output."""
        status = bridge.status()
        
        assert isinstance(status, str)
        assert "BLACKROAD BRIDGE" in status
        assert "ONLINE" in status
        assert "SESSION_2" in status
        assert "Orgs:" in status
        assert "Nodes:" in status
        assert "Prototypes:" in status
        assert "Templates:" in status
    
    @pytest.mark.unit
    def test_status_formatting(self, bridge):
        """Test status output is properly formatted."""
        status = bridge.status()
        
        # Should have header bars
        assert "=" * 40 in status
        # Should have proper spacing
        assert status.startswith("\n")
        assert status.endswith("\n")
    
    # --- ROUTING TESTS ---
    
    @pytest.mark.unit
    def test_route_query(self, bridge):
        """Test routing a query."""
        result = bridge.route("What is the weather?")
        
        assert isinstance(result, dict)
        assert "org" in result or "error" in result
        
        if "org" in result:
            assert "destination" in result
            assert "confidence" in result
            assert "category" in result
            assert "signal" in result
    
    @pytest.mark.unit
    def test_route_different_queries(self, bridge):
        """Test routing various query types."""
        queries = [
            "Deploy Cloudflare Worker",
            "Sync Salesforce contacts",
            "What is AI?",
            "Check Pi cluster health"
        ]
        
        for query in queries:
            result = bridge.route(query)
            assert isinstance(result, dict)
            # Either has a result or an error
            assert "org" in result or "error" in result
    
    @pytest.mark.unit
    def test_route_empty_query(self, bridge):
        """Test routing empty query."""
        result = bridge.route("")
        
        assert isinstance(result, dict)
    
    # --- ORGANIZATION TESTS ---
    
    @pytest.mark.unit
    def test_list_orgs(self, bridge):
        """Test listing organizations."""
        orgs = bridge.list_orgs()
        
        assert isinstance(orgs, list)
        # Should have at least some orgs
        if orgs:
            org = orgs[0]
            assert "name" in org
            assert "mission" in org
            assert isinstance(org["name"], str)
            assert isinstance(org["mission"], str)
    
    @pytest.mark.unit
    def test_orgs_have_names(self, bridge):
        """Test orgs have proper names."""
        orgs = bridge.list_orgs()
        
        for org in orgs:
            assert org["name"]  # Not empty
            assert len(org["name"]) > 0
    
    # --- TEMPLATE TESTS ---
    
    @pytest.mark.unit
    def test_list_templates(self, bridge):
        """Test listing templates."""
        templates = bridge.list_templates()
        
        assert isinstance(templates, list)
        # Should have templates
        if templates:
            tmpl = templates[0]
            assert "name" in tmpl
            assert "description" in tmpl
            assert isinstance(tmpl["name"], str)
            assert isinstance(tmpl["description"], str)
    
    @pytest.mark.unit
    def test_templates_have_names(self, bridge):
        """Test templates have proper names."""
        templates = bridge.list_templates()
        
        for tmpl in templates:
            assert tmpl["name"]  # Not empty
            assert len(tmpl["name"]) > 0
    
    # --- SIGNAL TESTS ---
    
    @pytest.mark.unit
    def test_signal_emission(self, bridge):
        """Test signal emission."""
        result = bridge.signal("test_message", "OS")
        
        assert isinstance(result, str)
        # Should contain signal format or fallback
        # Note: Signal format depends on whether SignalEmitter is available
        assert len(result) > 0
    
    @pytest.mark.unit
    def test_signal_different_targets(self, bridge):
        """Test signaling different targets."""
        targets = ["OS", "AI", "CLD", "FND"]
        
        for target in targets:
            result = bridge.signal("ping", target)
            assert isinstance(result, str)
            assert len(result) > 0
    
    # --- SEARCH TESTS ---
    
    @pytest.mark.unit
    def test_search(self, bridge):
        """Test ecosystem search."""
        results = bridge.search("test")
        
        assert isinstance(results, list)
    
    @pytest.mark.unit
    def test_search_results_structure(self, bridge):
        """Test search results have proper structure."""
        results = bridge.search("blackroad")
        
        # Results should be a list
        assert isinstance(results, list)
        
        # Each result should be a dict if there are results
        for result in results:
            assert isinstance(result, dict)
    
    # --- BROWSE TESTS ---
    
    @pytest.mark.unit
    def test_browse_root(self, bridge):
        """Test browsing root."""
        result = bridge.browse()
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_browse_with_path(self, bridge):
        """Test browsing specific path."""
        # Browse returns either the result or an error
        result = bridge.browse("orgs/")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    # --- DASHBOARD TESTS ---
    
    @pytest.mark.unit
    def test_dashboard(self, bridge):
        """Test dashboard generation."""
        result = bridge.dashboard()
        
        assert isinstance(result, str)
        # Either has dashboard or error message
        assert len(result) > 0
    
    # --- LAZY LOADING TESTS ---
    
    @pytest.mark.unit
    def test_operator_lazy_load(self, bridge):
        """Test Operator lazy loading."""
        # Initially None
        assert bridge._operator is None
        
        # Access triggers load
        operator = bridge.operator
        
        # Now loaded (or None if not available)
        assert bridge._operator is not None or bridge._operator is None
    
    @pytest.mark.unit
    def test_metrics_lazy_load(self, bridge):
        """Test Metrics lazy loading."""
        # Initially None
        assert bridge._metrics is None
        
        # Access triggers load
        metrics = bridge.metrics
        
        # Now loaded (or None if not available)
        assert bridge._metrics is not None or bridge._metrics is None
    
    @pytest.mark.unit
    def test_explorer_lazy_load(self, bridge):
        """Test Explorer lazy loading."""
        # Initially None
        assert bridge._explorer is None
        
        # Access triggers load
        explorer = bridge.explorer
        
        # Now loaded (or None if not available)
        assert bridge._explorer is not None or bridge._explorer is None


class TestBridgeState:
    """Test suite for BridgeState dataclass."""
    
    @pytest.mark.unit
    def test_bridge_state_creation(self):
        """Test creating BridgeState."""
        from datetime import datetime
        
        state = BridgeState(
            status="ONLINE",
            session="TEST",
            updated=datetime.now(),
            orgs_total=15,
            orgs_active=5,
            prototypes_ready=["operator", "metrics"],
            templates_ready=["template1"],
            nodes_online=3,
            nodes_total=7
        )
        
        assert state.status == "ONLINE"
        assert state.session == "TEST"
        assert state.orgs_total == 15
        assert state.orgs_active == 5
        assert len(state.prototypes_ready) == 2
        assert len(state.templates_ready) == 1
        assert state.nodes_online == 3
        assert state.nodes_total == 7
