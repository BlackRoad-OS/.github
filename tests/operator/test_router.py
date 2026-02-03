"""
Tests for the Operator Router module.

Tests the main routing logic that ties parser and classifier together.
"""

import pytest
from prototypes.operator.routing.core.router import (
    Operator,
    RouteResult,
    ORGS,
)
from prototypes.operator.routing.core.parser import InputType


class TestOperator:
    """Test suite for the Operator class."""
    
    @pytest.fixture
    def operator(self):
        """Create an Operator instance."""
        return Operator()
    
    # --- BASIC ROUTING TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_simple_query(self, operator):
        """Test routing a simple query."""
        result = operator.route("What is the weather?")
        
        assert isinstance(result, RouteResult)
        assert result.org_code in ORGS
        assert result.org == ORGS[result.org_code]["name"]
        assert result.confidence > 0
        assert result.timestamp is not None
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_ai_query(self, operator):
        """Test routing an AI query."""
        result = operator.route("Explain quantum computing")
        
        assert result.org_code == "AI"
        assert result.org == "BlackRoad-AI"
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_crm_query(self, operator):
        """Test routing a CRM query."""
        result = operator.route("Sync Salesforce contacts")
        
        assert result.org_code == "FND"
        assert result.org == "BlackRoad-Foundation"
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_cloud_query(self, operator):
        """Test routing a cloud deployment query."""
        result = operator.route("Deploy Cloudflare Worker")
        
        assert result.org_code == "CLD"
        assert result.org == "BlackRoad-Cloud"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_hardware_query(self, operator):
        """Test routing a hardware query."""
        result = operator.route("Monitor Raspberry Pi cluster status")
        
        # Could route to HW or CLD depending on patterns
        assert result.org_code in ["HW", "CLD"]
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_security_query(self, operator):
        """Test routing a security query."""
        result = operator.route("Configure vault security secrets")
        
        # Security queries could route to SEC, AI, or CLD
        assert result.org_code in ["SEC", "AI", "CLD"]
    
    # --- RESULT STRUCTURE TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_result_fields(self, operator):
        """Test RouteResult has all required fields."""
        result = operator.route("Test query")
        
        assert hasattr(result, 'destination')
        assert hasattr(result, 'org')
        assert hasattr(result, 'org_code')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'classification')
        assert hasattr(result, 'request')
        assert hasattr(result, 'timestamp')
        assert hasattr(result, 'signal')
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_result_to_dict(self, operator):
        """Test RouteResult conversion to dict."""
        result = operator.route("Test query")
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'org_code' in result_dict
        assert 'confidence' in result_dict
        assert 'timestamp' in result_dict
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_result_repr(self, operator):
        """Test RouteResult repr method."""
        result = operator.route("Test query")
        
        repr_str = repr(result)
        
        assert "RouteResult" in repr_str
        assert result.org in repr_str
        assert result.org_code in repr_str
    
    # --- INPUT TYPE TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_text_input(self, operator):
        """Test routing text input."""
        result = operator.route("Deploy worker")
        
        assert result.request.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_http_input(self, operator):
        """Test routing HTTP-style input."""
        http_data = {
            "method": "POST",
            "body": "Deploy Cloudflare Worker"
        }
        
        result = operator.route(http_data)
        
        assert result.request.input_type == InputType.HTTP
        assert result.org_code == "CLD"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_webhook_input(self, operator):
        """Test routing webhook input."""
        webhook_data = {
            "event": "deployment.created",
            "payload": {"action": "deploy"}
        }
        
        result = operator.route(webhook_data)
        
        assert result.request.input_type == InputType.WEBHOOK
    
    # --- CONFIDENCE TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_high_confidence(self, operator):
        """Test routing with high confidence."""
        # Very specific query
        result = operator.route("Deploy Cloudflare Worker to edge network")
        
        assert result.confidence > 0.7
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_confidence_range(self, operator):
        """Test confidence is always in valid range."""
        queries = [
            "What is AI?",
            "Deploy worker",
            "Update something",
            "Check health",
            "",
        ]
        
        for query in queries:
            result = operator.route(query)
            assert 0 <= result.confidence <= 1
    
    # --- SIGNAL TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_emits_signal(self, operator):
        """Test that routing emits a signal."""
        result = operator.route("Test query")
        
        assert result.signal is not None
        assert isinstance(result.signal, str)
        assert "→" in result.signal
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_signal_format(self, operator):
        """Test signal format."""
        result = operator.route("Deploy worker")
        
        # Signal format: "OS → ORG : routed"
        assert "→" in result.signal
        assert result.org_code in result.signal
    
    # --- ORGANIZATION REGISTRY TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_all_orgs_exist(self):
        """Test that all expected orgs are registered."""
        expected_orgs = [
            "OS", "AI", "CLD", "HW", "LAB", "SEC", "FND",
            "MED", "INT", "EDU", "GOV", "ARC", "STU", "VEN", "BBX"
        ]
        
        for org_code in expected_orgs:
            assert org_code in ORGS
            assert "name" in ORGS[org_code]
            assert "description" in ORGS[org_code]
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_org_names_valid(self):
        """Test that all org names are properly formatted."""
        for org_code, org_data in ORGS.items():
            assert org_data["name"].startswith("Black")
            assert len(org_data["description"]) > 0
    
    # --- EDGE CASES ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_empty_query(self, operator):
        """Test routing empty query."""
        result = operator.route("")
        
        assert isinstance(result, RouteResult)
        assert result.org_code in ORGS
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_none_input(self, operator):
        """Test routing None input."""
        result = operator.route(None)
        
        assert isinstance(result, RouteResult)
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_very_long_query(self, operator):
        """Test routing very long query."""
        long_query = "Deploy Cloudflare Worker " * 100
        
        result = operator.route(long_query)
        
        assert result.org_code == "CLD"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_unicode_query(self, operator):
        """Test routing with unicode characters."""
        result = operator.route("部署 Cloudflare Worker 🚀")
        
        assert isinstance(result, RouteResult)
        assert result.org_code in ORGS
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_special_characters(self, operator):
        """Test routing with special characters."""
        result = operator.route("Deploy @worker #production $env=prod")
        
        assert isinstance(result, RouteResult)
    
    # --- MULTIPLE QUERIES TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_multiple_queries_consistency(self, operator):
        """Test that same query returns consistent results."""
        query = "Deploy Cloudflare Worker"
        
        result1 = operator.route(query)
        result2 = operator.route(query)
        
        assert result1.org_code == result2.org_code
        assert result1.confidence == result2.confidence
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_different_queries(self, operator, sample_queries):
        """Test routing different types of queries."""
        for category, queries in sample_queries.items():
            for query in queries:
                result = operator.route(query)
                assert isinstance(result, RouteResult)
                assert result.org_code in ORGS


class TestRouteResult:
    """Test suite for RouteResult dataclass."""
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_route_result_creation(self, sample_route_result, sample_classification):
        """Test creating a RouteResult."""
        from prototypes.operator.routing.core.parser import Request, InputType
        from prototypes.operator.routing.core.classifier import Classification
        
        request = Request(
            raw="test",
            input_type=InputType.TEXT,
            query="test query",
            context={},
            metadata={}
        )
        
        classification = Classification(**sample_classification)
        
        result = RouteResult(
            destination="BlackRoad-AI",
            org="BlackRoad-AI",
            org_code="AI",
            confidence=0.85,
            classification=classification,
            request=request,
            timestamp="2026-01-27T19:00:00Z",
            signal="OS → AI : routed"
        )
        
        assert result.org_code == "AI"
        assert result.confidence == 0.85
