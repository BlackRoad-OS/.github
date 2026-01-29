#!/usr/bin/env python3
"""
BlackRoad MCP Server CLI

Usage:
    python -m blackroad_mcp                    # Run stdio server (for MCP clients)
    python -m blackroad_mcp --http             # Run HTTP server (for testing)
    python -m blackroad_mcp test               # Test tool calls
    python -m blackroad_mcp tools              # List available tools
    python -m blackroad_mcp resources          # List available resources
    python -m blackroad_mcp call <tool> [args] # Call a tool directly
"""

import sys
import json
import asyncio
import argparse
from typing import Optional

from .server import BlackRoadMCP


def cmd_stdio(args):
    """Run stdio transport (default MCP mode)."""
    from .transport import run_stdio

    # Suppress stderr output for clean MCP communication
    if not args.debug:
        sys.stderr = open('/dev/null', 'w')

    asyncio.run(run_stdio())


def cmd_http(args):
    """Run HTTP transport."""
    from .transport import run_http
    asyncio.run(run_http(host=args.host, port=args.port))


def cmd_tools(args):
    """List available tools."""
    server = BlackRoadMCP()

    print()
    print("  BLACKROAD MCP TOOLS")
    print("  " + "=" * 60)
    print()

    for tool in server.tools:
        print(f"  {tool.name}")
        print(f"    {tool.description[:70]}...")
        print()

    print(f"  Total: {len(server.tools)} tools")
    print()


def cmd_resources(args):
    """List available resources."""
    server = BlackRoadMCP()

    print()
    print("  BLACKROAD MCP RESOURCES")
    print("  " + "=" * 60)
    print()

    for res in server.resources:
        print(f"  {res.uri}")
        print(f"    {res.description}")
        print()

    print(f"  Total: {len(server.resources)} resources")
    print()


def cmd_call(args):
    """Call a tool directly."""
    server = BlackRoadMCP()

    # Parse arguments
    tool_args = {}
    if args.args:
        for arg in args.args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                # Try to parse as JSON
                try:
                    tool_args[key] = json.loads(value)
                except:
                    tool_args[key] = value
            else:
                # Positional argument for simple tools
                if args.tool == "route":
                    tool_args["query"] = arg
                elif args.tool == "dispatch":
                    tool_args["query"] = arg
                elif args.tool == "dispatch_to":
                    tool_args["org"] = arg
                elif args.tool == "get_node_config":
                    tool_args["node"] = arg

    print()
    print(f"  Calling: {args.tool}")
    if tool_args:
        print(f"  Args: {tool_args}")
    print()

    # Call the tool
    async def run():
        tool_map = {
            "route": server.tool_route,
            "dispatch": server.tool_dispatch,
            "dispatch_to": server.tool_dispatch_to,
            "health_check": server.tool_health_check,
            "list_orgs": server.tool_list_orgs,
            "list_routes": server.tool_list_routes,
            "process_webhook": server.tool_process_webhook,
            "get_signals": server.tool_get_signals,
            "get_node_config": server.tool_get_node_config,
        }

        if args.tool not in tool_map:
            print(f"  Unknown tool: {args.tool}")
            return

        result = await tool_map[args.tool](**tool_args)
        print("  Result:")
        print(json.dumps(result, indent=2))

    asyncio.run(run())
    print()


def cmd_test(args):
    """Run test suite."""
    server = BlackRoadMCP()

    print()
    print("  BLACKROAD MCP TEST SUITE")
    print("  " + "=" * 60)
    print()

    async def run_tests():
        tests = [
            ("route", {"query": "sync salesforce contacts"}),
            ("list_orgs", {}),
            ("list_routes", {"org": "FND"}),
            ("get_signals", {"limit": 5}),
            ("get_node_config", {"node": "lucidia"}),
        ]

        passed = 0
        failed = 0

        for tool_name, tool_args in tests:
            try:
                tool_map = {
                    "route": server.tool_route,
                    "list_orgs": server.tool_list_orgs,
                    "list_routes": server.tool_list_routes,
                    "get_signals": server.tool_get_signals,
                    "get_node_config": server.tool_get_node_config,
                }

                result = await tool_map[tool_name](**tool_args)

                if "error" in result:
                    print(f"  [FAIL] {tool_name}: {result['error']}")
                    failed += 1
                else:
                    print(f"  [PASS] {tool_name}")
                    if args.verbose:
                        print(f"         -> {json.dumps(result)[:80]}...")
                    passed += 1

            except Exception as e:
                print(f"  [FAIL] {tool_name}: {e}")
                failed += 1

        print()
        print(f"  Results: {passed} passed, {failed} failed")

    asyncio.run(run_tests())
    print()


def cmd_interactive(args):
    """Interactive mode for testing."""
    server = BlackRoadMCP()

    print()
    print("  BLACKROAD MCP - Interactive Mode")
    print("  " + "=" * 50)
    print()
    print("  Commands:")
    print("    route <query>        - Route a query")
    print("    dispatch <query>     - Dispatch a query")
    print("    orgs                 - List organizations")
    print("    routes [org]         - List routes")
    print("    health [org]         - Check health")
    print("    signals              - Get recent signals")
    print("    node <name>          - Get node config")
    print("    quit                 - Exit")
    print()

    async def run():
        while True:
            try:
                cmd = input("  mcp> ").strip()

                if not cmd:
                    continue

                parts = cmd.split(maxsplit=1)
                action = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if action in ("quit", "exit", "q"):
                    print("  Goodbye!")
                    break
                elif action == "route" and arg:
                    result = await server.tool_route(arg)
                    print(f"  -> {result.get('org_code', 'Unknown')}: {result.get('category', 'N/A')}")
                    print(f"     Confidence: {result.get('confidence', 0):.2f}")
                elif action == "dispatch" and arg:
                    result = await server.tool_dispatch(arg)
                    print(f"  -> {result.get('org_code')}.{result.get('service')}")
                elif action == "orgs":
                    result = await server.tool_list_orgs()
                    for org in result.get("orgs", []):
                        print(f"  [{org['code']}] {org['name']}")
                elif action == "routes":
                    result = await server.tool_list_routes(arg or None)
                    for route in result.get("routes", [])[:10]:
                        print(f"  {route['org']}.{route['service']} -> {route['endpoint'][:40]}")
                elif action == "health":
                    result = await server.tool_health_check(arg or None)
                    if "health" in result:
                        for org, services in result["health"].items():
                            print(f"  [{org}]")
                            for svc, status in services.items():
                                emoji = "🟢" if status == "healthy" else "🔴"
                                print(f"    {emoji} {svc}: {status}")
                    else:
                        print(f"  {arg}: {result.get('status', 'unknown')}")
                elif action == "signals":
                    result = await server.tool_get_signals(limit=10)
                    for sig in result.get("signals", []):
                        print(f"  [{sig.get('timestamp', '')[:19]}] {sig.get('type', 'unknown')}")
                elif action == "node" and arg:
                    result = await server.tool_get_node_config(arg)
                    if "error" in result:
                        print(f"  Error: {result['error']}")
                    else:
                        config = result.get("config", {})
                        node = config.get("node", {})
                        print(f"  {node.get('name', arg)}: {node.get('role', 'unknown')}")
                elif action == "help":
                    print("  Available commands:")
                    print("    route <query>        - Route a query to an org")
                    print("    dispatch <query>     - Dispatch to a service")
                    print("    orgs                 - List organizations")
                    print("    routes [org]         - List routes")
                    print("    health [org]         - Check health")
                    print("    signals              - Get recent signals")
                    print("    node <name>          - Get node config")
                    print("    help                 - Show this help")
                    print("    quit                 - Exit")
                else:
                    print(f"  Unknown command: {action}. Type 'help' for available commands.")

            except (EOFError, KeyboardInterrupt):
                print("\n  Goodbye!")
                break

    asyncio.run(run())


def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Run stdio server (for MCP clients)
  %(prog)s --http --port 8090        # Run HTTP server
  %(prog)s tools                     # List available tools
  %(prog)s resources                 # List available resources
  %(prog)s call route "sync salesforce"  # Call a tool
  %(prog)s test --verbose            # Run tests
  %(prog)s interactive               # Interactive mode

MCP Client Configuration:
  Add to your MCP client config:

  {
    "mcpServers": {
      "blackroad": {
        "command": "python",
        "args": ["-m", "blackroad_mcp"],
        "cwd": "/path/to/prototypes/mcp-server"
      }
    }
  }
        """,
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    subparsers = parser.add_subparsers(dest="command")

    # HTTP mode
    http_parser = parser.add_argument_group("HTTP mode")
    parser.add_argument("--http", action="store_true", help="Run HTTP server instead of stdio")
    parser.add_argument("--host", default="localhost", help="HTTP host (default: localhost)")
    parser.add_argument("--port", type=int, default=8090, help="HTTP port (default: 8090)")

    # Tools
    subparsers.add_parser("tools", help="List available tools")

    # Resources
    subparsers.add_parser("resources", help="List available resources")

    # Call
    call_parser = subparsers.add_parser("call", help="Call a tool")
    call_parser.add_argument("tool", help="Tool name")
    call_parser.add_argument("args", nargs="*", help="Tool arguments (key=value)")

    # Test
    test_parser = subparsers.add_parser("test", help="Run test suite")
    test_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # Interactive
    subparsers.add_parser("interactive", help="Interactive mode")

    args = parser.parse_args()

    if args.command == "tools":
        cmd_tools(args)
    elif args.command == "resources":
        cmd_resources(args)
    elif args.command == "call":
        cmd_call(args)
    elif args.command == "test":
        cmd_test(args)
    elif args.command == "interactive":
        cmd_interactive(args)
    elif args.http:
        cmd_http(args)
    else:
        # Default: stdio mode
        cmd_stdio(args)


if __name__ == "__main__":
    main()
