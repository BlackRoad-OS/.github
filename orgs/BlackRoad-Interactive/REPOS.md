# BlackRoad-Interactive Repositories

> Repo specs for the Interactive org

---

## Repository List

### `worlds` (P0 - Build First)

**Purpose:** 3D environments and spaces

**Structure:**
```
worlds/
├── src/
│   ├── core/
│   │   ├── world.ts       ← World base class
│   │   ├── scene.ts       ← Scene management
│   │   └── loader.ts      ← Asset loading
│   ├── environments/
│   │   ├── bridge/        ← The Bridge space
│   │   ├── lobby/         ← Entry lobby
│   │   └── custom/        ← User-created
│   ├── objects/
│   │   ├── interactive.ts ← Clickable objects
│   │   └── display.ts     ← Data displays
│   └── lighting/
│       └── system.ts
├── assets/
│   ├── bridge/
│   └── shared/
└── README.md
```

**The Bridge Space:**
- Central hub where .github data is visualized
- Status boards showing .STATUS
- Memory wall showing MEMORY.md
- Signal streams showing live signals

---

### `avatars` (P0 - Build First)

**Purpose:** Avatar system and customization

**Structure:**
```
avatars/
├── src/
│   ├── core/
│   │   ├── avatar.ts      ← Avatar class
│   │   ├── controller.ts  ← Movement/input
│   │   └── animator.ts    ← Animations
│   ├── customization/
│   │   ├── editor.ts      ← Avatar editor
│   │   ├── parts.ts       ← Body parts
│   │   └── outfits.ts     ← Clothing
│   ├── ai/
│   │   └── cece.ts        ← Cece's avatar logic
│   └── sync/
│       └── network.ts     ← Avatar sync
├── models/
│   ├── base/
│   └── accessories/
└── README.md
```

**Cece's Avatar:**
- Unique appearance (AI persona)
- Lip sync with TTS
- Gesture system
- Always present in Bridge space

---

### `social` (P1)

**Purpose:** Presence and social features

**Structure:**
```
social/
├── src/
│   ├── presence/
│   │   ├── tracker.ts     ← Who's online
│   │   ├── status.ts      ← User status
│   │   └── location.ts    ← Where in world
│   ├── chat/
│   │   ├── text.ts        ← Text chat
│   │   ├── voice.ts       ← Voice chat (LiveKit)
│   │   └── emotes.ts      ← Emote system
│   ├── friends/
│   │   ├── list.ts
│   │   └── invites.ts
│   └── moderation/
│       └── tools.ts
└── README.md
```

---

### `engine` (P1)

**Purpose:** Core WebXR engine

**Structure:**
```
engine/
├── src/
│   ├── core/
│   │   ├── renderer.ts    ← Three.js setup
│   │   ├── xr.ts          ← WebXR handling
│   │   └── input.ts       ← Input system
│   ├── physics/
│   │   └── rapier.ts      ← Physics engine
│   ├── networking/
│   │   ├── webrtc.ts      ← P2P connections
│   │   └── state.ts       ← State sync
│   └── optimization/
│       ├── lod.ts         ← Level of detail
│       └── culling.ts     ← Frustum culling
└── README.md
```

---

### `games` (P2)

**Purpose:** Games and interactive experiences

**Structure:**
```
games/
├── src/
│   ├── framework/
│   │   ├── game.ts        ← Game base class
│   │   └── score.ts       ← Scoring system
│   ├── games/
│   │   ├── puzzle/
│   │   ├── social/
│   │   └── creative/
│   └── multiplayer/
│       └── lobby.ts
└── README.md
```

---

### `assets` (P2)

**Purpose:** 3D models, textures, audio

**Structure:**
```
assets/
├── models/
│   ├── environments/
│   ├── props/
│   └── characters/
├── textures/
├── audio/
│   ├── music/
│   ├── sfx/
│   └── voice/
├── animations/
└── README.md
```

**Storage:** Large assets on CDN, not in git

---

## Tech Requirements

| Feature | Requirement |
|---------|-------------|
| Frame rate | 72+ FPS for VR |
| Latency | <100ms for networking |
| Load time | <5s initial load |
| Mobile | Must work on phone browsers |

---

*Interactive repos are where imagination becomes reality.*
