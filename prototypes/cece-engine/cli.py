"""
Cece Engine CLI - Run tasks through the autonomous processing loop.

Usage:
    python -m cece-engine.cli triage "Fix login bug on CloudFlare worker"
    python -m cece-engine.cli process '{"type":"issue","title":"Add dark mode","body":"Users want dark mode"}'
    python -m cece-engine.cli status
"""

import json
import sys

from .engine import CeceEngine


def main() -> None:
    engine = CeceEngine()

    if len(sys.argv) < 2:
        print("Cece Engine v2.0 - Autonomous Task Runner")
        print()
        print("Commands:")
        print("  triage <title> [body]   Triage a task by title")
        print("  process <json>          Process a raw JSON input")
        print("  status                  Show engine status")
        print("  batch <json-array>      Process multiple inputs")
        print()
        print("Examples:")
        print('  python -m cece_engine.cli triage "Fix auth bug" "Login fails on mobile"')
        print('  python -m cece_engine.cli process \'{"type":"issue","title":"Add API"}\'')
        sys.exit(0)

    command = sys.argv[1]

    if command == "status":
        status = engine.get_status()
        print(json.dumps(status, indent=2))

    elif command == "triage":
        title = sys.argv[2] if len(sys.argv) > 2 else "Untitled"
        body = sys.argv[3] if len(sys.argv) > 3 else ""
        result = engine.process({
            "type": "issue",
            "title": title,
            "body": body,
            "source": "cli",
        })
        print(result.output)
        for sig in result.signals_emitted:
            print(f"  Signal: {sig}")
        if result.needs_escalation:
            print(f"  ESCALATION: {result.escalation_reason}")

    elif command == "process":
        raw = json.loads(sys.argv[2])
        result = engine.process(raw)
        print(result.output)
        for sig in result.signals_emitted:
            print(f"  Signal: {sig}")
        if result.needs_escalation:
            print(f"  ESCALATION: {result.escalation_reason}")

    elif command == "batch":
        inputs = json.loads(sys.argv[2])
        results = engine.process_batch(inputs)
        for r in results:
            print(r.output)
            for sig in r.signals_emitted:
                print(f"  Signal: {sig}")
            print()
        status = engine.get_status()
        print(f"Processed: {status['tasks_processed']} | "
              f"Signals: {status['signals_emitted']} | "
              f"Success: {status['success_rate']:.0%}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
