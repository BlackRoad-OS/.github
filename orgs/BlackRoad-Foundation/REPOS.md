# BlackRoad-Foundation Repositories

> Repo specs for the Foundation org

---

## Repository List

### `salesforce` (P0 - Build First)

**Purpose:** Salesforce integration and sync

**Structure:**
```
salesforce/
├── src/
│   ├── client/
│   │   ├── auth.py        ← OAuth to Salesforce
│   │   ├── api.py         ← REST API client
│   │   └── bulk.py        ← Bulk API for sync
│   ├── sync/
│   │   ├── contacts.py    ← Contact sync
│   │   ├── leads.py       ← Lead sync
│   │   ├── opportunities.py
│   │   └── scheduler.py   ← Sync scheduler
│   ├── cache/
│   │   └── kv.py          ← Cloudflare KV cache
│   └── webhooks/
│       └── outbound.py    ← SF outbound messages
├── configs/
│   ├── objects.yaml       ← Objects to sync
│   └── fields.yaml        ← Field mappings
├── deploy/
│   └── lucidia.sh         ← Deploy to lucidia
└── README.md
```

**Runs on:** lucidia (Pi 5)
**API Budget:** 15,000 calls/day

---

### `billing` (P0 - Build First)

**Purpose:** Stripe integration, subscriptions

**Structure:**
```
billing/
├── src/
│   ├── stripe/
│   │   ├── client.py      ← Stripe client
│   │   ├── customers.py   ← Customer management
│   │   ├── subscriptions.py
│   │   ├── invoices.py
│   │   └── webhooks.py    ← Stripe webhooks
│   ├── plans/
│   │   ├── free.py
│   │   ├── pro.py
│   │   └── enterprise.py
│   ├── metering/
│   │   └── usage.py       ← Usage tracking
│   └── reports/
│       └── revenue.py
├── configs/
│   └── plans.yaml
└── README.md
```

---

### `crm` (P1)

**Purpose:** Customer data models and APIs

**Structure:**
```
crm/
├── src/
│   ├── models/
│   │   ├── customer.py
│   │   ├── organization.py
│   │   └── subscription.py
│   ├── api/
│   │   ├── customers.py   ← CRUD endpoints
│   │   └── search.py      ← Search customers
│   └── events/
│       └── publisher.py   ← Customer events
├── schemas/
│   └── customer.json
└── README.md
```

---

### `analytics` (P1)

**Purpose:** Business metrics and dashboards

**Structure:**
```
analytics/
├── src/
│   ├── metrics/
│   │   ├── mrr.py         ← MRR calculation
│   │   ├── churn.py       ← Churn analysis
│   │   ├── ltv.py         ← LTV calculation
│   │   └── cohorts.py     ← Cohort analysis
│   ├── dashboards/
│   │   └── executive.py   ← Executive dashboard
│   └── reports/
│       ├── weekly.py
│       └── monthly.py
└── README.md
```

---

### `support` (P2)

**Purpose:** Customer support and ticketing

**Structure:**
```
support/
├── src/
│   ├── tickets/
│   │   ├── create.py
│   │   ├── assign.py
│   │   └── resolve.py
│   ├── knowledge/
│   │   └── search.py      ← Knowledge base
│   └── chat/
│       └── widget.py      ← Chat widget
└── README.md
```

---

### `legal` (P2)

**Purpose:** Contracts and compliance

**Structure:**
```
legal/
├── documents/
│   ├── terms-of-service.md
│   ├── privacy-policy.md
│   ├── dpa.md             ← Data processing
│   └── sla.md             ← Service level
├── contracts/
│   └── templates/
│       ├── enterprise.md
│       └── reseller.md
└── README.md
```

---

## Salesforce Object Mapping

| SF Object | Local Table | Sync Frequency |
|-----------|-------------|----------------|
| Contact | customers | Real-time + daily |
| Lead | leads | Hourly |
| Opportunity | deals | Real-time |
| Account | organizations | Daily |

---

*Foundation repos are where revenue meets code.*
