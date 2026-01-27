# GitHub Integration

> **Code, CI/CD, automation.**

---

## Overview

GitHub is BlackRoad's code hosting and automation platform.

**Organization**: [BlackRoad-OS](../Orgs/BlackRoad-OS)  
**Status**: Active

---

## Features

- **Repositories**: Code hosting
- **Actions**: CI/CD workflows
- **Projects**: Task management
- **Wiki**: Documentation (you're reading it!)
- **Codespaces**: Cloud development

---

## GitHub Actions

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install && npm run build
```

---

## Template

Full guide at: `templates/github-ecosystem/`

---

*Code. Automate. Ship.*
