# Mobile SDK — Design Template

> **Approved design template for BlackRoad Mobile SDK documentation pages.**

## Usage

Copy `index.html` as the starting point for any Mobile SDK / library documentation page across BlackRoad properties.

## Sections

| Section | ID | Description |
|---|---|---|
| Nav | — | Sticky top bar with logo + nav links |
| Hero | — | Version label, title, description, metadata badges |
| Packages | `#packages` | Package grid cards (name, description, version, size) |
| Install | `#install` | Tabbed install commands (npm / yarn / pnpm) + peer deps |
| Platforms | `#platforms` | Support matrix table |
| Changelog | `#docs` | Version history entries |
| Footer | — | Org info, package count, license |

## Brand Tokens Applied

- **Font**: JetBrains Mono
- **Colors**: BlackRoad official palette (`--hot-pink`, `--cyber-blue`, `--vivid-purple`, gradients)
- **Spacing**: Golden-ratio scale (`--space-xs` → `--space-2xl`)
- **Theme**: Dark (`#0a0a0a` base)

## Customization

Replace the following values to adapt the template:

| Placeholder | Description |
|---|---|
| `Library v0.4.2` | Version label in the hero |
| `Mobile SDK` | Page title |
| Package cards | Update name, description, version, size for each package |
| Install commands | Update package scope/name |
| Peer dependencies | Add/remove as needed |
| Platform rows | Adjust version requirements and status |
| Changelog entries | Add new entries at the top |
| Footer text | Update org name, counts |
