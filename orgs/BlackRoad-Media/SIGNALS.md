# BlackRoad-Media Signals

> Signal handlers for the Media org

---

## Inbound Signals (MED receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `📝 OS → MED` | Bridge | Write about this | `content.create()` |
| `🔬 LAB → MED` | Labs | Research to publish | `blog.draft()` |
| `📚 EDU → MED` | Education | Tutorial ready | `docs.publish()` |
| `🎉 FND → MED` | Foundation | Milestone to announce | `announce()` |

---

## Outbound Signals (MED sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `📝 MED → OS` | Bridge | Content published | On publish |
| `📢 MED → ALL` | Broadcast | Announcement | On announce |
| `🎥 MED → OS` | Bridge | Video published | On video |
| `📊 MED → OS` | Bridge | Metrics update | Weekly |
| `🚀 MED → CLD` | Cloud | Deploy site | On update |

---

## Content Lifecycle Signals

```
# Draft created
📝 MED → OS : draft_created, type=blog, title="Architecture Deep Dive"

# In review
👀 MED → OS : content_review, id=123, reviewer=alexa

# Published
🎉 MED → OS : content_published, type=blog, url=/blog/architecture

# Promoted
📢 MED → ALL : content_promoted, platforms=[twitter, linkedin]
```

---

## Announcement Signals

```
# Major announcement
📢🔴 MED → ALL : announcement, type=major, title="BlackRoad Launch"

# Feature announcement
📢🟢 MED → ALL : announcement, type=feature, title="New API"

# Community update
📢⚪ MED → ALL : announcement, type=community, title="Discord Open"
```

---

## Metrics Signals

```
# Weekly metrics
📊 MED → OS : metrics_weekly, {
  "blog_views": 5000,
  "doc_reads": 12000,
  "social_reach": 50000,
  "new_followers": 200,
  "top_post": "/blog/architecture"
}

# Viral alert
🚀 MED → OS : content_viral, url=/blog/routing, views=50000, shares=500
```

---

## Documentation Signals

```
# Docs updated
📚 MED → OS : docs_updated, section=guides, pages=5

# New guide
📖 MED → OS : guide_published, title="Getting Started", url=/docs/quickstart

# API docs
📋 MED → OS : api_docs_updated, version=v1.2
```

---

## Social Signals

```
# Post published
🐦 MED → OS : social_post, platform=twitter, engagement=0

# Engagement update
📈 MED → OS : social_engagement, platform=twitter, likes=100, retweets=25

# Mention
👋 MED → OS : social_mention, platform=twitter, user=@someone, sentiment=positive
```

---

*Media signals spread the word.*
