# Design Tools Integration

> **Figma, Canva, and the visual layer of BlackRoad.**

```
Org: BlackRoad-Studio (STU)
Tools: Figma, Canva, Adobe CC
Output: Components, assets, brand
```

---

## The Design Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     DESIGN ECOSYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                      FIGMA                          │  │
│   │  Design System • UI Components • Prototypes         │  │
│   └─────────────────────────────────────────────────────┘  │
│                            ↓                                │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                      CANVA                          │  │
│   │  Social Media • Marketing • Quick Graphics          │  │
│   └─────────────────────────────────────────────────────┘  │
│                            ↓                                │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                    EXPORTS                          │  │
│   │  SVG • PNG • PDF • React Components • CSS           │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Figma

### Organization Structure

```
BlackRoad Design (Team)
├── 🎨 Design System
│   ├── Foundations
│   │   ├── Colors
│   │   ├── Typography
│   │   ├── Spacing
│   │   └── Grid
│   ├── Components
│   │   ├── Buttons
│   │   ├── Forms
│   │   ├── Cards
│   │   ├── Navigation
│   │   └── Modals
│   └── Patterns
│       ├── Layouts
│       ├── Data Display
│       └── Feedback
│
├── 🖥️ Products
│   ├── Dashboard
│   ├── Marketing Site
│   ├── Mobile App
│   └── Admin Panel
│
├── 🎭 Brand
│   ├── Logos
│   ├── Icons
│   ├── Illustrations
│   └── Photography Guidelines
│
└── 📐 Templates
    ├── Presentation Deck
    ├── Social Media
    └── Print Materials
```

### Design Tokens

```jsonc
// tokens.json (exported from Figma -- BlackRoad brand)
{
  "colors": {
    "brand": {
      "sunrise-orange":    "#FF9D00",
      "warm-orange":       "#FF6B00",
      "hot-pink":          "#FF0066",
      "electric-magenta":  "#FF006B",
      "deep-magenta":      "#D600AA",
      "vivid-purple":      "#7700FF",
      "cyber-blue":        "#0066FF"
    },
    "neutral": {
      "0":    "#ffffff",
      "50":   "#f8fafc",
      "900":  "#0f172a",
      "1000": "#000000"
    },
    "success": "#22c55e",
    "warning": "#FF9D00",
    "error":   "#FF0066"
  },
  "gradients": {
    "br":           "linear-gradient(180deg, #FF9D00 0%, #FF0066 75%)",
    "os":           "linear-gradient(180deg, #FF006B 0%, #0066FF 100%)",
    "full-spectrum": "linear-gradient(180deg, #FF9D00 0%, #FF0066 28%, #7700FF 71%, #0066FF 100%)"
  },
  "typography": {
    "fontFamily": {
      "primary": "JetBrains Mono, monospace",
      "mono":    "JetBrains Mono, monospace"
    },
    "fontSize": {
      "xs":  "0.75rem",
      "sm":  "0.875rem",
      "base": "1rem",
      "lg":  "1.125rem",
      "xl":  "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem"
    }
  },
  "spacing": {
    "xs":  "8px",
    "sm":  "13px",
    "md":  "21px",
    "lg":  "34px",
    "xl":  "55px",
    "2xl": "89px"
  },
  "borderRadius": {
    "none": "0",
    "sm":   "0.25rem",
    "md":   "0.5rem",
    "lg":   "1rem",
    "full": "9999px"
  }
}
```

### Figma API Usage

```python
import requests

FIGMA_TOKEN = "xxx"
FILE_KEY = "abc123"

headers = {"X-Figma-Token": FIGMA_TOKEN}

# Get file info
response = requests.get(
    f"https://api.figma.com/v1/files/{FILE_KEY}",
    headers=headers
)
file_data = response.json()

# Get specific node
response = requests.get(
    f"https://api.figma.com/v1/files/{FILE_KEY}/nodes",
    params={"ids": "1:2,1:3"},
    headers=headers
)

# Export as PNG
response = requests.get(
    f"https://api.figma.com/v1/images/{FILE_KEY}",
    params={
        "ids": "1:2",
        "format": "png",
        "scale": 2
    },
    headers=headers
)
image_urls = response.json()["images"]

# Get comments
response = requests.get(
    f"https://api.figma.com/v1/files/{FILE_KEY}/comments",
    headers=headers
)
comments = response.json()["comments"]
```

### Export Automation

```python
# figma_export.py
from figma_api import FigmaClient

client = FigmaClient(token="xxx")

# Export all icons as SVG
icons = client.get_components(
    file_key="abc123",
    name_pattern="icon/*"
)

for icon in icons:
    svg = client.export(icon.id, format="svg")
    with open(f"assets/icons/{icon.name}.svg", "w") as f:
        f.write(svg)

# Export design tokens
tokens = client.get_styles(file_key="abc123")
with open("tokens.json", "w") as f:
    json.dump(tokens.to_dict(), f, indent=2)

# Signal completion
print("🎨 STU → OS : assets_exported, count=", len(icons))
```

---

## Canva

### Workspace Structure

```
BlackRoad Brand Kit
├── 🎨 Brand Colors
│   ├── Primary:   #FF0066  (Hot Pink)
│   ├── Secondary: #7700FF  (Vivid Purple)
│   ├── Accent:    #FF9D00  (Sunrise Orange)
│   └── Gradient:  #FF9D00 → #FF0066 → #7700FF → #0066FF
│
├── 🔤 Brand Fonts
│   ├── Primary: JetBrains Mono
│   └── Mono:    JetBrains Mono
│
├── 🖼️ Logos
│   ├── Full Logo
│   ├── Icon Only
│   └── Wordmark
│
└── 📐 Templates
    ├── Social Media
    │   ├── Twitter Post
    │   ├── LinkedIn Post
    │   ├── Instagram Story
    │   └── YouTube Thumbnail
    ├── Presentations
    │   └── Pitch Deck
    └── Documents
        ├── One-Pager
        └── Report
```

### Canva API

```python
# Canva Connect API
import requests

CANVA_TOKEN = "xxx"
headers = {"Authorization": f"Bearer {CANVA_TOKEN}"}

# Create design from template
response = requests.post(
    "https://api.canva.com/v1/designs",
    headers=headers,
    json={
        "template_id": "DAFxxx",
        "title": "Q1 Report",
        "brand_template_data": {
            "title": "Q1 2026 Report",
            "subtitle": "BlackRoad Metrics"
        }
    }
)
design = response.json()

# Export design
response = requests.post(
    f"https://api.canva.com/v1/designs/{design['id']}/export",
    headers=headers,
    json={"format": "pdf"}
)
export_url = response.json()["url"]
```

---

## Asset Pipeline

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Figma   │ ──→ │  Export  │ ──→ │ Optimize │ ──→ │  Deploy  │
│  Design  │     │  Assets  │     │  (SVGO)  │     │   CDN    │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                      │
                      ▼
               ┌──────────┐
               │  GitHub  │
               │   Repo   │
               └──────────┘
```

### GitHub Action for Asset Sync

```yaml
# .github/workflows/sync-assets.yml
name: Sync Design Assets

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Export from Figma
        env:
          FIGMA_TOKEN: ${{ secrets.FIGMA_TOKEN }}
        run: |
          python scripts/figma_export.py

      - name: Optimize SVGs
        run: |
          npx svgo assets/icons/*.svg

      - name: Commit changes
        run: |
          git config user.name "Asset Bot"
          git config user.email "bot@blackroad.ai"
          git add assets/
          git diff --staged --quiet || git commit -m "🎨 Update design assets"
          git push
```

---

## Component Library

### React Components from Figma

```tsx
// components/Button.tsx
// Auto-generated from Figma

import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors font-mono',
  {
    variants: {
      variant: {
        primary: 'bg-brand-primary text-white hover:bg-brand-primary-strong',
        secondary: 'bg-brand-secondary text-white hover:bg-brand-secondary-strong',
        ghost: 'hover:bg-neutral-100 text-brand-primary',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      className={buttonVariants({ variant, size, className })}
      {...props}
    />
  );
}
```

### CSS Variables from Tokens

```css
/* styles/tokens.css */
/* Auto-generated from Figma tokens -- BlackRoad brand */

:root {
  /* Brand Colors */
  --sunrise-orange:    #FF9D00;
  --warm-orange:       #FF6B00;
  --hot-pink:          #FF0066;  /* PRIMARY */
  --electric-magenta:  #FF006B;
  --deep-magenta:      #D600AA;
  --vivid-purple:      #7700FF;
  --cyber-blue:        #0066FF;

  /* Neutral */
  --color-neutral-0:   #ffffff;
  --color-neutral-900: #0f172a;
  --color-black:       #000000;

  /* Gradients */
  --gradient-br:           linear-gradient(180deg, #FF9D00 0%, #FF0066 75%);
  --gradient-os:           linear-gradient(180deg, #FF006B 0%, #0066FF 100%);
  --gradient-full-spectrum: linear-gradient(180deg, #FF9D00 0%, #FF0066 28%, #7700FF 71%, #0066FF 100%);

  /* Typography */
  --font-primary: 'JetBrains Mono', monospace;
  --font-mono:    'JetBrains Mono', monospace;

  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;

  /* Spacing (Golden Ratio φ = 1.618) */
  --space-xs:  8px;
  --space-sm:  13px;
  --space-md:  21px;
  --space-lg:  34px;
  --space-xl:  55px;
  --space-2xl: 89px;

  /* Radius */
  --radius-sm:   0.25rem;
  --radius-md:   0.5rem;
  --radius-lg:   1rem;
  --radius-full: 9999px;
}
```

---

## Signals

```
🎨 STU → OS : design_updated, file="Design System", page="Buttons"
💬 STU → OS : comment_added, file="Dashboard", author="alexa"
📤 STU → OS : assets_exported, count=24, format="svg"
🖼️ STU → OS : canva_design_created, template="Social Post"
🔄 STU → OS : tokens_synced, changes=["colors.primary.500"]
```

---

## Quick Commands

```bash
# Export Figma assets
python -m design_tools.figma export --file abc123 --output ./assets

# Sync design tokens
python -m design_tools.tokens sync --source figma --output ./tokens

# Generate React components
python -m design_tools.codegen --tokens ./tokens.json --output ./components

# Optimize assets
npx svgo -f ./assets/icons -o ./assets/icons-optimized
```

---

*Design is how it works.*
