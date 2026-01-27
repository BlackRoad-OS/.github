#!/usr/bin/env python3
"""
Alexandria CLI - Explore the Library.

Usage:
    python -m alexandria models                    # List all models
    python -m alexandria models --domain math      # Models for math
    python -m alexandria models --recommend "write code"
    python -m alexandria domains                   # List domains
    python -m alexandria templates                 # List templates
    python -m alexandria agents                    # List agents
    python -m alexandria explore "physics simulations"
    python -m alexandria create proof --agent mathematician
    python -m alexandria stats
"""

import argparse
import json
from typing import Optional

from .library import Library
from .models import ModelCapability


def cmd_models(args):
    """List or search models."""
    lib = Library()

    print()
    print("  ALEXANDRIA MODEL CATALOG")
    print("  " + "=" * 60)
    print()

    if args.recommend:
        models = lib.recommend_model(
            args.recommend,
            local_only=not args.cloud,
            max_memory_gb=args.max_memory,
        )
        print(f"  Recommended for: {args.recommend}")
        print()
    elif args.domain:
        models = lib.models.for_domain(args.domain)
        print(f"  Models for domain: {args.domain}")
        print()
    elif args.capability:
        try:
            cap = ModelCapability(args.capability)
            models = lib.models.for_capability(cap)
            print(f"  Models with capability: {args.capability}")
            print()
        except ValueError:
            print(f"  Unknown capability: {args.capability}")
            return
    else:
        models = lib.models.local_only() if not args.cloud else lib.models.list_all()

    for model in models[:20]:
        provider_badge = f"[{model.provider[:3].upper()}]"
        size_badge = f"{model.size:>5}"
        quality_badge = {"basic": "★", "good": "★★", "excellent": "★★★", "sota": "★★★★"}.get(model.quality, "?")

        print(f"  {provider_badge} {model.name:30} {size_badge}  {quality_badge}")
        if args.verbose:
            print(f"        {model.description[:60]}...")
            print(f"        Domains: {', '.join(model.domains[:3])}")
            print(f"        Memory: {model.memory_gb}GB | Speed: {model.speed}")
            print()

    print()
    print(f"  Total: {len(models)} models")
    if not args.cloud:
        print("  (showing local only, use --cloud for all)")
    print()


def cmd_domains(args):
    """List domains."""
    lib = Library()

    print()
    print("  ALEXANDRIA DOMAINS")
    print("  " + "=" * 60)
    print()

    domains = lib.domains.list_all()

    if args.type:
        from .domains.registry import DomainType
        try:
            dtype = DomainType(args.type)
            domains = lib.domains.for_type(dtype)
        except ValueError:
            print(f"  Unknown type: {args.type}")
            return

    current_type = None
    for domain in domains:
        if domain.type.value != current_type:
            current_type = domain.type.value
            print(f"  [{current_type.upper()}]")

        print(f"    {domain.code:6} {domain.name:20}")
        if args.verbose:
            print(f"           {domain.description[:50]}...")
            print(f"           Models: {', '.join(domain.recommended_models[:2])}")
            print()

    print()
    print(f"  Total: {len(domains)} domains")
    print()


def cmd_templates(args):
    """List templates."""
    lib = Library()

    print()
    print("  ALEXANDRIA TEMPLATES")
    print("  " + "=" * 60)
    print()

    templates = lib.templates.list_templates(args.domain)

    for template in templates:
        required = len(template.required_fields())
        optional = len(template.optional_fields())

        print(f"  [{template.domain:5}] {template.name:20} ({required} req, {optional} opt)")
        if args.verbose:
            print(f"          {template.description}")
            print(f"          Philosophy: {template.philosophy[:50]}...")
            print()

    print()
    print(f"  Total: {len(templates)} templates")
    print()


def cmd_agents(args):
    """List agents."""
    lib = Library()

    print()
    print("  ALEXANDRIA AGENTS")
    print("  " + "=" * 60)
    print()

    agents = lib.agents.list_all()

    if args.domain:
        agents = lib.agents.for_domain(args.domain)

    if args.autonomous:
        agents = lib.agents.autonomous()

    for agent in agents:
        domains_str = ", ".join(agent.domains[:3])
        if len(agent.domains) > 3:
            domains_str += "..."

        auto_badge = " [AUTO]" if agent.can(lib.agents.agents[agent.name].permissions.__iter__().__next__()) else ""

        print(f"  {agent.name:15} | {domains_str:20}")
        if args.verbose:
            print(f"    Purpose: {agent.purpose[:50]}...")
            print(f"    Models: {', '.join(agent.preferred_models[:2])}")
            print()

    print()
    print(f"  Total: {len(agents)} agents")
    print()


def cmd_explore(args):
    """Explore the Library."""
    lib = Library()

    print()
    print("  EXPLORING ALEXANDRIA")
    print("  " + "=" * 60)
    print()
    print(f"  Query: {args.query}")
    print(f"  Agent: {args.agent}")
    print()

    results = lib.explore(args.query, agent=args.agent, domain=args.domain)

    if "error" in results:
        print(f"  Error: {results['error']}")
        return

    if results["models"]:
        print("  Models:")
        for m in results["models"]:
            print(f"    - {m['name']}: {m['description'][:40]}...")

    if results["domains"]:
        print()
        print("  Domains:")
        for d in results["domains"]:
            print(f"    - [{d['code']}] {d['name']}")

    if results["templates"]:
        print()
        print("  Templates:")
        for t in results["templates"]:
            print(f"    - {t['name']} ({t['domain']})")

    print()


def cmd_create(args):
    """Create from a template."""
    lib = Library()

    print()
    print("  CREATE FROM TEMPLATE")
    print("  " + "=" * 60)
    print()

    template = lib.templates.get_template(args.template)
    if not template:
        print(f"  Unknown template: {args.template}")
        return

    print(f"  Template: {template.name}")
    print(f"  Domain:   {template.domain}")
    print(f"  Agent:    {args.agent}")
    print()

    print("  Required fields:")
    for field in template.required_fields():
        print(f"    - {field.name}: {field.description}")

    print()
    print("  Optional fields:")
    for field in template.optional_fields()[:5]:
        default = f" (default: {field.default})" if field.default else ""
        print(f"    - {field.name}: {field.description}{default}")

    print()
    print(f"  Philosophy: {template.philosophy}")
    print()
    print("  Use lib.create('{0}', {{...}}, agent='{1}') to create an instance.".format(
        args.template, args.agent
    ))
    print()


def cmd_stats(args):
    """Show Library statistics."""
    lib = Library()

    print()
    print(lib.summary())


def cmd_interactive(args):
    """Interactive mode."""
    lib = Library()

    print()
    print("  ALEXANDRIA - Interactive Mode")
    print("  " + "=" * 50)
    print()
    print("  Commands:")
    print("    models [query]      - Search models")
    print("    domains             - List domains")
    print("    templates           - List templates")
    print("    agents              - List agents")
    print("    explore <query>     - Explore")
    print("    recommend <task>    - Recommend models")
    print("    stats               - Show stats")
    print("    quit                - Exit")
    print()

    while True:
        try:
            cmd = input("  alexandria> ").strip()

            if not cmd:
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if action in ("quit", "exit", "q"):
                print("  Farewell, explorer!")
                break
            elif action == "models":
                if arg:
                    models = lib.models.search(query=arg)
                else:
                    models = lib.models.local_only()[:10]
                for m in models[:10]:
                    print(f"    {m.name}: {m.description[:40]}...")
            elif action == "domains":
                for d in lib.domains.list_all():
                    print(f"    [{d.code}] {d.name}")
            elif action == "templates":
                for t in lib.templates.list_templates():
                    print(f"    {t.name} ({t.domain})")
            elif action == "agents":
                for a in lib.agents.list_all():
                    print(f"    {a.name}: {a.purpose[:40]}...")
            elif action == "explore" and arg:
                results = lib.explore(arg)
                if results.get("models"):
                    print("    Models:", ", ".join(m["name"] for m in results["models"]))
                if results.get("domains"):
                    print("    Domains:", ", ".join(d["code"] for d in results["domains"]))
            elif action == "recommend" and arg:
                models = lib.recommend_model(arg)
                for m in models[:5]:
                    print(f"    {m.name}: {m.description[:40]}...")
            elif action == "stats":
                print(lib.summary())
            else:
                print(f"    Unknown: {action}")

        except (EOFError, KeyboardInterrupt):
            print("\n  Farewell, explorer!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Alexandria - The Library for Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s models                          # List local models
  %(prog)s models --domain mathematics     # Math models
  %(prog)s models --recommend "write code" # Recommend for coding
  %(prog)s domains                         # List domains
  %(prog)s templates --domain CODE         # Code templates
  %(prog)s agents --autonomous             # Autonomous agents
  %(prog)s explore "physics simulations"   # Explore
  %(prog)s stats                           # Statistics
  %(prog)s interactive                     # Interactive mode
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # Models
    models_parser = subparsers.add_parser("models", help="List/search models")
    models_parser.add_argument("--domain", "-d", help="Filter by domain")
    models_parser.add_argument("--capability", "-c", help="Filter by capability")
    models_parser.add_argument("--recommend", "-r", help="Recommend for task")
    models_parser.add_argument("--cloud", action="store_true", help="Include cloud models")
    models_parser.add_argument("--max-memory", type=float, default=8.0, help="Max memory GB")
    models_parser.add_argument("-v", "--verbose", action="store_true")

    # Domains
    domains_parser = subparsers.add_parser("domains", help="List domains")
    domains_parser.add_argument("--type", "-t", help="Filter by type")
    domains_parser.add_argument("-v", "--verbose", action="store_true")

    # Templates
    templates_parser = subparsers.add_parser("templates", help="List templates")
    templates_parser.add_argument("--domain", "-d", help="Filter by domain")
    templates_parser.add_argument("-v", "--verbose", action="store_true")

    # Agents
    agents_parser = subparsers.add_parser("agents", help="List agents")
    agents_parser.add_argument("--domain", "-d", help="Filter by domain")
    agents_parser.add_argument("--autonomous", "-a", action="store_true", help="Only autonomous")
    agents_parser.add_argument("-v", "--verbose", action="store_true")

    # Explore
    explore_parser = subparsers.add_parser("explore", help="Explore the Library")
    explore_parser.add_argument("query", help="What to explore")
    explore_parser.add_argument("--agent", "-a", default="explorer", help="Agent to use")
    explore_parser.add_argument("--domain", "-d", help="Limit to domain")

    # Create
    create_parser = subparsers.add_parser("create", help="Create from template")
    create_parser.add_argument("template", help="Template name")
    create_parser.add_argument("--agent", "-a", default="assistant", help="Agent to use")

    # Stats
    subparsers.add_parser("stats", help="Show statistics")

    # Interactive
    subparsers.add_parser("interactive", help="Interactive mode")

    args = parser.parse_args()

    if args.command == "models":
        cmd_models(args)
    elif args.command == "domains":
        cmd_domains(args)
    elif args.command == "templates":
        cmd_templates(args)
    elif args.command == "agents":
        cmd_agents(args)
    elif args.command == "explore":
        cmd_explore(args)
    elif args.command == "create":
        cmd_create(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "interactive":
        cmd_interactive(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
