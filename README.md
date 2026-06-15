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
  InputSystem → WeaponSystem → MovementSystem → CollisionSystem → SpawnSystem → CleanupSystem → RenderSystem → HudSystem
```

## Running

```bash
# Desktop (requires Kivy + esper)
pip install kivy esper
python3 main.py

# Android APK (via CI or local buildozer)
buildozer android debug
```

## Current Version: v0.6

- [x] Player movement (drag-to-move, velocity-based)
- [x] Auto-fire bullets
- [x] Enemy spawning with wave scaling
- [x] AABB collision detection
- [x] Score tracking via events
- [x] Game over screen + restart
- [x] Ship selection (3 ships)
- [x] Zone/wave system (6 waves per zone, miniboss + boss)
- [x] Enemy AI behaviors (basic, miniboss strafe, boss patrol + shoot)
- [ ] Upgrade system between waves
- [ ] Tilt/accelerometer input
- [ ] More zones
- [ ] Shop + meta-progression

## Project Structure

```
dead-pixel/
├── main.py                    # App entry + lifecycle
├── game.py                    # Game loop + system wiring
├── constants.py               # Game-wide constants
├── buildozer.spec             # APK build config
├── components/__init__.py     # ECS data classes
├── factories/
│   ├── player_factory.py
│   ├── enemy_factory.py
│   └── bullet_factory.py
├── data/
│   ├── enemies.py             # Enemy definitions + scaling
│   ├── zones.py               # Zone biomes
│   ├── waves.py               # Wave composition
│   └── ships.py               # Ship definitions
├── systems/
│   ├── input_system.py
│   ├── movement_system.py
│   ├── weapon_system.py
│   ├── collision_system.py
│   ├── spawn_system.py
│   ├── render_system.py
│   ├── cleanup_system.py
│   └── hud_system.py
├── ui/
│   ├── screen_manager.py
│   ├── main_menu_screen.py
│   ├── ship_select_screen.py
│   └── game_over_screen.py
└── assets/                    # Sprite PNGs
```

## License

MIT
