"""
Prompt Registry
Central storage and management for prompt templates.
"""

import os
import json
import time
from typing import Optional

from template import PromptTemplate


class PromptRegistry:
    """
    Manages a collection of prompt templates with CRUD operations,
    search, and rendering.
    """

    def __init__(self):
        self._templates: dict[str, PromptTemplate] = {}
        self._render_log: list[dict] = []

    def register(self, template: PromptTemplate) -> None:
        """Register a template in the registry."""
        self._templates[template.id] = template

    def get(self, template_id: str) -> Optional[PromptTemplate]:
        """Get a template by ID."""
        return self._templates.get(template_id)

    def remove(self, template_id: str) -> bool:
        """Remove a template."""
        if template_id in self._templates:
            del self._templates[template_id]
            return True
        return False

    def list_templates(
        self,
        category: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> list[dict]:
        """List all templates, optionally filtered."""
        results = []
        for t in self._templates.values():
            if category and t.category != category:
                continue
            if tags and not all(tag in t.tags for tag in tags):
                continue
            results.append(t.to_dict())
        return sorted(results, key=lambda x: x["usage_count"], reverse=True)

    def render(
        self,
        template_id: str,
        variables: Optional[dict] = None,
        provider: Optional[str] = None,
    ) -> dict:
        """
        Render a template by ID.

        Returns: {"system": str, "user": str}
        Raises: KeyError if template not found, ValueError if variables missing
        """
        template = self._templates.get(template_id)
        if not template:
            raise KeyError(f"Template not found: {template_id}")

        # Validate variables
        missing = template.validate(variables or {})
        if missing:
            raise ValueError(f"Missing variables for '{template_id}': {missing}")

        result = template.render(variables, provider)

        self._render_log.append({
            "timestamp": time.time(),
            "template_id": template_id,
            "provider": provider,
            "variables_keys": list((variables or {}).keys()),
        })

        return result

    def search(self, query: str) -> list[dict]:
        """Search templates by name, description, or tags."""
        query_lower = query.lower()
        results = []
        for t in self._templates.values():
            if (
                query_lower in t.name.lower()
                or query_lower in t.description.lower()
                or any(query_lower in tag.lower() for tag in t.tags)
            ):
                results.append(t.to_dict())
        return results

    def load_defaults(self) -> int:
        """Load the default template library."""
        defaults = _get_default_templates()
        for t in defaults:
            self.register(t)
        return len(defaults)

    def stats(self) -> dict:
        """Registry statistics."""
        templates = list(self._templates.values())
        total_usage = sum(t.usage_count for t in templates)
        categories = {}
        for t in templates:
            categories[t.category] = categories.get(t.category, 0) + 1

        return {
            "total_templates": len(templates),
            "total_renders": total_usage,
            "categories": categories,
            "most_used": sorted(
                [t.to_dict() for t in templates],
                key=lambda x: x["usage_count"],
                reverse=True,
            )[:5],
        }


def _get_default_templates() -> list[PromptTemplate]:
    """Built-in template library for BlackRoad."""
    return [
        PromptTemplate(
            id="code_review",
            name="Code Review",
            description="Review code for bugs, security issues, and improvements",
            system_prompt=(
                "You are an expert code reviewer. Analyze the provided code for "
                "bugs, security vulnerabilities, performance issues, and style. "
                "Be specific and actionable."
            ),
            user_prompt=(
                "Review this {{language}} code:\n\n"
                "```{{language}}\n{{code}}\n```\n\n"
                "Focus areas: {{focus}}"
            ),
            category="code",
            tags=["code", "review", "security"],
            variables=["language", "code"],
            defaults={"focus": "bugs, security, performance", "language": "python"},
        ),
        PromptTemplate(
            id="summarize",
            name="Summarize Text",
            description="Summarize text to a target length and style",
            system_prompt=(
                "You are a precise summarizer. Summarize the given text to "
                "{{length}} length. Style: {{style}}."
            ),
            user_prompt="Summarize the following:\n\n{{text}}",
            category="text",
            tags=["text", "summarize", "content"],
            variables=["text"],
            defaults={"length": "medium", "style": "professional"},
        ),
        PromptTemplate(
            id="route_classify",
            name="Route Classifier",
            description="Classify a user request to determine the best route",
            system_prompt=(
                "You are a request classifier for BlackRoad's routing engine. "
                "Given a user request, classify it into one of these categories: "
                "{{categories}}. Respond with only the category name."
            ),
            user_prompt="Classify this request: {{request}}",
            category="routing",
            tags=["routing", "classify", "operator"],
            variables=["request"],
            defaults={
                "categories": "code, data, search, creative, analysis, system"
            },
        ),
        PromptTemplate(
            id="debug_assist",
            name="Debug Assistant",
            description="Help debug an error or issue",
            system_prompt=(
                "You are a debugging expert. Analyze the error, identify the root "
                "cause, and provide a fix. Be concise and specific."
            ),
            user_prompt=(
                "Language: {{language}}\n"
                "Error: {{error}}\n\n"
                "Code context:\n```{{language}}\n{{code}}\n```\n\n"
                "What's wrong and how to fix it?"
            ),
            category="code",
            tags=["code", "debug", "error"],
            variables=["error", "code"],
            defaults={"language": "python"},
        ),
        PromptTemplate(
            id="api_docs",
            name="API Documentation Generator",
            description="Generate API documentation from code",
            system_prompt=(
                "You are a technical writer. Generate clear, complete API documentation "
                "in {{format}} format for the given code."
            ),
            user_prompt=(
                "Generate API docs for:\n\n"
                "```{{language}}\n{{code}}\n```"
            ),
            category="docs",
            tags=["docs", "api", "generate"],
            variables=["code"],
            defaults={"language": "python", "format": "markdown"},
        ),
        PromptTemplate(
            id="security_scan",
            name="Security Scanner",
            description="Scan code for security vulnerabilities",
            system_prompt=(
                "You are a security analyst. Scan the code for OWASP Top 10 "
                "vulnerabilities, injection flaws, auth issues, and data exposure. "
                "Rate severity as CRITICAL, HIGH, MEDIUM, or LOW."
            ),
            user_prompt=(
                "Security scan this {{language}} code:\n\n"
                "```{{language}}\n{{code}}\n```"
            ),
            category="security",
            tags=["security", "scan", "owasp"],
            variables=["code"],
            defaults={"language": "python"},
        ),
        PromptTemplate(
            id="commit_message",
            name="Commit Message Generator",
            description="Generate a commit message from a diff",
            system_prompt=(
                "You write concise, descriptive git commit messages. "
                "Use conventional commit format: type(scope): description. "
                "Keep under 72 chars for the subject line."
            ),
            user_prompt="Generate a commit message for this diff:\n\n{{diff}}",
            category="git",
            tags=["git", "commit", "automation"],
            variables=["diff"],
        ),
        PromptTemplate(
            id="data_analysis",
            name="Data Analysis",
            description="Analyze data and provide insights",
            system_prompt=(
                "You are a data analyst. Analyze the provided data, identify "
                "patterns, anomalies, and actionable insights. Format: {{format}}."
            ),
            user_prompt=(
                "Analyze this data:\n\n{{data}}\n\n"
                "Questions: {{questions}}"
            ),
            category="analysis",
            tags=["data", "analysis", "insights"],
            variables=["data"],
            defaults={"questions": "Key patterns and anomalies?", "format": "bullet points"},
        ),
    ]


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    """Demo the prompt registry."""
    print("BlackRoad Prompt Template Registry")
    print("=" * 40)

    reg = PromptRegistry()
    count = reg.load_defaults()
    print(f"Loaded {count} default templates\n")

    # List all
    print("Available Templates:")
    for t in reg.list_templates():
        print(f"  [{t['category']:>10}] {t['id']:<20} - {t['description'][:50]}")

    # Demo render
    print("\n--- Demo Render ---")
    result = reg.render("code_review", {
        "code": "def transfer(amount, to):\n  db.execute(f'UPDATE accounts SET balance={amount} WHERE user={to}')",
        "language": "python",
        "focus": "SQL injection",
    })
    print(f"System: {result['system'][:80]}...")
    print(f"User: {result['user'][:120]}...")

    print(f"\n{json.dumps(reg.stats(), indent=2)}")


if __name__ == "__main__":
    main()
