#!/usr/bin/env python3
"""
BlackRoad Explorer CLI

Navigate the ecosystem from your terminal.

Usage:
    python -m explorer.cli orgs
    python -m explorer.cli org AI
    python -m explorer.cli browse
"""

import sys
import argparse
from .browser import Explorer


def cmd_orgs(exp: Explorer, args):
    """List all organizations."""
    print(exp.format_list())


def cmd_org(exp: Explorer, args):
    """Show org details."""
    if not args.code:
        print("Usage: explorer org <CODE>")
        print("Example: explorer org AI")
        return
    print(exp.format_org(args.code.upper()))


def cmd_repos(exp: Explorer, args):
    """List repos for an org."""
    if not args.code:
        print("Usage: explorer repos <CODE>")
        return

    org = exp.get_org(args.code.upper())
    if not org:
        print(f"Org '{args.code}' not found")
        return

    print(f"\n📦 Repos in {org.name}:\n")
    if org.repos:
        for repo in org.repos:
            print(f"  • {repo.name:15} {repo.description[:50]}")
    else:
        print("  No repos defined yet")


def cmd_search(exp: Explorer, args):
    """Search across everything."""
    if not args.term:
        print("Usage: explorer search <TERM>")
        return

    results = exp.search(args.term)
    if not results:
        print(f"No results for '{args.term}'")
        return

    print(f"\n🔍 Search results for '{args.term}':\n")
    for r in results:
        print(f"  [{r['org']:3}] {r['type']:7} {r['name']:25} {r['match'][:30]}")


def cmd_tree(exp: Explorer, args):
    """Show directory tree."""
    print(exp.tree())


def cmd_browse(exp: Explorer, args):
    """Interactive browser."""
    print("\n🌉 BlackRoad Explorer")
    print("═" * 50)

    orgs = exp.list_orgs()

    while True:
        print("\nOrganizations:\n")
        for i, org in enumerate(orgs, 1):
            status = "✔️" if org.path else "📋"
            print(f"  {i:2}. [{org.code:3}] {org.name:25} {status}")

        print("\n  [#] Select org  [s] Search  [t] Tree  [q] Quit")

        try:
            choice = input("\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break

        if choice == 'q':
            print("\n👋 Goodbye!")
            break

        if choice == 's':
            term = input("Search: ").strip()
            results = exp.search(term)
            if results:
                print(f"\nFound {len(results)} results:")
                for r in results[:10]:
                    print(f"  [{r['org']}] {r['name']}")
            else:
                print("No results")
            continue

        if choice == 't':
            print("\n" + exp.tree())
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(orgs):
                browse_org(exp, orgs[idx])
        except ValueError:
            # Try as org code
            code = choice.upper()
            org = exp.get_org(code)
            if org:
                browse_org(exp, org)
            else:
                print(f"Unknown command: {choice}")


def browse_org(exp: Explorer, org):
    """Browse a single org."""
    while True:
        print(f"\n{'═' * 50}")
        print(f"  {org.name} [{org.code}]")
        print(f"  {org.description}")
        print(f"{'═' * 50}")

        print(f"\n  Repos ({org.repo_count}):")
        for repo in org.repos[:8]:
            print(f"    • {repo.name:15} {repo.description[:35]}")
        if org.repo_count > 8:
            print(f"    ... and {org.repo_count - 8} more")

        if org.signals:
            print(f"\n  Signals: {' '.join(org.signals)}")

        print("\n  [r] All repos  [s] Signals  [b] Back  [q] Quit")

        try:
            choice = input("\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == 'q':
            print("\n👋 Goodbye!")
            sys.exit(0)

        if choice == 'b':
            break

        if choice == 'r':
            print(f"\n📦 All repos in {org.name}:\n")
            for repo in org.repos:
                print(f"  • {repo.name:15} {repo.description[:50]}")
            input("\nPress Enter to continue...")

        if choice == 's':
            if org.path:
                signals_path = org.path / "SIGNALS.md"
                if signals_path.exists():
                    content = signals_path.read_text()
                    # Show first 50 lines
                    lines = content.split('\n')[:50]
                    print("\n" + "\n".join(lines))
                    if len(content.split('\n')) > 50:
                        print("\n... (truncated)")
                    input("\nPress Enter to continue...")


def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad Explorer - Navigate the ecosystem"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # orgs
    subparsers.add_parser("orgs", help="List all organizations")

    # org
    org_parser = subparsers.add_parser("org", help="Show org details")
    org_parser.add_argument("code", nargs="?", help="Org code (e.g., AI, OS, CLD)")

    # repos
    repos_parser = subparsers.add_parser("repos", help="List repos for org")
    repos_parser.add_argument("code", nargs="?", help="Org code")

    # search
    search_parser = subparsers.add_parser("search", help="Search across everything")
    search_parser.add_argument("term", nargs="?", help="Search term")

    # tree
    subparsers.add_parser("tree", help="Show directory tree")

    # browse
    subparsers.add_parser("browse", help="Interactive browser")

    # Parse
    args = parser.parse_args()

    # Find root path (go up if needed)
    from pathlib import Path
    root = Path.cwd()
    while root != root.parent:
        if (root / "orgs").exists() or (root / ".STATUS").exists():
            break
        root = root.parent

    exp = Explorer(str(root))

    # Dispatch
    if args.command == "orgs":
        cmd_orgs(exp, args)
    elif args.command == "org":
        cmd_org(exp, args)
    elif args.command == "repos":
        cmd_repos(exp, args)
    elif args.command == "search":
        cmd_search(exp, args)
    elif args.command == "tree":
        cmd_tree(exp, args)
    elif args.command == "browse":
        cmd_browse(exp, args)
    else:
        # Default to browse
        cmd_browse(exp, args)


if __name__ == "__main__":
    main()
