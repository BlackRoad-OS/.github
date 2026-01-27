# BlackRoad-Ventures Signals

> Signal handlers for the Ventures org

---

## Inbound Signals (VEN receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🏪 * → VEN` | Any | Marketplace listing | `marketplace.list()` |
| `💳 CLD → VEN` | Cloud | Payment received | `orders.process()` |
| `🤝 FND → VEN` | Foundation | Partner inquiry | `partnerships.review()` |

---

## Outbound Signals (VEN sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `💰 VEN → FND` | Foundation | Sale completed | On purchase |
| `🤝 VEN → OS` | Bridge | Partnership signed | On agreement |
| `📈 VEN → OS` | Bridge | Revenue milestone | On milestone |
| `🏪 VEN → OS` | Bridge | New listing | On list |
| `💸 VEN → FND` | Foundation | Payout processed | On payout |

---

## Sales Signals

```
# Purchase
💰 VEN → FND : sale, product="routing-plugin", price=$29, buyer=user_123

# Subscription
🔄 VEN → FND : subscription_started, plan=pro, user=123, mrr=+$10
🔄 VEN → FND : subscription_renewed, plan=pro, user=123
🔄 VEN → FND : subscription_canceled, plan=pro, user=123, mrr=-$10

# Enterprise
🏢 VEN → FND : enterprise_deal, company="Acme", value=$50000, term=1y
```

---

## Marketplace Signals

```
# Listing
🏪 VEN → OS : listing_created, type=plugin, name="AI Router Pro", creator=dev_456

# Review
⭐ VEN → OS : review_added, product="AI Router Pro", rating=5, reviewer=user_789

# Payout
💸 VEN → FND : creator_payout, creator=dev_456, amount=$290, period=Jan_2026
```

---

## Partnership Signals

```
# Partner inquiry
📨 VEN → OS : partner_inquiry, company="BigCorp", type=integration

# Agreement signed
🤝 VEN → OS : partnership_signed, partner="BigCorp", type=reseller, share=30%

# Partner revenue
💰 VEN → FND : partner_revenue, partner="BigCorp", amount=$5000
```

---

## Milestone Signals

```
# Revenue milestone
📈 VEN → OS : milestone, type=mrr, value=$10000, date=2026-01-27

# Customer milestone
👥 VEN → OS : milestone, type=customers, value=1000, date=2026-01-27

# GMV milestone
💰 VEN → OS : milestone, type=gmv, value=$100000, date=2026-01-27
```

---

## Affiliate Signals

```
# Referral
🔗 VEN → OS : affiliate_referral, affiliate=aff_123, referred=user_456

# Conversion
💰 VEN → OS : affiliate_conversion, affiliate=aff_123, sale=$10

# Payout
💸 VEN → FND : affiliate_payout, affiliate=aff_123, amount=$200
```

---

*Ventures signals track the money.*
