# BlackRoad-Media Repositories

> Repo specs for the Media org

---

## Repository List

### `blog` (P0 - Build First)

**Purpose:** Blog posts and announcements

**Structure:**
```
blog/
├── posts/
│   ├── 2026/
│   │   ├── 01-welcome.md
│   │   ├── 02-architecture.md
│   │   └── ...
│   └── drafts/
├── templates/
│   ├── post.md
│   └── announcement.md
├── assets/
│   └── images/
├── config/
│   └── blog.yaml
└── README.md
```

**Post Format:**
```markdown
---
title: Post Title
date: 2026-01-27
author: Alexa
tags: [architecture, vision]
---

# Post Title

Content here...
```

---

### `docs` (P0 - Build First)

**Purpose:** Public documentation

**Structure:**
```
docs/
├── getting-started/
│   ├── quickstart.md
│   ├── installation.md
│   └── first-steps.md
├── guides/
│   ├── routing.md
│   ├── deployment.md
│   └── ...
├── reference/
│   ├── api.md
│   ├── cli.md
│   └── config.md
├── concepts/
│   ├── architecture.md
│   ├── streams.md
│   └── signals.md
└── README.md
```

**Powered by:** Deployed via BlackRoad-Cloud/pages

---

### `brand` (P1)

**Purpose:** Brand assets and guidelines

**Structure:**
```
brand/
├── logos/
│   ├── primary/
│   │   ├── blackroad-logo.svg
│   │   ├── blackroad-logo.png
│   │   └── blackroad-logo-white.svg
│   ├── icons/
│   └── variations/
├── colors/
│   └── palette.md
├── typography/
│   └── fonts.md
├── guidelines/
│   ├── usage.md
│   ├── voice.md
│   └── examples/
└── README.md
```

**Color Palette:**
- Primary: `#000000` (Black)
- Secondary: `#FFFFFF` (White)
- Accent: `#0066FF` (Electric Blue)

---

### `social` (P1)

**Purpose:** Social media content

**Structure:**
```
social/
├── templates/
│   ├── twitter/
│   ├── linkedin/
│   └── threads/
├── scheduled/
│   └── 2026-01/
├── evergreen/
│   └── tips/
├── assets/
│   └── graphics/
└── README.md
```

---

### `video` (P2)

**Purpose:** Video content and tutorials

**Structure:**
```
video/
├── scripts/
│   ├── tutorials/
│   └── demos/
├── assets/
│   ├── thumbnails/
│   └── b-roll/
├── published/
│   └── links.md
└── README.md
```

---

### `press` (P2)

**Purpose:** Press kit and media resources

**Structure:**
```
press/
├── kit/
│   ├── press-release-template.md
│   ├── fact-sheet.md
│   ├── founder-bio.md
│   └── logos/              ← High-res logos
├── coverage/
│   └── mentions.md         ← Press mentions
├── contacts/
│   └── media.md
└── README.md
```

---

## Content Calendar

| Day | Content Type |
|-----|--------------|
| Mon | Technical blog post |
| Tue | Social engagement |
| Wed | Documentation update |
| Thu | Community spotlight |
| Fri | Week in review |

---

## Publishing Flow

```
[Draft] → [Review] → [Edit] → [Publish] → [Promote]
    │         │         │         │           │
    ▼         ▼         ▼         ▼           ▼
  Write    Feedback   Polish    Deploy      Share
```

---

*Media repos tell the BlackRoad story.*
