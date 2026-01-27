# BlackRoad-Ventures Repositories

> Repo specs for the Ventures org

---

## Repository List

### `marketplace` (P1)

**Purpose:** Product marketplace platform

**Structure:**
```
marketplace/
├── src/
│   ├── api/
│   │   ├── listings.py    ← Product listings
│   │   ├── orders.py      ← Order management
│   │   ├── reviews.py     ← Reviews/ratings
│   │   └── payouts.py     ← Creator payouts
│   ├── models/
│   │   ├── product.py
│   │   ├── order.py
│   │   └── creator.py
│   └── services/
│       ├── search.py
│       └── recommendation.py
├── frontend/
│   └── ...
└── README.md
```

**Product Types:**
- Plugins (routing extensions)
- Templates (starter configs)
- Agents (pre-built agents)
- Services (professional services)

---

### `commerce` (P1)

**Purpose:** E-commerce building blocks

**Structure:**
```
commerce/
├── src/
│   ├── cart/
│   │   └── cart.py
│   ├── checkout/
│   │   └── checkout.py
│   ├── payments/
│   │   ├── stripe.py
│   │   └── crypto.py
│   ├── shipping/
│   │   └── calculator.py
│   └── tax/
│       └── calculator.py
└── README.md
```

---

### `partnerships` (P2)

**Purpose:** Partner integrations and management

**Structure:**
```
partnerships/
├── integrations/
│   ├── salesforce/
│   ├── slack/
│   ├── notion/
│   └── ...
├── partner-portal/
│   └── ...
├── agreements/
│   └── templates/
└── README.md
```

---

### `affiliate` (P2)

**Purpose:** Affiliate program

**Structure:**
```
affiliate/
├── src/
│   ├── tracking/
│   │   └── links.py
│   ├── commissions/
│   │   └── calculate.py
│   ├── payouts/
│   │   └── payout.py
│   └── dashboard/
│       └── stats.py
└── README.md
```

**Commission Structure:**
- 20% first year
- 10% ongoing
- 30 day cookie

---

### `ventures` (P2)

**Purpose:** Business experiments

**Structure:**
```
ventures/
├── experiments/
│   ├── api-marketplace/
│   │   ├── hypothesis.md
│   │   ├── mvp/
│   │   └── results.md
│   ├── white-label/
│   │   └── ...
│   └── training/
│       └── ...
├── templates/
│   └── experiment-template.md
└── README.md
```

---

## Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 1K requests/mo, community support |
| Pro | $10/mo | 100K requests/mo, priority support |
| Team | $50/mo | 1M requests/mo, team features |
| Enterprise | Custom | Unlimited, SLA, dedicated support |

---

## Marketplace Economics

| Party | Share |
|-------|-------|
| Creator | 90% |
| BlackRoad | 10% |
| Payment processor | ~3% (from BlackRoad share) |

---

*Ventures repos turn features into revenue.*
