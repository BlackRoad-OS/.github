"""
Webhook Signature Verification
Verify authenticity of incoming webhooks from various providers.
Implements HMAC verification, timestamp checking, and replay protection.
"""

import hmac
import hashlib
import time
import json
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class VerifyResult(Enum):
    VALID = "valid"
    INVALID_SIGNATURE = "invalid_signature"
    EXPIRED_TIMESTAMP = "expired_timestamp"
    REPLAY_DETECTED = "replay_detected"
    MISSING_HEADER = "missing_header"
    UNKNOWN_PROVIDER = "unknown_provider"
    ERROR = "error"


@dataclass
class VerificationRecord:
    """Record of a webhook verification attempt."""
    timestamp: float
    provider: str
    result: VerifyResult
    source_ip: str = ""
    event_type: str = ""
    details: str = ""

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "provider": self.provider,
            "result": self.result.value,
            "source_ip": self.source_ip,
            "event_type": self.event_type,
            "details": self.details,
        }


class WebhookVerifier:
    """
    Verifies webhook signatures from multiple providers.

    Features:
    - HMAC-SHA256 signature verification
    - Timestamp freshness checking (anti-replay)
    - Nonce tracking for replay protection
    - Per-provider verification strategies
    - Audit logging of all verification attempts
    """

    # Maximum age of a webhook timestamp (5 minutes)
    MAX_TIMESTAMP_AGE = 300

    # Nonce cache size for replay protection
    MAX_NONCES = 10000

    def __init__(self):
        self._secrets: dict[str, str] = {}  # provider -> secret
        self._nonces: set[str] = set()
        self._nonce_timestamps: list[tuple[float, str]] = []
        self._log: list[VerificationRecord] = []
        self._stats = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "expired": 0,
            "replay": 0,
        }

    def register_secret(self, provider: str, secret: str) -> None:
        """Register a webhook secret for a provider."""
        self._secrets[provider] = secret

    def verify(
        self,
        provider: str,
        headers: dict,
        body: bytes,
        source_ip: str = "",
    ) -> VerifyResult:
        """
        Verify an incoming webhook.

        Args:
            provider: Provider name (github, stripe, slack, etc.)
            headers: HTTP headers (case-insensitive keys)
            body: Raw request body as bytes
            source_ip: Source IP for logging

        Returns:
            VerifyResult indicating pass/fail
        """
        self._stats["total"] += 1

        # Normalize headers to lowercase
        headers_lower = {k.lower(): v for k, v in headers.items()}

        # Dispatch to provider-specific verification
        verifiers = {
            "github": self._verify_github,
            "stripe": self._verify_stripe,
            "slack": self._verify_slack,
            "salesforce": self._verify_salesforce,
            "generic": self._verify_generic,
        }

        verify_fn = verifiers.get(provider)
        if not verify_fn:
            result = VerifyResult.UNKNOWN_PROVIDER
        else:
            try:
                result = verify_fn(headers_lower, body)
            except Exception as e:
                result = VerifyResult.ERROR
                self._log_verification(provider, result, source_ip, details=str(e))
                return result

        # Update stats
        if result == VerifyResult.VALID:
            self._stats["valid"] += 1
        elif result == VerifyResult.INVALID_SIGNATURE:
            self._stats["invalid"] += 1
        elif result == VerifyResult.EXPIRED_TIMESTAMP:
            self._stats["expired"] += 1
        elif result == VerifyResult.REPLAY_DETECTED:
            self._stats["replay"] += 1

        # Extract event type for logging
        event_type = (
            headers_lower.get("x-github-event", "")
            or headers_lower.get("x-slack-event", "")
            or ""
        )

        self._log_verification(provider, result, source_ip, event_type)
        return result

    # ── Provider-Specific Verification ──────────────────────────────

    def _verify_github(self, headers: dict, body: bytes) -> VerifyResult:
        """
        GitHub webhook verification.
        Header: X-Hub-Signature-256 = sha256=<hex>
        """
        signature = headers.get("x-hub-signature-256", "")
        if not signature:
            return VerifyResult.MISSING_HEADER

        secret = self._secrets.get("github", "")
        if not secret:
            return VerifyResult.ERROR

        # GitHub format: sha256=<hex_digest>
        if not signature.startswith("sha256="):
            return VerifyResult.INVALID_SIGNATURE

        expected = "sha256=" + hmac.new(
            secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, expected):
            return VerifyResult.VALID
        return VerifyResult.INVALID_SIGNATURE

    def _verify_stripe(self, headers: dict, body: bytes) -> VerifyResult:
        """
        Stripe webhook verification.
        Header: Stripe-Signature = t=<timestamp>,v1=<signature>
        """
        sig_header = headers.get("stripe-signature", "")
        if not sig_header:
            return VerifyResult.MISSING_HEADER

        secret = self._secrets.get("stripe", "")
        if not secret:
            return VerifyResult.ERROR

        # Parse Stripe signature header
        elements = {}
        for item in sig_header.split(","):
            key, _, value = item.partition("=")
            elements[key.strip()] = value.strip()

        timestamp_str = elements.get("t", "")
        signature = elements.get("v1", "")

        if not timestamp_str or not signature:
            return VerifyResult.MISSING_HEADER

        # Check timestamp freshness
        try:
            timestamp = int(timestamp_str)
        except ValueError:
            return VerifyResult.INVALID_SIGNATURE

        if abs(time.time() - timestamp) > self.MAX_TIMESTAMP_AGE:
            return VerifyResult.EXPIRED_TIMESTAMP

        # Replay check
        nonce = f"stripe:{timestamp}:{signature[:16]}"
        if self._is_replay(nonce):
            return VerifyResult.REPLAY_DETECTED

        # Compute expected signature
        signed_payload = f"{timestamp}.".encode("utf-8") + body
        expected = hmac.new(
            secret.encode("utf-8"),
            signed_payload,
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, expected):
            self._record_nonce(nonce)
            return VerifyResult.VALID
        return VerifyResult.INVALID_SIGNATURE

    def _verify_slack(self, headers: dict, body: bytes) -> VerifyResult:
        """
        Slack webhook verification.
        Headers: X-Slack-Signature, X-Slack-Request-Timestamp
        Format: v0=<hmac_sha256(v0:timestamp:body)>
        """
        signature = headers.get("x-slack-signature", "")
        timestamp_str = headers.get("x-slack-request-timestamp", "")

        if not signature or not timestamp_str:
            return VerifyResult.MISSING_HEADER

        secret = self._secrets.get("slack", "")
        if not secret:
            return VerifyResult.ERROR

        # Timestamp freshness
        try:
            timestamp = int(timestamp_str)
        except ValueError:
            return VerifyResult.INVALID_SIGNATURE

        if abs(time.time() - timestamp) > self.MAX_TIMESTAMP_AGE:
            return VerifyResult.EXPIRED_TIMESTAMP

        # Replay check
        nonce = f"slack:{timestamp}:{signature[:16]}"
        if self._is_replay(nonce):
            return VerifyResult.REPLAY_DETECTED

        # Compute signature
        sig_basestring = f"v0:{timestamp}:".encode("utf-8") + body
        expected = "v0=" + hmac.new(
            secret.encode("utf-8"),
            sig_basestring,
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, expected):
            self._record_nonce(nonce)
            return VerifyResult.VALID
        return VerifyResult.INVALID_SIGNATURE

    def _verify_salesforce(self, headers: dict, body: bytes) -> VerifyResult:
        """
        Salesforce outbound message verification.
        Uses HMAC-SHA256 with a shared secret.
        """
        signature = headers.get("x-salesforce-signature", "")
        if not signature:
            return VerifyResult.MISSING_HEADER

        secret = self._secrets.get("salesforce", "")
        if not secret:
            return VerifyResult.ERROR

        expected = hmac.new(
            secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, expected):
            return VerifyResult.VALID
        return VerifyResult.INVALID_SIGNATURE

    def _verify_generic(self, headers: dict, body: bytes) -> VerifyResult:
        """
        Generic HMAC-SHA256 verification.
        Header: X-Signature = <hex_digest>
        """
        signature = headers.get("x-signature", "")
        if not signature:
            return VerifyResult.MISSING_HEADER

        secret = self._secrets.get("generic", "")
        if not secret:
            return VerifyResult.ERROR

        expected = hmac.new(
            secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, expected):
            return VerifyResult.VALID
        return VerifyResult.INVALID_SIGNATURE

    # ── Replay Protection ───────────────────────────────────────────

    def _is_replay(self, nonce: str) -> bool:
        """Check if this nonce was already seen."""
        return nonce in self._nonces

    def _record_nonce(self, nonce: str) -> None:
        """Record a nonce to prevent replay."""
        self._nonces.add(nonce)
        self._nonce_timestamps.append((time.time(), nonce))

        # Evict old nonces
        if len(self._nonces) > self.MAX_NONCES:
            cutoff = time.time() - self.MAX_TIMESTAMP_AGE * 2
            self._nonce_timestamps = [
                (t, n) for t, n in self._nonce_timestamps if t > cutoff
            ]
            self._nonces = {n for _, n in self._nonce_timestamps}

    # ── Logging ─────────────────────────────────────────────────────

    def _log_verification(
        self,
        provider: str,
        result: VerifyResult,
        source_ip: str = "",
        event_type: str = "",
        details: str = "",
    ) -> None:
        """Log a verification attempt."""
        record = VerificationRecord(
            timestamp=time.time(),
            provider=provider,
            result=result,
            source_ip=source_ip,
            event_type=event_type,
            details=details,
        )
        self._log.append(record)
        if len(self._log) > 5000:
            self._log = self._log[-5000:]

    # ── Status ──────────────────────────────────────────────────────

    def status(self) -> dict:
        """Get verifier status and stats."""
        return {
            "registered_providers": list(self._secrets.keys()),
            "stats": dict(self._stats),
            "nonce_cache_size": len(self._nonces),
            "recent_log": [r.to_dict() for r in self._log[-10:]],
        }

    def status_summary(self) -> str:
        """Human-readable status."""
        s = self._stats
        total = s["total"] or 1
        lines = [
            "╔══════════════════════════════════════╗",
            "║   WEBHOOK SIGNATURE VERIFIER         ║",
            "╠══════════════════════════════════════╣",
            f"║  Total Verified: {s['total']:<19}║",
            f"║  Valid:          {s['valid']:<8} ({s['valid']*100//total:>3}%)     ║",
            f"║  Invalid:        {s['invalid']:<8} ({s['invalid']*100//total:>3}%)     ║",
            f"║  Expired:        {s['expired']:<8} ({s['expired']*100//total:>3}%)     ║",
            f"║  Replay:         {s['replay']:<8} ({s['replay']*100//total:>3}%)     ║",
            "╠══════════════════════════════════════╣",
            f"║  Providers: {', '.join(self._secrets.keys()):<23}║",
            f"║  Nonce Cache: {len(self._nonces):<22}║",
            "╚══════════════════════════════════════╝",
        ]
        return "\n".join(lines)


# ── CLI Demo ────────────────────────────────────────────────────────

def main():
    """Demo webhook verification."""
    print("BlackRoad Webhook Signature Verifier")
    print("=" * 40)

    verifier = WebhookVerifier()

    # Register secrets
    verifier.register_secret("github", "test-secret-github")
    verifier.register_secret("stripe", "test-secret-stripe")
    verifier.register_secret("slack", "test-secret-slack")
    verifier.register_secret("generic", "test-secret-generic")

    # Test GitHub verification
    body = b'{"action": "opened", "pull_request": {"title": "test"}}'
    secret = "test-secret-github"
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

    result = verifier.verify(
        provider="github",
        headers={"X-Hub-Signature-256": sig, "X-GitHub-Event": "pull_request"},
        body=body,
        source_ip="140.82.115.0",
    )
    print(f"GitHub verify: {result.value}")

    # Test invalid signature
    result = verifier.verify(
        provider="github",
        headers={"X-Hub-Signature-256": "sha256=invalid"},
        body=body,
        source_ip="1.2.3.4",
    )
    print(f"Invalid sig:   {result.value}")

    # Test generic
    body2 = b'{"event": "test"}'
    sig2 = hmac.new(b"test-secret-generic", body2, hashlib.sha256).hexdigest()
    result = verifier.verify(
        provider="generic",
        headers={"X-Signature": sig2},
        body=body2,
    )
    print(f"Generic verify: {result.value}")

    print()
    print(verifier.status_summary())


if __name__ == "__main__":
    main()
