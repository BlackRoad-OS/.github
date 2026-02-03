# TODO

> **The task board for The Bridge.**
> Track what needs doing across the BlackRoad ecosystem.

---

## How It Works

- Add tasks under the right category
- Use signal markers for status: `[ ]` open, `[x]` done, `[~]` in progress, `[!]` blocked
- The `todo-tracker` workflow auto-creates issues from `TODO:` comments in code
- Keep it honest. If it's done, check it off. If it's blocked, say why.

---

## Core Infrastructure (OS)

- [ ] Deploy operator v2 with confidence-weighted routing
- [ ] Set up Tailscale mesh between all Pi nodes
- [ ] Implement health check aggregation across nodes
- [x] Add rate limiting to dispatcher
- [ ] Create operator CLI packaging (pip install)

## Intelligence Layer (AI)

- [ ] Build AI provider failover chain (Claude -> GPT -> Llama)
- [ ] Implement prompt template registry
- [ ] Add token usage tracking per-route
- [ ] Set up Hailo-8 inference pipeline on lucidia
- [ ] Create model evaluation benchmarks

## Cloud & Edge (CLD)

- [ ] Deploy API gateway worker to Cloudflare
- [ ] Set up webhook receiver worker
- [ ] Configure Cloudflare Tunnel to Pi cluster
- [ ] Implement edge caching for common routes
- [ ] Add geo-routing rules

## Hardware (HW)

- [ ] Complete octavia node setup (Hailo-8 driver)
- [ ] Set up aria NVMe storage pool
- [ ] Flash alice with agent runtime
- [ ] Build ESP32 sensor mesh prototype
- [ ] Create node auto-discovery protocol

## Security (SEC)

- [ ] Implement API key rotation system
- [ ] Set up secrets vault (HashiCorp or SOPS)
- [ ] Add webhook signature verification
- [ ] Create audit log pipeline
- [ ] Define RBAC roles for org access

## Business Layer (FND)

- [ ] Connect Salesforce sandbox environment
- [ ] Set up Stripe test billing flow
- [ ] Build CRM sync engine prototype
- [ ] Create customer onboarding automation
- [ ] Design pricing model for routing-as-a-service

## Content & Creative (MED/STU)

- [ ] Set up docs site (Astro or Docusaurus)
- [ ] Create BlackRoad brand kit in Figma
- [ ] Build component library for dashboard UI
- [ ] Write getting-started guide for contributors
- [ ] Design system documentation

## DevOps & Automation

- [ ] Add end-to-end integration tests
- [ ] Set up staging environment
- [ ] Create release automation workflow
- [ ] Build deployment dashboard
- [ ] Add Slack/Discord notification hooks

---

## Completed

_Move items here when done._

- [x] Blueprint all 15 organizations
- [x] Build operator routing prototype
- [x] Create metrics dashboard prototype
- [x] Set up CI pipeline
- [x] Define signal protocol
- [x] Map all integrations (30+)
- [x] Create route registry (33 rules)
- [x] Configure GitHub Actions workflows (8)
- [x] Build MCP server for AI assistants
- [x] Define node configurations (7 nodes)
- [x] Add rate limiting to dispatcher

---

## Quick Add

Drop quick notes here. Triage later.

- [ ] _Add new items here..._

---

*The Bridge builds itself one task at a time.*
