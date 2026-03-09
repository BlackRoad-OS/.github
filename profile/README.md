# BlackRoad OS

**Sovereign AI infrastructure built from bare metal up.**

---

## The Stack

790 MB of code across 229 repositories. 20+ languages. One person.

```
Python ............. 193 MB    TypeScript ......... 187 MB
HTML ............... 150 MB    Shell ............... 43 MB
Go .................. 43 MB    C / C++ ............. 27 MB
JavaScript .......... 22 MB    Cuda / Metal ........ 1.8 MB
Rust, HCL, Vue, MDX, GLSL, RouterOS, Ruby, Jupyter ...
```

71 repos with substantial code (>100KB). 155 more with working implementations.

---

## What We Built

### Core Platform

The operating system layer: a CLI, SDK, API gateway, and operator framework that ties everything together.

- **blackroad-cli** -- Command-line interface for managing the entire stack (Python, Shell, JS)
- **blackroad-sdk** -- Multi-language SDK: Python, TypeScript, Rust, Go
- **blackroad-api** -- REST API with rate limiting, webhooks, audit logging, feature flags
- **blackroad-gateway** -- Edge gateway in TypeScript and Go
- **blackroad-operator** -- Orchestration engine (240 MB, TypeScript/Python/Go)
- **blackroad-core** -- Shared libraries and configuration management
- **blackroad-infra** -- Infrastructure-as-code: provisioning, networking, deployment pipelines

### Lucidia AI

A custom AI system with its own models, agents, memory architecture, and reasoning engines.

- **lucidia-core** -- Central AI runtime: model loading, inference pipeline, memory integration
- **lucidia-agents** -- Autonomous agent framework (TypeScript/JS)
- **lucidia-ai-models** -- Custom model definitions, fine-tuning configs, Ollama integration
- **lucidia-cli** -- 968-file CLI tool for interacting with Lucidia (Python)
- **blackroad-ai-memory-bridge** -- Persistent memory system bridging sessions and contexts
- **blackroad-agents** -- Multi-agent orchestration with task routing
- **blackroad-multi-ai-system** -- Coordinator for running multiple AI backends simultaneously
- **blackroad-ai-inference-accelerator** -- Hailo-8 integration (52 TOPS across two accelerators)
- **remember** -- Long-term memory storage and retrieval (156K+ FTS5 entries, 228 SQLite databases)

### Infrastructure

A 5-node Raspberry Pi cluster running production workloads, meshed with WireGuard, fronted by Cloudflare.

- **5 Raspberry Pi 5 nodes** -- Alice (gateway, Pi-hole, PostgreSQL, Qdrant), Cecilia (AI inference, TTS, MinIO, 16 Ollama models), Octavia (1TB NVMe, Gitea with 207 repos, Docker Swarm leader), Aria (Portainer, Headscale), Lucidia (334 web apps, FastAPI services, GitHub Actions runner)
- **2 DigitalOcean droplets** -- Headscale coordination, Nginx reverse proxy, WireGuard hub
- **WireGuard mesh** -- Full mesh VPN across all nodes with automatic failover
- **Cloudflare edge** -- 95+ Pages deployments, 18 tunnels, 48+ custom domains, 40 KV namespaces, 7 D1 databases, 10 R2 buckets
- **Docker Swarm** -- Container orchestration across the cluster
- **RoadNet** -- Custom carrier network with 5 Wi-Fi access points, per-node subnets, Pi-hole DNS
- **blackroad-pi-ops** -- Fleet management: health monitoring, power optimization, auto-healing
- **blackroad-cluster** -- Cluster coordination and service discovery
- **blackroad-dashboards** -- Monitoring and observability for the entire fleet

### Web

Production web applications and 48+ domains.

- **blackroad-io-app** -- Main application (Next.js, 3 MB)
- **lucidia-earth-website** -- Lucidia public site (TypeScript, 1.8 MB)
- **blackroad-web** -- Corporate web platform (TypeScript/CSS, 848 KB)
- **blackroad-progress-dashboard** -- Real-time project tracking
- **blackroad-templates** -- 15 page templates following brand system (Space Grotesk, JetBrains Mono, Inter)
- **blackroad-chrome-extension** -- Browser extension
- **blackroad-vscode-extension** -- VS Code integration
- **blackroad-figma-plugin** -- Design tool integration
- **blackroad-prism-console** -- Full admin console (4,973 source files, TypeScript, Airtable, PostgreSQL)

### Math and Research

Original research in simulation theory, quantum mathematics, and formal proofs.

- **quantum-math-lab** -- Computational experiments in quantum mathematics (Python)
- **simulation-theory** -- Simulation theory research and modeling (Python)
- **native-ai-quantum-energy** -- Intersection of AI, quantum computing, and energy systems
- **blackroad-math** -- Mathematical foundations library (Python/TypeScript, 205 KB)
- **lucidia-math** -- Applied mathematics for AI reasoning (1.6 MB)
- **blackroad-os-pack-research-lab** -- Research environment with Jupyter notebooks

### Tools

232 shell scripts and a fleet of automation tools.

- **blackroad-scripts** -- 400+ shell scripts for daily operations (6.1 MB)
- **blackroad-analysis** -- System analysis and reporting (Shell/Awk, 1.8 MB)
- **blackroad-cicd-pipeline** -- CI/CD automation
- **blackroad-os-deploy** -- Deployment orchestration (TypeScript/Shell/Python)
- **blackroad-os-disaster-recovery** -- Backup and recovery (Python/C)
- **claude-collaboration-system** -- AI-assisted development workflow (Shell)
- **blackroad-cron** -- Scheduled task management
- **audit-tools** -- Security auditing suite (Python/Shell)
- **penetration-testing** -- Security testing framework

### Creative

3D environments, music production, and a metaverse.

- **blackroad-os-metaverse** -- 3D virtual environment (JavaScript, 710 KB)
- **lucidia-3d-wilderness** -- Procedural 3D wilderness generation
- **blackroad-os-music** -- Music studio tools
- **video-studio** -- Video production pipeline
- **writing-studio** -- Content creation tools
- **canvas-studio** -- Visual design tools
- **blackroad-roadworld** -- Interactive world engine (JavaScript/CSS)

### RoadC Language

A custom programming language built from scratch.

- **Lexer** -- Tokenizer with Python-style indentation (colon + INDENT/DEDENT)
- **Parser** -- Full AST generation
- **Interpreter** -- Tree-walking evaluator
- **Supports**: functions, recursion, if/elif/else, while, for, strings, integers, floats, `let`/`var`/`const`, `match`, `spawn`, `space` (3D primitives)

---

## Architecture

```
                         Cloudflare Edge
                    (95 Pages, 18 tunnels, 48 domains)
                              |
              +---------------+---------------+
              |               |               |
         Alice (.49)    Cecilia (.96)    Octavia (.100)
         Pi 400         Pi 5             Pi 5 + 1TB NVMe
         Gateway        AI Inference     Gitea + Swarm
         Pi-hole        16 Ollama        207 repos
         PostgreSQL     Hailo-8          Hailo-8
         Qdrant         TTS/MinIO        NATS
              |               |               |
              +-------WireGuard Mesh----------+
              |               |               |
         Aria (.98)     Lucidia (.38)    Mac (.28)
         Pi 5           Pi 5             Dev machine
         Portainer      334 web apps     400+ scripts
         Headscale      FastAPI          RoadC compiler
                        GH Actions       228 SQLite DBs
                              |
              +---------------+---------------+
              |                               |
         gematria (DO)              anastasia (DO)
         NYC3, 4cpu/8GB             NYC1, WG hub
         WireGuard peer             Headscale + Nginx
```

All nodes run power-optimized configurations with conservative CPU governors, automated health monitoring every 5 minutes, and self-healing autonomy scripts.

---

## Key Repos

| Repository | What it is |
|---|---|
| [blackroad](https://github.com/BlackRoad-OS-Inc/blackroad) | Main monorepo -- the OS itself |
| [blackroad-operator](https://github.com/BlackRoad-OS-Inc/blackroad-operator) | Orchestration engine (240 MB, TS/Python/Go) |
| [blackroad-cli](https://github.com/BlackRoad-OS-Inc/blackroad-cli) | Command-line interface |
| [blackroad-sdk](https://github.com/BlackRoad-OS-Inc/blackroad-sdk) | Multi-language SDK (Python, TS, Rust, Go) |
| [blackroad-api](https://github.com/BlackRoad-OS-Inc/blackroad-api) | REST API layer |
| [blackroad-gateway](https://github.com/BlackRoad-OS-Inc/blackroad-gateway) | Edge gateway (TypeScript, Go) |
| [lucidia-core](https://github.com/BlackRoad-OS/lucidia-core) | AI runtime and inference pipeline |
| [blackroad-scripts](https://github.com/blackboxprogramming/blackroad-scripts) | 400+ shell scripts |
| [blackroad-infra](https://github.com/BlackRoad-OS-Inc/blackroad-infra) | Infrastructure-as-code |
| [blackroad-pi-ops](https://github.com/BlackRoad-OS/blackroad-pi-ops) | Pi cluster fleet management |
| [quantum-math-lab](https://github.com/blackboxprogramming/quantum-math-lab) | Quantum mathematics research |
| [simulation-theory](https://github.com/BlackRoad-OS/simulation-theory) | Simulation theory modeling |
| [blackroad-web](https://github.com/BlackRoad-OS-Inc/blackroad-web) | Web platform (Next.js/TypeScript) |
| [BLACKROAD-OS-BRAND-LOCK](https://github.com/blackboxprogramming/BLACKROAD-OS-BRAND-LOCK) | Brand system and design templates |

---

Built by [Alexa Amundson](https://github.com/blackboxprogramming).
