"""Salesforce webhook handler."""

import hmac
import hashlib
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class SalesforceHandler(WebhookHandler):
    """
    Handle Salesforce webhooks (Outbound Messages & Platform Events).

    Events:
    - Lead created/updated
    - Contact created/updated
    - Opportunity created/updated/closed
    - Account created/updated
    - Custom object changes
    """

    name = "salesforce"
    target_org = "FND"

    # Salesforce object to signal type mapping
    OBJECT_MAP = {
        "Lead": {
            "created": SignalType.LEAD_CREATED,
            "updated": SignalType.LEAD_UPDATED,
        },
        "Contact": {
            "created": SignalType.CONTACT_CREATED,
            "updated": SignalType.CONTACT_UPDATED,
        },
        "Opportunity": {
            "created": SignalType.OPPORTUNITY_CREATED,
            "updated": SignalType.RECORD_UPDATED,
            "Closed Won": SignalType.DEAL_CLOSED,
            "Closed Lost": SignalType.DEAL_LOST,
        },
        "Account": {
            "created": SignalType.ACCOUNT_CREATED,
            "updated": SignalType.RECORD_UPDATED,
        },
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for Salesforce webhook indicators."""
        # Check for SOAPAction header (Outbound Messages)
        soap_action = self.get_header(headers, "SOAPAction")
        if soap_action and "salesforce" in soap_action.lower():
            return True

        # Check for Platform Event structure
        if "sObjectType" in body or "sobjectType" in body:
            return True

        # Check for Salesforce-specific fields
        if body.get("attributes", {}).get("type"):
            return True

        return False

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify Salesforce webhook (org ID validation)."""
        if not secret:
            return True

        # For Salesforce, secret is typically the Org ID
        # Check if OrganizationId matches
        try:
            body_dict = self._parse_json(body)
            org_id = body_dict.get("OrganizationId") or body_dict.get("organizationId", "")
            return org_id == secret
        except:
            return False

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse Salesforce webhook into Signal."""
        # Determine object type and action
        sobject_type = (
            body.get("sObjectType") or
            body.get("sobjectType") or
            body.get("attributes", {}).get("type", "Unknown")
        )

        # Determine action from change type or status
        action = body.get("ChangeEventHeader", {}).get("changeType", "updated").lower()
        if action == "create":
            action = "created"

        # Check for opportunity status
        stage = body.get("StageName", "")
        if stage in ("Closed Won", "Closed Lost"):
            action = stage

        # Get signal type
        object_signals = self.OBJECT_MAP.get(sobject_type, {})
        signal_type = object_signals.get(action, SignalType.RECORD_UPDATED)

        # Extract data
        data = {
            "event": f"{sobject_type}.{action}",
            "object_type": sobject_type,
            "action": action,
            "id": body.get("Id", ""),
            "name": body.get("Name", ""),
        }

        # Add type-specific fields
        if sobject_type == "Lead":
            data.update({
                "email": body.get("Email", ""),
                "company": body.get("Company", ""),
                "status": body.get("Status", ""),
            })
        elif sobject_type == "Contact":
            data.update({
                "email": body.get("Email", ""),
                "account_id": body.get("AccountId", ""),
            })
        elif sobject_type == "Opportunity":
            data.update({
                "stage": stage,
                "amount": body.get("Amount", 0),
                "close_date": body.get("CloseDate", ""),
                "account_id": body.get("AccountId", ""),
            })
        elif sobject_type == "Account":
            data.update({
                "industry": body.get("Industry", ""),
                "type": body.get("Type", ""),
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
