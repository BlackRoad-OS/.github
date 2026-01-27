#!/usr/bin/env python3
"""
AI Router CLI

Route to intelligence from the command line.

Usage:
    ai-router complete "What is 2+2?"
    ai-router complete "Write code" --provider anthropic
    ai-router complete "Analyze" --chain hailo,ollama,openai
    ai-router embed "Hello world"
    ai-router health
    ai-router costs --period day
"""

import asyncio
import argparse
import sys
from typing import Optional


def run_async(coro):
    """Run an async function."""
    return asyncio.get_event_loop().run_until_complete(coro)


async def cmd_complete(args):
    """Complete a prompt."""
    from .routing.router import Router

    router = Router(strategy=args.strategy)

    # Parse chain if provided
    chain = args.chain.split(",") if args.chain else None

    print()
    print(f"  Prompt: {args.prompt[:60]}{'...' if len(args.prompt) > 60 else ''}")
    print(f"  Strategy: {args.strategy}")
    if args.provider:
        print(f"  Provider: {args.provider}")
    if chain:
        print(f"  Chain: {' → '.join(chain)}")
    print()
    print("  " + "-" * 50)
    print()

    result = await router.complete(
        args.prompt,
        provider=args.provider,
        chain=chain,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    if result.success:
        print(f"  Response ({result.final_provider}):")
        print()
        # Indent response
        for line in result.content.split("\n"):
            print(f"    {line}")
        print()
        print("  " + "-" * 50)
        print(f"  Latency: {result.total_latency_ms}ms")
        print(f"  Cost: ${result.total_cost:.4f}")
        print(f"  Providers tried: {len(result.routes_tried)}")
    else:
        print(f"  Error: {result.error}")
        print(f"  Providers tried: {len(result.routes_tried)}")
        for route in result.routes_tried:
            print(f"    - {route.provider}: {route.error}")

    print()


async def cmd_stream(args):
    """Stream a completion."""
    from .routing.router import Router

    router = Router(strategy=args.strategy)

    print()
    print(f"  Prompt: {args.prompt[:60]}{'...' if len(args.prompt) > 60 else ''}")
    print()
    print("  Response:")
    print("  ", end="", flush=True)

    async for chunk in router.complete_stream(
        args.prompt,
        provider=args.provider,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    ):
        print(chunk, end="", flush=True)

    print()
    print()


async def cmd_embed(args):
    """Generate embeddings."""
    from .routing.router import Router

    router = Router()

    print()
    print(f"  Text: {args.text[:60]}{'...' if len(args.text) > 60 else ''}")

    result = await router.embed(args.text, provider=args.provider)

    print(f"  Provider: {result.provider}")
    print(f"  Model: {result.model}")
    print(f"  Dimensions: {result.dimensions}")
    print(f"  Cost: ${result.cost:.4f}")
    print(f"  Latency: {result.latency_ms}ms")
    print()

    if args.show_vector:
        print(f"  Vector (first 10): {result.embeddings[0][:10]}")
        print()


async def cmd_health(args):
    """Check provider health."""
    from .routing.router import Router

    router = Router()

    print()
    print("  PROVIDER HEALTH")
    print("  " + "=" * 40)
    print()

    results = await router.health_check_all()

    for provider, status in results.items():
        emoji = "🟢" if status.value == "healthy" else "🟡" if status.value == "degraded" else "🔴"
        print(f"  {emoji} {provider:15} {status.value}")

    print()


def cmd_costs(args):
    """Show cost report."""
    from .tracking.costs import CostTracker

    tracker = CostTracker(storage_path=args.storage)

    report = tracker.report(period=args.period)

    print()
    print(report.summary())
    print()


def cmd_interactive(args):
    """Interactive mode."""
    from .routing.router import Router

    router = Router(strategy=args.strategy)

    print()
    print("  AI ROUTER - Interactive Mode")
    print("  " + "=" * 40)
    print()
    print("  Commands:")
    print("    /provider <name>  - Set provider (openai, anthropic, hailo, ollama)")
    print("    /strategy <name>  - Set strategy (cost, latency, quality, local_first)")
    print("    /health           - Check provider health")
    print("    /quit             - Exit")
    print()

    provider = None
    strategy = args.strategy

    while True:
        try:
            prompt = input("  > ").strip()

            if not prompt:
                continue

            if prompt.startswith("/"):
                parts = prompt[1:].split(maxsplit=1)
                cmd = parts[0].lower()

                if cmd == "quit" or cmd == "exit":
                    print("  Goodbye!")
                    break
                elif cmd == "provider":
                    provider = parts[1] if len(parts) > 1 else None
                    print(f"  Provider set to: {provider or 'auto'}")
                elif cmd == "strategy":
                    strategy = parts[1] if len(parts) > 1 else "cost"
                    router = Router(strategy=strategy)
                    print(f"  Strategy set to: {strategy}")
                elif cmd == "health":
                    run_async(cmd_health(args))
                else:
                    print(f"  Unknown command: {cmd}")
                continue

            # Run completion
            result = run_async(router.complete(prompt, provider=provider))

            if result.success:
                print()
                print(f"  [{result.final_provider}] {result.content}")
                print()
            else:
                print(f"  Error: {result.error}")

        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="AI Router - Route to intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s complete "What is 2+2?"
  %(prog)s complete "Write Python code" --provider anthropic
  %(prog)s complete "Analyze" --chain hailo,ollama,openai
  %(prog)s complete "Hello" --strategy quality
  %(prog)s stream "Tell me a story"
  %(prog)s embed "Hello world"
  %(prog)s health
  %(prog)s costs --period day
  %(prog)s interactive
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # Complete
    complete_parser = subparsers.add_parser("complete", help="Complete a prompt")
    complete_parser.add_argument("prompt", help="Prompt to complete")
    complete_parser.add_argument("--provider", "-p", help="Specific provider")
    complete_parser.add_argument("--chain", "-c", help="Fallback chain (comma-separated)")
    complete_parser.add_argument("--strategy", "-s", default="cost",
                                 help="Routing strategy (cost, latency, quality, local_first)")
    complete_parser.add_argument("--max-tokens", type=int, default=1024)
    complete_parser.add_argument("--temperature", type=float, default=0.7)

    # Stream
    stream_parser = subparsers.add_parser("stream", help="Stream a completion")
    stream_parser.add_argument("prompt", help="Prompt to complete")
    stream_parser.add_argument("--provider", "-p", help="Specific provider")
    stream_parser.add_argument("--strategy", "-s", default="cost")
    stream_parser.add_argument("--max-tokens", type=int, default=1024)
    stream_parser.add_argument("--temperature", type=float, default=0.7)

    # Embed
    embed_parser = subparsers.add_parser("embed", help="Generate embeddings")
    embed_parser.add_argument("text", help="Text to embed")
    embed_parser.add_argument("--provider", "-p", help="Specific provider")
    embed_parser.add_argument("--show-vector", action="store_true", help="Show vector")

    # Health
    subparsers.add_parser("health", help="Check provider health")

    # Costs
    costs_parser = subparsers.add_parser("costs", help="Show cost report")
    costs_parser.add_argument("--period", default="all",
                              help="Period: hour, day, week, month, all")
    costs_parser.add_argument("--storage", default=".ai-router-costs.json",
                              help="Cost storage file")

    # Interactive
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    interactive_parser.add_argument("--strategy", "-s", default="cost")

    args = parser.parse_args()

    if args.command == "complete":
        run_async(cmd_complete(args))
    elif args.command == "stream":
        run_async(cmd_stream(args))
    elif args.command == "embed":
        run_async(cmd_embed(args))
    elif args.command == "health":
        run_async(cmd_health(args))
    elif args.command == "costs":
        cmd_costs(args)
    elif args.command == "interactive":
        cmd_interactive(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
