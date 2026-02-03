"""
Tests for the Operator Parser module.

Tests input parsing and normalization for various input types.
"""

import pytest
import json
from prototypes.operator.routing.core.parser import (
    Parser,
    Request,
    InputType
)


class TestParser:
    """Test suite for the Parser class."""
    
    @pytest.fixture
    def parser(self):
        """Create a Parser instance."""
        return Parser()
    
    # --- TEXT INPUT TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_simple_text(self, parser):
        """Test parsing simple text input."""
        result = parser.parse("What is the weather?")
        
        assert isinstance(result, Request)
        assert result.query == "What is the weather?"
        assert result.input_type == InputType.TEXT
        assert result.raw == "What is the weather?"
        assert result.context == {}
        assert result.metadata == {}
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_text_with_whitespace(self, parser):
        """Test parsing text with leading/trailing whitespace."""
        result = parser.parse("  Hello world  ")
        
        assert result.query == "Hello world"
        assert result.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_empty_string(self, parser):
        """Test parsing empty string."""
        result = parser.parse("")
        
        assert result.query == ""
        assert result.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_text_with_context(self, parser):
        """Test parsing text with additional context."""
        context = {"user": "alexa", "source": "cli"}
        result = parser.parse("Test query", context=context)
        
        assert result.query == "Test query"
        assert result.context == context
    
    # --- HTTP INPUT TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_http_request(self, parser):
        """Test parsing HTTP request."""
        http_data = {
            "method": "POST",
            "path": "/api/query",
            "body": "Deploy worker",
            "headers": {"Content-Type": "application/json"}
        }
        
        result = parser.parse(http_data, input_type=InputType.HTTP)
        
        assert result.query == "Deploy worker"
        assert result.input_type == InputType.HTTP
        assert result.metadata["method"] == "POST"
        assert result.metadata["path"] == "/api/query"
        assert "headers" in result.metadata
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_http_auto_detect(self, parser):
        """Test auto-detection of HTTP input."""
        http_data = {
            "method": "GET",
            "query": "list users"
        }
        
        result = parser.parse(http_data)
        
        assert result.input_type == InputType.HTTP
        assert result.query == "list users"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_http_with_query_param(self, parser):
        """Test parsing HTTP with query parameter."""
        http_data = {
            "method": "GET",
            "query": "search customers"
        }
        
        result = parser.parse(http_data, input_type=InputType.HTTP)
        
        assert result.query == "search customers"
    
    # --- WEBHOOK INPUT TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_webhook(self, parser):
        """Test parsing webhook payload."""
        webhook_data = {
            "event": "customer.created",
            "payload": {"id": "123", "name": "Test Customer"},
            "source": "stripe"
        }
        
        result = parser.parse(webhook_data, input_type=InputType.WEBHOOK)
        
        assert result.query == "webhook:customer.created"
        assert result.input_type == InputType.WEBHOOK
        assert result.metadata["event"] == "customer.created"
        assert result.metadata["source"] == "stripe"
        assert "payload" in result.metadata
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_webhook_auto_detect(self, parser):
        """Test auto-detection of webhook input."""
        webhook_data = {
            "event": "push",
            "repository": "test-repo"
        }
        
        result = parser.parse(webhook_data)
        
        assert result.input_type == InputType.WEBHOOK
        assert "webhook:" in result.query
    
    # --- SIGNAL INPUT TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_signal(self, parser):
        """Test parsing signal string."""
        signal = "✔️ OS → AI : query_routed"
        
        result = parser.parse(signal, input_type=InputType.SIGNAL)
        
        assert result.query == "query_routed"
        assert result.input_type == InputType.SIGNAL
        assert result.metadata["signal"] == signal
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_signal_auto_detect(self, parser):
        """Test auto-detection of signal input."""
        signal = "📡 AI → OS : inference_complete"
        
        result = parser.parse(signal)
        
        assert result.input_type == InputType.SIGNAL
        assert "inference_complete" in result.query
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_signal_without_colon(self, parser):
        """Test parsing signal without colon separator."""
        signal = "✔️ OS → AI signal_sent"
        
        result = parser.parse(signal, input_type=InputType.SIGNAL)
        
        # Should fall back to the full signal as query
        assert result.input_type == InputType.SIGNAL
    
    # --- CLI INPUT TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_cli_string(self, parser):
        """Test parsing CLI string input."""
        result = parser.parse("deploy worker", input_type=InputType.CLI)
        
        assert result.query == "deploy worker"
        assert result.input_type == InputType.CLI
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_cli_list(self, parser):
        """Test parsing CLI list input (argv style)."""
        cli_args = ["deploy", "worker", "--env=prod"]
        
        result = parser.parse(cli_args, input_type=InputType.CLI)
        
        assert result.query == "deploy worker --env=prod"
        assert result.input_type == InputType.CLI
    
    # --- TYPE DETECTION TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_detect_text_type(self, parser):
        """Test detection of text input."""
        result = parser.parse("regular text query")
        assert result.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_detect_signal_type(self, parser):
        """Test detection of signal input."""
        result = parser.parse("✔️ Test signal")
        assert result.input_type == InputType.SIGNAL
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_detect_http_type(self, parser):
        """Test detection of HTTP input."""
        result = parser.parse({"method": "POST", "body": "test"})
        assert result.input_type == InputType.HTTP
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_detect_webhook_type(self, parser):
        """Test detection of webhook input."""
        result = parser.parse({"event": "test.event", "payload": {}})
        assert result.input_type == InputType.WEBHOOK
    
    # --- EDGE CASES ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_unicode_text(self, parser):
        """Test parsing text with unicode characters."""
        result = parser.parse("Hello 世界! 🌍")
        
        assert result.query == "Hello 世界! 🌍"
        assert result.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_special_characters(self, parser):
        """Test parsing text with special characters."""
        query = "Query with <tags> & special @chars #test"
        result = parser.parse(query)
        
        assert result.query == query
        assert result.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_multiline_text(self, parser):
        """Test parsing multiline text."""
        query = """First line
        Second line
        Third line"""
        
        result = parser.parse(query)
        
        assert "First line" in result.query
        assert "Third line" in result.query
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_none_input(self, parser):
        """Test parsing None input."""
        result = parser.parse(None)
        
        assert result.query == "None"
        assert result.input_type == InputType.TEXT
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_parse_integer_input(self, parser):
        """Test parsing integer input."""
        result = parser.parse(12345)
        
        assert result.query == "12345"
        assert result.input_type == InputType.TEXT
