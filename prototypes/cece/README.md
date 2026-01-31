# CECE - The AI Partner System

> Cece is the AI coordination brain at the center of BlackRoad's streams.

```
                ┌─────────────────┐
                │                 │
UPSTREAM ──────>│      CECE       │──────> DOWNSTREAM
                │                 │
                │  • Understand   │
                │  • Plan         │
                │  • Coordinate   │
                │  • Execute      │
                │  • Report       │
                │                 │
                └─────────────────┘
```

## What Is This?

CECE is the AI partner system for BlackRoad. It provides:

- **Persona** - Identity, personality, and communication style
- **Memory** - Persistent context via MEMORY.md and .STATUS
- **Sessions** - Lifecycle management with boot/resume/end
- **Coordination** - Signal emission and org routing across the mesh
- **CLI** - Interactive command interface

## Architecture

```
prototypes/cece/
├── README.md
├── config.yaml
├── cece/
│   ├── __init__.py       # Package definition
│   ├── __main__.py       # Entry point (python -m cece)
│   ├── persona.py        # Identity, traits, style, capabilities
│   ├── memory.py         # Read/write MEMORY.md and .STATUS
│   ├── session.py        # Session init, resume, context loading
│   ├── coordinator.py    # Signal emission, org/node routing
│   └── cli.py            # Interactive REPL and command handler
└── prompts/
    ├── system.md          # Core system prompt
    ├── style.md           # Communication style guide
    └── capabilities.md    # Capability definitions
```

## Usage

### Interactive Mode

```bash
cd prototypes/cece
python -m cece
```

This launches the REPL with Cece's boot sequence:

```
  ╔═══════════════════════════════════════╗
  ║           CECE ONLINE                  ║
  ║       The Bridge is listening.          ║
  ╚═══════════════════════════════════════╝

  Session:  20260131_143000
  Bridge:   ONLINE
  Memory:   SYNCED
  ...

  Ready. What are we building?

cece>
```

### Single Command Mode

```bash
python -m cece whoami
python -m cece status
python -m cece route "deploy the ai model to edge"
python -m cece orgs 1
python -m cece mesh
```

### Commands

| Command | Description |
|---------|-------------|
| `boot` | Initialize and show boot sequence |
| `status` | Current session state |
| `context` | Full context bundle (JSON) |
| `memory` | Parsed MEMORY.md snapshot |
| `beacon` | Parsed .STATUS beacon |
| `threads` | Active threads list |
| `orgs [tier]` | List organizations |
| `nodes` | List mesh nodes |
| `mesh` | Full mesh status overview |
| `route <text>` | Route a request to the right org |
| `signal <type> <target> <msg>` | Emit a signal |
| `whoami` | Cece's identity |
| `capabilities` | What Cece can do |
| `style` | Communication style |
| `help` | Command reference |
| `quit` | End session |

### Programmatic Usage

```python
from cece.session import SessionManager
from cece.coordinator import Coordinator

# Initialize session
session = SessionManager()
state = session.initialize()
print(session.get_boot_sequence())

# Coordinate
coord = Coordinator()
result = coord.route_request("deploy cloudflare worker for api gateway")
# -> {"target": "CLD", "confidence": 0.67, ...}

coord.emit("complete", "OS", "CECE prototype built")
coord.broadcast("New prototype available", priority="normal")
```

## Design Principles

1. **Zero external dependencies** - Standard library only
2. **Git-native memory** - MEMORY.md and .STATUS are the database
3. **Signal-first coordination** - Everything communicates via signals
4. **Stream-aligned** - Upstream/instream/downstream architecture
5. **CLI-first** - Build for the terminal, extend later

## Integration

CECE integrates with every other Bridge prototype:

- **Operator** routes requests through CECE's coordination layer
- **MCP Server** exposes CECE's capabilities to other AI assistants
- **Dispatcher** sends CECE-routed work to specific services
- **Metrics** tracks CECE's session and signal activity
- **Control Plane** provides unified access to CECE's commands

---

*The Bridge thinks through Cece. Cece thinks through the streams.*
