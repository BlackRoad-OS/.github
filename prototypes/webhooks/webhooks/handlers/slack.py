"""Slack webhook handler."""

import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class SlackHandler(WebhookHandler):
    """
    Handle Slack webhooks (Events API & Interactions).

    Events:
    - Message posted
    - Reaction added
    - Channel created
    - User joined
    - App mentioned
    - Slash commands
    - Interactive components (buttons, modals)
    """

    name = "slack"
    target_org = "OS"  # Slack is general communication

    # Event type to signal mapping
    EVENT_MAP = {
        # Messages
        "message": SignalType.MESSAGE,
        "message.channels": SignalType.MESSAGE,
        "message.groups": SignalType.MESSAGE,
        "message.im": SignalType.DIRECT_MESSAGE,
        "message.mpim": SignalType.GROUP_MESSAGE,
        # Reactions
        "reaction_added": SignalType.REACTION,
        "reaction_removed": SignalType.REACTION,
        # Channels
        "channel_created": SignalType.CHANNEL_CREATED,
        "channel_deleted": SignalType.CHANNEL_DELETED,
        "channel_archive": SignalType.CHANNEL_ARCHIVED,
        # Members
        "member_joined_channel": SignalType.USER_JOINED,
        "member_left_channel": SignalType.USER_LEFT,
        "team_join": SignalType.USER_JOINED,
        # App
        "app_mention": SignalType.MENTION,
        "app_home_opened": SignalType.APP_OPENED,
        # Files
        "file_shared": SignalType.FILE_SHARED,
        "file_deleted": SignalType.FILE_DELETED,
        # Interactive
        "block_actions": SignalType.BUTTON_CLICK,
        "view_submission": SignalType.FORM_SUBMIT,
        "shortcut": SignalType.SHORTCUT,
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for Slack webhook headers."""
        # Check for Slack signature header
        if self.get_header(headers, "X-Slack-Signature"):
            return True

        # Check for Slack-specific fields
        if body.get("token") and body.get("team_id"):
            return True

        # Check for Events API structure
        if body.get("type") in ("url_verification", "event_callback"):
            return True

        return False

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify Slack webhook signature."""
        if not secret:
            return True

        signature = self.get_header(headers, "X-Slack-Signature")
        timestamp = self.get_header(headers, "X-Slack-Request-Timestamp")

        if not signature or not timestamp:
            return False

        # Check timestamp isn't too old (5 minutes)
        try:
            ts = int(timestamp)
            if abs(time.time() - ts) > 300:
                return False
        except ValueError:
            return False

        # Compute expected signature
        sig_basestring = f"v0:{timestamp}:{body.decode()}"
        expected = "v0=" + hmac.new(
            secret.encode(),
            sig_basestring.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse Slack webhook into Signal."""
        # Handle URL verification (Slack setup)
        if body.get("type") == "url_verification":
            return Signal(
                type=SignalType.PING,
                source=self.name,
                target=self.target_org,
                data={
                    "event": "url_verification",
                    "challenge": body.get("challenge", ""),
                },
                raw=body,
            )

        # Handle Events API
        if body.get("type") == "event_callback":
            return self._parse_event(body)

        # Handle interactive payloads
        if body.get("type") in ("block_actions", "view_submission", "shortcut"):
            return self._parse_interactive(body)

        # Handle slash commands
        if body.get("command"):
            return self._parse_command(body)

        # Fallback
        return Signal(
            type=SignalType.CUSTOM,
            source=self.name,
            target=self.target_org,
            data={"event": "unknown", "raw_type": body.get("type", "")},
            raw=body,
        )

    def _parse_event(self, body: Dict[str, Any]) -> Signal:
        """Parse Slack Events API payload."""
        event = body.get("event", {})
        event_type = event.get("type", "unknown")

        # Handle message subtypes
        if event_type == "message" and event.get("subtype"):
            event_type = f"message.{event.get('subtype')}"

        signal_type = self.EVENT_MAP.get(event_type, SignalType.CUSTOM)

        data = {
            "event": event_type,
            "team_id": body.get("team_id", ""),
            "channel": event.get("channel", ""),
            "user": event.get("user", ""),
            "ts": event.get("ts", ""),
        }

        # Message events
        if "message" in event_type:
            data.update({
                "text": event.get("text", "")[:200],  # Truncate long messages
                "thread_ts": event.get("thread_ts", ""),
            })

        # Reaction events
        elif "reaction" in event_type:
            data.update({
                "reaction": event.get("reaction", ""),
                "item_ts": event.get("item", {}).get("ts", ""),
            })

        # Member events
        elif "member" in event_type or "team_join" in event_type:
            data.update({
                "user_id": event.get("user", event.get("user", {}).get("id", "")),
            })

        # App mention
        elif event_type == "app_mention":
            data.update({
                "text": event.get("text", "")[:200],
                "mentioned_user_id": body.get("authorizations", [{}])[0].get("user_id", ""),
            })

        return Signal(
            type=signal_type,
            source=self.name,
            target=self.target_org,
            data=data,
            raw=body,
        )

    def _parse_interactive(self, body: Dict[str, Any]) -> Signal:
        """Parse Slack interactive payload."""
        payload_type = body.get("type", "unknown")
        signal_type = self.EVENT_MAP.get(payload_type, SignalType.BUTTON_CLICK)

        user = body.get("user", {})
        channel = body.get("channel", {})

        data = {
            "event": payload_type,
            "user_id": user.get("id", ""),
            "user_name": user.get("username", ""),
            "channel": channel.get("id", ""),
            "trigger_id": body.get("trigger_id", ""),
        }

        # Block actions (button clicks, selects, etc.)
        if payload_type == "block_actions":
            actions = body.get("actions", [{}])
            action = actions[0] if actions else {}
            data.update({
                "action_id": action.get("action_id", ""),
                "block_id": action.get("block_id", ""),
                "value": action.get("value", action.get("selected_option", {}).get("value", "")),
            })

        # View submissions (modals)
        elif payload_type == "view_submission":
            view = body.get("view", {})
            data.update({
                "view_id": view.get("id", ""),
                "callback_id": view.get("callback_id", ""),
                "values": view.get("state", {}).get("values", {}),
            })

        return Signal(
            type=signal_type,
            source=self.name,
            target=self.target_org,
            data=data,
            raw=body,
        )

    def _parse_command(self, body: Dict[str, Any]) -> Signal:
        """Parse Slack slash command."""
        return Signal(
            type=SignalType.COMMAND,
            source=self.name,
            target=self.target_org,
            data={
                "event": "slash_command",
                "command": body.get("command", ""),
                "text": body.get("text", ""),
                "user_id": body.get("user_id", ""),
                "user_name": body.get("user_name", ""),
                "channel": body.get("channel_id", ""),
                "team_id": body.get("team_id", ""),
                "trigger_id": body.get("trigger_id", ""),
            },
            raw=body,
        )
