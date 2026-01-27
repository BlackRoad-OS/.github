#!/usr/bin/env python3
"""
Salesforce Sync CLI.

Usage:
    python -m salesforce_sync.cli init
    python -m salesforce_sync.cli sync
    python -m salesforce_sync.cli status
    python -m salesforce_sync.cli query Contact
"""

import argparse
from datetime import datetime
from .sync.engine import SFSync


def cmd_init(args, sync: SFSync):
    """Initialize database and tables."""
    print("Initializing Salesforce Sync...")

    # Just accessing the properties creates the tables
    _ = sync.contacts
    _ = sync.leads
    _ = sync.accounts
    _ = sync.opportunities

    print("✔️ Database initialized")
    print(f"   Path: {sync.db_path}")


def cmd_connect(args, sync: SFSync):
    """Test Salesforce connection."""
    print("Connecting to Salesforce...")

    if sync.connect():
        print("✔️ Connected successfully")
        print(f"   Instance: {sync.client.instance_url}")
    else:
        print("❌ Connection failed")


def cmd_sync(args, sync: SFSync):
    """Run sync from Salesforce."""
    print("Syncing from Salesforce...")

    if not sync.connect():
        print("❌ Failed to connect")
        return

    results = sync.sync_all()

    total = sum(results.values())
    print(f"✔️ Synced {total} records")
    for obj, count in results.items():
        print(f"   {obj}: {count}")


def cmd_push(args, sync: SFSync):
    """Push local changes to Salesforce."""
    print("Pushing to Salesforce...")

    if not sync.connect():
        print("❌ Failed to connect")
        return

    results = sync.push_all()

    total = sum(results.values())
    print(f"✔️ Pushed {total} records")
    for obj, count in results.items():
        if count > 0:
            print(f"   {obj}: {count}")


def cmd_status(args, sync: SFSync):
    """Show sync status."""
    stats = sync.stats()

    print("📊 Salesforce Sync Status")
    print("═" * 40)
    print(f"   Contacts:      {stats['contacts']:,}")
    print(f"   Leads:         {stats['leads']:,}")
    print(f"   Accounts:      {stats['accounts']:,}")
    print(f"   Opportunities: {stats['opportunities']:,}")
    print()
    print(f"   Last sync:     {stats['last_sync'] or 'Never'}")
    print(f"   API calls:     {stats['api_calls']:,}")
    print(f"   API remaining: {stats['api_remaining']:,}")


def cmd_list(args, sync: SFSync):
    """List records of a type."""
    obj_type = args.object.lower()

    if obj_type == "contact":
        records = sync.contacts.all(limit=args.limit)
        for r in records:
            print(f"  {r.id}  {r.full_name:30} {r.email or ''}")
    elif obj_type == "lead":
        records = sync.leads.all(limit=args.limit)
        for r in records:
            print(f"  {r.id}  {r.full_name:20} @ {r.company or 'Unknown'}")
    elif obj_type == "account":
        records = sync.accounts.all(limit=args.limit)
        for r in records:
            print(f"  {r.id}  {r.name:30} {r.industry or ''}")
    elif obj_type == "opportunity":
        records = sync.opportunities.all(limit=args.limit)
        for r in records:
            amt = f"${r.amount:,.0f}" if r.amount else "TBD"
            print(f"  {r.id}  {r.name:30} {amt:>12} {r.stage or ''}")
    else:
        print(f"Unknown object type: {obj_type}")


def cmd_search(args, sync: SFSync):
    """Search records."""
    obj_type = args.object.lower()
    term = args.term

    if obj_type == "contact":
        results = sync.contacts.search(email=term) + sync.contacts.search(last_name=term)
    elif obj_type == "lead":
        results = sync.leads.search(company=term) + sync.leads.search(last_name=term)
    elif obj_type == "account":
        results = sync.accounts.search(name=term)
    else:
        results = []

    print(f"Found {len(results)} results for '{term}':")
    for r in results:
        print(f"  {r}")


def main():
    parser = argparse.ArgumentParser(description="Salesforce Sync CLI")

    parser.add_argument(
        "--db", "-d",
        default="./data/salesforce.db",
        help="Database path"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init
    subparsers.add_parser("init", help="Initialize database")

    # connect
    subparsers.add_parser("connect", help="Test SF connection")

    # sync
    subparsers.add_parser("sync", help="Sync from Salesforce")

    # push
    subparsers.add_parser("push", help="Push to Salesforce")

    # status
    subparsers.add_parser("status", help="Show status")

    # list
    list_parser = subparsers.add_parser("list", help="List records")
    list_parser.add_argument("object", help="Object type (contact, lead, account, opportunity)")
    list_parser.add_argument("--limit", "-l", type=int, default=20, help="Limit")

    # search
    search_parser = subparsers.add_parser("search", help="Search records")
    search_parser.add_argument("object", help="Object type")
    search_parser.add_argument("term", help="Search term")

    args = parser.parse_args()

    # Create sync instance
    sync = SFSync(db_path=args.db)

    # Dispatch
    if args.command == "init":
        cmd_init(args, sync)
    elif args.command == "connect":
        cmd_connect(args, sync)
    elif args.command == "sync":
        cmd_sync(args, sync)
    elif args.command == "push":
        cmd_push(args, sync)
    elif args.command == "status":
        cmd_status(args, sync)
    elif args.command == "list":
        cmd_list(args, sync)
    elif args.command == "search":
        cmd_search(args, sync)
    else:
        parser.print_help()

    sync.close()


if __name__ == "__main__":
    main()
