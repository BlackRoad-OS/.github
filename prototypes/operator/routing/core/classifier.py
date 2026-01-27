"""
Classifier - Determines what type of request this is.

Uses pattern matching and keyword analysis to classify requests.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import re


@dataclass
class Classification:
    """Classification result."""
    category: str
    org_code: str
    confidence: float
    matched_patterns: List[str]

    def __repr__(self):
        return f"Classification({self.category}, org={self.org_code}, conf={self.confidence:.2f})"


# Default classification rules
DEFAULT_RULES = [
    {
        "category": "ai",
        "org_code": "AI",
        "patterns": [
            r"\b(what|who|why|how|when|where)\b",
            r"\b(weather|forecast|temperature)\b",
            r"\b(explain|describe|tell me|help)\b",
            r"\b(generate|create|write|draft)\b",
            r"\b(summarize|analyze|translate)\b",
            r"\b(claude|gpt|llm|ai|model)\b",
        ],
        "keywords": ["question", "ask", "query", "chat"]
    },
    {
        "category": "crm",
        "org_code": "FND",
        "patterns": [
            r"\b(customer|contact|lead|account|opportunity)\b",
            r"\b(salesforce|sf|crm)\b",
            r"\b(sales|pipeline|deal|revenue)\b",
            r"\b(subscription|billing|invoice)\b",
        ],
        "keywords": ["customer", "sales", "crm", "salesforce"]
    },
    {
        "category": "storage",
        "org_code": "ARC",
        "patterns": [
            r"\b(store|save|backup|archive)\b",
            r"\b(file|document|data|blob)\b",
            r"\b(retrieve|fetch|download)\b",
            r"\b(delete|remove|cleanup)\b",
        ],
        "keywords": ["storage", "file", "backup", "archive"]
    },
    {
        "category": "security",
        "org_code": "SEC",
        "patterns": [
            r"\b(auth|login|logout|password)\b",
            r"\b(permission|access|role)\b",
            r"\b(encrypt|decrypt|secret)\b",
            r"\b(audit|compliance|security)\b",
        ],
        "keywords": ["security", "auth", "permission"]
    },
    {
        "category": "infrastructure",
        "org_code": "CLD",
        "patterns": [
            r"\b(deploy|deployment|release)\b",
            r"\b(server|node|cluster|container)\b",
            r"\b(cloudflare|worker|edge)\b",
            r"\b(scale|scaling|load)\b",
        ],
        "keywords": ["deploy", "infrastructure", "cloud"]
    },
    {
        "category": "hardware",
        "org_code": "HW",
        "patterns": [
            r"\b(raspberry|pi|rpi)\b",
            r"\b(lucidia|octavia|aria|alice)\b",
            r"\b(hailo|inference|edge)\b",
            r"\b(esp32|lora|sensor|iot)\b",
        ],
        "keywords": ["hardware", "node", "device", "sensor"]
    },
    {
        "category": "metaverse",
        "org_code": "INT",
        "patterns": [
            r"\b(metaverse|vr|ar|xr|webxr)\b",
            r"\b(avatar|world|3d|three\.?js)\b",
            r"\b(game|interactive|immersive)\b",
        ],
        "keywords": ["metaverse", "vr", "game", "3d"]
    },
    {
        "category": "media",
        "org_code": "MED",
        "patterns": [
            r"\b(blog|post|article|content)\b",
            r"\b(publish|announce|social)\b",
            r"\b(video|image|media)\b",
        ],
        "keywords": ["content", "media", "publish"]
    },
    {
        "category": "education",
        "org_code": "EDU",
        "patterns": [
            r"\b(learn|tutorial|course|lesson)\b",
            r"\b(documentation|docs|guide)\b",
            r"\b(example|demo|walkthrough)\b",
        ],
        "keywords": ["learn", "tutorial", "documentation"]
    },
    {
        "category": "governance",
        "org_code": "GOV",
        "patterns": [
            r"\b(vote|proposal|brip)\b",
            r"\b(governance|policy|rule)\b",
            r"\b(constitution|amendment)\b",
        ],
        "keywords": ["governance", "vote", "policy"]
    },
    {
        "category": "design",
        "org_code": "STU",
        "patterns": [
            r"\b(design|ui|ux|interface)\b",
            r"\b(logo|icon|brand|style)\b",
            r"\b(component|theme|color)\b",
        ],
        "keywords": ["design", "ui", "brand"]
    },
    {
        "category": "commerce",
        "org_code": "VEN",
        "patterns": [
            r"\b(marketplace|shop|buy|sell)\b",
            r"\b(product|listing|order)\b",
            r"\b(partner|affiliate)\b",
        ],
        "keywords": ["commerce", "marketplace", "partner"]
    },
    {
        "category": "enterprise",
        "org_code": "BBX",
        "patterns": [
            r"\b(enterprise|corporate|sla)\b",
            r"\b(compliance|soc2|hipaa|gdpr)\b",
            r"\b(onboarding|implementation)\b",
        ],
        "keywords": ["enterprise", "compliance", "sla"]
    },
    {
        "category": "experiment",
        "org_code": "LAB",
        "patterns": [
            r"\b(experiment|test|prototype)\b",
            r"\b(research|explore|try)\b",
            r"\b(sandbox|lab|poc)\b",
        ],
        "keywords": ["experiment", "research", "prototype"]
    },
]


class Classifier:
    """
    Classify requests into categories.

    Examples:
        >>> classifier = Classifier()
        >>> result = classifier.classify("What is the weather?")
        >>> result.category
        'ai'
        >>> result.org_code
        'AI'
    """

    def __init__(self, rules: Optional[List[Dict]] = None):
        """Initialize with optional custom rules."""
        self.rules = rules or DEFAULT_RULES
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for performance."""
        for rule in self.rules:
            rule["_compiled"] = [
                re.compile(p, re.IGNORECASE)
                for p in rule.get("patterns", [])
            ]

    def classify(self, query: str) -> Classification:
        """
        Classify a query.

        Args:
            query: The text to classify

        Returns:
            Classification with category, org, and confidence
        """
        query_lower = query.lower()
        scores: Dict[str, Dict] = {}

        for rule in self.rules:
            category = rule["category"]
            org_code = rule["org_code"]
            score = 0.0
            matched = []

            # Check compiled patterns
            for i, pattern in enumerate(rule.get("_compiled", [])):
                if pattern.search(query):
                    score += 1.0
                    matched.append(rule["patterns"][i])

            # Check keywords
            for keyword in rule.get("keywords", []):
                if keyword in query_lower:
                    score += 0.5
                    matched.append(f"keyword:{keyword}")

            if score > 0:
                scores[category] = {
                    "org_code": org_code,
                    "score": score,
                    "matched": matched
                }

        # Find best match
        if not scores:
            # Default to AI for unknown queries
            return Classification(
                category="ai",
                org_code="AI",
                confidence=0.5,
                matched_patterns=["default:unknown_query"]
            )

        best_category = max(scores.keys(), key=lambda k: scores[k]["score"])
        best = scores[best_category]

        # Normalize confidence (max 1.0)
        max_possible = max(len(r.get("patterns", [])) + len(r.get("keywords", [])) * 0.5
                          for r in self.rules)
        confidence = min(best["score"] / max_possible * 2, 1.0)

        return Classification(
            category=best_category,
            org_code=best["org_code"],
            confidence=confidence,
            matched_patterns=best["matched"]
        )

    def classify_batch(self, queries: List[str]) -> List[Classification]:
        """Classify multiple queries."""
        return [self.classify(q) for q in queries]
