# Organization Blueprints

> **The Bridge holds the blueprints. Orgs pull their specs from here.**

---

## The Pattern

```
BlackRoad-OS/.github/orgs/
├── BlackRoad-OS/       ← Meta! The Bridge blueprints itself
├── BlackRoad-AI/       ← Blueprint for AI org
├── BlackRoad-Cloud/    ← Blueprint for Cloud org
├── BlackRoad-Labs/     ← Blueprint for Labs org
└── ...                 ← All 15 orgs have blueprints here
```

When a new org spins up:
1. Check the blueprint here
2. Create the repos defined in the spec
3. Pull initial configs from the blueprint
4. Signal back to Bridge: `✔️ [ORG] → OS : Initialized`

---

## Blueprint Structure

Each org blueprint contains:

```
orgs/[OrgName]/
├── README.md           ← What this org does
├── REPOS.md            ← What repos should exist
├── STRUCTURE.md        ← Directory/file structure specs
└── SIGNALS.md          ← Org-specific signal handlers
```

---

## Org Status

| Org | Code | Blueprint | Live |
|-----|------|-----------|------|
| BlackRoad-OS | `OS` | ✔️ (you're in it) | ✔️ |
| BlackRoad-AI | `AI` | ✔️ | 💤 |
| BlackRoad-Cloud | `CLD` | ✔️ | 💤 |
| BlackRoad-Labs | `LAB` | ✔️ | 💤 |
| BlackRoad-Security | `SEC` | ✔️ | 💤 |
| BlackRoad-Foundation | `FND` | ✔️ | 💤 |
| BlackRoad-Media | `MED` | ✔️ | 💤 |
| BlackRoad-Hardware | `HW` | ✔️ | 💤 |
| BlackRoad-Interactive | `INT` | ✔️ | 💤 |
| BlackRoad-Education | `EDU` | ✔️ | 💤 |
| BlackRoad-Gov | `GOV` | ✔️ | 💤 |
| BlackRoad-Archive | `ARC` | ✔️ | 💤 |
| BlackRoad-Studio | `STU` | ✔️ | 💤 |
| BlackRoad-Ventures | `VEN` | ✔️ | 💤 |
| Blackbox-Enterprises | `BBX` | ✔️ | 💤 |

---

*Blueprints are truth. Orgs are instances.*
