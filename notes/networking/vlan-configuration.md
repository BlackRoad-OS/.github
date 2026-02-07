# VLAN Configuration - Cisco Switch

## What is a VLAN?

A **Virtual LAN (VLAN)** segments a physical network into isolated logical networks at Layer 2. Devices in different VLANs cannot communicate without a router (Layer 3).

## Configuration Steps

### 1. Create a VLAN

```
Switch(config)# vlan 10
Switch(config-vlan)# name IT_Department
```

### 2. Assign VLAN to a Port

```
Switch(config)# interface Fa0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
```

### 3. Verification

```
Switch# show vlan brief
Switch# show interface fa0/1 switchport
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `vlan <id>` | Create VLAN with given ID |
| `name <name>` | Name the VLAN |
| `interface Fa0/1` | Select a port |
| `switchport mode access` | Set port to access mode (single VLAN) |
| `switchport access vlan <id>` | Assign port to VLAN |
| `show vlan brief` | View all VLANs and port assignments |
| `show interface fa0/1 switchport` | View port's VLAN config |

## VLAN Modes

- **Access mode**: Port belongs to one VLAN (end devices)
- **Trunk mode**: Port carries traffic for multiple VLANs (switch-to-switch links)

## Connections

- VLANs segment traffic at Layer 2, while [IPv4 Subnetting](ipv4-subnetting.md) segments at Layer 3
- [DNS](dns.md) resolves names within and across VLAN boundaries
