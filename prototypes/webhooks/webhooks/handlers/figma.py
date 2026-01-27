"""Figma webhook handler."""

import hmac
import hashlib
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class FigmaHandler(WebhookHandler):
    """
    Handle Figma webhooks.

    Events:
    - File updated
    - File deleted
    - File version updated
    - Comment added
    - Library published
    - Component updated
    """

    name = "figma"
    target_org = "STU"  # Design goes to Studio

    # Event type to signal mapping
    EVENT_MAP = {
        "FILE_UPDATE": SignalType.FILE_UPDATED,
        "FILE_DELETE": SignalType.FILE_DELETED,
        "FILE_VERSION_UPDATE": SignalType.VERSION_CREATED,
        "FILE_COMMENT": SignalType.COMMENT,
        "LIBRARY_PUBLISH": SignalType.LIBRARY_PUBLISHED,
        "COMPONENT_UPDATE": SignalType.COMPONENT_UPDATED,
        "STYLE_UPDATE": SignalType.STYLE_UPDATED,
        "PING": SignalType.PING,
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for Figma webhook indicators."""
        # Check for Figma-specific header
        if self.get_header(headers, "X-Figma-Signature"):
            return True

        # Check for Figma event structure
        if body.get("event_type") and body.get("file_key"):
            return True

        # Check for webhook_id (Figma format)
        if body.get("webhook_id") and body.get("passcode"):
            return True

        return False

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify Figma webhook signature."""
        if not secret:
            return True

        signature = self.get_header(headers, "X-Figma-Signature")
        if not signature:
            # Fallback to passcode verification
            try:
                body_dict = self._parse_json(body)
                return body_dict.get("passcode") == secret
            except:
                return False

        # Verify HMAC signature
        expected = hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse Figma webhook into Signal."""
        event_type = body.get("event_type", "UNKNOWN")
        signal_type = self.EVENT_MAP.get(event_type, SignalType.CUSTOM)

        # Handle ping/test webhooks
        if event_type == "PING" or body.get("test"):
            return Signal(
                type=SignalType.PING,
                source=self.name,
                target=self.target_org,
                data={"event": "ping", "webhook_id": body.get("webhook_id", "")},
                raw=body,
            )

        data = {
            "event": event_type,
            "file_key": body.get("file_key", ""),
            "file_name": body.get("file_name", ""),
            "timestamp": body.get("timestamp", ""),
            "webhook_id": body.get("webhook_id", ""),
        }

        # File update events
        if event_type in ("FILE_UPDATE", "FILE_VERSION_UPDATE"):
            data.update({
                "version_id": body.get("version_id", ""),
                "label": body.get("label", ""),
                "description": body.get("description", ""),
                "triggered_by": body.get("triggered_by", {}).get("handle", ""),
            })

        # Comment events
        elif event_type == "FILE_COMMENT":
            comment = body.get("comment", [{}])
            if isinstance(comment, list) and comment:
                comment = comment[0]
            data.update({
                "comment_id": body.get("comment_id", ""),
                "comment": comment.get("text", "") if isinstance(comment, dict) else str(comment)[:200],
                "user": body.get("triggered_by", {}).get("handle", ""),
                "parent_id": body.get("parent_id", ""),
            })

        # Library events
        elif event_type == "LIBRARY_PUBLISH":
            data.update({
                "library_name": body.get("library_name", ""),
                "library_version": body.get("library_version", ""),
                "components_added": body.get("components_added", []),
                "components_modified": body.get("components_modified", []),
                "components_deleted": body.get("components_deleted", []),
            })

        # Component/style events
        elif event_type in ("COMPONENT_UPDATE", "STYLE_UPDATE"):
            data.update({
                "component_key": body.get("component_key", ""),
                "component_name": body.get("component_name", ""),
                "change_type": body.get("change_type", ""),
            })

        # File deletion
        elif event_type == "FILE_DELETE":
            data.update({
                "deleted_at": body.get("deleted_at", ""),
            })

        return Signal(
            type=signal_type,
            source=self.name,
            target=self.target_org,
            data=data,
            raw=body,
        )

    def _parse_json(self, body: bytes) -> Dict[str, Any]:
        """Parse JSON body."""
        import json
        return json.loads(body.decode())
