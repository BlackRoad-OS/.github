# BlackRoad-Gov Repositories

> Repo specs for the Governance org

---

## Repository List

### `proposals` (P0 - Build First)

**Purpose:** BlackRoad Improvement Proposals (BRIPs)

**Structure:**
```
proposals/
├── brips/
│   ├── brip-0001-governance.md
│   ├── brip-0002-token.md
│   └── ...
├── templates/
│   ├── brip-template.md
│   └── rfc-template.md
├── process/
│   └── how-to-propose.md
└── README.md
```

**BRIP States:**
- `draft` - Being written
- `review` - Open for feedback
- `voting` - Active vote
- `accepted` - Passed
- `rejected` - Failed
- `implemented` - Done

---

### `voting` (P1)

**Purpose:** Voting mechanisms and tools

**Structure:**
```
voting/
├── src/
│   ├── mechanisms/
│   │   ├── simple-majority.py
│   │   ├── supermajority.py
│   │   └── ranked-choice.py
│   ├── verification/
│   │   └── audit.py
│   └── ui/
│       └── ballot.py
├── contracts/         ← Future: on-chain voting
└── README.md
```

---

### `constitution` (P1)

**Purpose:** Core rules and principles

**Structure:**
```
constitution/
├── core/
│   ├── mission.md
│   ├── values.md
│   └── principles.md
├── rules/
│   ├── decision-making.md
│   ├── membership.md
│   └── amendments.md
├── history/
│   └── changes.md
└── README.md
```

---

### `treasury` (P2)

**Purpose:** Budget and financial governance

**Structure:**
```
treasury/
├── budget/
│   ├── 2026.md
│   └── ...
├── spending/
│   └── log.md
├── proposals/
│   └── ...
├── reports/
│   ├── quarterly/
│   └── annual/
└── README.md
```

---

### `elections` (P2)

**Purpose:** Leadership elections

**Structure:**
```
elections/
├── positions/
│   └── council.md
├── candidates/
│   └── ...
├── results/
│   └── ...
├── process/
│   └── how-elections-work.md
└── README.md
```

---

## Proposal Categories

| Category | Scope | Threshold |
|----------|-------|-----------|
| Technical | Code changes | Simple majority |
| Process | How we work | Simple majority |
| Financial | Budget >$1000 | Supermajority |
| Constitutional | Core rules | Unanimous |
| Emergency | Urgent issues | Council only |

---

*Governance repos are where democracy meets code.*
