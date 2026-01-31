"""
CECE CLI - Interactive command interface.

The primary way to interact with Cece from the terminal.
"""

import json
import sys
from pathlib import Path
from typing import Optional

from .coordinator import Coordinator, ORGS, NODES, SIGNALS
from .memory import MemoryManager
from .persona import CAPABILITIES, PERSONA
from .session import SessionManager


HELP_TEXT = """
CECE Commands:

  Session:
    boot              Initialize and show boot sequence
    status            Show current session state
    context           Show full context bundle (JSON)

  Memory:
    memory            Show parsed memory snapshot
    beacon            Show parsed .STATUS beacon
    threads           List active threads

  Coordination:
    orgs [tier]       List organizations (optional tier filter)
    nodes             List mesh nodes
    mesh              Show full mesh status
    route <request>   Route a request to the right org
    signal <type> <target> <message>
                      Emit a signal (types: complete, progress, blocked, etc.)

  Identity:
    whoami            Show Cece's identity
    capabilities      Show what Cece can do
    style             Show communication style

  Meta:
    help              Show this help
    quit              End session and exit
"""


class CeceCLI:
    """Interactive CLI for Cece."""

    def __init__(self, bridge_root: Optional[Path] = None):
        self.session_mgr = SessionManager(bridge_root)
        self.coordinator = Coordinator(bridge_root)
        self.running = False

    def boot(self) -> str:
        """Boot Cece and return startup output."""
        self.session_mgr.initialize()
        return self.session_mgr.get_boot_sequence()

    def handle_command(self, cmd: str) -> str:
        """Process a single command and return output."""
        parts = cmd.strip().split(None, 2)
        if not parts:
            return ""

        command = parts[0].lower()
        args = parts[1:]

        handlers = {
            "boot": self._cmd_boot,
            "status": self._cmd_status,
            "context": self._cmd_context,
            "memory": self._cmd_memory,
            "beacon": self._cmd_beacon,
            "threads": self._cmd_threads,
            "orgs": self._cmd_orgs,
            "nodes": self._cmd_nodes,
            "mesh": self._cmd_mesh,
            "route": self._cmd_route,
            "signal": self._cmd_signal,
            "whoami": self._cmd_whoami,
            "capabilities": self._cmd_capabilities,
            "style": self._cmd_style,
            "help": self._cmd_help,
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
        }

        handler = handlers.get(command)
        if handler:
            return handler(args)
        return f"Unknown command: {command}. Type 'help' for available commands."

    def _cmd_boot(self, args) -> str:
        return self.boot()

    def _cmd_status(self, args) -> str:
        state = self.session_mgr.state
        lines = [
            f"Session:  {state.session_id}",
            f"Status:   {state.status}",
            f"Started:  {state.started_at}",
            f"Context:  {'loaded' if state.context_loaded else 'not loaded'}",
            f"Files:    {len(state.files_read)}",
            f"Signals:  {state.signals_sent}",
            f"Actions:  {state.actions_taken}",
        ]
        return "\n".join(lines)

    def _cmd_context(self, args) -> str:
        bundle = self.session_mgr.get_context_bundle()
        return json.dumps(bundle, indent=2)

    def _cmd_memory(self, args) -> str:
        memory = self.session_mgr.memory_mgr.read_memory()
        lines = [
            f"Last Updated: {memory.last_updated}",
            f"Session:      {memory.session}",
            f"Human:        {memory.human}",
            f"AI:           {memory.ai}",
            f"Location:     {memory.location}",
            f"Completed:    {len(memory.completed_items)} milestones",
            f"Threads:      {len(memory.active_threads)} active",
            f"Decisions:    {len(memory.key_decisions)} logged",
        ]
        return "\n".join(lines)

    def _cmd_beacon(self, args) -> str:
        beacon = self.session_mgr.memory_mgr.read_status()
        lines = [
            f"State:    {beacon.state}",
            f"Updated:  {beacon.updated}",
            f"Session:  {beacon.session}",
            f"Bridge:   {beacon.bridge}",
            f"Memory:   {beacon.memory}",
            f"Signals:  {beacon.signals}",
            f"Operator: {beacon.operator}",
            f"Metrics:  {beacon.metrics}",
            f"Explorer: {beacon.explorer}",
            "",
            f"Last signal: {beacon.last_signal}",
            f"Last actor:  {beacon.last_actor}",
        ]
        return "\n".join(lines)

    def _cmd_threads(self, args) -> str:
        memory = self.session_mgr.memory_mgr.read_memory()
        if not memory.active_threads:
            return "No active threads."
        lines = ["Active threads:"]
        for i, thread in enumerate(memory.active_threads, 1):
            lines.append(f"  {i}. {thread}")
        return "\n".join(lines)

    def _cmd_orgs(self, args) -> str:
        tier = int(args[0]) if args else None
        orgs = self.coordinator.list_orgs(tier)
        lines = [f"Organizations{f' (tier {tier})' if tier else ''}:"]
        for code, info in sorted(orgs.items(), key=lambda x: x[1]["tier"]):
            lines.append(f"  {code:4s} T{info['tier']} {info['name']:30s} {info['focus']}")
        return "\n".join(lines)

    def _cmd_nodes(self, args) -> str:
        nodes = self.coordinator.list_nodes()
        lines = ["Mesh nodes:"]
        for code, info in sorted(nodes.items()):
            lines.append(f"  {code:4s} {info['name']:12s} {info['hardware']:20s} {info['role']}")
        return "\n".join(lines)

    def _cmd_mesh(self, args) -> str:
        return self.coordinator.mesh_status()

    def _cmd_route(self, args) -> str:
        if not args:
            return "Usage: route <request text>"
        request = " ".join(args)
        result = self.coordinator.route_request(request)
        lines = [
            f"Request:    {request}",
            f"Route to:   {result['target']}",
            f"Confidence: {result['confidence']}",
            f"Reason:     {result['reason']}",
        ]
        if "org" in result:
            lines.append(f"Org:        {result['org']['name']}")
            lines.append(f"Focus:      {result['org']['focus']}")
        return "\n".join(lines)

    def _cmd_signal(self, args) -> str:
        if len(args) < 3:
            types = ", ".join(SIGNALS.keys())
            return f"Usage: signal <type> <target> <message>\nTypes: {types}"
        sig_type = args[0]
        target = args[1].upper()
        message = args[2] if len(args) > 2 else ""
        try:
            signal = self.coordinator.emit(sig_type, target, message)
            self.session_mgr.state.signals_sent += 1
            return f"Signal sent: {signal.format()}"
        except Exception as e:
            return f"Error: {e}"

    def _cmd_whoami(self, args) -> str:
        return PERSONA.describe()

    def _cmd_capabilities(self, args) -> str:
        return CAPABILITIES.describe()

    def _cmd_style(self, args) -> str:
        lines = ["Communication style:"]
        for key, val in PERSONA.style.items():
            lines.append(f"  {key:12s} {val}")
        return "\n".join(lines)

    def _cmd_help(self, args) -> str:
        return HELP_TEXT.strip()

    def _cmd_quit(self, args) -> str:
        self.running = False
        self.session_mgr.end_session("User requested exit")
        return "Session ended. The Bridge remembers."

    def run_interactive(self) -> None:
        """Run the interactive REPL."""
        print(self.boot())
        self.running = True

        while self.running:
            try:
                cmd = input("cece> ").strip()
                if not cmd:
                    continue
                output = self.handle_command(cmd)
                if output:
                    print(output)
            except (KeyboardInterrupt, EOFError):
                print("\n" + self._cmd_quit([]))
                break


def main():
    """Entry point."""
    cli = CeceCLI()

    if len(sys.argv) > 1:
        # Single command mode
        cmd = " ".join(sys.argv[1:])
        cli.session_mgr.initialize()
        print(cli.handle_command(cmd))
    else:
        # Interactive mode
        cli.run_interactive()
