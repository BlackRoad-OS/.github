"""
Signal - The universal message format.

Every webhook becomes a signal that flows through the mesh.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class SignalType(Enum):
    """Types of signals."""
    # GitHub
    PUSH = "push"
    PULL_REQUEST = "pull_request"
    ISSUE = "issue"
    WORKFLOW_RUN = "workflow_run"
    RELEASE = "release"
    COMMENT = "comment"

    # Salesforce
    RECORD_CREATED = "record_created"
    RECORD_UPDATED = "record_updated"
    RECORD_DELETED = "record_deleted"
    LEAD_CREATED = "lead_created"
    LEAD_UPDATED = "lead_updated"
    CONTACT_CREATED = "contact_created"
    CONTACT_UPDATED = "contact_updated"
    OPPORTUNITY_CREATED = "opportunity_created"
    ACCOUNT_CREATED = "account_created"
    DEAL_CLOSED = "deal_closed"
    DEAL_LOST = "deal_lost"

    # Stripe
    PAYMENT_RECEIVED = "payment_received"
    PAYMENT_FAILED = "payment_failed"
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    INVOICE_PAID = "invoice_paid"

    # Cloudflare
    WORKER_DEPLOYED = "worker_deployed"
    DEPLOY_SUCCESS = "deploy_success"
    DEPLOY_FAILED = "deploy_failed"
    SECURITY_ALERT = "security_alert"
    CERTIFICATE_EXPIRING = "certificate_expiring"
    CERTIFICATE_EXPIRED = "certificate_expired"
    HEALTH_CHANGED = "health_changed"
    AUDIT_LOG = "audit_log"
    BILLING_ALERT = "billing_alert"
    TRAFFIC_SPIKE = "traffic_spike"
    ERROR_RATE_HIGH = "error_rate_high"

    # Slack
    SLASH_COMMAND = "slash_command"
    COMMAND = "command"
    MESSAGE = "message"
    DIRECT_MESSAGE = "direct_message"
    GROUP_MESSAGE = "group_message"
    REACTION = "reaction"
    CHANNEL_CREATED = "channel_created"
    CHANNEL_DELETED = "channel_deleted"
    CHANNEL_ARCHIVED = "channel_archived"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    MENTION = "mention"
    APP_OPENED = "app_opened"
    FILE_SHARED = "file_shared"
    BUTTON_CLICK = "button_click"
    FORM_SUBMIT = "form_submit"
    SHORTCUT = "shortcut"

    # Google Cloud
    FILE_CREATED = "file_created"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"
    FILE_UPLOADED = "file_uploaded"
    BUILD_STARTED = "build_started"
    BUILD_PROGRESS = "build_progress"
    BUILD_SUCCESS = "build_success"
    BUILD_FAILED = "build_failed"
    BUILD_TIMEOUT = "build_timeout"
    RESOURCE_CREATED = "resource_created"
    RESOURCE_DELETED = "resource_deleted"
    RESOURCE_STARTED = "resource_started"
    RESOURCE_STOPPED = "resource_stopped"
    JOB_COMPLETED = "job_completed"

    # Figma
    DESIGN_UPDATED = "design_updated"
    COMMENT_ADDED = "comment_added"
    FILE_UPDATED = "file_updated"
    VERSION_CREATED = "version_created"
    LIBRARY_PUBLISHED = "library_published"
    COMPONENT_UPDATED = "component_updated"
    STYLE_UPDATED = "style_updated"

    # Generic
    CUSTOM = "custom"
    PING = "ping"
    ERROR = "error"


@dataclass
class Signal:
    """
    A signal flowing through the BlackRoad mesh.

    Every external event becomes a signal with:
    - type: What happened
    - source: Where it came from (provider)
    - target: Where it should go (org)
    - data: The payload
    """
    type: SignalType
    source: str                    # Provider name (github, stripe, etc.)
    target: str                    # Target org code (OS, FND, AI, etc.)
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    id: str = ""
    raw: Optional[Dict[str, Any]] = None  # Original webhook payload

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if not self.id:
            import hashlib
            content = f"{self.type.value}{self.source}{self.timestamp}"
            self.id = hashlib.sha256(content.encode()).hexdigest()[:12]

    def format(self) -> str:
        """Format as BlackRoad signal string."""
        emoji = self._get_emoji()
        data_str = ", ".join(f"{k}={v}" for k, v in list(self.data.items())[:3])
        return f"{emoji} {self.source.upper()} → {self.target} : {self.type.value}, {data_str}"

    def _get_emoji(self) -> str:
        """Get emoji for signal type."""
        emoji_map = {
            # GitHub
            SignalType.PUSH: "📥",
            SignalType.PULL_REQUEST: "🔀",
            SignalType.ISSUE: "📝",
            SignalType.WORKFLOW_RUN: "⚙️",
            SignalType.RELEASE: "🚀",
            SignalType.COMMENT: "💬",
            # Salesforce
            SignalType.RECORD_CREATED: "➕",
            SignalType.RECORD_UPDATED: "📝",
            SignalType.RECORD_DELETED: "🗑️",
            # Stripe
            SignalType.PAYMENT_RECEIVED: "💰",
            SignalType.PAYMENT_FAILED: "❌",
            SignalType.SUBSCRIPTION_CREATED: "📦",
            SignalType.SUBSCRIPTION_CANCELLED: "📦",
            SignalType.INVOICE_PAID: "🧾",
            # Cloudflare
            SignalType.WORKER_DEPLOYED: "🌐",
            SignalType.TRAFFIC_SPIKE: "📈",
            SignalType.ERROR_RATE_HIGH: "⚠️",
            # Slack
            SignalType.SLASH_COMMAND: "⌨️",
            SignalType.MESSAGE: "💬",
            # Google
            SignalType.FILE_CREATED: "📄",
            SignalType.FILE_MODIFIED: "📝",
            SignalType.FILE_DELETED: "🗑️",
            # Figma
            SignalType.DESIGN_UPDATED: "🎨",
            SignalType.COMMENT_ADDED: "💬",
            # Generic
            SignalType.CUSTOM: "📡",
            SignalType.PING: "🏓",
            SignalType.ERROR: "❌",
        }
        return emoji_map.get(self.type, "📡")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "source": self.source,
            "target": self.target,
            "data": self.data,
            "timestamp": self.timestamp,
            "formatted": self.format(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Signal":
        """Create from dictionary."""
        return cls(
            type=SignalType(data["type"]),
            source=data["source"],
            target=data["target"],
            data=data.get("data", {}),
            timestamp=data.get("timestamp", ""),
            id=data.get("id", ""),
        )
