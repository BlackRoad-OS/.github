"""Cloudflare webhook handler."""

import hmac
import hashlib
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class CloudflareHandler(WebhookHandler):
    """
    Handle Cloudflare webhooks (Notifications).

    Events:
    - Worker deployed
    - Pages deployment
    - SSL certificate expiring
    - DDoS attack detected
    - Origin health changed
    """

    name = "cloudflare"
    target_org = "CLD"

    # Alert type to signal mapping
    ALERT_MAP = {
        # Workers
        "workers_alert_deployment_success": SignalType.DEPLOY_SUCCESS,
        "workers_alert_deployment_failure": SignalType.DEPLOY_FAILED,
        # Pages
        "pages_deployment_success": SignalType.DEPLOY_SUCCESS,
        "pages_deployment_failure": SignalType.DEPLOY_FAILED,
        # Security
        "ddos_attack_l4": SignalType.SECURITY_ALERT,
        "ddos_attack_l7": SignalType.SECURITY_ALERT,
        "waf_attack": SignalType.SECURITY_ALERT,
        # SSL
        "ssl_certificate_expiring": SignalType.CERTIFICATE_EXPIRING,
        "ssl_certificate_expired": SignalType.CERTIFICATE_EXPIRED,
        # Health
        "origin_health_status_changed": SignalType.HEALTH_CHANGED,
        "load_balancing_health_alert": SignalType.HEALTH_CHANGED,
        # General
        "zone_audit_log": SignalType.AUDIT_LOG,
        "billing_usage_alert": SignalType.BILLING_ALERT,
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for Cloudflare webhook headers."""
        # Check for CF webhook signature header
        if self.get_header(headers, "CF-Webhook-Auth"):
            return True

        # Check for Cloudflare notification structure
        if body.get("data", {}).get("alert_type"):
            return True

        # Check for account_id field
        if "account_id" in body or "zone_id" in body:
            return True

        return False

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify Cloudflare webhook signature."""
        if not secret:
            return True

        auth_token = self.get_header(headers, "CF-Webhook-Auth")
        if not auth_token:
            return False

        # Simple token comparison
        return hmac.compare_digest(auth_token, secret)

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse Cloudflare webhook into Signal."""
        data_block = body.get("data", body)
        alert_type = data_block.get("alert_type", "unknown")
        signal_type = self.ALERT_MAP.get(alert_type, SignalType.CUSTOM)

        data = {
            "event": alert_type,
            "alert_type": alert_type,
            "account_id": body.get("account_id", ""),
            "zone_id": body.get("zone_id", ""),
        }

        # Worker/Pages deployments
        if "deployment" in alert_type or "workers" in alert_type or "pages" in alert_type:
            deployment = data_block.get("deployment", data_block)
            data.update({
                "worker_name": deployment.get("script_name", ""),
                "environment": deployment.get("environment", "production"),
                "version": deployment.get("version_id", ""),
                "status": "success" if "success" in alert_type else "failed",
            })

        # Security alerts
        elif "ddos" in alert_type or "waf" in alert_type or "attack" in alert_type:
            data.update({
                "attack_type": alert_type,
                "severity": data_block.get("severity", "high"),
                "target": data_block.get("target", ""),
                "mitigation": data_block.get("mitigation_status", "mitigated"),
            })

        # SSL/Certificate events
        elif "ssl" in alert_type or "certificate" in alert_type:
            data.update({
                "certificate_id": data_block.get("certificate_id", ""),
                "hostname": data_block.get("hostname", ""),
                "expiry_date": data_block.get("expiry_date", ""),
                "days_until_expiry": data_block.get("days_until_expiry", 0),
            })

        # Health events
        elif "health" in alert_type:
            data.update({
                "origin": data_block.get("origin", ""),
                "pool_id": data_block.get("pool_id", ""),
                "previous_status": data_block.get("previous_status", ""),
                "new_status": data_block.get("new_status", ""),
            })

        # Billing
        elif "billing" in alert_type:
            data.update({
                "usage_type": data_block.get("usage_type", ""),
                "current_usage": data_block.get("current_usage", 0),
                "limit": data_block.get("limit", 0),
            })

        return Signal(
            type=signal_type,
            source=self.name,
            target=self.target_org,
            data=data,
            raw=body,
        )
