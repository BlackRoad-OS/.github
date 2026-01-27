# BlackRoad-Labs Blueprint

> **The Experiment Layer**
> Code: `LAB`

---

## Mission

Break things safely. Learn fast. Ship what works.

```
[Idea] → [Experiment] → [Validate] → [Graduate to Prod Org]
```

---

## Core Principle

**Labs is where ideas go to be tested, not to die.**

- Every crazy idea gets a fair shot
- Failure is data, not defeat
- Successful experiments graduate to their proper org
- Nothing in Labs is sacred - delete freely

---

## What Lives Here

| Repo | Purpose | Lifespan |
|------|---------|----------|
| `experiments` | Active experiments | Temporary |
| `prototypes` | Working proofs-of-concept | Until graduation |
| `research` | Papers, notes, findings | Permanent |
| `sandbox` | Quick tests, throwaway code | Ephemeral |
| `archive` | Graduated/failed experiments | Historical |

---

## Experiment Lifecycle

```
┌─────────────┐
│   IDEA      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  SANDBOX    │  ← Quick & dirty test
│  (hours)    │
└──────┬──────┘
       │
       ├── Fails → 🗑️ Delete
       │
       ▼
┌─────────────┐
│ EXPERIMENT  │  ← Structured test
│  (days)     │
└──────┬──────┘
       │
       ├── Fails → 📝 Document why → Archive
       │
       ▼
┌─────────────┐
│ PROTOTYPE   │  ← Working demo
│  (weeks)    │
└──────┬──────┘
       │
       ├── Not viable → 📝 Document → Archive
       │
       ▼
┌─────────────┐
│ GRADUATION  │  ← Move to production org
│             │
└─────────────┘
       │
       ├── AI feature → BlackRoad-AI
       ├── Cloud feature → BlackRoad-Cloud
       ├── Hardware → BlackRoad-Hardware
       └── etc.
```

---

## Experiment Format

Every experiment has:

```
experiments/
└── YYYY-MM-experiment-name/
    ├── README.md         ← Hypothesis, approach
    ├── RESULTS.md        ← Findings
    ├── src/              ← Code
    └── data/             ← Test data
```

### README Template

```markdown
# Experiment: [Name]

## Hypothesis
What we're testing.

## Approach
How we're testing it.

## Success Criteria
How we know if it worked.

## Timeline
Expected duration.

## Status
[ ] Sandbox → [ ] Experiment → [ ] Prototype → [ ] Graduate
```

---

## Current Research Areas

| Area | Question | Status |
|------|----------|--------|
| Routing | Can we route 10K req/s on a Pi? | 🔬 |
| Edge AI | Hailo-8 latency for real-time? | 🔬 |
| Mesh | LoRa range in urban environment? | 📋 |
| Metaverse | WebXR performance on mobile? | 📋 |

---

## Integration Points

### Upstream (receives from)
- All orgs - "Can we try X?"
- `OS` - Strategic experiments

### Downstream (sends to)
- Graduating experiments → Target org
- Findings → `EDU` (education/docs)
- Failures → `ARC` (archive)

### Signals
```
🧪 LAB → OS : Starting experiment X
📊 LAB → OS : Experiment X results: [summary]
🎓 LAB → [ORG] : Graduating feature Y to [ORG]
🗑️ LAB → ARC : Archiving failed experiment Z
```

---

## Rules of Labs

1. **No production dependencies** - Labs can break
2. **Time-boxed** - Experiments have deadlines
3. **Document everything** - Even failures
4. **Delete freely** - No attachment to code
5. **Graduate quickly** - If it works, move it out

---

*The lab is where we learn. Production is where we earn.*
