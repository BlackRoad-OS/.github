"""Google Cloud webhook handler (Pub/Sub Push)."""

import base64
import json
from typing import Dict, Any, Optional
from .base import WebhookHandler
from ..signal import Signal, SignalType


class GoogleHandler(WebhookHandler):
    """
    Handle Google Cloud Pub/Sub push webhooks.

    Events:
    - Cloud Build completed
    - Cloud Functions deployed
    - GCE instance state changed
    - Cloud Storage object created
    - BigQuery job completed
    - Cloud Run deployment
    """

    name = "google"
    target_org = "CLD"

    # Event type to signal mapping
    EVENT_MAP = {
        # Cloud Build
        "google.cloud.cloudbuild.build.v1.created": SignalType.BUILD_STARTED,
        "google.cloud.cloudbuild.build.v1.updated": SignalType.BUILD_PROGRESS,
        "SUCCESS": SignalType.BUILD_SUCCESS,
        "FAILURE": SignalType.BUILD_FAILED,
        "TIMEOUT": SignalType.BUILD_TIMEOUT,
        # Cloud Functions
        "google.cloud.functions.function.v1.deployed": SignalType.DEPLOY_SUCCESS,
        "google.cloud.functions.function.v1.deleted": SignalType.RESOURCE_DELETED,
        # GCE
        "google.compute.instance.v1.insert": SignalType.RESOURCE_CREATED,
        "google.compute.instance.v1.delete": SignalType.RESOURCE_DELETED,
        "google.compute.instance.v1.start": SignalType.RESOURCE_STARTED,
        "google.compute.instance.v1.stop": SignalType.RESOURCE_STOPPED,
        # Cloud Storage
        "google.cloud.storage.object.v1.finalized": SignalType.FILE_UPLOADED,
        "google.cloud.storage.object.v1.deleted": SignalType.FILE_DELETED,
        "google.cloud.storage.object.v1.metadataUpdated": SignalType.RECORD_UPDATED,
        # BigQuery
        "google.cloud.bigquery.job.v1.completed": SignalType.JOB_COMPLETED,
        # Cloud Run
        "google.cloud.run.service.v1.created": SignalType.DEPLOY_SUCCESS,
        "google.cloud.run.service.v1.deleted": SignalType.RESOURCE_DELETED,
        # Pub/Sub
        "google.cloud.pubsub.topic.v1.messagePublished": SignalType.MESSAGE,
    }

    def can_handle(self, headers: Dict[str, str], body: Dict[str, Any]) -> bool:
        """Check for Google Cloud Pub/Sub push format."""
        # Check for Pub/Sub message structure
        if body.get("message", {}).get("data"):
            return True

        # Check for subscription field
        if body.get("subscription", "").startswith("projects/"):
            return True

        return False

    def verify(self, headers: Dict[str, str], body: bytes, secret: Optional[str] = None) -> bool:
        """Verify Google Cloud webhook (via OIDC token)."""
        if not secret:
            return True

        # Google Cloud uses OIDC tokens in Authorization header
        auth_header = self.get_header(headers, "Authorization")
        if not auth_header:
            return False

        # In production, verify the JWT token
        # For now, check token presence
        if auth_header.startswith("Bearer "):
            return True

        return False

    def parse(self, headers: Dict[str, str], body: Dict[str, Any]) -> Signal:
        """Parse Google Cloud Pub/Sub webhook into Signal."""
        message = body.get("message", {})

        # Decode base64 data
        data_b64 = message.get("data", "")
        try:
            decoded = base64.b64decode(data_b64).decode()
            payload = json.loads(decoded)
        except:
            payload = {"raw_data": data_b64}

        # Get event type from attributes or payload
        attributes = message.get("attributes", {})
        event_type = (
            attributes.get("eventType") or
            attributes.get("ce-type") or
            payload.get("protoPayload", {}).get("methodName") or
            payload.get("status", "unknown")
        )

        signal_type = self.EVENT_MAP.get(event_type, SignalType.CUSTOM)

        data = {
            "event": event_type,
            "message_id": message.get("messageId", ""),
            "publish_time": message.get("publishTime", ""),
            "subscription": body.get("subscription", ""),
        }

        # Add attributes
        data["attributes"] = attributes

        # Cloud Build events
        if "cloudbuild" in str(attributes) or "build" in payload:
            build = payload.get("build", payload)
            status = build.get("status", "")
            signal_type = self.EVENT_MAP.get(status, SignalType.BUILD_PROGRESS)
            data.update({
                "build_id": build.get("id", ""),
                "status": status,
                "project_id": build.get("projectId", ""),
                "source": build.get("source", {}).get("repoSource", {}).get("repoName", ""),
                "branch": build.get("source", {}).get("repoSource", {}).get("branchName", ""),
                "duration": build.get("timing", {}).get("BUILD", {}).get("endTime", ""),
            })

        # Cloud Storage events
        elif "storage" in event_type.lower() or "bucket" in str(payload):
            resource = payload.get("resource", payload)
            data.update({
                "bucket": resource.get("bucket", payload.get("bucket", "")),
                "object": resource.get("name", payload.get("name", "")),
                "size": resource.get("size", 0),
                "content_type": resource.get("contentType", ""),
            })

        # GCE events
        elif "compute" in event_type.lower() or "instance" in str(payload):
            resource = payload.get("resource", payload)
            data.update({
                "instance": resource.get("name", ""),
                "zone": resource.get("zone", ""),
                "machine_type": resource.get("machineType", ""),
                "status": resource.get("status", ""),
            })

        # BigQuery events
        elif "bigquery" in event_type.lower() or "job" in str(payload):
            job = payload.get("job", payload)
            data.update({
                "job_id": job.get("jobReference", {}).get("jobId", ""),
                "project_id": job.get("jobReference", {}).get("projectId", ""),
                "job_type": job.get("configuration", {}).keys(),
                "state": job.get("status", {}).get("state", ""),
            })

        return Signal(
            type=signal_type,
            source=self.name,
            target=self.target_org,
            data=data,
            raw=body,
        )
