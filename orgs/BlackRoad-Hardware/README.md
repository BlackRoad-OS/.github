# BlackRoad-Hardware Blueprint

> **The Physical Layer**
> Code: `HW`

---

## Mission

Own the iron. Control the compute. No landlords.

```
[Cloud] ←→ [Mesh] ←→ [Pi Cluster] ←→ [Edge Devices]
```

---

## Core Principle

**Hardware you own can't be taken away.**

- Raspberry Pi cluster = always-on compute we control
- Hailo-8 accelerators = 26 TOPS of AI without cloud bills
- ESP32/LoRa = sensors everywhere, mesh networking
- Tailscale = encrypted connectivity without exposed ports

---

## The Fleet

### Compute Nodes

| Node | Hardware | Role | Location |
|------|----------|------|----------|
| **lucidia** | Pi 5 + Pironman + Hailo-8 | Salesforce sync, RoadChain | Home |
| **octavia** | Pi 5 + Pironman + Hailo-8 | AI inference, 3D printing | Home |
| **aria** | Pi 5 | Agent orchestration | Home |
| **alice** | Pi 400 | K8s control plane, mesh root | Home |
| **shellfish** | Digital Ocean | Public gateway, backup | Cloud |

### Dev Machines

| Device | Type | Role |
|--------|------|------|
| **cecilia** | Mac | Primary development |
| **arcadia** | iPhone | Mobile interface |

### Edge Devices (Future)

| Type | Purpose | Count |
|------|---------|-------|
| ESP32 | Sensors, controllers | Many |
| LoRa modules | Long-range mesh | TBD |
| Cameras | Vision (via Hailo) | TBD |

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `nodes` | Pi cluster configs, Ansible playbooks | P0 |
| `mesh` | Tailscale configs, network topology | P0 |
| `hailo` | Hailo-8 setup, model deployment | P1 |
| `esp32` | ESP32 firmware, sensor code | P1 |
| `lora` | LoRa mesh networking | P2 |
| `3dprint` | 3D printer configs (octavia) | P2 |

---

## Network Topology

```
                         INTERNET
                             │
                    ┌────────┴────────┐
                    │   CLOUDFLARE    │
                    │   (Edge/CDN)    │
                    └────────┬────────┘
                             │
                    Cloudflare Tunnel
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │ shellfish│    │  alice   │    │ cecilia  │
      │ (DO)     │    │ (Pi 400) │    │ (Mac)    │
      │ Gateway  │    │ Mesh Root│    │ Dev      │
      └────┬─────┘    └────┬─────┘    └────┬─────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    TAILSCALE MESH
                    (encrypted P2P)
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ lucidia │      │ octavia │      │  aria   │
    │ Pi5+H8  │      │ Pi5+H8  │      │  Pi5    │
    │ SF/Chain│      │ AI/3D   │      │ Agents  │
    └─────────┘      └─────────┘      └─────────┘
         │
    ┌────┴────┐
    │ ESP32s  │  (Future: sensor mesh)
    │ LoRa    │
    └─────────┘
```

---

## Integration Points

### Upstream (receives from)
- `CLD` - Requests via Cloudflare Tunnel
- `OS` - Operator commands
- `AI` - Inference requests for Hailo

### Downstream (sends to)
- `OS` - Telemetry, status
- `ARC` - Logs, metrics
- Physical world (3D printing, sensors)

### Signals
```
💓 HW → OS : Node heartbeats
🌡️ HW → OS : Sensor readings
🖨️ HW → OS : Print job status
⚠️ HW → OS : Hardware alert
```

---

## Hailo-8 Specs

| Metric | Value |
|--------|-------|
| TOPS | 26 |
| Power | 2.5W |
| Interface | PCIe |
| Models | YOLO, classification, custom |

**Key Insight:** 26 TOPS for 2.5W means we can run serious AI inference on a Pi without cloud costs.

---

*The mesh is ours. Every node, every wire.*
