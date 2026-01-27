# BlackRoad-Archive Blueprint

> **The Memory Layer**
> Code: `ARC`

---

## Mission

Store everything. Forget nothing. Retrieve instantly.

```
[Data] → [Store] → [Index] → [Retrieve] → [Analyze]
```

---

## Core Principle

**Data is the new oil. Archives are the refinery.**

- Nothing gets deleted, only archived
- Everything is searchable
- Multiple redundancy levels
- Time-travel through history

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `storage` | Storage backends, APIs | P0 |
| `backup` | Backup strategies, scripts | P0 |
| `search` | Search and retrieval | P1 |
| `retention` | Retention policies | P1 |
| `migration` | Data migration tools | P2 |

---

## Storage Tiers

```
┌─────────────────────────────────────────────────────────┐
│                    STORAGE TIERS                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   HOT         │  WARM        │  COLD        │  GLACIER  │
│   (instant)   │  (seconds)   │  (minutes)   │  (hours)  │
│               │              │              │           │
│   • Active    │  • Recent    │  • Old       │  • Legal  │
│     data      │    logs      │    backups   │    holds  │
│   • Cache     │  • Last 30d  │  • Last year │  • 7+ yrs │
│               │              │              │           │
│   KV/Redis    │  S3/R2      │  R2 IA      │  Glacier  │
│               │              │              │           │
│   $$$$        │  $$$         │  $$          │  $        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Backup Strategy

| Data Type | Frequency | Retention | Location |
|-----------|-----------|-----------|----------|
| Database | Hourly | 30 days | R2 |
| Configs | On change | Forever | Git |
| Logs | Daily | 1 year | R2 → Glacier |
| User data | Hourly | Forever | R2 |
| Secrets | On rotation | 90 days | Encrypted |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ALL ORGS                              │
│                       │                                  │
│                       ▼                                  │
│              ┌─────────────────┐                        │
│              │  ARCHIVE API    │                        │
│              └────────┬────────┘                        │
│                       │                                  │
│         ┌─────────────┼─────────────┐                   │
│         ▼             ▼             ▼                   │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│    │   HOT   │  │  WARM   │  │  COLD   │              │
│    │   KV    │  │   R2    │  │ Glacier │              │
│    └─────────┘  └─────────┘  └─────────┘              │
│         │             │             │                   │
│         └─────────────┼─────────────┘                   │
│                       ▼                                  │
│              ┌─────────────────┐                        │
│              │  SEARCH INDEX   │                        │
│              │  (Meilisearch)  │                        │
│              └─────────────────┘                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Integration Points

### Upstream (receives from)
- All orgs - Data to archive
- `SEC` - Audit logs
- `FND` - Financial records
- `GOV` - Governance records

### Downstream (sends to)
- All orgs - Retrieved data
- `AI` - Historical context
- `LAB` - Research data

### Signals
```
📦 ARC → OS : Data archived
🔍 ARC → * : Search results
♻️ ARC → OS : Data migrated to cold
⚠️ ARC → OS : Storage alert
```

---

## Retention Policies

| Data Class | Hot | Warm | Cold | Delete |
|------------|-----|------|------|--------|
| User data | 7d | 30d | 1y | Never |
| Logs | 1d | 30d | 1y | 7y |
| Audit | 7d | 90d | 7y | Never |
| Backups | 1d | 7d | 30d | 1y |
| Legal | - | - | - | Never |

---

*The archive remembers everything so we don't have to.*
