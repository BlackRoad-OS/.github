# BlackRoad Architecture Overview

> **The Core Thesis:** BlackRoad is a routing company, not an AI company.

---

## Executive Summary

We don't train models or buy GPUs. We connect users to intelligence that already exists (Claude, GPT, Llama, NumPy, legal databases, etc.) through an orchestration layer we own.

**The insight:** Intelligence is already trained. Libraries already exist. The value is in routing requests to the right tool at the right time—not in building another brain.

---

## Infrastructure (~$40/month recurring)

| Layer | Service | Role |
|-------|---------|------|
| Edge/CDN | Cloudflare | Handles millions of connections, DNS, DDoS |
| CRM/Data | Salesforce (Free Dev Edition) | Customer data, 15K API calls/day |
| Code/CI | GitHub Enterprise | 15 organizations, deployment |
| Mesh Network | Tailscale | Private encrypted connections between nodes |
| Cloud Node | Digital Ocean (Shellfish) | Internet-facing server |

---

## Hardware (Owned, Not Rented)

A Raspberry Pi cluster running specialized roles:

| Node | Hardware | Role |
|------|----------|------|
| **lucidia** | Pi 5 + Pironman + Hailo-8 | Salesforce sync, RoadChain/Bitcoin |
| **octavia** | Pi 5 + Pironman + Hailo-8 | AI routing decisions (26 TOPS), 3D printing |
| **aria** | Pi 5 | Agent orchestration, Cloudflare Workers |
| **alice** | Pi 400 | Kubernetes + VPN hub (mesh root) |
| **shellfish** | Digital Ocean droplet | Public-facing gateway |

Plus dev machines (Mac = "cecilia", iPhone = "arcadia") and edge devices (ESP32s, LoRa modules for future deployment).

---

## The Control Plane

```
┌─────────────────────────────────────────────────────────────┐
│              BLACKROAD UNIFIED CONTROL                       │
├─────────────────┬─────────────────┬─────────────────────────┤
│   SALESFORCE    │   CLOUDFLARE    │      GITHUB             │
│   CRM + API     │   Edge + DNS    │    Code + CI            │
└────────┬────────┴────────┬────────┴──────────┬──────────────┘
         │                 │                   │
         └────────────────┬┴───────────────────┘
                          ▼
                    ┌──────────┐
                    │ OPERATOR │  ← We own this
                    └────┬─────┘
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌─────────┐
    │ lucidia │    │ octavia  │    │  aria   │
    │ SF/Chain│    │ Hailo-8  │    │ Agents  │
    └────┬────┘    └────┬─────┘    └────┬────┘
         └───────────────┼───────────────┘
                         ▼
                    ┌─────────┐
                    │  alice  │  ← K8s + VPN hub
                    └─────────┘
```

**Key insight:** The OPERATOR sits between us and all external services. Cloudflare, Salesforce, and GitHub are utilities we command—not landlords we rent from. The control plane lives on hardware we own.

---

## The Routing Pattern

```
[User Request] → [Operator] → [Route to Right Tool] → [Answer]
                     │
                     ├── Physics question? → NumPy/SciPy
                     ├── Language task? → Claude/GPT API
                     ├── Customer lookup? → Salesforce API
                     ├── Legal question? → Legal database
                     └── Fast inference? → Hailo-8 local
```

The agent doesn't need to be smart. It needs to know **who to call.**

---

## The Business Model

| What We Own | What We Don't Need |
|-------------|-------------------|
| Customer relationships | Training models |
| Routing/orchestration logic | GPUs |
| Data and state | Data centers |
| The Operator | The intelligence itself |

When better models come out, we add them to the router. Infrastructure stays the same.

---

## The Math

At $1/user/month:

- 1M users = $12M/year
- 100M users = $1.2B/year
- 1B users = $12B/year

Ceiling: everyone who ever talks to AI.

---

## Organization Structure

BlackRoad operates across 15 specialized GitHub organizations:

| Organization | Focus |
|--------------|-------|
| **BlackRoad-OS** | Core operating system, operator, infrastructure |
| **BlackRoad-AI** | AI models, routing, inference |
| **BlackRoad-Cloud** | Cloud services, deployment |
| **BlackRoad-Labs** | Research, experiments |
| **BlackRoad-Security** | Security tools, auditing |
| **BlackRoad-Foundation** | CRM, business tools |
| **BlackRoad-Media** | Content, publishing |
| **BlackRoad-Hardware** | IoT, ESP32, Pi projects |
| **BlackRoad-Education** | Learning, documentation |
| **BlackRoad-Gov** | Governance, voting |
| **BlackRoad-Interactive** | Games, 3D, metaverse |
| **BlackRoad-Archive** | Storage, backup |
| **BlackRoad-Studio** | Design, creative tools |
| **BlackRoad-Ventures** | Business, commerce |
| **Blackbox-Enterprises** | Enterprise solutions |

---

## Domain Registry

All domains are orchestrated via Cloudflare. Cloudflare Tunnels expose local Raspberry Pi nodes to the public internet for local inference without exposing internal network ports.

| Domain | Use Case | Organization |
|--------|----------|--------------|
| blackboxprogramming.io | Developer Education and APIs | Blackbox-Enterprises |
| blackroad.io | Core Project Landing Page | BlackRoad-OS |
| blackroad.company | Corporate and HR Operations | BlackRoad-Ventures |
| blackroad.me | Personal Agent Identity Nodes | BlackRoad-AI |
| blackroad.network | Distributed Network Interface | BlackRoad-Cloud |
| blackroad.systems | Infrastructure and System Ops | BlackRoad-Cloud |
| blackroadai.com | AI Research and API Hosting | BlackRoad-AI |
| blackroadinc.us | US-based Governance and Legal | BlackRoad-Gov |
| blackroadqi.com | Quantum Intelligence Research | BlackRoad-Labs |
| blackroadquantum.com | Primary Quantum Lab Interface | BlackRoad-Labs |
| lucidia.earth | Memory Layer and Personal AI | BlackRoad-AI |
| lucidia.studio | Creative and Asset Management | BlackRoad-Studio |
| roadchain.io | Blockchain and Witnessing Ledger | BlackRoad-Security |
| roadcoin.io | Tokenomics and Financial Interface | BlackRoad-Ventures |

See [`routes/domains.yaml`](routes/domains.yaml) for the machine-readable registry.

---

## @blackroad-agents Deca-Layered Scaffold

Every task entered into the BlackRoad system follows a ten-step scaffolding process triggered by the `@blackroad-agents` command.

| Step | Name | Description |
|------|------|-------------|
| 1 | **Initial Reviewer** | Layer 6 (Lucidia Core) reviews the request for clarity, security compliance, and resource availability. Generates a preliminary execution plan. |
| 2 | **Task Distribution to Organization** | Routes the task to one of the 15 BlackRoad organizations based on functional domain (hardware, security, cloud, etc.). |
| 3 | **Task Distribution to Team** | Refines and distributes the task within the selected org. Handles human-in-the-loop (HITL) requirements—pauses for manual approval on high-risk operations. |
| 4 | **Task Update to Project** | Records the task on a GitHub Project board. Metadata (Request ID, timeline) is synchronized with Salesforce for an enterprise-level audit trail. |
| 5 | **Task Distribution to Agent** | Assigns a specialized autonomous agent (e.g., `fastapi-coder-agent`, `doctl-infrastructure-agent`). Agents follow the Planner-Executor-Reflector design pattern. |
| 6 | **Task Distribution to Repository** | The agent identifies the target repository, creates a new branch, and follows GitHub Flow for isolated testing. |
| 7 | **Task Distribution to Device** | Routes to the device layer for physical execution—firmware updates to Pi nodes, rebuilding DigitalOcean Droplets, or offloading to local clusters. |
| 8 | **Task Distribution to Drive** | Distributes artifacts (logs, reports, documentation) to Google Drive via a Service Account (GSA) pattern for consistent write access. |
| 9 | **Task Distribution to Cloudflare** | Executes network configuration changes—creating Cloudflare Tunnels, modifying DNS records—to make new services immediately reachable and secured. |
| 10 | **Task Distribution to Website Editor** | Updates the presentation layer via an AI-driven website editor or headless CMS for autonomous content generation. |

---

## BlackRoad CLI v3 Layered Architecture

The CLI loads six distinct layers of functionality (Layers 3–8):

| Layer | Name | Description |
|-------|------|-------------|
| 3 | **Agents/System** | Foundation for autonomous agent lifecycle management and system-level processes. |
| 4 | **Deploy/Orchestration** | Logic for infrastructure provisioning across cloud and local nodes. |
| 5 | **Branches/Environments** | Management of ephemeral environments and git-branching logic for agentic code tests. |
| 6 | **Lucidia Core/Memory** | Critical memory layer storing long-term context, state transitions, and simulation data. |
| 7 | **Orchestration** | High-level task distribution logic that powers the @blackroad-agents scaffold. |
| 8 | **Network/API** | External interface providing REST and GraphQL endpoints for the @BlackRoadBot matrix. |

A failure in Layer 8 (Network) does not affect the persistence of state in Layer 6 (Memory). Each layer is designed for independent resilience.

---

## Infrastructure Offloading and Rate Limit Mitigation

To bypass centralized rate limits (e.g., GitHub Copilot RPM/token limits), BlackRoad offloads requests to local Raspberry Pi 5 clusters.

### Local Inference Hardware

| Component | Specification | Role |
|-----------|---------------|------|
| Compute Node | Raspberry Pi 5 (8GB LPDDR4X) | General Purpose Inference and Control |
| Inference Accelerator | Raspberry Pi AI Hat 2 (40 TOPS) | Dedicated INT8 LLM Processing |
| Network Layer | Gigabit Ethernet with PoE+ HAT | Synchronized Node Communication |
| Storage | NVMe SSD (M.2 Interface, 256GB+) | Model Weights and Agent Memory |
| Software Stack | LiteLLM Proxy / Ollama / llama.cpp | API Hosting and Load Balancing |

### Copilot Proxy Configuration

Override the default GitHub Copilot endpoints to redirect traffic to a local LiteLLM proxy:

```bash
export GH_COPILOT_OVERRIDE_PROXY_URL="http://raspberrypi.local:4000"
```

Note: `GH_COPILOT_OVERRIDE_PROXY_URL` is a BlackRoad-specific configuration knob that is only honored by a custom Copilot proxy/shim which reads this environment variable and rewrites Copilot traffic accordingly. Stock GitHub Copilot clients do not support this variable out of the box; to use this pattern you must integrate or implement a wrapper that explicitly consumes it.
The LiteLLM proxy translates requests into OpenAI-compatible format and distributes them across the cluster using round-robin load balancing. This ensures proprietary codebase context never leaves the local network.

### Rate Limit Mitigation Strategies

| Provider | Observed Limit | Mitigation Protocol |
|----------|----------------|---------------------|
| GitHub Copilot | RPM / Token Exhaustion | Redirect to local Raspberry Pi LiteLLM proxy |
| Hugging Face Hub | IP-based Rate Limit | Rotate HF_TOKEN or use authenticated SSH keys |
| Google Drive | Individual User Quota | Use Shared Drives with GSA "Content Manager" role |
| DigitalOcean API | Concurrent Build Limits | Queue tasks via Layer 7 Orchestration |
| Salesforce API | Daily API Request Cap | Batch updates via Data Cloud Streaming Transforms |

---

## @BlackRoadBot Routing Matrix

When a user comments `@BlackRoadBot` on a GitHub issue or PR, the bot identifies target platforms based on natural language intent.

- **Salesforce CRM:** Maps GitHub events to Salesforce objects via Apex middleware. Creates Case/Task objects and ingests telemetry via Data Cloud.
- **Hugging Face:** Routes specialized reasoning tasks to Hugging Face Inference Endpoints for high-compute tasks exceeding Pi cluster capacity.
- **Ollama:** Exposes local models (e.g., Llama-3.2-3B-Instruct-GGUF) via Cloudflare Tunnel for routine inference tasks.
- **DigitalOcean:** Manages droplet lifecycle via `doctl` in GitHub Actions—rebuilds, scaling, and provisioning.
- **Railway:** Deploys ephemeral test environments for feature branches via the Railway CLI.

---

## roadchain Witnessing Architecture

The roadchain functions as a "witnessing" architecture rather than a consensus-based blockchain. Every state transition—agent commits, bot routing, task completions—is hashed using SHA-256 and appended to a non-terminating ledger. This creates an immutable record of "what happened" rather than "what is true."

---

## Future Scaling: 30k Agents

The `blackroad-30k-agents` project aims to orchestrate 30,000 autonomous agents using Kubernetes auto-scaling and self-healing. This requires transitioning from Pi clusters to larger ARM-based data centers that mirror the decentralized witnessing architecture of roadchain.

---

## Implementation Guide

The FastAPI pattern is the starting point:

1. **Expose endpoints** (`/physics/hydrogen`, `/relativity/time-dilation`)
2. **Operator routes** (keyword matching → right function)
3. **Log everything** (JSON audit trail → future ledger)

This is the Operator pattern in miniature. Start with physics, extend to every domain.

---

## Verification

- **Source of Truth:** GitHub (BlackRoad-OS) + Cloudflare
- **Hash Verification:** PS-SHA-∞ (infinite cascade hashing)
- **Authorization:** Alexa's pattern via Claude/ChatGPT

---

*Last Updated: 2026-02-27*
*BlackRoad OS, Inc. - Proprietary and Confidential*
