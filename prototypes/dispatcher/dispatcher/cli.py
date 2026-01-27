#!/usr/bin/env python3
"""
Dispatcher CLI

Route requests to services from the command line.

Usage:
    python -m dispatcher dispatch "sync salesforce contacts"
    python -m dispatcher dispatch-to FND salesforce --data '{"action": "sync"}'
    python -m dispatcher routes
    python -m dispatcher health
    python -m dispatcher ping FND.salesforce
"""

import asyncio
import argparse
import json
from typing import Optional


def run_async(coro):
    """Run an async function."""
    return asyncio.get_event_loop().run_until_complete(coro)


async def cmd_dispatch(args):
    """Dispatch a query."""
    from .core import Dispatcher

    dispatcher = Dispatcher(mock=args.mock)

    print()
    print(f"  Query: {args.query[:60]}{'...' if len(args.query) > 60 else ''}")
    print()

    data = json.loads(args.data) if args.data else None

    result = await dispatcher.dispatch(args.query, data=data)

    print()
    if result.success:
        print(f"  Routed to: {result.org} ({result.org_code})")
        print(f"  Service:   {result.service}")
        print(f"  Endpoint:  {result.endpoint}")
        print(f"  Latency:   {result.latency_ms}ms")
        if result.response and result.response.data:
            print()
            print("  Response:")
            response_str = json.dumps(result.response.data, indent=2)
            for line in response_str.split("\n")[:20]:
                print(f"    {line}")
    else:
        print(f"  Error: {result.error}")

    print()
    await dispatcher.close()


async def cmd_dispatch_to(args):
    """Dispatch to specific org/service."""
    from .core import Dispatcher

    dispatcher = Dispatcher(mock=args.mock)

    print()
    print(f"  Target: {args.org}.{args.service or 'default'}")

    data = json.loads(args.data) if args.data else None

    result = await dispatcher.dispatch_to(args.org, args.service, data=data)

    print()
    if result.success:
        print(f"  Service:  {result.service}")
        print(f"  Endpoint: {result.endpoint}")
        print(f"  Latency:  {result.latency_ms}ms")
        if result.response and result.response.data:
            print()
            print("  Response:")
            response_str = json.dumps(result.response.data, indent=2)
            for line in response_str.split("\n")[:20]:
                print(f"    {line}")
    else:
        print(f"  Error: {result.error}")

    print()
    await dispatcher.close()


def cmd_routes(args):
    """List all routes."""
    from .core import Dispatcher

    dispatcher = Dispatcher()

    print()
    print("  BLACKROAD ROUTES")
    print("  " + "=" * 60)
    print()

    routes = dispatcher.list_routes()

    current_org = None
    for route in routes:
        if route["org"] != current_org:
            current_org = route["org"]
            print(f"  [{route['org']}] {route['org_name']}")

        type_badge = "ext" if route["type"] == "external" else "int"
        print(f"    └─ {route['service']:15} [{type_badge}] {route['endpoint'][:40]}")

    print()
    print(f"  Total: {len(routes)} routes across {len(set(r['org'] for r in routes))} orgs")
    print()


async def cmd_health(args):
    """Check health of all services."""
    from .core import Dispatcher
    from .client import ServiceStatus

    dispatcher = Dispatcher()

    print()
    print("  SERVICE HEALTH")
    print("  " + "=" * 50)
    print()

    if args.org:
        # Check specific org
        org = dispatcher.registry.get_org(args.org)
        if not org:
            print(f"  Unknown org: {args.org}")
            return

        for name, service in org.services.items():
            status = await dispatcher.health_check(args.org, name)
            emoji = "🟢" if status == ServiceStatus.HEALTHY else "🟡" if status == ServiceStatus.DEGRADED else "🔴" if status == ServiceStatus.UNHEALTHY else "⚪"
            print(f"  {emoji} {args.org}.{name:15} {status.value}")
    else:
        # Check all
        results = await dispatcher.health_check_all()
        for org_code, services in results.items():
            print(f"  [{org_code}]")
            for name, status in services.items():
                emoji = "🟢" if status == ServiceStatus.HEALTHY else "🟡" if status == ServiceStatus.DEGRADED else "🔴" if status == ServiceStatus.UNHEALTHY else "⚪"
                print(f"    {emoji} {name:15} {status.value}")

    print()
    await dispatcher.close()


async def cmd_ping(args):
    """Ping a service."""
    from .core import Dispatcher

    dispatcher = Dispatcher()

    # Parse org.service
    parts = args.target.split(".")
    org_code = parts[0]
    service_name = parts[1] if len(parts) > 1 else None

    endpoint = dispatcher.registry.get_endpoint(org_code, service_name)

    if not endpoint:
        print(f"  Unknown target: {args.target}")
        return

    print()
    print(f"  Pinging: {args.target}")
    print(f"  Endpoint: {endpoint}")

    reachable, latency = await dispatcher.client.ping(endpoint)

    if reachable:
        print(f"  Result: 🟢 Reachable ({latency}ms)")
    else:
        print(f"  Result: 🔴 Unreachable")

    print()
    await dispatcher.close()


def cmd_interactive(args):
    """Interactive mode."""
    from .core import Dispatcher

    dispatcher = Dispatcher(mock=args.mock)

    print()
    print("  BLACKROAD DISPATCHER - Interactive Mode")
    print("  " + "=" * 50)
    print()
    print("  Commands:")
    print("    <query>           - Dispatch a query")
    print("    /to ORG [SVC]     - Dispatch to specific org/service")
    print("    /routes           - List all routes")
    print("    /health           - Check health")
    print("    /quit             - Exit")
    print()

    while True:
        try:
            query = input("  dispatch> ").strip()

            if not query:
                continue

            if query.startswith("/"):
                parts = query[1:].split()
                cmd = parts[0].lower()

                if cmd in ("quit", "exit", "q"):
                    print("  Goodbye!")
                    break
                elif cmd == "routes":
                    cmd_routes(args)
                elif cmd == "health":
                    run_async(cmd_health(args))
                elif cmd == "to" and len(parts) >= 2:
                    org = parts[1]
                    service = parts[2] if len(parts) > 2 else None
                    result = run_async(dispatcher.dispatch_to(org, service))
                    if result.success:
                        print(f"  -> {result.org}.{result.service}")
                    else:
                        print(f"  Error: {result.error}")
                else:
                    print(f"  Unknown command: {cmd}")
                continue

            # Dispatch the query
            result = run_async(dispatcher.dispatch(query))

            if result.success:
                print(f"  -> {result.org}.{result.service} ({result.latency_ms}ms)")
            else:
                print(f"  Error: {result.error}")

        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

    run_async(dispatcher.close())


def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad Dispatcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s dispatch "sync salesforce contacts"
  %(prog)s dispatch-to FND salesforce
  %(prog)s routes
  %(prog)s health
  %(prog)s health --org FND
  %(prog)s ping FND.salesforce
  %(prog)s interactive
        """
    )

    parser.add_argument("--mock", action="store_true", help="Use mock client")

    subparsers = parser.add_subparsers(dest="command")

    # Dispatch
    dispatch_parser = subparsers.add_parser("dispatch", help="Dispatch a query")
    dispatch_parser.add_argument("query", help="Query to dispatch")
    dispatch_parser.add_argument("--data", "-d", help="JSON data to send")
    dispatch_parser.add_argument("--mock", action="store_true")

    # Dispatch-to
    dispatch_to_parser = subparsers.add_parser("dispatch-to", help="Dispatch to specific org/service")
    dispatch_to_parser.add_argument("org", help="Org code (e.g., FND)")
    dispatch_to_parser.add_argument("service", nargs="?", help="Service name")
    dispatch_to_parser.add_argument("--data", "-d", help="JSON data to send")
    dispatch_to_parser.add_argument("--mock", action="store_true")

    # Routes
    subparsers.add_parser("routes", help="List all routes")

    # Health
    health_parser = subparsers.add_parser("health", help="Check service health")
    health_parser.add_argument("--org", help="Specific org to check")

    # Ping
    ping_parser = subparsers.add_parser("ping", help="Ping a service")
    ping_parser.add_argument("target", help="Target (e.g., FND.salesforce)")

    # Interactive
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    interactive_parser.add_argument("--mock", action="store_true")

    args = parser.parse_args()

    if args.command == "dispatch":
        run_async(cmd_dispatch(args))
    elif args.command == "dispatch-to":
        run_async(cmd_dispatch_to(args))
    elif args.command == "routes":
        cmd_routes(args)
    elif args.command == "health":
        run_async(cmd_health(args))
    elif args.command == "ping":
        run_async(cmd_ping(args))
    elif args.command == "interactive":
        cmd_interactive(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
