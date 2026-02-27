# BlackRoad Header Template

> **The standard navigation header for all BlackRoad web properties.**

---

## Preview

```
┌──────────────────────────────────────────────────────────────┐
│ ■ BlackRoad   home   docs   agents                           │
└──────────────────────────────────────────────────────────────┘
```

Black background · JetBrains Mono · white wordmark · muted nav links

---

## Usage

Drop `index.html` into any project and include the `<header>` block:

```html
<header class="br-header">
  <a class="br-header__wordmark" href="/">BlackRoad</a>
  <nav>
    <ul class="br-header__nav">
      <li><a href="/">home</a></li>
      <li><a href="/docs">docs</a></li>
      <li><a href="/agents">agents</a></li>
    </ul>
  </nav>
</header>
```

Copy the styles from `index.html` into your project stylesheet or paste the `<style>` block into your `<head>`.

---

## Design Tokens

| Token | Value |
|-------|-------|
| Background | `#000000` |
| Wordmark color | `#ffffff` |
| Nav link color | `#999999` |
| Nav link hover | `#ffffff` |
| Font family | `JetBrains Mono, monospace` |
| Wordmark size | `1.25rem / 700` |
| Nav link size | `0.875rem / 400` |
| Padding | `21px 34px` (`--space-md` / `--space-lg`) |
| Nav gap | `34px` (`--space-lg`) |

See [BRAND.md](../../BRAND.md) for the full BlackRoad design system.

---

## Extending

Add extra nav links by appending `<li>` items inside `.br-header__nav`.

```html
<li><a href="/pricing">pricing</a></li>
```

---

*Built to the [BlackRoad Brand Guidelines](../../BRAND.md).*
