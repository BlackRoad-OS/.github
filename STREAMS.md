# BlackRoad Streams

> Data flows like water. Know the streams.

---

## The Three Streams

```
    UPSTREAM              INSTREAM              DOWNSTREAM
    ────────              ────────              ──────────

    Inputs                Processing            Outputs
    Requests              Routing               Responses
    Questions             Thinking              Answers
    Raw data              Transform             Clean data
    User intent           Decisions             Actions

         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │  PULL   │   ──►   │ PROCESS │   ──►   │  PUSH   │
    └─────────┘         └─────────┘         └─────────┘
```

---

## Stream Definitions

### UPSTREAM (Inputs)

Everything that flows INTO the system.

| Source | Type | Example |
|--------|------|---------|
| Users | Requests | "What's the weather?" |
| APIs | Data | Salesforce contacts, GitHub issues |
| Sensors | Telemetry | ESP32 readings, LoRa packets |
| Webhooks | Events | Stripe payments, GitHub pushes |
| Cron | Scheduled | Daily syncs, hourly checks |
| You (Alexa) | Commands | Conversations via Claude Code |

### INSTREAM (Processing)

Where decisions happen. The OPERATOR lives here.

| Process | What It Does |
|---------|--------------|
| Parse | Understand the input |
| Route | Decide who handles it |
| Transform | Convert between formats |
| Validate | Check correctness |
| Enrich | Add context |
| Log | Record for audit trail |

### DOWNSTREAM (Outputs)

Everything that flows OUT of the system.

| Destination | Type | Example |
|-------------|------|---------|
| Users | Responses | Answers, confirmations |
| APIs | Updates | SF record updates, GitHub commits |
| Nodes | Commands | Pi tasks, Hailo inference jobs |
| Storage | Persistence | Database writes, file saves |
| Ledger | Audit | RoadChain entries |
| You (Alexa) | Reports | Status updates, completions |

---

## Stream Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         .github (BRIDGE)                          │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                        INSTREAM                             │  │
│  │                                                             │  │
│  │   ┌─────────┐    ┌──────────┐    ┌─────────┐             │  │
│  │   │  Parse  │───►│  Route   │───►│ Execute │             │  │
│  │   └─────────┘    └──────────┘    └─────────┘             │  │
│  │                       │                                    │  │
│  │                       ▼                                    │  │
│  │                  ┌──────────┐                             │  │
│  │                  │ OPERATOR │                             │  │
│  │                  └──────────┘                             │  │
│  │                                                             │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                    │
│       ▲                                           │                │
│       │                                           ▼                │
│  ┌────┴────┐                                ┌─────────┐           │
│  │UPSTREAM │                                │DOWNSTREAM│           │
│  └─────────┘                                └─────────┘           │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
         ▲                                           │
         │                                           ▼
┌────────┴────────┐                        ┌─────────────────┐
│    EXTERNAL     │                        │    EXTERNAL     │
│                 │                        │                 │
│ • Cloudflare    │                        │ • Pi Nodes      │
│ • Salesforce    │                        │ • APIs          │
│ • GitHub        │                        │ • Users         │
│ • Users         │                        │ • Storage       │
│ • Webhooks      │                        │ • Ledger        │
└─────────────────┘                        └─────────────────┘
```

---

## Cece's Role (That's Me)

I sit at the center of the streams:

```
                    ┌─────────────────┐
                    │                 │
    UPSTREAM ──────►│      CECE       │──────► DOWNSTREAM
                    │                 │
                    │  • Understand   │
                    │  • Plan         │
                    │  • Execute      │
                    │  • Report       │
                    │                 │
                    └─────────────────┘
```

**What I do:**

1. **Pull upstream** - Read issues, check status, receive your commands
2. **Process instream** - Think, plan, make decisions
3. **Push downstream** - Write code, create files, trigger actions
4. **Report back** - Tell you what happened

---

## Stream Examples

### Example 1: You Ask Me to Build Something

```
UPSTREAM:   You: "Create a new API endpoint"
INSTREAM:   Cece: Parse → Plan → Write code
DOWNSTREAM: Push to repo → Create PR → Notify you
```

### Example 2: Webhook Triggers Action

```
UPSTREAM:   GitHub webhook: "New issue created"
INSTREAM:   Operator: Route → Assign to Cece
DOWNSTREAM: Cece: Analyze → Respond → Update issue
```

### Example 3: Scheduled Sync

```
UPSTREAM:   Cron: "Daily Salesforce sync"
INSTREAM:   lucidia: Pull SF data → Transform
DOWNSTREAM: Update local DB → Log to ledger
```

---

## Stream Commands

When we're working together, think in streams:

| Command | Stream | What Happens |
|---------|--------|--------------|
| `pull` | Upstream | Fetch latest from sources |
| `sync` | Upstream | Bidirectional sync |
| `process` | Instream | Run transformations |
| `route` | Instream | Decide destinations |
| `push` | Downstream | Send to targets |
| `deploy` | Downstream | Ship to production |
| `report` | Downstream | Send status to you |

---

## The Golden Rule

> **Everything is a stream.**
>
> Data flows in, gets processed, flows out.
> The OPERATOR routes the streams.
> The BRIDGE (.github) is where we watch them flow.
>
> Simple. Scalable. Ours.

---

*Last Updated: 2026-01-27*
*Flow state: Active*
