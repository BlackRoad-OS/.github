# BlackRoad Webhook Receiver

Central webhook processing system for the BlackRoad mesh. Receives inbound webhooks from external providers, converts them to internal signals, and dispatches them to the appropriate org.

## Quick Start

```bash
# Run the webhook receiver
python -m webhooks

# Or import directly
python -c "from webhooks import WebhookReceiver; print('ready')"
```

## Supported Providers

| Provider | Events |
|----------|--------|
| GitHub | Push, PR, issues, actions |
| Salesforce | Record changes, triggers |
| Stripe | Payments, subscriptions |
| Cloudflare | Worker events, alerts |
| Slack | Commands, events |
| Google | Drive changes, calendar |
| Figma | Design updates, comments |

## How It Works

```
External Service → Webhook HTTP POST → WebhookReceiver → Signal → Dispatcher → Org
```

1. **Receive** — Inbound HTTP POST with provider-specific payload
2. **Identify** — Detect the provider from headers/payload
3. **Handle** — Provider-specific handler parses the payload
4. **Signal** — Convert to a typed `Signal` with source, type, and data
5. **Dispatch** — Route the signal to the appropriate org

## Core Components

| Module | Purpose |
|--------|---------|
| `receiver.py` | Central `WebhookReceiver` class and routing logic |
| `signal.py` | `Signal` and `SignalType` definitions |
| `handlers/` | Per-provider webhook handlers |
| `cli.py` | CLI for running the receiver and inspecting signals |

## Usage

```python
from webhooks import WebhookReceiver

receiver = WebhookReceiver()
result = await receiver.process(request)
# → WebhookResult(success=True, signal=Signal(type=payment_received, source=stripe, ...))
```

## Signals

```
📨 OS → OS : webhook_received, provider=github, event=push
💰 FND → OS : payment_received, customer=cus_xxx, amount=$100
🔀 OS → OS : pr_opened, repo=operator, number=42
⚠️ OS → OS : webhook_failed, provider=stripe, error="invalid signature"
```
