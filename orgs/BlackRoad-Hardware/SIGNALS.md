# BlackRoad-Hardware Signals

> Signal handlers for the Hardware org

---

## Inbound Signals (HW receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🎯 OS → HW` | Bridge | Run command on node | `nodes.exec()` |
| `🎯 AI → HW` | AI | Inference request | `hailo.infer()` |
| `🔄 OS → HW` | Bridge | Sync configs | `ansible.deploy()` |
| `🔴 SEC → HW` | Security | Lockdown node | `nodes.isolate()` |

---

## Outbound Signals (HW sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `💓 HW → OS` | Bridge | Node heartbeat | Every 60s |
| `🌡️ HW → OS` | Bridge | Temperature/metrics | On threshold |
| `✔️ HW → AI` | AI | Inference complete | After Hailo job |
| `🖨️ HW → OS` | Bridge | Print status | On state change |
| `⚠️ HW → OS` | Bridge | Hardware alert | On issue |
| `❌ HW → OS` | Bridge | Node down | On failure |

---

## Heartbeat Format

```
# Every 60 seconds per node
💓 HW.lucidia → OS : {
  "uptime": "3d 14h 22m",
  "cpu": 23,
  "mem": 45,
  "temp": 52,
  "disk": 34,
  "services": ["salesforce-sync", "roadchain"]
}
```

---

## Sensor Signals (ESP32)

```
# Temperature sensor
🌡️ HW.esp32-001 → OS : temp=23.5, humidity=45, battery=87%

# Motion sensor
👁️ HW.esp32-002 → OS : motion=true, zone=front-door

# Generic sensor
📡 HW.esp32-xxx → OS : type=X, value=Y, ts=Z
```

---

## Print Signals (Octavia)

```
# Print lifecycle
⏳ HW.octavia → OS : print_start, file=widget.gcode, est=2h30m
📊 HW.octavia → OS : print_progress, 45%, layer=120/267
✔️ HW.octavia → OS : print_complete, file=widget.gcode, time=2h22m
❌ HW.octavia → OS : print_failed, reason=filament_runout
```

---

## Alert Signals

```
# Temperature warning
⚠️🌡️ HW.octavia → OS : temp=78C, throttling=true

# Disk space
⚠️💾 HW.lucidia → OS : disk=91%, action=cleanup_needed

# Network issue
⚠️📡 HW.aria → OS : mesh_latency=500ms, degraded=true

# Node down
❌ HW.alice → OS : offline, last_seen=2min_ago
```

---

## Mesh Status Signal

```
# Mesh topology update
🕸️ HW → OS : {
  "nodes_online": 4,
  "nodes_total": 5,
  "offline": ["shellfish"],
  "mesh_health": "degraded"
}
```

---

*Hardware speaks in signals. We listen.*
