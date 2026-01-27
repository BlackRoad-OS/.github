# Blackbox-Enterprises Signals

> Signal handlers for the Enterprise org

---

## Inbound Signals (BBX receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🏢 FND → BBX` | Foundation | Enterprise lead | `sales.qualify()` |
| `⬆️ VEN → BBX` | Ventures | Upsell opportunity | `sales.review()` |
| `🔐 SEC → BBX` | Security | Security requirements | `compliance.review()` |
| `🚨 CLD → BBX` | Cloud | SLA breach risk | `sla.alert()` |

---

## Outbound Signals (BBX sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `🏢 BBX → OS` | Bridge | Enterprise activity | On milestone |
| `📝 BBX → FND` | Foundation | Proposal sent | On proposal |
| `✅ BBX → FND` | Foundation | Deal closed | On close |
| `🎯 BBX → OS` | Bridge | SLA alert | On threshold |
| `🤝 BBX → OS` | Bridge | Customer success | On milestone |

---

## Sales Cycle Signals

```
# Lead qualified
🏢 BBX → OS : lead_qualified, company="BigCorp", value=$100K, stage=discovery

# Discovery complete
🔍 BBX → OS : discovery_complete, company="BigCorp", pain_points=[...]

# Proposal sent
📝 BBX → FND : proposal_sent, company="BigCorp", value=$100K

# Security review
🔐 BBX → SEC : security_review_requested, company="BigCorp"
✅ SEC → BBX : security_review_passed, company="BigCorp"

# Deal closed
✅ BBX → FND : deal_closed, company="BigCorp", value=$100K, term=1y, arr=+$100K
```

---

## Onboarding Signals

```
# Kickoff
🚀 BBX → OS : onboarding_started, customer="BigCorp", csm="Alice"

# Milestones
📊 BBX → OS : onboarding_progress, customer="BigCorp", phase="technical", progress=60%

# Go-live
🎉 BBX → OS : customer_live, customer="BigCorp", time_to_value=28d
```

---

## SLA Signals

```
# SLA status
📊 BBX → OS : sla_status, customer="BigCorp", uptime=99.95%, target=99.9%

# SLA warning
⚠️ BBX → OS : sla_warning, customer="BigCorp", metric=uptime, current=99.85%, target=99.9%

# SLA breach
🚨 BBX → OS : sla_breach, customer="BigCorp", metric=uptime, actual=99.7%, target=99.9%
🚨 BBX → FND : sla_credit, customer="BigCorp", amount=$5000

# Incident
🔥 BBX → OS : incident_started, customer="BigCorp", severity=P1
✅ BBX → OS : incident_resolved, customer="BigCorp", duration=45m
```

---

## Customer Success Signals

```
# Health score
📊 BBX → OS : health_score, customer="BigCorp", score=85, trend=up

# Expansion opportunity
📈 BBX → VEN : expansion_opportunity, customer="BigCorp", potential=$50K

# Renewal
🔄 BBX → FND : renewal_upcoming, customer="BigCorp", value=$100K, date=2027-01-15
✅ BBX → FND : renewal_closed, customer="BigCorp", value=$120K, growth=20%

# Churn risk
⚠️ BBX → OS : churn_risk, customer="BigCorp", score=0.7, reasons=[...]
```

---

*Enterprise signals drive the big deals.*
