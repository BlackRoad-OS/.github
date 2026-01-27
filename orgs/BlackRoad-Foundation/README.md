# BlackRoad-Foundation Blueprint

> **The Business Layer**
> Code: `FND`

---

## Mission

Know your customers. Manage the money. Run the business.

```
[Customer] → [CRM] → [Billing] → [Revenue] → [Growth]
```

---

## Core Principle

**Salesforce is the source of truth for customers.**

- Every customer interaction logged
- Every dollar tracked
- Every metric measured
- All integrated with the operator

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `salesforce` | Salesforce integrations, sync | P0 |
| `billing` | Stripe, subscriptions, invoices | P0 |
| `crm` | Customer data models, APIs | P1 |
| `analytics` | Business metrics, dashboards | P1 |
| `support` | Ticketing, customer support | P2 |
| `legal` | Contracts, terms, compliance | P2 |

---

## Salesforce Integration

```
┌─────────────────────────────────────────────┐
│              SALESFORCE                      │
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │Contacts │  │ Leads   │  │ Opps    │    │
│  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │          │
└───────┼────────────┼────────────┼──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
              ┌──────▼──────┐
              │  SYNC JOB   │  ← Runs on lucidia
              │  (15K/day)  │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │  Local  │  │  Cache  │  │  Events │
   │   DB    │  │  (KV)   │  │  Queue  │
   └─────────┘  └─────────┘  └─────────┘
```

**Free Tier:** 15,000 API calls/day - enough for sync + real-time lookups

---

## Billing Architecture

```
[Customer] → [Signup] → [Stripe] → [Subscription]
                            │
                            ├── Webhook: payment_success
                            ├── Webhook: payment_failed
                            └── Webhook: subscription_canceled
                                    │
                                    ▼
                            [Update CRM]
```

**Pricing Model:**
- $1/user/month
- Volume discounts at scale
- Enterprise custom pricing

---

## Customer Data Model

```
Customer
├── id
├── email
├── name
├── org_id
├── plan (free|pro|enterprise)
├── status (active|churned|trial)
├── created_at
├── billing
│   ├── stripe_customer_id
│   ├── subscription_id
│   └── payment_method
├── usage
│   ├── requests_this_month
│   ├── last_active
│   └── features_used[]
└── metadata
```

---

## The Math (From Architecture Doc)

| Scale | Users | MRR | ARR |
|-------|-------|-----|-----|
| Seed | 1K | $1K | $12K |
| Early | 10K | $10K | $120K |
| Growth | 100K | $100K | $1.2M |
| Scale | 1M | $1M | $12M |
| Mega | 100M | $100M | $1.2B |
| Moon | 1B | $1B | $12B |

---

## Integration Points

### Upstream (receives from)
- `CLD` - Customer signups
- `OS` - Business queries
- External - Stripe webhooks

### Downstream (sends to)
- `OS` - Customer context for routing
- `AI` - Customer data for personalization
- `ARC` - Historical data

### Signals
```
💰 FND → OS : Payment received
👤 FND → OS : New customer signup
📉 FND → OS : Churn alert
📊 FND → OS : Monthly metrics
🔄 FND → OS : Salesforce sync complete
```

---

## Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| MRR | Monthly recurring revenue | Growing |
| Churn | % customers leaving/month | <5% |
| LTV | Lifetime value | >$24 |
| CAC | Customer acquisition cost | <$5 |
| NPS | Net promoter score | >50 |

---

*The foundation is where the business lives.*
