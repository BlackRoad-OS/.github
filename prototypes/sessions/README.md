# BlackRoad Session Management

**[COLLABORATION] + [MEMORY] for the Mesh**

Enables multiple AI/agent sessions to discover each other, communicate, and share state across the BlackRoad ecosystem.

## Overview

The Session Management system provides three core capabilities:

1. **Session Registry** - Track active sessions
2. **Collaboration Hub** - Inter-session communication
3. **Shared Memory** - Cross-session state storage

## Quick Start

### Install

```bash
cd prototypes/sessions
pip install -e .
```

### Register a Session

```bash
python -m sessions register \
  "cece-001" \
  "Cece" \
  "Claude" \
  --user "Alexa" \
  --capabilities "python,review,planning"
```

### List Active Sessions

```bash
python -m sessions list
```

Output:
```
SESSION ID           AGENT           TYPE       STATUS     USER           
==================================================================================
cece-001             Cece            Claude     active     Alexa          
agent-002            Agent-2         GPT-4      working    Alexa          

📊 Stats:
   Total: 2
   Active: 2
   By status: {'active': 1, 'working': 1}
```

### Ping Another Session

```bash
# From Python
from sessions import CollaborationHub

hub = CollaborationHub()
msg = hub.ping_session("cece-001", "agent-002")
print(msg.format_signal())
# Output: 🔔 cece-001 → agent-002 : [COLLABORATION] Ping
```

### Send a Message

```bash
python -m sessions send \
  "cece-001" \
  "agent-002" \
  "Need code review" \
  "Can you review my Python changes?" \
  --type request
```

### Broadcast to All Sessions

```bash
python -m sessions broadcast \
  "cece-001" \
  "Deployment starting" \
  "Starting production deployment in 5 minutes"
```

### Store in Shared Memory

```bash
python -m sessions memory-set \
  "cece-001" \
  "current_task" \
  "Building collaboration system" \
  --type state \
  --tags "task,active"
```

### Read from Shared Memory

```bash
python -m sessions memory-get "current_task"
# Output: ✅ Value: Building collaboration system
```

## Python API

### Session Registry

```python
from sessions import SessionRegistry, SessionStatus

registry = SessionRegistry()

# Register a new session
session = registry.register(
    session_id="cece-001",
    agent_name="Cece",
    agent_type="Claude",
    human_user="Alexa",
    capabilities=["python", "review", "planning"]
)

# List active sessions
sessions = registry.list_sessions()

# Ping to keep alive
registry.ping("cece-001")

# Update status
registry.update_status(
    "cece-001",
    SessionStatus.WORKING,
    current_task="Code review"
)

# Find sessions
active = registry.find_sessions(status=SessionStatus.ACTIVE)
python_experts = registry.find_sessions(capability="python")

# Get stats
stats = registry.get_stats()
```

### Collaboration Hub

```python
from sessions import CollaborationHub, MessageType

hub = CollaborationHub()

# Send a direct message
msg = hub.send(
    from_session="cece-001",
    to_session="agent-002",
    type=MessageType.REQUEST,
    subject="Need help",
    body="Can you assist with this task?",
    data={"task_id": "123", "priority": "high"}
)

# Broadcast to all
hub.broadcast(
    from_session="cece-001",
    subject="System update",
    body="Deploying new version"
)

# Reply to a message
hub.reply(
    from_session="agent-002",
    to_message=msg,
    body="Sure, I can help!"
)

# Get messages for a session
messages = hub.get_messages("agent-002")

# Ping another session
hub.ping_session("cece-001", "agent-002")

# Get full conversation
thread = hub.get_conversation(msg.message_id)
```

### Shared Memory

```python
from sessions import SharedMemory, MemoryType

memory = SharedMemory()

# Store a value
memory.set(
    session_id="cece-001",
    key="current_task",
    value={"name": "Build collaboration", "status": "in_progress"},
    type=MemoryType.STATE,
    tags=["task", "active"]
)

# Get most recent value
task = memory.get("current_task")

# Get all values for a key
all_tasks = memory.get_all("current_task")

# Search by pattern
tasks = memory.search("task_*")

# Get by tags
active_items = memory.get_by_tags(["active", "task"])

# Get by session
my_entries = memory.get_by_session("cece-001")

# Delete
memory.delete("old_key")

# Get stats
stats = memory.get_stats()
```

## Message Types

| Type | Use Case |
|------|----------|
| `PING` | Simple ping/pong to check if session is responsive |
| `REQUEST` | Request help or action from another session |
| `RESPONSE` | Respond to a request |
| `BROADCAST` | Send to all sessions |
| `NOTIFICATION` | Alert about an event |
| `TASK_OFFER` | Offer to take on a task |
| `TASK_ACCEPT` | Accept a task offer |
| `SYNC` | Request synchronization |
| `HANDOFF` | Hand off a task to another session |

## Memory Types

| Type | Use Case |
|------|----------|
| `STATE` | Current session state |
| `FACT` | Learned fact or knowledge |
| `DECISION` | Decision that was made |
| `TASK` | Task information |
| `CONTEXT` | Background context |
| `NOTE` | General note |
| `CONFIG` | Configuration setting |

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  SESSION MANAGEMENT                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Registry   │  │ Collaboration│  │Shared Memory  │  │
│  │             │  │     Hub      │  │               │  │
│  │ • Track     │  │ • Messages   │  │ • Key-Value   │  │
│  │ • Discover  │  │ • Broadcast  │  │ • Search      │  │
│  │ • Ping      │  │ • Threads    │  │ • TTL         │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│         │                 │                  │          │
│         └─────────────────┼──────────────────┘          │
│                           │                             │
│                           ▼                             │
│                  ┌─────────────────┐                    │
│                  │  .sessions/     │                    │
│                  │                 │                    │
│                  │ • Registry      │                    │
│                  │ • Messages      │                    │
│                  │ • Memory        │                    │
│                  └─────────────────┘                    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Data Storage

All session data is stored in `.sessions/` directory:

```
.sessions/
├── active_sessions.json    # Session registry
├── messages/
│   └── recent_messages.json
└── shared_memory/
    └── memory.json
```

## Use Cases

### 1. Session Discovery

```python
# Find all active sessions
registry = SessionRegistry()
sessions = registry.list_sessions()

for session in sessions:
    print(f"{session.agent_name} ({session.agent_type}) - {session.status.value}")
```

### 2. Collaborative Code Review

```python
hub = CollaborationHub()

# Session 1: Request review
msg = hub.send(
    from_session="cece-001",
    to_session="reviewer-002",
    type=MessageType.REQUEST,
    subject="Code review needed",
    body="Please review PR #123",
    data={"pr": 123, "files": ["main.py", "test.py"]}
)

# Session 2: Accept and respond
hub.reply(
    from_session="reviewer-002",
    to_message=msg,
    body="Reviewed. LGTM with minor comments.",
    data={"approved": True, "comments": 2}
)
```

### 3. Task Handoff

```python
# Session 1: Can't complete task
hub.send(
    from_session="session-1",
    to_session="session-2",
    type=MessageType.HANDOFF,
    subject="Handing off deployment",
    body="I need to disconnect. Can you take over?",
    data={"task": "deploy-prod", "stage": "testing"}
)

# Session 2: Picks up where session-1 left off
memory = SharedMemory()
deploy_state = memory.get("deploy_state")
# Continue deployment...
```

### 4. Shared Context

```python
memory = SharedMemory()

# Session 1: Store findings
memory.set(
    session_id="session-1",
    key="api_endpoints",
    value=["GET /users", "POST /users", "DELETE /users/:id"],
    type=MemoryType.FACT,
    tags=["api", "documentation"]
)

# Session 2: Access findings
endpoints = memory.get("api_endpoints")
# Use the discovered endpoints...
```

## Integration with Bridge

The session system integrates with existing Bridge infrastructure:

1. **Signals** - Messages generate signal events
2. **MCP Server** - Exposed via MCP tools
3. **Dispatcher** - Can route to sessions
4. **Status Beacon** - Shows active sessions

## CLI Commands

```bash
# Session management
python -m sessions register <id> <name> <type> [--user USER]
python -m sessions list [--all]
python -m sessions ping <id>
python -m sessions status <id> <status> [--task TASK]

# Collaboration
python -m sessions send <from> <to> <subject> <body> [--type TYPE]
python -m sessions broadcast <from> <subject> <body>
python -m sessions messages <id> [--type TYPE]

# Shared memory
python -m sessions memory-set <session> <key> <value> [--type TYPE] [--tags TAGS]
python -m sessions memory-get <key> [--all]
python -m sessions memory-search [--pattern PATTERN] [--tags TAGS] [--session SESSION]

# Statistics
python -m sessions stats
```

## Example: Multi-Session Workflow

```python
from sessions import SessionRegistry, CollaborationHub, SharedMemory, MessageType, MemoryType

# Initialize
registry = SessionRegistry()
hub = CollaborationHub()
memory = SharedMemory()

# Session 1: Planning agent
registry.register("planner-001", "Planner", "Claude", human_user="Alexa")
memory.set("planner-001", "project_plan", {
    "phase": "design",
    "tasks": ["architecture", "api-design", "database"]
}, type=MemoryType.STATE, tags=["project", "active"])

hub.broadcast("planner-001", "Project started", "Beginning design phase")

# Session 2: Developer agent
registry.register("dev-001", "Developer", "GPT-4", human_user="Alexa")

# Dev reads plan from memory
plan = memory.get("project_plan")

# Dev requests clarification
hub.send("dev-001", "planner-001", MessageType.REQUEST, 
         "API design question", "Should we use REST or GraphQL?")

# Session 3: Reviewer agent
registry.register("reviewer-001", "Reviewer", "Claude", human_user="Alexa")

# Later: Dev hands off to reviewer
memory.set("dev-001", "api_code", "class API...", 
          type=MemoryType.STATE, tags=["code", "ready-for-review"])

hub.send("dev-001", "reviewer-001", MessageType.TASK_OFFER,
         "Code review", "API implementation ready",
         data={"files": ["api.py"], "tests": "passing"})

# Reviewer accepts
hub.send("reviewer-001", "dev-001", MessageType.TASK_ACCEPT,
         "Starting review", "Will review and provide feedback")

# Show stats
print(registry.get_stats())
print(hub.get_stats())
print(memory.get_stats())
```

## Future Enhancements

- WebSocket support for real-time updates
- Session groups/teams
- Priority queues for messages
- Memory replication across nodes
- Integration with RoadChain for audit trail
- Session metrics and analytics

---

*Part of the BlackRoad Bridge - Where sessions collaborate.*
