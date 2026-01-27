"""GitHub webhook handler."""

import hmac
import hashlib
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class GitHubHandler(WebhookHandler):
    """
    Handle GitHub webhooks.

    Events:
    - push: Code pushed to repo
    - pull_request: PR opened/closed/merged
    - issues: Issue created/updated
    - workflow_run: Action completed
    - release: New release published
    """

    name = "github"
    target_org = "OS"

    # Event to signal type mapping
    EVENT_MAP = {
        "push": SignalType.PUSH,
        "pull_request": SignalType.PULL_REQUEST,
        "issues": SignalType.ISSUE,
        "issue_comment": SignalType.COMMENT,
        "workflow_run": SignalType.WORKFLOW_RUN,
        "release": SignalType.RELEASE,
        "ping": SignalType.PING,
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for GitHub webhook headers."""
        return self.get_header(headers, "X-GitHub-Event") is not None

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify GitHub webhook signature."""
        if not secret:
            return True

        signature = self.get_header(headers, "X-Hub-Signature-256")
        if not signature:
            return False

        expected = "sha256=" + hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse GitHub webhook into Signal."""
        event = self.get_header(headers, "X-GitHub-Event") or "unknown"
        signal_type = self.EVENT_MAP.get(event, SignalType.CUSTOM)

        # Extract relevant data based on event type
        data = self._extract_data(event, body)

        # Determine target org based on repo
        target = self._determine_target(body)

        return Signal(
            type=signal_type,
            source=self.name,
            target=target,
            data=data,
            raw=body,
        )

    def _extract_data(self, event: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant data from webhook body."""
        repo = body.get("repository", {})
        sender = body.get("sender", {})

        data = {
            "event": event,
            "repo": repo.get("full_name", ""),
            "sender": sender.get("login", ""),
        }

        if event == "push":
            data.update({
                "branch": body.get("ref", "").replace("refs/heads/", ""),
                "commits": len(body.get("commits", [])),
                "message": body.get("head_commit", {}).get("message", "")[:50],
            })

        elif event == "pull_request":
            pr = body.get("pull_request", {})
            data.update({
                "action": body.get("action", ""),
                "number": pr.get("number"),
                "title": pr.get("title", "")[:50],
                "merged": pr.get("merged", False),
            })

        elif event == "issues":
            issue = body.get("issue", {})
            data.update({
                "action": body.get("action", ""),
                "number": issue.get("number"),
                "title": issue.get("title", "")[:50],
            })

        elif event == "workflow_run":
            workflow = body.get("workflow_run", {})
            data.update({
                "action": body.get("action", ""),
                "workflow": workflow.get("name", ""),
                "status": workflow.get("status", ""),
                "conclusion": workflow.get("conclusion", ""),
            })

        elif event == "release":
            release = body.get("release", {})
            data.update({
                "action": body.get("action", ""),
                "tag": release.get("tag_name", ""),
                "name": release.get("name", ""),
            })

        return data

    def _determine_target(self, body: Dict[str, Any]) -> str:
        """Determine target org based on repo name."""
        repo = body.get("repository", {}).get("full_name", "")

        # Map repos to orgs
        org_map = {
            "BlackRoad-OS": "OS",
            "BlackRoad-AI": "AI",
            "BlackRoad-Cloud": "CLD",
            "BlackRoad-Hardware": "HW",
            "BlackRoad-Labs": "LAB",
            "BlackRoad-Security": "SEC",
            "BlackRoad-Foundation": "FND",
            "BlackRoad-Media": "MED",
            "BlackRoad-Interactive": "INT",
            "BlackRoad-Education": "EDU",
            "BlackRoad-Gov": "GOV",
            "BlackRoad-Archive": "ARC",
            "BlackRoad-Studio": "STU",
            "BlackRoad-Ventures": "VEN",
            "Blackbox-Enterprises": "BBX",
        }

        for org_name, code in org_map.items():
            if repo.startswith(org_name):
                return code

        return "OS"  # Default
