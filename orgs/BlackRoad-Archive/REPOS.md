# BlackRoad-Archive Repositories

> Repo specs for the Archive org

---

## Repository List

### `storage` (P0 - Build First)

**Purpose:** Storage backends and APIs

**Structure:**
```
storage/
├── src/
│   ├── backends/
│   │   ├── r2.py          ← Cloudflare R2
│   │   ├── kv.py          ← Cloudflare KV
│   │   ├── s3.py          ← AWS S3 compatible
│   │   └── glacier.py     ← AWS Glacier
│   ├── api/
│   │   ├── store.py       ← Store data
│   │   ├── retrieve.py    ← Get data
│   │   └── delete.py      ← Soft delete
│   ├── tiering/
│   │   └── policy.py      ← Auto-tier data
│   └── encryption/
│       └── at_rest.py
├── configs/
│   └── storage.yaml
└── README.md
```

---

### `backup` (P0 - Build First)

**Purpose:** Backup strategies and automation

**Structure:**
```
backup/
├── src/
│   ├── jobs/
│   │   ├── database.py    ← DB backups
│   │   ├── configs.py     ← Config backups
│   │   └── full.py        ← Full system backup
│   ├── scheduler/
│   │   └── cron.py
│   ├── verify/
│   │   └── integrity.py   ← Backup verification
│   └── restore/
│       └── restore.py
├── scripts/
│   ├── backup.sh
│   └── restore.sh
└── README.md
```

---

### `search` (P1)

**Purpose:** Search and retrieval

**Structure:**
```
search/
├── src/
│   ├── indexer/
│   │   └── index.py       ← Build search index
│   ├── query/
│   │   └── search.py      ← Query interface
│   ├── engines/
│   │   ├── meilisearch.py
│   │   └── elasticsearch.py
│   └── api/
│       └── search_api.py
└── README.md
```

---

### `retention` (P1)

**Purpose:** Data retention policies

**Structure:**
```
retention/
├── policies/
│   ├── user-data.yaml
│   ├── logs.yaml
│   ├── audit.yaml
│   └── legal.yaml
├── src/
│   ├── enforcer/
│   │   └── policy.py      ← Enforce policies
│   ├── legal-hold/
│   │   └── hold.py        ← Legal holds
│   └── gdpr/
│       └── delete.py      ← GDPR deletion
└── README.md
```

---

### `migration` (P2)

**Purpose:** Data migration tools

**Structure:**
```
migration/
├── src/
│   ├── tier/
│   │   └── migrate.py     ← Tier migration
│   ├── format/
│   │   └── convert.py     ← Format conversion
│   └── bulk/
│       └── transfer.py    ← Bulk transfers
├── scripts/
│   └── migrate.sh
└── README.md
```

---

## Storage Costs (Cloudflare R2)

| Operation | Cost |
|-----------|------|
| Storage | $0.015/GB/month |
| Class A (write) | $4.50/million |
| Class B (read) | $0.36/million |
| Egress | Free! |

**R2 Advantage:** Zero egress fees = huge savings at scale

---

*Archive repos are where data goes to live forever.*
