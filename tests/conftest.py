"""
Shared pytest fixtures and configuration for BlackRoad tests.

This module provides common fixtures used across all test modules.
"""

import pytest
from datetime import datetime
from typing import Dict, Any


@pytest.fixture
def sample_queries():
    """Common test queries for routing."""
    return {
        "ai": [
            "What is the weather?",
            "Tell me about Python",
            "Generate a hello world program",
            "Explain quantum computing",
        ],
        "crm": [
            "Sync Salesforce contacts",
            "Update customer pipeline",
            "Create new lead",
            "Show billing invoices",
        ],
        "cloud": [
            "Deploy Cloudflare Worker",
            "Update edge function",
            "Configure CDN",
            "Scale kubernetes cluster",
        ],
        "hardware": [
            "Check Pi cluster health",
            "Update node configuration",
            "Deploy to lucidia",
            "Monitor IoT sensors",
        ],
        "security": [
            "Rotate API keys",
            "Update firewall rules",
            "Run security audit",
            "Configure vault secrets",
        ],
    }


@pytest.fixture
def sample_org_codes():
    """Valid organization codes."""
    return [
        "OS", "AI", "CLD", "HW", "LAB", "SEC", "FND",
        "MED", "INT", "EDU", "GOV", "ARC", "STU", "VEN", "BBX"
    ]


@pytest.fixture
def mock_timestamp():
    """Fixed timestamp for testing."""
    return "2026-01-27T19:00:00Z"


@pytest.fixture
def mock_datetime(monkeypatch, mock_timestamp):
    """Mock datetime to return fixed timestamp."""
    class MockDatetime:
        @staticmethod
        def now():
            return datetime.fromisoformat(mock_timestamp.replace('Z', '+00:00'))
        
        @staticmethod
        def utcnow():
            return datetime.fromisoformat(mock_timestamp.replace('Z', '+00:00'))
    
    monkeypatch.setattr('datetime.datetime', MockDatetime)
    return MockDatetime


@pytest.fixture
def sample_classification():
    """Sample classification result."""
    return {
        "category": "ai",
        "org_code": "AI",
        "confidence": 0.85,
        "matched_patterns": ["what", "explain"],
    }


@pytest.fixture
def sample_route_result():
    """Sample route result."""
    return {
        "destination": "BlackRoad-AI",
        "org": "BlackRoad-AI",
        "org_code": "AI",
        "confidence": 0.85,
        "timestamp": "2026-01-27T19:00:00Z",
    }


@pytest.fixture
def capture_signals(monkeypatch):
    """Capture emitted signals for testing."""
    signals = []
    
    def mock_emit(signal: str, **kwargs):
        signals.append({"signal": signal, **kwargs})
    
    # This will be patched in actual tests
    return signals


# Markers for test organization
def pytest_configure(config):
    """Configure custom markers."""
    markers = [
        "unit: Unit tests - fast, no external dependencies",
        "integration: Integration tests - may use external services",
        "slow: Slow tests - may take several seconds",
        "operator: Tests for Operator prototype",
        "metrics: Tests for Metrics prototype",
        "dispatcher: Tests for Dispatcher prototype",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)
