# Stripe Billing

> **Payments, subscriptions, invoices. The $1/user/month engine.**

```
Org: BlackRoad-Foundation (FND)
Node: lucidia
Model: $1/user/month subscriptions
```

---

## What It Does

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Customer  │  ────→  │   Stripe    │  ────→  │  BlackRoad  │
│   Payment   │         │   Process   │ webhook │   Handle    │
└─────────────┘         └─────────────┘         └─────────────┘
```

1. **Products & Prices** - Define what you sell
2. **Customers** - Track who's paying
3. **Subscriptions** - Recurring revenue
4. **Invoices** - Billing records
5. **Webhooks** - Real-time payment events

---

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your Stripe keys

# Initialize products
python -m stripe_billing.cli setup

# Start webhook server
python -m stripe_billing.cli webhook --port 8000
```

---

## The $1/User/Month Model

```python
# Product setup
PRODUCTS = {
    "blackroad_basic": {
        "name": "BlackRoad Basic",
        "price": 100,  # cents
        "interval": "month",
        "features": ["API access", "1 workspace"]
    },
    "blackroad_pro": {
        "name": "BlackRoad Pro",
        "price": 500,
        "interval": "month",
        "features": ["API access", "10 workspaces", "Priority support"]
    },
    "blackroad_enterprise": {
        "name": "BlackRoad Enterprise",
        "price": None,  # Custom
        "interval": "month",
        "features": ["Everything", "SLA", "Dedicated support"]
    }
}
```

---

## Data Models

### Customer
```python
@dataclass
class Customer:
    id: str                    # cus_xxx
    email: str
    name: Optional[str]
    metadata: Dict[str, str]   # blackroad_user_id, etc.
    created: datetime

    # Computed
    subscriptions: List[Subscription]
    mrr: int  # Monthly recurring revenue in cents
```

### Subscription
```python
@dataclass
class Subscription:
    id: str                    # sub_xxx
    customer_id: str
    status: str                # active, canceled, past_due
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool

    items: List[SubscriptionItem]

    @property
    def is_active(self) -> bool:
        return self.status in ("active", "trialing")
```

### Invoice
```python
@dataclass
class Invoice:
    id: str                    # in_xxx
    customer_id: str
    subscription_id: Optional[str]
    status: str                # draft, open, paid, void
    amount_due: int            # cents
    amount_paid: int
    created: datetime
    due_date: Optional[datetime]
```

---

## Webhook Events

| Event | Signal | Action |
|-------|--------|--------|
| `customer.subscription.created` | `📦 FND → OS` | Provision access |
| `customer.subscription.deleted` | `📦 FND → OS` | Revoke access |
| `invoice.paid` | `💰 FND → OS` | Record payment |
| `invoice.payment_failed` | `⚠️ FND → OS` | Alert, retry |
| `customer.created` | `👤 FND → OS` | Sync customer |

---

## API Usage

```python
from stripe_billing import StripeClient, Customer, Subscription

client = StripeClient()

# Create customer
customer = client.customers.create(
    email="user@example.com",
    name="Jane Doe",
    metadata={"blackroad_id": "usr_123"}
)

# Create subscription
subscription = client.subscriptions.create(
    customer_id=customer.id,
    price_id="price_xxx",  # $1/month price
)

# Check status
if subscription.is_active:
    grant_access(customer.metadata["blackroad_id"])

# Cancel at period end
client.subscriptions.cancel(
    subscription.id,
    cancel_at_period_end=True
)

# Get MRR
mrr = client.metrics.mrr()
print(f"MRR: ${mrr / 100:,.2f}")
```

---

## CLI Commands

```bash
# Setup products and prices
stripe_billing setup

# List customers
stripe_billing customers list

# Get customer details
stripe_billing customers get cus_xxx

# Create subscription
stripe_billing subscriptions create --customer cus_xxx --price price_xxx

# MRR report
stripe_billing metrics mrr
# MRR: $4,523.00 (4,523 active subscriptions)

# Start webhook server
stripe_billing webhook --port 8000
```

---

## Directory Structure

```
stripe-billing/
├── stripe_billing/
│   ├── __init__.py
│   ├── models/
│   │   ├── customer.py
│   │   ├── subscription.py
│   │   ├── invoice.py
│   │   └── price.py
│   ├── client.py          ← Stripe API wrapper
│   ├── webhooks.py        ← Webhook handlers
│   ├── metrics.py         ← MRR, churn, etc.
│   └── cli.py
├── config.yaml
├── .env.example
└── requirements.txt
```

---

## Signals

```
💰 FND → OS : payment_received, customer=cus_xxx, amount=$100
📦 FND → OS : subscription_started, customer=cus_xxx, plan=basic
⚠️ FND → OS : payment_failed, customer=cus_xxx, retry=1
📊 FND → OS : mrr_update, mrr=$4523, change=+$100
🎉 FND → OS : milestone, mrr=$10000
```

---

*$1 at a time. Scale to millions.*
