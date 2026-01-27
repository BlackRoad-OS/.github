# BlackRoad-Gov Signals

> Signal handlers for the Governance org

---

## Inbound Signals (GOV receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `📜 * → GOV` | Any | Submit proposal | `proposals.create()` |
| `🗳️ * → GOV` | Any | Cast vote | `voting.cast()` |
| `💰 FND → GOV` | Foundation | Budget request | `treasury.review()` |

---

## Outbound Signals (GOV sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `📜 GOV → OS` | Bridge | Proposal submitted | On create |
| `🗳️ GOV → ALL` | Broadcast | Voting open | On vote start |
| `✅ GOV → ALL` | Broadcast | Proposal passed | On pass |
| `❌ GOV → ALL` | Broadcast | Proposal rejected | On reject |
| `⚖️ GOV → *` | Target org | Enforce decision | On implement |

---

## Proposal Lifecycle Signals

```
# Submission
📜 GOV → OS : proposal_submitted, id=BRIP-42, title="New Feature"

# Review period
👀 GOV → ALL : review_open, id=BRIP-42, duration=7d

# Voting
🗳️ GOV → ALL : voting_open, id=BRIP-42, duration=3d, type=simple_majority
📊 GOV → OS : voting_progress, id=BRIP-42, yes=65%, no=35%, turnout=45%

# Result
✅ GOV → ALL : proposal_passed, id=BRIP-42, yes=72%, turnout=61%
# or
❌ GOV → ALL : proposal_rejected, id=BRIP-42, yes=48%, turnout=55%

# Implementation
⚖️ GOV → AI : implement_brip, id=BRIP-42
✔️ AI → GOV : brip_implemented, id=BRIP-42
```

---

## Treasury Signals

```
# Budget proposal
💰 GOV → OS : budget_proposal, amount=$5000, purpose="Infrastructure"

# Spending approval
✅ GOV → FND : spending_approved, amount=$5000, recipient=vendor_x

# Report
📊 GOV → OS : treasury_report, balance=$50000, spent_mtd=$3000
```

---

## Election Signals

```
# Election announced
🗳️ GOV → ALL : election_announced, position=council, nominations_open=7d

# Candidates
👤 GOV → ALL : candidate_nominated, position=council, candidate=alice

# Voting
🗳️ GOV → ALL : election_voting_open, position=council, duration=3d

# Results
🏆 GOV → ALL : election_results, position=council, winner=alice, votes=234
```

---

*Governance signals are the voice of the community.*
