"""
Tests for the Operator Classifier module.

Tests pattern matching and request classification.
"""

import pytest
from prototypes.operator.routing.core.classifier import (
    Classifier,
    Classification,
)


class TestClassifier:
    """Test suite for the Classifier class."""
    
    @pytest.fixture
    def classifier(self):
        """Create a Classifier instance."""
        return Classifier()
    
    # --- AI CLASSIFICATION TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_ai_question(self, classifier):
        """Test classification of AI questions."""
        query = "What is the weather today?"
        
        result = classifier.classify(query)
        
        assert isinstance(result, Classification)
        assert result.org_code == "AI"
        assert result.category == "ai"
        assert result.confidence > 0
        assert len(result.matched_patterns) > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_ai_generation(self, classifier):
        """Test classification of AI generation requests."""
        query = "Generate a Python function"
        
        result = classifier.classify(query)
        
        assert result.org_code == "AI"
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_ai_explanation(self, classifier):
        """Test classification of explanation requests."""
        query = "Explain quantum computing"
        
        result = classifier.classify(query)
        
        assert result.org_code == "AI"
        assert "explain" in [p.lower() for p in result.matched_patterns] or result.category == "ai"
    
    # --- CRM CLASSIFICATION TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_crm_salesforce(self, classifier):
        """Test classification of Salesforce queries."""
        query = "Sync Salesforce contacts"
        
        result = classifier.classify(query)
        
        assert result.org_code == "FND"
        assert result.category == "crm"
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_crm_customer(self, classifier):
        """Test classification of customer queries."""
        query = "Update customer record"
        
        result = classifier.classify(query)
        
        assert result.org_code == "FND"
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_crm_billing(self, classifier):
        """Test classification of billing queries."""
        query = "Process subscription invoice"
        
        result = classifier.classify(query)
        
        assert result.org_code == "FND"
        assert result.category == "crm"
    
    # --- CLOUD CLASSIFICATION TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_cloud_deployment(self, classifier):
        """Test classification of cloud deployment."""
        query = "Deploy Cloudflare Worker"
        
        result = classifier.classify(query)
        
        assert result.org_code == "CLD"
        assert result.confidence > 0.5
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_cloud_kubernetes(self, classifier):
        """Test classification of Kubernetes queries."""
        query = "Scale kubernetes pods"
        
        result = classifier.classify(query)
        
        assert result.org_code == "CLD"
    
    # --- HARDWARE CLASSIFICATION TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_hardware_pi(self, classifier):
        """Test classification of Pi cluster queries."""
        query = "Monitor Raspberry Pi cluster health status"
        
        result = classifier.classify(query)
        
        # Could be HW or CLD depending on patterns
        assert result.org_code in ["HW", "CLD"]
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_hardware_iot(self, classifier):
        """Test classification of IoT queries."""
        query = "Monitor IoT sensors"
        
        result = classifier.classify(query)
        
        assert result.org_code == "HW"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_hardware_node(self, classifier):
        """Test classification of node queries."""
        query = "Update hardware on lucidia node"
        
        result = classifier.classify(query)
        
        # Could be HW or CLD depending on context
        assert result.org_code in ["HW", "CLD"]
    
    # --- SECURITY CLASSIFICATION TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_security_keys(self, classifier):
        """Test classification of security key queries."""
        query = "Rotate security API keys in vault"
        
        result = classifier.classify(query)
        
        # Security related query
        assert result.org_code in ["SEC", "AI"]
        assert result.confidence > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_security_vault(self, classifier):
        """Test classification of vault queries."""
        query = "Configure vault security secrets"
        
        result = classifier.classify(query)
        
        # Security or cloud related
        assert result.org_code in ["SEC", "AI", "CLD"]
    
    # --- CONFIDENCE SCORING TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_high_confidence_classification(self, classifier):
        """Test high confidence classification."""
        # Query with multiple matching patterns
        query = "Deploy Cloudflare Worker to edge CDN"
        
        result = classifier.classify(query)
        
        assert result.confidence > 0.7
        assert len(result.matched_patterns) >= 2
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_low_confidence_classification(self, classifier):
        """Test low confidence classification."""
        # Ambiguous query
        query = "Update the thing"
        
        result = classifier.classify(query)
        
        # Should still return a classification, but with lower confidence
        assert isinstance(result, Classification)
        assert 0 <= result.confidence <= 1
    
    # --- EDGE CASES ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_empty_string(self, classifier):
        """Test classification of empty string."""
        result = classifier.classify("")
        
        assert isinstance(result, Classification)
        assert result.confidence >= 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_very_short_query(self, classifier):
        """Test classification of very short query."""
        result = classifier.classify("hi")
        
        assert isinstance(result, Classification)
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_very_long_query(self, classifier):
        """Test classification of very long query."""
        query = "Deploy " * 100 + "Cloudflare Worker"
        
        result = classifier.classify(query)
        
        assert result.org_code == "CLD"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_case_insensitive(self, classifier):
        """Test case-insensitive classification."""
        queries = [
            "Deploy CLOUDFLARE worker",
            "deploy cloudflare WORKER",
            "DEPLOY CLOUDFLARE WORKER",
        ]
        
        for query in queries:
            result = classifier.classify(query)
            assert result.org_code == "CLD"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_with_punctuation(self, classifier):
        """Test classification with punctuation."""
        query = "What is the weather today?"
        
        result = classifier.classify(query)
        
        assert result.org_code == "AI"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classify_with_special_chars(self, classifier):
        """Test classification with special characters."""
        query = "Sync Salesforce contacts @ 5pm!"
        
        result = classifier.classify(query)
        
        assert result.org_code == "FND"
    
    # --- PATTERN MATCHING TESTS ---
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_multiple_pattern_matches(self, classifier):
        """Test query matching multiple patterns."""
        query = "Deploy worker and sync Salesforce"
        
        result = classifier.classify(query)
        
        # Should classify based on strongest match
        assert isinstance(result, Classification)
        assert len(result.matched_patterns) > 0
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_pattern_boundaries(self, classifier):
        """Test word boundary matching."""
        # "cloudflare" should match, but "loud" in "cloudflare" shouldn't match "loud"
        query = "Deploy to Cloudflare"
        
        result = classifier.classify(query)
        
        assert result.org_code == "CLD"
    
    @pytest.mark.unit
    @pytest.mark.operator
    def test_classification_result_repr(self, classifier):
        """Test Classification repr method."""
        result = classifier.classify("What is AI?")
        
        repr_str = repr(result)
        
        assert "Classification" in repr_str
        assert result.category in repr_str
        assert result.org_code in repr_str
