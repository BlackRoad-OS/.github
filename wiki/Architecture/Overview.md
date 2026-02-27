# Architecture Overview

> **The big picture: How BlackRoad works.**

---

## The Vision

BlackRoad is a **routing company**, not an AI company. We don't build intelligence - we route to it.

```
Traditional AI Company:
  Build Model → Host Model → Serve Model → Monetize

BlackRoad:
  Route Request → Find Best Service → Connect User → Monetize
```

**Key Insight**: Intelligence is becoming commoditized. The value is in knowing which intelligence to use and when.

---

## The Three Layers

```
┌─────────────────────────────────────────────────────┐
│                   LAYER 3: USER                     │
│              Applications & Interfaces              │
├─────────────────────────────────────────────────────┤
│                   LAYER 2: BRIDGE                   │
│           Routing, Coordination, Memory             │
├─────────────────────────────────────────────────────┤
│               LAYER 1: ORGANIZATIONS                │
│           15 Specialized Domains                    │
└─────────────────────────────────────────────────────┘
```

### Layer 1: Organizations (15 Domains)

Specialized organizations for different capabilities:

- **BlackRoad-OS**: The Bridge, mesh, control plane
- **BlackRoad-AI**: AI/ML routing and aggregation
- **BlackRoad-Cloud**: Edge compute, Cloudflare workers
- **BlackRoad-Hardware**: Pi cluster, IoT devices, Hailo-8
- **BlackRoad-Labs**: R&D and experiments
- **BlackRoad-Security**: Auth, secrets, zero trust
- **BlackRoad-Foundation**: CRM, billing, Salesforce/Stripe
- **BlackRoad-Media**: Content, blog, social
- **BlackRoad-Interactive**: Gaming, metaverse, 3D
- **BlackRoad-Education**: Learning platform, tutorials
- **BlackRoad-Gov**: Governance, voting, policies
- **BlackRoad-Archive**: Storage, backup, preservation
- **BlackRoad-Studio**: Design system, UI/UX
- **BlackRoad-Ventures**: Marketplace, investments
- **Blackbox-Enterprises**: Stealth enterprise projects

### Layer 2: The Bridge

The Bridge (`BlackRoad-OS/.github`) is the central coordination point.

**Components:**
- **Operator**: Routes requests to appropriate organization
- **Memory**: Persistent context across sessions
- **Signals**: Agent coordination protocol
- **Streams**: Data flow patterns (upstream/instream/downstream)
- **Status**: Real-time health beacon

**Why Git?**
- Version controlled coordination
- Distributed by default
- Survives disconnects
- Human-readable

### Layer 3: User Interface

**Current:**
- CLI tools (operator, metrics, explorer)
- GitHub interfaces (repos, issues, PRs)
- Direct API access

**Future:**
- Web dashboard
- Mobile app
- Metaverse interface (long-term vision)

---

## Core Patterns

### Pattern 1: Routing

```
Request → Operator → Organization → Service → Response
```

**Example:**
```bash
User: "What's the weather in SF?"
  ↓
Operator: Classifies as AI request (95%)
  ↓
BlackRoad-AI: Routes to weather service
  ↓
Response: "72°F, sunny"
```

### Pattern 2: Signals

Agents communicate via signals:

```
✔️ AI → OS : route_complete, service=openai, latency=234ms
```

**Signal Format:**
```
[ICON] [FROM] → [TO] : [ACTION], [metadata...]
```

See the `SIGNALS.md` document in the main repository for the full protocol.

### Pattern 3: Streams

Data flows through three stages:

1. **Upstream**: Data entering BlackRoad
   - API requests
   - Webhook events
   - User inputs

2. **Instream**: Internal processing
   - Routing
   - Transformation
   - Coordination

3. **Downstream**: Data leaving BlackRoad
   - API responses
   - External service calls
   - User outputs

See [Streams](../STREAMS.md) for details.

### Pattern 4: Memory

Persistent context survives disconnects:

```bash
Session 1:
  → Build feature X
  → Update MEMORY.md

[Disconnect]

Session 2:
  → Read MEMORY.md
  → Continue feature X
```

---

## Key Components

### The Operator

**Purpose**: Route requests to the right organization.

**Components:**
1. **Parser**: Extracts intent from request
2. **Classifier**: Determines which org can handle it
3. **Router**: Selects best org (with confidence score)
4. **Emitter**: Sends signal with routing decision

**Algorithm:**
```python
def route(request):
    intent = parser.parse(request)
    scores = classifier.score_all_orgs(intent)
    best_org = max(scores, key=lambda x: x.confidence)
    emitter.signal(f"✔️ OS → {best_org.code} : routed")
    return best_org
```

See [The Operator](Operator) for deep dive.

### The Bridge Files

| File | Purpose |
|------|---------|
| `INDEX.md` | Navigation hub |
| `MEMORY.md` | Persistent context |
| `.STATUS` | Real-time health |
| `SIGNALS.md` | Coordination protocol |
| `STREAMS.md` | Data flow patterns |
| `REPO_MAP.md` | Ecosystem structure |
| `BLACKROAD_ARCHITECTURE.md` | Vision document |

### Organization Blueprints

Each org has:
- `README.md`: Mission, vision, architecture
- `REPOS.md`: List of repositories
- `SIGNALS.md`: Signal patterns

**Location**: `orgs/[ORG-NAME]/`

---

## Data Flow Example

### User Request: "Deploy my app to production"

```
1. USER
   │
   ▼
2. UPSTREAM
   │ API Gateway receives request
   │ Webhook triggers deployment
   │
   ▼
3. BRIDGE (INSTREAM)
   │ Operator parses: "deploy" action
   │ Classifier scores: Cloud=90%, OS=70%
   │ Router selects: BlackRoad-Cloud
   │ Signal: 📡 OS → CLD : deploy_requested
   │
   ▼
4. ORGANIZATION
   │ BlackRoad-Cloud receives request
   │ Determines: Cloudflare Workers deployment
   │ Signal: ✔️ CLD → OS : deploying, worker=api
   │
   ▼
5. DOWNSTREAM
   │ Cloudflare API called
   │ Worker deployed to edge
   │ Signal: ✔️ CLD → OS : deployed, url=api.blackroad.dev
   │
   ▼
6. RESPONSE
   │ Status returned to user
   │ Metrics updated
   │ Memory recorded
```

---

## Scaling Model

### Business Model

- **Base**: $1/user/month
- **Scale**: 1M users = $1M/month = $12M/year
- **Target**: 100M users = $1.2B/year

### Technical Scale

**Edge Compute:**
- Cloudflare Workers (serverless, global)
- 200+ data centers
- Auto-scaling

**Hardware:**
- Pi cluster for critical services
- Own the hardware, rent nothing critical
- 4 nodes: lucidia, octavia, aria, alice

**AI Routing:**
- Don't host models
- Route to best service (OpenAI, Anthropic, Cohere, etc.)
- Aggregate responses

---

## Security Architecture

### Zero Trust Model

- No implicit trust
- Always verify
- Least privilege access

### Secrets Management

- Vault for secrets
- Rotation policies
- No secrets in git

### Authentication

- OAuth 2.0 / OIDC
- Multi-factor authentication
- Session management

See [BlackRoad-Security](../Orgs/BlackRoad-Security) for details.

---

## Technology Stack

### Languages

- **Python**: Operator, metrics, prototypes
- **JavaScript/TypeScript**: Cloudflare Workers, frontend
- **Go**: High-performance services (future)

### Infrastructure

- **GitHub**: Code, coordination, CI/CD
- **Cloudflare**: Edge compute, CDN, DNS
- **Raspberry Pi**: Critical services, local compute

### Integrations

- **Salesforce**: CRM, customer data
- **Stripe**: Billing, payments
- **Google Drive**: Document sync
- **GitHub**: Code hosting, automation

See [Integrations](../Integrations/Salesforce) for guides.

---

## Design Principles

1. **Route, Don't Build**: Use existing services when possible
2. **Own Critical Infrastructure**: Pi cluster for core services
3. **Git-Based Coordination**: The Bridge lives in git
4. **Signal Everything**: All actions emit signals
5. **Memory Persists**: Context survives disconnects
6. **15 Organizations**: Specialized domains, not monoliths
7. **Edge First**: Cloudflare for global distribution
8. **$1/User/Month**: Simple, scalable pricing

---

## Future Architecture

### Phase 1: Current (CLI + Git)
- Operator prototype
- Manual routing
- Git-based coordination

### Phase 2: API Layer (2026)
- REST/GraphQL APIs
- Automated routing
- Webhook integrations

### Phase 3: Web Dashboard (2026)
- Real-time monitoring
- Organization management
- User interface

### Phase 4: Metaverse (Long-term)
- 3D interface
- Spatial computing
- VR/AR experiences

---

## Learn More

- **[The Bridge](Bridge)** - Central coordination details
- **[The Operator](Operator)** - Routing engine deep dive
- **[Organizations](../Orgs/BlackRoad-OS)** - Explore the 15 orgs
- **[Signals](../SIGNALS.md)** - Coordination protocol

---

*Architecture is destiny. Route wisely.*
