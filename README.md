# Dead Pixel

A roguelite space shooter for Android. Survive infinite waves of enemies, collect upgrades, and build your ship each run.

## Gameplay

- **Portrait vertical shooter** — enemies spawn from the top, you shoot from the bottom
- **Drag-to-move** — touch and drag to move your ship (tilt mode planned)
- **Auto-fire** — your ship shoots automatically, focus on dodging
- **Wave-based** — enemies get faster, tougher, and more numerous each wave
- **Roguelite runs** — upgrade between waves, but death resets your build

## Tech Stack

| Layer | Tech |
|-------|------|
| Language | Python 3.10 |
| Framework | Kivy (UI + rendering) |
| Architecture | ECS via esper 3.7 |
| Build | Buildozer → Android APK |
| CI | GitHub Actions |

## Architecture

Entity Component System — data is separate from logic:

- **Components** (`components/`) — pure data classes (Position, Velocity, Health, etc.)
- **Systems** (`systems/`) — processors that run each frame (Input, Movement, Collision, etc.)
- **Factories** (`factories/`) — entity creation functions (player, enemy, bullet)
- **Data** (`data/`) — static definitions (enemy types, scaling constants)

```
Frame loop:
  InputSystem → WeaponSystem → MovementSystem → RenderSystem
                                    ↑               |
                              CollisionSystem   CleanupSystem
                                    |
                              SpawnSystem
```

## Running

```bash
# Desktop (requires Kivy + esper)
pip install kivy esper pillow
python3 main.py

# Android APK (via CI or local buildozer)
buildozer android debug
```

## Current Version: v0.3

- [x] Player movement (drag-to-move, velocity-based)
- [x] Auto-fire bullets
- [x] Enemy spawning with wave scaling
- [x] AABB collision detection
- [x] Score tracking via events
- [ ] Game over screen + restart (v0.4)
- [ ] Upgrade system between waves (v0.5)
- [ ] Tilt/accelerometer input (v0.6)
- [ ] Multiple enemy types (future)
- [ ] Shop + meta-progression (future)

## Project Structure

```
space-hunter/
├── main.py                    # App entry + lifecycle
├── game.py                    # Game loop + system wiring
├── constants.py               # Game-wide constants
├── buildozer.spec             # APK build config
├── generate_assets.py         # ASCII art → PNG
├── components/__init__.py     # ECS data classes
├── factories/
│   ├── player_factory.py
│   ├── enemy_factory.py
│   └── bullet_factory.py
├── data/
│   └── enemies.py             # Enemy definitions + scaling
├── systems/
│   ├── input_system.py
│   ├── movement_system.py
│   ├── weapon_system.py
│   ├── collision_system.py
│   ├── spawn_system.py
│   ├── render_system.py
│   └── cleanup_system.py
└── assets/                    # Sprite PNGs
```

## License

MIT
