# BlackRoad-Hardware Repositories

> Repo specs for the Hardware org

---

## Repository List

### `nodes` (P0 - Build First)

**Purpose:** Pi cluster configuration and management

**Structure:**
```
nodes/
├── ansible/
│   ├── inventory.yml     ← Node inventory
│   ├── playbooks/
│   │   ├── setup.yml     ← Initial setup
│   │   ├── update.yml    ← System updates
│   │   ├── deploy.yml    ← App deployment
│   │   └── backup.yml    ← Backup configs
│   └── roles/
│       ├── common/       ← Shared setup
│       ├── k8s/          ← Kubernetes (alice)
│       ├── hailo/        ← Hailo setup
│       └── services/     ← Per-node services
├── configs/
│   ├── lucidia/
│   │   └── config.yaml
│   ├── octavia/
│   │   └── config.yaml
│   ├── aria/
│   │   └── config.yaml
│   └── alice/
│       └── config.yaml
├── scripts/
│   ├── health-check.sh
│   ├── reboot-all.sh
│   └── status.sh
└── README.md
```

---

### `mesh` (P0 - Build First)

**Purpose:** Tailscale mesh network configuration

**Structure:**
```
mesh/
├── tailscale/
│   ├── acls.json         ← Access control lists
│   ├── dns.json          ← MagicDNS config
│   └── routes.json       ← Subnet routes
├── topology/
│   └── network.md        ← Network diagram
├── scripts/
│   ├── join-mesh.sh
│   ├── leave-mesh.sh
│   └── status.sh
└── README.md
```

**Key Features:**
- Zero-config VPN
- Encrypted P2P connections
- No exposed ports
- Works through NAT

---

### `hailo` (P1)

**Purpose:** Hailo-8 AI accelerator setup and models

**Structure:**
```
hailo/
├── setup/
│   ├── install.sh        ← Driver installation
│   └── verify.sh         ← Verification script
├── models/
│   ├── yolov8n.hef       ← Object detection
│   ├── resnet50.hef      ← Classification
│   └── custom/           ← Our trained models
├── inference/
│   ├── server.py         ← Inference server
│   └── client.py         ← Test client
├── benchmarks/
│   └── results.md
└── README.md
```

---

### `esp32` (P1)

**Purpose:** ESP32 firmware for sensors and controllers

**Structure:**
```
esp32/
├── firmware/
│   ├── sensor-node/      ← Generic sensor firmware
│   ├── controller/       ← Actuator control
│   └── gateway/          ← ESP32 → Pi bridge
├── platformio.ini
├── lib/
│   ├── blackroad/        ← Our shared library
│   └── ...
└── README.md
```

**Features:**
- PlatformIO for builds
- OTA updates
- MQTT to mesh
- Deep sleep for battery

---

### `lora` (P2)

**Purpose:** LoRa long-range mesh networking

**Structure:**
```
lora/
├── firmware/
│   └── lora-node/        ← LoRa transceiver code
├── gateway/
│   └── pi-gateway/       ← Pi LoRa gateway
├── protocol/
│   └── blackroad-lora.md ← Our LoRa protocol
└── README.md
```

---

### `3dprint` (P2)

**Purpose:** 3D printer configs for octavia

**Structure:**
```
3dprint/
├── klipper/
│   └── printer.cfg       ← Klipper config
├── models/
│   └── ...               ← STL files
├── scripts/
│   ├── start-print.py
│   └── monitor.py
└── README.md
```

---

## Node Specifications

| Node | CPU | RAM | Storage | Special |
|------|-----|-----|---------|---------|
| lucidia | Pi 5 | 8GB | 256GB NVMe | Hailo-8 |
| octavia | Pi 5 | 8GB | 256GB NVMe | Hailo-8 + 3D printer |
| aria | Pi 5 | 8GB | 128GB SD | - |
| alice | Pi 400 | 4GB | 128GB SD | Built-in keyboard |

---

*Silicon we own. Networks we control.*
