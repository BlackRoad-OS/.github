# BlackRoad-Studio Signals

> Signal handlers for the Studio org

---

## Inbound Signals (STU receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🎨 OS → STU` | Bridge | Design needed | `design.create()` |
| `🐛 * → STU` | Any | Design bug | `bugs.fix()` |
| `📐 MED → STU` | Media | Brand update | `tokens.update()` |

---

## Outbound Signals (STU sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `🎨 STU → OS` | Bridge | Design ready | On complete |
| `🧩 STU → ALL` | Broadcast | Component released | On release |
| `📐 STU → ALL` | Broadcast | Token changed | On token update |
| `🖼️ STU → MED` | Media | Asset created | On asset |
| `📦 STU → CLD` | Cloud | Package published | On publish |

---

## Design Signals

```
# Design started
🎨 STU → OS : design_started, feature="user_settings"

# Design ready
✅ STU → OS : design_ready, feature="user_settings", figma_link=...

# Design feedback
💬 STU → OS : design_feedback_requested, feature="user_settings"
```

---

## Component Signals

```
# Component created
🧩 STU → ALL : component_created, name="Button", version="1.0.0"

# Component updated
🔄 STU → ALL : component_updated, name="Button", version="1.1.0", breaking=false

# Breaking change
⚠️ STU → ALL : component_breaking, name="Modal", version="2.0.0", migration_guide=...

# Package published
📦 STU → CLD : package_published, name="@blackroad/ui", version="1.5.0"
```

---

## Token Signals

```
# Token added
📐 STU → ALL : token_added, name="color-accent", value="#0066FF"

# Token changed
📐 STU → ALL : token_changed, name="color-primary", old="#0055DD", new="#0066FF"

# Token deprecated
⚠️ STU → ALL : token_deprecated, name="color-old", replacement="color-new"
```

---

## Asset Signals

```
# Asset created
🖼️ STU → MED : asset_created, type="illustration", name="hero-image"

# Icon added
✨ STU → ALL : icon_added, name="settings", variants=["outline", "solid"]
```

---

*Studio signals announce what's beautiful and new.*
