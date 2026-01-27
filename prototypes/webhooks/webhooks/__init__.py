"""
BlackRoad Webhook Receiver

Catch inbound signals from everywhere.

Supported providers:
- GitHub (push, PR, issues, actions)
- Salesforce (record changes, triggers)
- Stripe (payments, subscriptions)
- Cloudflare (worker events, alerts)
- Slack (commands, events)
- Custom (any JSON webhook)

Usage:
    from webhooks import WebhookReceiver

    receiver = WebhookReceiver()
    signal = await receiver.process(request)
    # → Signal(type=payment_received, source=stripe, data={...})
"""

__version__ = "0.1.0"

from .receiver import WebhookReceiver, WebhookResult, process_webhook
from .signal import Signal, SignalType

__all__ = [
    "WebhookReceiver",
    "WebhookResult",
    "process_webhook",
    "Signal",
    "SignalType",
]
