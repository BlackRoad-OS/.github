#!/usr/bin/env python3
"""
Webhook CLI - Test and simulate webhooks.

Usage:
    python -m webhooks simulate github push
    python -m webhooks simulate stripe payment_intent.succeeded
    python -m webhooks handlers
    python -m webhooks server --port 8080
"""

import argparse
import json
import sys
from typing import Dict, Any

from .receiver import WebhookReceiver, process_webhook
from .signal import SignalType


# Sample webhook payloads for testing
SAMPLE_WEBHOOKS: Dict[str, Dict[str, Any]] = {
    "github.push": {
        "headers": {
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": "sha256=test",
        },
        "body": {
            "ref": "refs/heads/main",
            "repository": {
                "full_name": "BlackRoad-OS/.github",
            },
            "sender": {"login": "alexa"},
            "head_commit": {
                "message": "Add webhook receiver",
            },
            "commits": [{"id": "abc123"}],
        },
    },
    "github.pull_request": {
        "headers": {
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": "sha256=test",
        },
        "body": {
            "action": "opened",
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "sender": {"login": "alexa"},
            "pull_request": {
                "number": 42,
                "title": "Add new feature",
                "merged": False,
            },
        },
    },
    "github.workflow_run": {
        "headers": {
            "X-GitHub-Event": "workflow_run",
            "X-Hub-Signature-256": "sha256=test",
        },
        "body": {
            "action": "completed",
            "repository": {"full_name": "BlackRoad-OS/.github"},
            "sender": {"login": "github-actions[bot]"},
            "workflow_run": {
                "name": "CI",
                "status": "completed",
                "conclusion": "success",
            },
        },
    },
    "stripe.payment_intent.succeeded": {
        "headers": {
            "Stripe-Signature": "t=1234567890,v1=test",
        },
        "body": {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_123",
                    "amount": 10000,
                    "currency": "usd",
                    "customer": "cus_123",
                    "status": "succeeded",
                },
            },
        },
    },
    "stripe.subscription.created": {
        "headers": {
            "Stripe-Signature": "t=1234567890,v1=test",
        },
        "body": {
            "type": "customer.subscription.created",
            "data": {
                "object": {
                    "id": "sub_123",
                    "customer": "cus_123",
                    "status": "active",
                    "plan": {
                        "id": "plan_pro",
                        "amount": 4900,
                    },
                },
            },
        },
    },
    "salesforce.lead_created": {
        "headers": {
            "Content-Type": "application/json",
        },
        "body": {
            "sObjectType": "Lead",
            "Id": "00Q123456789",
            "Name": "John Doe",
            "Email": "john@example.com",
            "Company": "Acme Inc",
            "Status": "Open",
            "ChangeEventHeader": {"changeType": "create"},
        },
    },
    "salesforce.opportunity_won": {
        "headers": {
            "Content-Type": "application/json",
        },
        "body": {
            "sObjectType": "Opportunity",
            "Id": "006123456789",
            "Name": "Big Deal",
            "StageName": "Closed Won",
            "Amount": 50000,
            "AccountId": "001123456789",
            "CloseDate": "2024-01-15",
        },
    },
    "cloudflare.worker_deployed": {
        "headers": {
            "CF-Webhook-Auth": "test-token",
        },
        "body": {
            "data": {
                "alert_type": "workers_alert_deployment_success",
                "deployment": {
                    "script_name": "api-worker",
                    "environment": "production",
                    "version_id": "v123",
                },
            },
            "account_id": "abc123",
        },
    },
    "slack.message": {
        "headers": {
            "X-Slack-Signature": "v0=test",
            "X-Slack-Request-Timestamp": "1234567890",
        },
        "body": {
            "type": "event_callback",
            "team_id": "T123",
            "event": {
                "type": "message",
                "channel": "C123",
                "user": "U123",
                "text": "Hello, BlackRoad!",
                "ts": "1234567890.123456",
            },
        },
    },
    "slack.app_mention": {
        "headers": {
            "X-Slack-Signature": "v0=test",
            "X-Slack-Request-Timestamp": "1234567890",
        },
        "body": {
            "type": "event_callback",
            "team_id": "T123",
            "event": {
                "type": "app_mention",
                "channel": "C123",
                "user": "U123",
                "text": "<@U456> deploy to production",
                "ts": "1234567890.123456",
            },
            "authorizations": [{"user_id": "U456"}],
        },
    },
    "figma.file_update": {
        "headers": {
            "X-Figma-Signature": "test",
        },
        "body": {
            "event_type": "FILE_UPDATE",
            "file_key": "abc123",
            "file_name": "App Design",
            "timestamp": "2024-01-15T12:00:00Z",
            "webhook_id": "wh_123",
            "triggered_by": {"handle": "designer"},
        },
    },
    "figma.comment": {
        "headers": {
            "X-Figma-Signature": "test",
        },
        "body": {
            "event_type": "FILE_COMMENT",
            "file_key": "abc123",
            "file_name": "App Design",
            "comment_id": "comment_123",
            "comment": [{"text": "Can we make this button bigger?"}],
            "triggered_by": {"handle": "reviewer"},
        },
    },
}


def cmd_simulate(args):
    """Simulate a webhook."""
    webhook_key = f"{args.provider}.{args.event}"

    if webhook_key not in SAMPLE_WEBHOOKS:
        print(f"\n  Unknown webhook: {webhook_key}")
        print(f"\n  Available webhooks:")
        for key in sorted(SAMPLE_WEBHOOKS.keys()):
            print(f"    - {key}")
        print()
        return

    sample = SAMPLE_WEBHOOKS[webhook_key]
    headers = sample["headers"]
    body = json.dumps(sample["body"]).encode()

    print()
    print(f"  SIMULATING: {webhook_key}")
    print("  " + "=" * 50)
    print()

    # Process the webhook
    result = process_webhook(headers, body)

    if result.success and result.signal:
        print(f"  Handler:  {result.handler}")
        print(f"  Verified: {'Yes' if result.verified else 'No (no secret)'}")
        print(f"  Time:     {result.processing_time_ms}ms")
        print()
        print(f"  Signal:")
        print(f"    {result.signal.format()}")
        print()
        print(f"  Signal Data:")
        for key, value in result.signal.data.items():
            print(f"    {key}: {value}")
    else:
        print(f"  Error: {result.error}")

    print()


def cmd_handlers(args):
    """List available handlers."""
    receiver = WebhookReceiver()

    print()
    print("  WEBHOOK HANDLERS")
    print("  " + "=" * 50)
    print()

    for handler in receiver.handlers:
        print(f"  [{handler.name.upper():12}] -> {handler.target_org}")

    print()
    print(f"  Total: {len(receiver.handlers)} handlers")
    print()


def cmd_signal_types(args):
    """List all signal types."""
    print()
    print("  SIGNAL TYPES")
    print("  " + "=" * 50)
    print()

    current_category = None
    for sig_type in SignalType:
        # Group by category based on naming
        name = sig_type.value
        if "_" in name:
            category = name.split("_")[0].upper()
        else:
            category = "GENERAL"

        if category != current_category:
            current_category = category
            print(f"\n  [{category}]")

        print(f"    {sig_type.value}")

    print()


def cmd_test(args):
    """Run all sample webhooks as a test."""
    receiver = WebhookReceiver()

    print()
    print("  WEBHOOK TEST SUITE")
    print("  " + "=" * 50)
    print()

    passed = 0
    failed = 0

    for webhook_key, sample in sorted(SAMPLE_WEBHOOKS.items()):
        headers = sample["headers"]
        body = json.dumps(sample["body"]).encode()

        result = receiver.process(headers, body)

        if result.success:
            passed += 1
            status = "PASS"
            signal_str = result.signal.format() if result.signal else ""
        else:
            failed += 1
            status = "FAIL"
            signal_str = result.error or ""

        print(f"  [{status}] {webhook_key}")
        if args.verbose:
            print(f"         -> {signal_str}")

    print()
    print(f"  Results: {passed} passed, {failed} failed")
    print()

    # Print stats
    if args.verbose:
        stats = receiver.stats
        print("  Statistics:")
        print(f"    Total processed: {stats['total']}")
        print(f"    Success rate: {stats['success_rate']*100:.1f}%")
        print(f"    Avg processing: {stats['avg_processing_ms']:.1f}ms")
        print()


def cmd_serve(args):
    """Start a webhook server (requires aiohttp)."""
    try:
        import asyncio
        from aiohttp import web
    except ImportError:
        print("\n  Error: aiohttp is required for server mode")
        print("  Install with: pip install aiohttp")
        print()
        return

    receiver = WebhookReceiver()

    async def handle_webhook(request: web.Request) -> web.Response:
        """Handle incoming webhook."""
        try:
            headers = dict(request.headers)
            body = await request.read()

            result = receiver.process(headers, body)

            if result.success and result.signal:
                print(f"  {result.signal.format()}")

            return web.json_response(result.to_dict())

        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_health(request: web.Request) -> web.Response:
        """Health check endpoint."""
        return web.json_response({"status": "healthy", "handlers": len(receiver.handlers)})

    async def handle_stats(request: web.Request) -> web.Response:
        """Stats endpoint."""
        return web.json_response(receiver.stats)

    app = web.Application()
    app.router.add_post("/webhook", handle_webhook)
    app.router.add_post("/webhook/{provider}", handle_webhook)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/stats", handle_stats)

    print()
    print("  WEBHOOK SERVER")
    print("  " + "=" * 50)
    print()
    print(f"  Listening on port {args.port}")
    print()
    print("  Endpoints:")
    print("    POST /webhook          - Receive any webhook")
    print("    POST /webhook/{provider} - Receive with hint")
    print("    GET  /health           - Health check")
    print("    GET  /stats            - Processing stats")
    print()

    web.run_app(app, port=args.port, print=None)


def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad Webhook CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s simulate github push
  %(prog)s simulate stripe payment_intent.succeeded
  %(prog)s simulate salesforce lead_created
  %(prog)s handlers
  %(prog)s types
  %(prog)s test --verbose
  %(prog)s serve --port 8080
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # Simulate
    sim_parser = subparsers.add_parser("simulate", help="Simulate a webhook")
    sim_parser.add_argument("provider", help="Provider (github, stripe, etc.)")
    sim_parser.add_argument("event", help="Event type (push, payment_intent.succeeded, etc.)")

    # Handlers
    subparsers.add_parser("handlers", help="List webhook handlers")

    # Signal types
    subparsers.add_parser("types", help="List signal types")

    # Test
    test_parser = subparsers.add_parser("test", help="Run test suite")
    test_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # Serve
    serve_parser = subparsers.add_parser("serve", help="Start webhook server")
    serve_parser.add_argument("--port", "-p", type=int, default=8080, help="Port to listen on")

    args = parser.parse_args()

    if args.command == "simulate":
        cmd_simulate(args)
    elif args.command == "handlers":
        cmd_handlers(args)
    elif args.command == "types":
        cmd_signal_types(args)
    elif args.command == "test":
        cmd_test(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
