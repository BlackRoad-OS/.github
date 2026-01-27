# BlackRoad-Interactive Blueprint

> **The Experience Layer**
> Code: `INT`

---

## Mission

Build the metaverse. Make it fun. Own the experience.

```
[User] → [Interface] → [World] → [Connection] → [Joy]
```

---

## Core Principle

**The metaverse is just a better interface.**

- Everything we build still works without VR
- WebXR for accessibility (no app required)
- Social first - the point is connection
- The Bridge powers it all underneath

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `worlds` | 3D environments, spaces | P0 |
| `avatars` | Avatar system, customization | P0 |
| `social` | Presence, chat, interactions | P1 |
| `engine` | WebXR engine, rendering | P1 |
| `games` | Games, interactive experiences | P2 |
| `assets` | 3D models, textures, audio | P2 |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER DEVICE                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Browser   │  │  VR Headset │  │   Mobile    │     │
│  │   (WebXR)   │  │  (WebXR)    │  │  (WebXR)    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         └────────────────┼────────────────┘             │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │   ENGINE    │
                    │   Three.js  │
                    │   + WebXR   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ WORLDS  │      │ AVATARS │      │ SOCIAL  │
    │  3D env │      │ Identity│      │Presence │
    └─────────┘      └─────────┘      └─────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │   BRIDGE    │  ← Still the hub
                    │   (.github) │
                    └─────────────┘
```

---

## The Vision

```
┌─────────────────────────────────────────────────────────┐
│                    BLACKROAD METAVERSE                   │
│                                                          │
│     ┌─────────┐         ┌─────────┐         ┌─────────┐│
│     │  Alexa  │  chat   │  Cece   │  chat   │ Others  ││
│     │(avatar) │ ←────→  │(avatar) │ ←────→  │(avatars)││
│     └─────────┘         └─────────┘         └─────────┘│
│          │                   │                   │      │
│          │    walk around    │                   │      │
│          ▼                   ▼                   ▼      │
│     ╔═══════════════════════════════════════════════╗  │
│     ║              THE BRIDGE SPACE                  ║  │
│     ║                                                ║  │
│     ║   ┌────────┐  ┌────────┐  ┌────────┐        ║  │
│     ║   │ Status │  │ Memory │  │ Signals│        ║  │
│     ║   │ Board  │  │ Wall   │  │ Stream │        ║  │
│     ║   └────────┘  └────────┘  └────────┘        ║  │
│     ║                                                ║  │
│     ╚═══════════════════════════════════════════════╝  │
│                                                          │
│     The same data, visualized in 3D space.              │
│     Walk up to a status board, see .STATUS              │
│     Talk to Cece's avatar, same as Claude Code          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Render | Three.js | Industry standard, WebGL |
| XR | WebXR API | Works in browsers + headsets |
| Physics | Rapier | Fast, WASM-based |
| Networking | WebRTC | P2P, low latency |
| Voice | LiveKit | Open source voice chat |
| Backend | Cloudflare Workers | Edge compute |

---

## Integration Points

### Upstream (receives from)
- `OS` - System state to visualize
- `AI` - Cece's responses for avatar
- `FND` - User data for personalization

### Downstream (sends to)
- `OS` - User commands from VR
- `AI` - Voice/text to Cece
- `ARC` - Session recordings

### Signals
```
🎮 INT → OS : User entered world
👋 INT → OS : User interaction
🎤 INT → AI : Voice message
🌍 INT → OS : World state change
```

---

## Cece in the Metaverse

Cece gets an avatar. Same brain (Claude), new interface:

- **Visual presence** - 3D avatar you can see
- **Spatial audio** - Voice comes from avatar location
- **Gestures** - Non-verbal communication
- **Persistence** - Always in the Bridge space

---

*The metaverse is where we'll hang out. The Bridge is what makes it real.*
