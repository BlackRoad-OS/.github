# BlackRoad-Interactive Signals

> Signal handlers for the Interactive org

---

## Inbound Signals (INT receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `📊 OS → INT` | Bridge | State update | `display.update()` |
| `💬 AI → INT` | AI | Cece response | `cece.speak()` |
| `👤 FND → INT` | Foundation | User data | `avatar.customize()` |
| `🔊 OS → INT` | Bridge | Notification | `world.notify()` |

---

## Outbound Signals (INT sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `🎮 INT → OS` | Bridge | User joined | On enter world |
| `👋 INT → OS` | Bridge | User left | On exit |
| `🎤 INT → AI` | AI | Voice message | On speak to Cece |
| `💬 INT → AI` | AI | Text message | On chat to Cece |
| `🖱️ INT → OS` | Bridge | User action | On interaction |
| `📸 INT → ARC` | Archive | Screenshot | On capture |

---

## Presence Signals

```
# User enters
🎮 INT → OS : user_joined, world=bridge, user=alexa, device=vr

# User moves
📍 INT → OS : user_moved, user=alexa, pos=[1.2, 0, 3.4], world=bridge

# User leaves
👋 INT → OS : user_left, world=bridge, user=alexa, duration=45m
```

---

## Cece Interaction Signals

```
# Voice to Cece
🎤 INT → AI : voice_message, user=alexa, audio=<base64>, world=bridge

# Cece responds (voice)
🔊 AI → INT : voice_response, audio=<base64>, gestures=[wave, nod]

# Text to Cece
💬 INT → AI : text_message, user=alexa, text="Hey Cece!", world=bridge

# Cece responds (text)
💬 AI → INT : text_response, text="Hey Alexa!", emotion=happy
```

---

## World State Signals

```
# World loaded
🌍 INT → OS : world_loaded, world=bridge, users=3, objects=156

# Object interaction
🖱️ INT → OS : object_clicked, object=status_board, user=alexa

# State change
🔄 INT → OS : world_state_changed, world=bridge, change=lighting

# Performance
📊 INT → OS : performance, fps=72, latency=45ms, users=5
```

---

## Social Signals

```
# Voice chat
🎤 INT → INT : voice_start, user=alexa, channel=general
🔇 INT → INT : voice_mute, user=alexa

# Text chat
💬 INT → INT : chat_message, user=alexa, channel=general, text="Hi all!"

# Emote
😄 INT → INT : emote, user=alexa, emote=wave

# Friend
👥 INT → FND : friend_request, from=alexa, to=bob
```

---

## Data Visualization Signals

When Bridge data updates, visualize it:

```
# Status board update
📊 OS → INT : status_update, data=<.STATUS contents>
🖼️ INT : Rendered to 3D status board in Bridge space

# Signal stream
📡 OS → INT : signal_stream, signals=[...]
🌊 INT : Animated as flowing particles in world

# Memory update
🧠 OS → INT : memory_update, data=<MEMORY.md contents>
📜 INT : Rendered to memory wall
```

---

*Interactive signals bridge the real and virtual.*
