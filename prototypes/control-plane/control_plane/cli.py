"""
BlackRoad Control Plane CLI

The unified command interface for the Bridge.

Usage:
    python -m control_plane.cli status      # Quick status
    python -m control_plane.cli dashboard   # Full dashboard
    python -m control_plane.cli route       # Route a query
    python -m control_plane.cli browse      # Browse ecosystem
    python -m control_plane.cli orgs        # List organizations
    python -m control_plane.cli templates   # List templates
    python -m control_plane.cli signal      # Emit a signal
    python -m control_plane.cli search      # Search ecosystem
"""

import sys
import argparse
from .bridge import get_bridge


def cmd_status(args):
    """Show quick status."""
    bridge = get_bridge()
    print(bridge.status())


def cmd_dashboard(args):
    """Show full dashboard."""
    bridge = get_bridge()
    print(bridge.dashboard())


def cmd_route(args):
    """Route a query."""
    bridge = get_bridge()

    if args.query:
        query = " ".join(args.query)
    else:
        print("Enter query (Ctrl+D to finish):")
        query = sys.stdin.read().strip()

    if not query:
        print("No query provided")
        return

    result = bridge.route(query)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print()
    print(f"  Query:       {query[:50]}{'...' if len(query) > 50 else ''}")
    print(f"  Destination: {result['destination']}")
    print(f"  Org:         {result['org']}")
    print(f"  Category:    {result['category']}")
    print(f"  Confidence:  {result['confidence']:.0%}")
    print()
    if result.get('signal'):
        print(f"  Signal: {result['signal']}")
    print()


def cmd_browse(args):
    """Browse the ecosystem."""
    bridge = get_bridge()
    path = args.path if args.path else ""
    print(bridge.browse(path))


def cmd_orgs(args):
    """List organizations."""
    bridge = get_bridge()
    orgs = bridge.list_orgs()

    print()
    print("  BLACKROAD ORGANIZATIONS")
    print("  " + "=" * 50)
    print()

    for org in orgs:
        status = "ACTIVE" if "BlackRoad-OS" in org['name'] else "PLANNED"
        print(f"  [{status:7}] {org['name']}")
        print(f"            {org['mission'][:60]}")
        print()

    print(f"  Total: {len(orgs)} organizations")
    print()


def cmd_templates(args):
    """List templates."""
    bridge = get_bridge()
    templates = bridge.list_templates()

    print()
    print("  BLACKROAD TEMPLATES")
    print("  " + "=" * 50)
    print()

    for tmpl in templates:
        print(f"  {tmpl['name']}")
        print(f"    {tmpl['description'][:60]}")
        print()

    print(f"  Total: {len(templates)} templates")
    print()


def cmd_signal(args):
    """Emit a signal."""
    bridge = get_bridge()

    message = " ".join(args.message) if args.message else "ping"
    target = args.target if args.target else "OS"

    result = bridge.signal(message, target)
    print(result)


def cmd_search(args):
    """Search the ecosystem."""
    bridge = get_bridge()

    query = " ".join(args.query) if args.query else ""
    if not query:
        print("Usage: search <query>")
        return

    results = bridge.search(query)

    print()
    print(f"  Search: {query}")
    print("  " + "-" * 40)
    print()

    if not results:
        print("  No results found")
    else:
        for r in results[:20]:  # Limit to 20
            print(f"  [{r['type']:6}] {r['path']}")

    print()
    print(f"  Found: {len(results)} results")
    print()


def cmd_interactive(args):
    """Interactive mode."""
    bridge = get_bridge()

    print()
    print("  BLACKROAD CONTROL PLANE")
    print("  " + "=" * 40)
    print()
    print("  Commands: status, dashboard, route, browse, orgs, templates, signal, search, quit")
    print()

    while True:
        try:
            cmd = input("  bridge> ").strip().lower()

            if not cmd:
                continue
            elif cmd in ("quit", "exit", "q"):
                print("  Goodbye!")
                break
            elif cmd == "status":
                print(bridge.status())
            elif cmd == "dashboard":
                print(bridge.dashboard())
            elif cmd == "orgs":
                cmd_orgs(args)
            elif cmd == "templates":
                cmd_templates(args)
            elif cmd.startswith("route "):
                query = cmd[6:]
                result = bridge.route(query)
                if "error" not in result:
                    print(f"  -> {result['org']} ({result['confidence']:.0%})")
            elif cmd.startswith("browse"):
                path = cmd[7:].strip() if len(cmd) > 6 else ""
                print(bridge.browse(path))
            elif cmd.startswith("search "):
                query = cmd[7:]
                results = bridge.search(query)
                for r in results[:10]:
                    print(f"  {r['path']}")
            elif cmd.startswith("signal "):
                msg = cmd[7:]
                print(bridge.signal(msg))
            else:
                print(f"  Unknown command: {cmd}")
                print("  Try: status, dashboard, route, browse, orgs, templates, signal, search, quit")

        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad Control Plane",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status              Show quick status
  %(prog)s dashboard           Show full dashboard
  %(prog)s route "help me"     Route a query
  %(prog)s browse orgs/        Browse ecosystem
  %(prog)s orgs                List organizations
  %(prog)s templates           List templates
  %(prog)s signal "ping"       Emit a signal
  %(prog)s search "salesforce" Search ecosystem
  %(prog)s                     Interactive mode
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # Status
    subparsers.add_parser("status", help="Show quick status")

    # Dashboard
    subparsers.add_parser("dashboard", help="Show full dashboard")

    # Route
    route_parser = subparsers.add_parser("route", help="Route a query")
    route_parser.add_argument("query", nargs="*", help="Query to route")

    # Browse
    browse_parser = subparsers.add_parser("browse", help="Browse ecosystem")
    browse_parser.add_argument("path", nargs="?", default="", help="Path to browse")

    # Orgs
    subparsers.add_parser("orgs", help="List organizations")

    # Templates
    subparsers.add_parser("templates", help="List templates")

    # Signal
    signal_parser = subparsers.add_parser("signal", help="Emit a signal")
    signal_parser.add_argument("message", nargs="*", help="Signal message")
    signal_parser.add_argument("-t", "--target", default="OS", help="Target org")

    # Search
    search_parser = subparsers.add_parser("search", help="Search ecosystem")
    search_parser.add_argument("query", nargs="*", help="Search query")

    args = parser.parse_args()

    # Dispatch
    if args.command == "status":
        cmd_status(args)
    elif args.command == "dashboard":
        cmd_dashboard(args)
    elif args.command == "route":
        cmd_route(args)
    elif args.command == "browse":
        cmd_browse(args)
    elif args.command == "orgs":
        cmd_orgs(args)
    elif args.command == "templates":
        cmd_templates(args)
    elif args.command == "signal":
        cmd_signal(args)
    elif args.command == "search":
        cmd_search(args)
    else:
        # No command - interactive mode
        cmd_interactive(args)


if __name__ == "__main__":
    main()
