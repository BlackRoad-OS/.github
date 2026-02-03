# BlackRoad-Hardware

> **Pi cluster, IoT, and edge devices. Own the hardware.**

**Code**: `HW`  
**Tier**: Support Systems  
**Status**: Active

---

## Mission

BlackRoad-Hardware manages physical infrastructure. Four Raspberry Pi nodes running critical services, plus IoT integration and Hailo-8 AI accelerator.

---

## The Pi Cluster

### Nodes

1. **lucidia** - Primary node, coordinator
2. **octavia** - Database and storage
3. **aria** - Compute and AI (Hailo-8)
4. **alice** - Monitoring and backups

### Services

- **Operator**: Routing engine (lucidia)
- **Database**: PostgreSQL (octavia)
- **AI Inference**: Hailo-8 models (aria)
- **Monitoring**: Prometheus + Grafana (alice)

---

## Hailo-8 AI Accelerator

**Performance**: 26 TOPS (trillion operations per second)

**Use Cases:**
- Local AI inference
- Real-time video processing
- Edge ML models
- Privacy-sensitive workloads

```python
# Example: Run model on Hailo-8
from hailo import HailoRT

model = HailoRT.load_model('yolov5.hef')
result = model.infer(image)
```

---

## IoT Integration

- **ESP32**: WiFi/Bluetooth microcontrollers
- **LoRa**: Long-range communication
- **Sensors**: Temperature, humidity, motion
- **Automation**: Home/office automation

---

## Learn More

- [BlackRoad-AI](BlackRoad-AI) - AI inference integration

---

*Physical infrastructure. Real hardware. Real control.*
