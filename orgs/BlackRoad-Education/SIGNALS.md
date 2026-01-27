# BlackRoad-Education Signals

> Signal handlers for the Education org

---

## Inbound Signals (EDU receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `📝 LAB → EDU` | Labs | Research to document | `docs.draft()` |
| `🆕 * → EDU` | Any | New feature to document | `docs.create()` |
| `❓ FND → EDU` | Foundation | Support question → FAQ | `faq.add()` |
| `📊 MED → EDU` | Media | Content analytics | `improve()` |

---

## Outbound Signals (EDU sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `📚 EDU → OS` | Bridge | Docs updated | On publish |
| `🎓 EDU → OS` | Bridge | Course published | On course |
| `✅ EDU → FND` | Foundation | User completed path | On completion |
| `🚀 EDU → CLD` | Cloud | Deploy docs site | On update |

---

## Learning Signals

```
# Course progress
📖 EDU → OS : course_started, user=123, course=quickstart
📊 EDU → OS : course_progress, user=123, course=quickstart, progress=60%
✅ EDU → OS : course_completed, user=123, course=quickstart, time=25m

# Achievement
🏆 EDU → OS : badge_earned, user=123, badge=first_route
🎓 EDU → OS : certification_earned, user=123, cert=developer
```

---

## Documentation Signals

```
# Doc updates
📚 EDU → OS : docs_updated, section=guides, pages=3
📝 EDU → OS : doc_created, path=/docs/guides/new-feature

# Coverage
📊 EDU → OS : doc_coverage, total=95%, missing=[feature_x, feature_y]
```

---

## Feedback Signals

```
# User feedback
👍 EDU → OS : feedback_positive, page=/docs/quickstart
👎 EDU → OS : feedback_negative, page=/docs/api, issue="unclear"

# FAQ
❓ EDU → OS : faq_added, question="How do I...?", source=support
```

---

*Education signals measure understanding.*
