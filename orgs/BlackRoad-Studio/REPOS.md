# BlackRoad-Studio Repositories

> Repo specs for the Studio org

---

## Repository List

### `design-system` (P0 - Build First)

**Purpose:** Design tokens, guidelines, documentation

**Structure:**
```
design-system/
├── tokens/
│   ├── colors.json
│   ├── typography.json
│   ├── spacing.json
│   ├── shadows.json
│   └── motion.json
├── guidelines/
│   ├── principles.md
│   ├── accessibility.md
│   ├── responsive.md
│   └── dark-mode.md
├── assets/
│   ├── logos/
│   └── fonts/
├── build/
│   ├── css/
│   └── js/
└── README.md
```

---

### `ui` (P0 - Build First)

**Purpose:** React/Vue component library

**Structure:**
```
ui/
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.styles.ts
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   ├── Card/
│   │   ├── Modal/
│   │   ├── Table/
│   │   └── ...
│   ├── hooks/
│   ├── utils/
│   └── index.ts
├── stories/              ← Storybook
│   └── ...
├── package.json
└── README.md
```

---

### `icons` (P1)

**Purpose:** Custom icon library

**Structure:**
```
icons/
├── src/
│   ├── svg/
│   │   ├── arrow-right.svg
│   │   ├── check.svg
│   │   └── ...
│   ├── react/           ← React components
│   └── sprite.svg       ← SVG sprite
├── build/
│   ├── icons.css
│   └── icons.js
└── README.md
```

---

### `themes` (P1)

**Purpose:** Color themes and dark mode

**Structure:**
```
themes/
├── themes/
│   ├── light.json
│   ├── dark.json
│   └── system.json
├── src/
│   ├── provider.tsx     ← Theme provider
│   └── hooks.ts         ← useTheme hook
└── README.md
```

---

### `prototypes` (P2)

**Purpose:** Design prototypes and experiments

**Structure:**
```
prototypes/
├── figma/
│   └── links.md         ← Figma file links
├── html/
│   └── ...              ← HTML prototypes
├── experiments/
│   └── ...
└── README.md
```

---

### `illustrations` (P2)

**Purpose:** Custom illustrations and graphics

**Structure:**
```
illustrations/
├── svg/
│   ├── hero/
│   ├── empty-states/
│   └── features/
├── source/              ← Source files (Figma, etc)
└── README.md
```

---

## Component Standards

Every component needs:
- [ ] TypeScript types
- [ ] Accessibility (ARIA)
- [ ] Keyboard support
- [ ] Dark mode support
- [ ] Storybook story
- [ ] Unit tests
- [ ] Documentation

---

*Studio repos turn design into code.*
