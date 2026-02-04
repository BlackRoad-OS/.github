# Webhook Signature Verification

> **Trust nothing. Verify everything.**

Verifies the authenticity of incoming webhooks from GitHub, Stripe,
Slack, Salesforce, and other providers using HMAC signatures,
timestamps, and replay protection.

## Architecture

```
[Incoming Webhook]
        │
        ├── headers (signature, timestamp)
        ├── body (raw payload)
        │
        ▼
[Signature Verifier]
        │
        ├── 1. Check timestamp freshness (anti-replay)
        ├── 2. Compute expected HMAC
        ├── 3. Constant-time compare
        ├── 4. Log verification result
        └── 5. Accept or reject
```

## Supported Providers

| Provider | Signature Header | Algorithm |
|----------|-----------------|-----------|
| GitHub | `X-Hub-Signature-256` | HMAC-SHA256 |
| Stripe | `Stripe-Signature` | HMAC-SHA256 with timestamp |
| Slack | `X-Slack-Signature` | HMAC-SHA256 with timestamp |
| Salesforce | Custom header | HMAC-SHA256 |
| Generic | `X-Signature` | Configurable |

## Files

| File | Purpose |
|------|---------|
| `verifier.py` | Core verification engine with provider support |
