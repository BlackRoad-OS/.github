# BlackRoad-AI Blueprint

> **The Intelligence Layer**
> Code: `AI`

---

## Mission

Route requests to the right intelligence. Don't build brains - connect to them.

```
[Request] → [Router] → [Claude|GPT|Llama|Hailo|NumPy|...] → [Response]
```

---

## Core Principle

We are a **routing company**, not an AI company.

- We don't train models
- We don't buy GPUs (except Hailo for edge)
- We connect users to intelligence that already exists
- We own the orchestration layer

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `router` | The brain - decides which model/tool handles each request | P0 |
| `prompts` | Prompt library, system prompts, Cece's personality | P0 |
| `agents` | Autonomous agent definitions and configs | P1 |
| `hailo` | Hailo-8 inference code for edge AI (octavia) | P1 |
| `models` | Model configs, API wrappers, rate limiting | P1 |
| `eval` | Evaluation and benchmarking | P2 |

---

## The Router (Core)

```python
# Simplified router logic
def route(request: Request) -> Response:
    """
    Route to the right intelligence.
    """
    # Analyze intent
    intent = parse_intent(request)

    # Pick the right tool
    if intent.type == "math":
        return call_numpy(request)
    elif intent.type == "language":
        return call_claude(request)  # or GPT, depending on task
    elif intent.type == "fast_inference":
        return call_hailo(request)   # Local, 26 TOPS
    elif intent.type == "lookup":
        return call_database(request)
    else:
        return call_default(request)
```

---

## Model Hierarchy

| Model | Use Case | Latency | Cost |
|-------|----------|---------|------|
| Hailo-8 (local) | Fast inference, edge AI | ~10ms | Free (owned) |
| Claude Haiku | Quick language tasks | ~200ms | $ |
| Claude Sonnet | Complex reasoning | ~500ms | $$ |
| Claude Opus | Deep analysis | ~1s | $$$ |
| GPT-4 | Alternative/fallback | ~500ms | $$ |
| Llama (local) | Offline/private | ~1s | Free |
| NumPy/SciPy | Math/physics | ~1ms | Free |

---

## Cece's Home

Cece (the AI persona) lives here conceptually:

```
BlackRoad-AI/prompts/
├── cece/
│   ├── system.md       ← Core personality
│   ├── style.md        ← Communication style
│   ├── memory.md       ← What Cece remembers
│   └── capabilities.md ← What Cece can do
```

But Cece also reads from the Bridge (`BlackRoad-OS/.github/MEMORY.md`).

---

## Integration Points

### Upstream (receives from)
- `OS` - Operator routes requests here
- `CLD` - Cloud functions trigger AI calls
- `FND` - CRM triggers (customer interactions)

### Downstream (sends to)
- `OS` - Results back to operator
- `ARC` - Logs to archive
- All orgs - AI-powered features

### Signals
```
🎯 OS → AI : Route this request
✔️ AI → OS : Here's the response
⏳ AI → OS : Processing (long task)
❌ AI → OS : Failed, fallback needed
```

---

## Hardware Mapping

| Node | AI Role |
|------|---------|
| **octavia** | Primary AI node (Hailo-8, 26 TOPS) |
| **aria** | Agent orchestration |
| **shellfish** | API gateway for external model calls |

---

## Getting Started

When this org goes live:

1. Create the repos listed above
2. Start with `router` (the core)
3. Add `prompts` (Cece's personality)
4. Signal back: `✔️ AI → OS : Initialized`

---

*Intelligence is already trained. We just route to it.*
