# BlackRoad-Foundation Signals

> Signal handlers for the Foundation org

---

## Inbound Signals (FND receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `👤 CLD → FND` | Cloud | New signup | `crm.create_customer()` |
| `🔍 OS → FND` | Bridge | Customer lookup | `crm.get_customer()` |
| `💳 CLD → FND` | Cloud | Payment webhook | `billing.process_webhook()` |
| `🔄 OS → FND` | Bridge | Force sync | `salesforce.sync()` |

---

## Outbound Signals (FND sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `👤 FND → OS` | Bridge | New customer | On signup |
| `💰 FND → OS` | Bridge | Payment success | On payment |
| `⚠️ FND → OS` | Bridge | Payment failed | On failure |
| `📉 FND → OS` | Bridge | Churn alert | On cancel |
| `🔄 FND → OS` | Bridge | Sync complete | After sync |
| `📊 FND → OS` | Bridge | Metrics update | Daily |

---

## Customer Lifecycle Signals

```
# Signup
👤 FND → OS : customer_created, id=123, plan=free, source=organic

# Upgrade
⬆️ FND → OS : customer_upgraded, id=123, from=free, to=pro

# Payment
💰 FND → OS : payment_success, id=123, amount=$12, mrr_delta=+$1

# Usage milestone
🎯 FND → OS : usage_milestone, id=123, requests=10000

# Churn risk
⚠️ FND → OS : churn_risk, id=123, score=0.8, reason=inactive_14d

# Churned
📉 FND → OS : customer_churned, id=123, reason=voluntary, mrr_delta=-$1
```

---

## Salesforce Sync Signals

```
# Scheduled sync
🔄 FND → OS : sf_sync_started, type=daily
📊 FND → OS : sf_sync_progress, contacts=1200/5000, leads=800/2000
✔️ FND → OS : sf_sync_complete, duration=12m, records=7000

# Real-time sync
⚡ FND → OS : sf_realtime, object=Contact, action=update, id=003xxx

# Sync error
❌ FND → OS : sf_sync_error, object=Lead, error=rate_limited
```

---

## Billing Signals

```
# Subscription
💳 FND → OS : subscription_created, customer=123, plan=pro
💳 FND → OS : subscription_renewed, customer=123, plan=pro
💳 FND → OS : subscription_canceled, customer=123, reason=...

# Invoice
📄 FND → OS : invoice_created, customer=123, amount=$12
💰 FND → OS : invoice_paid, customer=123, amount=$12
⚠️ FND → OS : invoice_failed, customer=123, attempt=2/3

# Revenue
📊 FND → OS : revenue_daily, mrr=$50000, new=$500, churned=$200
```

---

## Metrics Signals

```
# Daily metrics
📊 FND → OS : metrics_daily, {
  "mrr": 50000,
  "customers": 5000,
  "new_today": 50,
  "churned_today": 5,
  "churn_rate": 0.1,
  "ltv": 120
}

# Alert thresholds
🚨 FND → OS : metric_alert, metric=churn_rate, value=6%, threshold=5%
```

---

*Foundation signals are the heartbeat of the business.*
