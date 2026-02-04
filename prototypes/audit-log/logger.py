"""
Audit Logger
Structured, append-only audit logging for all BlackRoad system events.
"""

import time
import uuid
import json
from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum

from store import AuditStore


class Outcome(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"
    ERROR = "error"
    SKIPPED = "skipped"


class Severity(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """An immutable audit log entry."""
    id: str
    timestamp: float
    actor: str          # Who did it: "cece", "user:alexa", "system", "webhook:github"
    action: str         # What happened: "route.request", "config.update"
    resource: str       # What was affected: "provider:claude", "route:code_review"
    outcome: Outcome
    severity: Severity
    category: str = ""  # "auth", "route", "webhook", "config", "deploy", "admin"
    details: dict = field(default_factory=dict)
    session_id: str = ""
    correlation_id: str = ""
    source_ip: str = ""
    duration_ms: float = 0.0
    tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
            "actor": self.actor,
            "action": self.action,
            "resource": self.resource,
            "outcome": self.outcome.value,
            "severity": self.severity.value,
            "category": self.category,
            "details": self.details,
            "session_id": self.session_id,
            "correlation_id": self.correlation_id,
            "source_ip": self.source_ip,
            "duration_ms": self.duration_ms,
            "tags": self.tags,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class AuditLogger:
    """
    Central audit logger for BlackRoad.

    Usage:
        logger = AuditLogger(session_id="sess_123")
        logger.log("cece", "route.request", "provider:claude", Outcome.SUCCESS)

    All events are:
    - Timestamped with unique IDs
    - Stored in append-only storage
    - Indexed for fast querying
    - Exportable for compliance
    """

    def __init__(
        self,
        session_id: str = "",
        store: Optional[AuditStore] = None,
    ):
        self.session_id = session_id or f"sess_{uuid.uuid4().hex[:8]}"
        self.store = store or AuditStore()
        self._security_actions = {
            "auth.login_failed",
            "auth.key_rotate",
            "webhook.rejected",
            "webhook.replay",
            "admin.role_change",
            "admin.secret_update",
            "config.delete",
            "deploy.rollback",
        }
        self._alert_callbacks: list = []

    def log(
        self,
        actor: str,
        action: str,
        resource: str,
        outcome: Outcome = Outcome.SUCCESS,
        severity: Optional[Severity] = None,
        category: str = "",
        details: Optional[dict] = None,
        correlation_id: str = "",
        source_ip: str = "",
        duration_ms: float = 0.0,
        tags: Optional[list] = None,
    ) -> AuditEvent:
        """
        Log an audit event.

        Args:
            actor: Who performed the action
            action: What action was taken (dot-separated)
            resource: What was affected
            outcome: Result of the action
            severity: Log severity (auto-determined if not set)
            category: Event category (auto-determined from action if not set)
            details: Additional context
            correlation_id: Link related events
            source_ip: Source IP address
            duration_ms: How long the action took
            tags: Additional tags

        Returns:
            The created AuditEvent
        """
        # Auto-determine category from action
        if not category:
            category = action.split(".")[0] if "." in action else "general"

        # Auto-determine severity
        if severity is None:
            if outcome == Outcome.DENIED:
                severity = Severity.WARNING
            elif outcome == Outcome.ERROR:
                severity = Severity.ERROR
            elif action in self._security_actions:
                severity = Severity.WARNING
            else:
                severity = Severity.INFO

        event = AuditEvent(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            timestamp=time.time(),
            actor=actor,
            action=action,
            resource=resource,
            outcome=outcome,
            severity=severity,
            category=category,
            details=details or {},
            session_id=self.session_id,
            correlation_id=correlation_id or f"cor_{uuid.uuid4().hex[:8]}",
            source_ip=source_ip,
            duration_ms=duration_ms,
            tags=tags or [],
        )

        # Store the event
        self.store.append(event)

        # Check for security alerts
        if action in self._security_actions or severity in (Severity.ERROR, Severity.CRITICAL):
            self._emit_alert(event)

        return event

    # ── Convenience Methods ─────────────────────────────────────────

    def log_route(
        self,
        provider: str,
        route: str,
        outcome: Outcome,
        tokens: int = 0,
        cost: float = 0.0,
        latency_ms: float = 0.0,
        failover_from: str = "",
    ) -> AuditEvent:
        """Log a routing event."""
        details = {
            "tokens": tokens,
            "cost": cost,
        }
        if failover_from:
            details["failover_from"] = failover_from

        return self.log(
            actor="system",
            action="route.request" if not failover_from else "route.failover",
            resource=f"provider:{provider}",
            outcome=outcome,
            details=details,
            duration_ms=latency_ms,
            tags=[f"route:{route}"],
        )

    def log_webhook(
        self,
        provider: str,
        event_type: str,
        verified: bool,
        source_ip: str = "",
        reason: str = "",
    ) -> AuditEvent:
        """Log a webhook event."""
        action = "webhook.verified" if verified else "webhook.rejected"
        outcome = Outcome.SUCCESS if verified else Outcome.DENIED

        return self.log(
            actor=f"webhook:{provider}",
            action=action,
            resource=f"webhook:{event_type}",
            outcome=outcome,
            source_ip=source_ip,
            details={"reason": reason} if reason else {},
        )

    def log_auth(
        self,
        actor: str,
        action: str,
        success: bool,
        source_ip: str = "",
        details: Optional[dict] = None,
    ) -> AuditEvent:
        """Log an authentication event."""
        return self.log(
            actor=actor,
            action=f"auth.{action}",
            resource="auth",
            outcome=Outcome.SUCCESS if success else Outcome.FAILURE,
            source_ip=source_ip,
            details=details,
        )

    def log_config(
        self,
        actor: str,
        action: str,
        resource: str,
        old_value: Any = None,
        new_value: Any = None,
    ) -> AuditEvent:
        """Log a configuration change."""
        details = {}
        if old_value is not None:
            details["old_value"] = str(old_value)[:200]
        if new_value is not None:
            details["new_value"] = str(new_value)[:200]

        return self.log(
            actor=actor,
            action=f"config.{action}",
            resource=resource,
            details=details,
        )

    # ── Alerting ────────────────────────────────────────────────────

    def on_alert(self, callback) -> None:
        """Register a callback for security alerts."""
        self._alert_callbacks.append(callback)

    def _emit_alert(self, event: AuditEvent) -> None:
        """Emit a security alert."""
        for cb in self._alert_callbacks:
            try:
                cb(event)
            except Exception:
                pass  # Alert callbacks should not break logging

    # ── Querying ────────────────────────────────────────────────────

    def query(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        category: Optional[str] = None,
        outcome: Optional[Outcome] = None,
        since: Optional[float] = None,
        limit: int = 100,
    ) -> list[dict]:
        """Query audit events with filters."""
        return self.store.query(
            actor=actor,
            action=action,
            category=category,
            outcome=outcome.value if outcome else None,
            since=since,
            limit=limit,
        )

    def summary(self) -> dict:
        """Get audit log summary."""
        return self.store.summary()

    def export_json(self, since: Optional[float] = None) -> str:
        """Export events as JSON for compliance."""
        events = self.store.query(since=since, limit=10000)
        return json.dumps(events, indent=2)


# ── CLI Demo ────────────────────────────────────────────────────────

def main():
    print("BlackRoad Audit Log Pipeline")
    print("=" * 40)

    logger = AuditLogger(session_id="demo_session")

    # Simulate events
    logger.log_route("claude", "code_review", Outcome.SUCCESS, tokens=450, cost=0.003, latency_ms=1200)
    logger.log_route("gpt", "summarize", Outcome.SUCCESS, tokens=200, cost=0.001, latency_ms=800)
    logger.log_route("claude", "debug", Outcome.FAILURE, latency_ms=30000)
    logger.log_route("gpt", "debug", Outcome.SUCCESS, tokens=600, cost=0.005, latency_ms=1500, failover_from="claude")
    logger.log_webhook("github", "push", verified=True, source_ip="140.82.115.0")
    logger.log_webhook("unknown", "test", verified=False, source_ip="1.2.3.4", reason="invalid_signature")
    logger.log_auth("user:alexa", "login", success=True, source_ip="192.168.1.1")
    logger.log_config("cece", "update", "provider:claude", old_value="sonnet-3.5", new_value="sonnet-4")

    # Print summary
    summary = logger.summary()
    print(f"\nTotal events: {summary['total_events']}")
    print(f"Categories: {json.dumps(summary['by_category'], indent=2)}")
    print(f"Outcomes: {json.dumps(summary['by_outcome'], indent=2)}")
    print(f"\nRecent events:")
    for evt in logger.query(limit=5):
        print(f"  [{evt['severity']:>8}] {evt['actor']:<16} {evt['action']:<24} -> {evt['outcome']}")


if __name__ == "__main__":
    main()
