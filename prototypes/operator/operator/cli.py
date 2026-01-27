#!/usr/bin/env python3
"""
BlackRoad Operator CLI

Usage:
    python -m operator.cli "What is the weather?"
    python -m operator.cli --explain "Update customer record"
    python -m operator.cli --stats
"""

import sys
import argparse
from .core.router import Operator


def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad Operator - Route requests to the right destination"
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="The query to route"
    )

    parser.add_argument(
        "-e", "--explain",
        action="store_true",
        help="Show detailed explanation of routing"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show routing statistics"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode"
    )

    args = parser.parse_args()

    # Create operator
    op = Operator()

    # Handle different modes
    if args.stats:
        print("Routing Statistics:")
        print(f"  Total routes: {op.stats['total']}")
        return

    if args.interactive:
        interactive_mode(op)
        return

    if not args.query:
        parser.print_help()
        return

    # Route the query
    if args.explain:
        print(op.explain(args.query))
    else:
        result = op.route(args.query)

        if args.verbose:
            print(f"Query: {result.request.query}")
            print(f"Classification: {result.classification.category}")
            print(f"Destination: {result.org}")
            print(f"Confidence: {result.confidence:.1%}")
            print(f"Signal: {result.signal}")
        else:
            print(f"→ {result.org} ({result.confidence:.0%})")
            print(f"  {result.signal}")


def interactive_mode(op: Operator):
    """Interactive routing mode."""
    print("BlackRoad Operator - Interactive Mode")
    print("Type 'quit' to exit, 'stats' for statistics")
    print("-" * 40)

    while True:
        try:
            query = input("\n🎯 > ").strip()

            if not query:
                continue

            if query.lower() in ("quit", "exit", "q"):
                print("👋 Goodbye!")
                break

            if query.lower() == "stats":
                stats = op.stats
                print(f"\n📊 Statistics:")
                print(f"   Total routes: {stats['total']}")
                print(f"   By org: {stats['by_org']}")
                print(f"   Avg confidence: {stats['avg_confidence']:.1%}")
                continue

            if query.lower() == "help":
                print("\nCommands:")
                print("  <query>  - Route a query")
                print("  stats    - Show statistics")
                print("  quit     - Exit")
                continue

            # Route the query
            result = op.route(query)
            print(f"\n   {result.signal}")
            print(f"   → {result.org} ({result.confidence:.0%})")
            print(f"   Category: {result.classification.category}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
