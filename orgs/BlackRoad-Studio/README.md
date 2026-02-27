# BlackRoad-Studio Blueprint

> **The Creative Layer**
> Code: `STU`

---

## Mission

Design with purpose. Create with joy. Ship with pride.

```
[Vision] → [Design] → [Prototype] → [Polish] → [Ship]
```

---

## Core Principle

**Design is how it works, not just how it looks.**

- Function drives form
- Consistency builds trust
- Accessibility is non-negotiable
- Delight is in the details

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `design-system` | Components, tokens, guidelines | P0 |
| `ui` | UI component library | P0 |
| `icons` | Icon library | P1 |
| `themes` | Color themes, dark mode | P1 |
| `prototypes` | Design prototypes | P2 |
| `illustrations` | Custom illustrations | P2 |

---

## Design System

```
┌─────────────────────────────────────────────────────────┐
│                   DESIGN SYSTEM                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   TOKENS          COMPONENTS       PATTERNS              │
│   ───────         ──────────       ────────              │
│   • Colors        • Button         • Forms               │
│   • Typography    • Input          • Navigation          │
│   • Spacing       • Card           • Data display        │
│   • Shadows       • Modal          • Feedback            │
│   • Motion        • Table          • Layouts             │
│                                                          │
│   Variables →     Building    →    Complete              │
│   that change     blocks           solutions             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Design Tokens

```css
/* Colors -- BlackRoad Brand */
--sunrise-orange:    #FF9D00;
--warm-orange:       #FF6B00;
--hot-pink:          #FF0066;  /* PRIMARY */
--electric-magenta:  #FF006B;
--deep-magenta:      #D600AA;
--vivid-purple:      #7700FF;
--cyber-blue:        #0066FF;

/* Neutral */
--color-background: #000000;
--color-surface:    #1A1A1A;
--color-text:       #FFFFFF;
--color-text-muted: #888888;

/* Semantic */
--color-success: #00CC66;
--color-warning: #FF9D00;
--color-error:   #FF0066;

/* Gradients */
--gradient-br:           linear-gradient(180deg, #FF9D00 0%, #FF0066 75%);
--gradient-os:           linear-gradient(180deg, #FF006B 0%, #0066FF 100%);
--gradient-full-spectrum: linear-gradient(180deg, #FF9D00 0%, #FF0066 28%, #7700FF 71%, #0066FF 100%);

/* Typography */
--font-primary: 'JetBrains Mono', monospace;
--font-mono:    'JetBrains Mono', monospace;

/* Spacing (Golden Ratio φ = 1.618) */
--space-xs:  8px;
--space-sm:  13px;
--space-md:  21px;
--space-lg:  34px;
--space-xl:  55px;
--space-2xl: 89px;

/* Motion */
--duration-fast:   100ms;
--duration-normal: 200ms;
--duration-slow:   300ms;
--easing: cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Accessibility Standards

| Requirement | Standard |
|-------------|----------|
| Color contrast | WCAG AA (4.5:1 text) |
| Keyboard nav | Full support |
| Screen readers | ARIA labels |
| Motion | Respect prefers-reduced-motion |
| Focus | Visible focus indicators |

---

## Integration Points

### Upstream (receives from)
- `OS` - Feature requirements
- `MED` - Brand guidelines
- `INT` - 3D/VR requirements

### Downstream (sends to)
- All orgs - Design components
- `CLD` - Built components
- `MED` - Visual assets

### Signals
```
🎨 STU → OS : Design updated
🧩 STU → ALL : Component released
📐 STU → OS : Token changed
🖼️ STU → MED : Asset created
```

---

## Design Principles

1. **Clarity** - Remove confusion, not features
2. **Consistency** - Same problem, same solution
3. **Efficiency** - Fewer clicks, faster results
4. **Delight** - Small moments of joy
5. **Accessibility** - Everyone can use it

---

*Studio is where ideas become interfaces.*
