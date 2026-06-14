# Space Hunter — Senior Review + Promoted Plan

---

## Senior Review

**Altitude diagnosis:** Mixed — fog on rendering bridge and Kivy-esper integration, tunnel on file structure.

### Blockers

- **[B1] esper 3.7 API is module-level, not `World()`.** Plan uses `world = esper.World()` and `world.get_components()`. Actual API: `esper.create_entity()`, `esper.get_components()`, `esper.process()`, `esper.add_processor()`. No `World` class exists in 3.7. Evidence: `python3 -c "import esper; print(dir(esper))"` — no `World` attribute. **Fix:** All code must use module-level esper calls.

- **[B2] No rendering bridge defined.** Plan says entities are Kivy Widgets but esper entities are plain ints. How does a Position component update a Kivy widget on screen? Plan skips this entirely — this is the hardest integration point. **Fix:** Define a RenderSystem that syncs Position components to Kivy widget positions.

### Major

- **[M1] Bullet component has no damage field.** Collision system uses `bullet.damage` but Bullet dataclass only has `owner: str`. **Fix:** Add `damage: int` to Bullet or pull from Weapon component.

- **[M2] Upgrade lambdas won't serialize.** Plan defines upgrades as lambda functions — can't save to JSON for persistence, can't display upgrade descriptions cleanly. **Fix:** Define upgrades as data with field path + value modifier.

- **[M3] No Kivy lifecycle handling.** Android apps pause/resume. No mention of `on_pause`/`on_resume` or `on_stop`. **Fix:** Add lifecycle methods to App class, pause/unpause game loop.

### Minor

- **[m1]** `Sprite.widget: Any` is fragile — should be typed as Optional[KivyWidget] or similar.
- **[m2]** Code style says "event-driven" but no event system defined. esper has `dispatch_event`/`set_handler` — use it or remove the claim.

### What the junior got right

- ECS choice correct for roguelite scope
- Wave-based spawning with data-driven definitions
- Clear file structure with separation of concerns
- Prototype scope is well-bounded

---

## Promoted Plan (v2)

# Space Hunter — Roguelite Space Shooter Plan

## Context
Building an Android APK roguelite space shooter with ASCII art assets. Top-down vertical shooter where the player survives infinite waves, collects upgrades, and creates builds during runs. Prototype first, expand later. Built with Python + Kivy + Buildozer on Termux-chroot.

---

## Architecture: Full ECS with esper 3.7

Using **esper 3.7** — lightweight Python ECS. Module-level API (no World class).

```python
# Components are pure data (dataclasses)
@dataclass
class Position:
    x: float
    y: float

@dataclass
class Health:
    current: int
    max_hp: int

@dataclass
class Weapon:
    damage: int
    fire_rate: float
    fire_cooldown: float = 0.0
    projectile_count: int = 1

@dataclass
class Speed:
    value: float  # pixels per second

@dataclass
class Velocity:
    dx: float
    dy: float

@dataclass
class Collider:
    width: float
    height: float

@dataclass
class Renderable:
    """Marks entity for rendering. RenderSystem manages Kivy widget."""
    source: str
    widget: Any = None  # Kivy Image widget, managed by RenderSystem

@dataclass
class Player:
    """Tag component for the player entity."""

@dataclass
class Enemy:
    """Tag component for enemy entities."""

@dataclass
class Bullet:
    owner: str      # "player" or "enemy"
    damage: int     # damage per hit

@dataclass
class Pickup:
    upgrade_id: str

@dataclass
class Currency:
    gold: int = 0

@dataclass
class Inventory:
    items: list = field(default_factory=list)  # list of item IDs

@dataclass
class SynergyBonus:
    id: str
    active: bool = False
```

```python
# Systems use esper.Processor base class
class CollisionSystem(esper.Processor):
    def process(self, dt):
        for ent_a, (pos_a, col_a, bullet) in esper.get_components(Position, Collider, Bullet):
            for ent_b, (pos_b, col_b, health) in esper.get_components(Position, Collider, Health):
                if self.aabb_overlap(pos_a, col_a, pos_b, col_b):
                    health.current -= bullet.damage
                    esper.delete_entity(ent_a)
                    if health.current <= 0:
                        esper.delete_entity(ent_b)
```

**Rendering bridge — RenderSystem:**
esper entities are ints. Kivy widgets are separate. RenderSystem syncs them:
```python
class RenderSystem(esper.Processor):
    def __init__(self, game_widget):
        self.game = game_widget  # Kivy game container

    def process(self, dt):
        for ent, (pos, rend) in esper.get_components(Position, Renderable):
            if rend.widget is None:
                rend.widget = Image(source=rend.source, size=(40, 40))
                self.game.add_widget(rend.widget)
            rend.widget.pos = (pos.x, pos.y)

        # Cleanup: remove widgets for deleted entities
        # (handled via esper delete_entity + widget removal in cleanup system)
```

**Why esper over custom component system:**
- Collision needs Position + Collider across all entity types
- Build system modifies Weapon + Stats on player
- Wave system spawns enemies with Health + Velocity + AI
- Status effects add/remove components dynamically
- All of this is natural with esper, spaghetti with inheritance

---

## File Structure

```
space-hunter/
├── main.py                    # App entry, creates World + runs
├── game.py                    # Game loop, system orchestration
├── buildozer.spec             # APK build config
├── generate_assets.py         # ASCII art → PNG generator
│
├── components/                # Pure data — no logic
│   ├── __init__.py
│   ├── position.py            # Position(x, y)
│   ├── velocity.py            # Velocity(dx, dy)
│   ├── health.py              # Health(current, max_hp)
│   ├── weapon.py              # Weapon(damage, fire_rate, projectile_count)
│   ├── collider.py            # Collider(width, height)
│   ├── sprite.py              # Sprite(source, widget)
│   └── tags.py                # Player, Enemy, Bullet(owner), Pickup(upgrade_id)
│
├── systems/                   # Process components each frame
│   ├── __init__.py
│   ├── input_system.py        # Touch → player Position
│   ├── movement_system.py     # Position += Velocity
│   ├── weapon_system.py       # Auto-fire bullets from Weapon
│   ├── collision_system.py    # AABB checks, damage, entity deletion
│   ├── spawn_system.py        # Wave-based enemy spawning
│   ├── cleanup_system.py      # Remove off-screen entities
│   ├── hud_system.py          # Update score/HP/wave labels
│   ├── shop_system.py         # Buy/sell logic, inventory management
│   └── synergy_system.py      # Detect item combos, apply bonuses
│
├── factories/                 # Entity creation helpers
│   ├── __init__.py
│   ├── player_factory.py      # Creates player entity with all components
│   ├── enemy_factory.py       # Creates enemy by type
│   └── bullet_factory.py      # Creates bullet from weapon stats
│
├── data/                      # Static definitions
│   ├── __init__.py
│   ├── upgrades.py            # Upgrade definitions (stat modifications)
│   ├── enemies.py             # Enemy type stat blocks
│   ├── waves.py               # Wave composition + scaling
│   ├── shop_items.py          # Buyable items with costs + effects
│   └── synergies.py           # Combo definitions (item A + B → bonus)
│
├── ui/                        # Kivy overlay screens
│   ├── __init__.py
│   ├── hud.py                 # Score, HP bar, wave number
│   ├── upgrade_screen.py      # Pick 1 of 3 upgrades overlay
│   ├── shop_screen.py         # Between-wave shop overlay
│   └── game_over_screen.py    # Death stats + restart
│
└── assets/
    ├── player.png
    ├── enemy.png
    └── bullet.png
```

---

## Core Systems Design

### 1. Game Loop (`game.py`)
```python
# esper 3.7 module-level API + Kivy Clock
class SpaceHunterGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        esper.clear_database()

        # Register systems (priority=0 runs first)
        esper.add_processor(InputSystem(), priority=0)
        esper.add_processor(WeaponSystem(), priority=1)
        esper.add_processor(MovementSystem(), priority=2)
        esper.add_processor(SpawnSystem(), priority=3)
        esper.add_processor(RenderSystem(self), priority=4)
        esper.add_processor(CollisionSystem(), priority=5)
        esper.add_processor(CleanupSystem(self), priority=6)
        esper.add_processor(HudSystem(), priority=7)

        self.game_loop = Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        esper.process(dt)

    def pause(self):
        self.game_loop.cancel()

    def resume(self):
        self.game_loop = Clock.schedule_interval(self.update, 1/60)
```

### 2. Spawn System (`systems/spawn_system.py`)
**Hybrid model:**
- Waves defined by data (enemy types + counts)
- Between waves: upgrade choices
- Every 5 waves: shop appears
- Difficulty scales: more enemies, faster, new types unlock

```python
# Wave data example
wave_1 = {"enemies": [{"type": "basic", "count": 5}]}
wave_5 = {"enemies": [{"type": "basic", "count": 8}, {"type": "fast", "count": 3}]}
wave_10 = {"enemies": [{"type": "basic", "count": 10}, {"type": "fast", "count": 5}, {"type": "tank", "count": 2}]}
```

### 3. Upgrade System
**Prototype scope — stat boosts applied to player components**
- On wave complete: show 3 random upgrades
- Player picks one, component modified directly via esper

```python
# Upgrades are data, not lambdas — serializable, displayable
@dataclass
class UpgradeDef:
    id: str
    name: str
    description: str
    component: type        # which component to modify
    field: str             # which field
    modifier: float        # additive value

UPGRADES = [
    UpgradeDef("damage_up", "+Damage", "Increase bullet damage", Weapon, "damage", 2),
    UpgradeDef("fire_rate_up", "+Fire Rate", "Shoot faster", Weapon, "fire_rate", -0.1),
    UpgradeDef("speed_up", "+Speed", "Move faster", Speed, "value", 50),
    UpgradeDef("max_hp_up", "+Max HP", "More health", Health, "max_hp", 20),
]

def apply_upgrade(player_entity: int, upgrade: UpgradeDef) -> None:
    comp = esper.component_for_entity(player_entity, upgrade.component)
    current = getattr(comp, upgrade.field)
    setattr(comp, upgrade.field, current + upgrade.modifier)
    # Special case: max_hp also heals
    if upgrade.component == Health and upgrade.field == "max_hp":
        comp.current += upgrade.modifier
```

**Full game expansion path:**
- Pickup items that drop from enemies (passive synergies)
- Shop with currency earned from kills
- Weapon types (spread shot, laser, missile)
- Ship hull unlocks (meta-progression)
- Status effect components (poison, freeze, burn) added/removed dynamically

### Shop Items (`data/shop_items.py`)
```python
@dataclass
class ShopItemDef:
    id: str
    name: str
    description: str
    cost: int
    component: type        # which component to modify
    field: str             # which field
    modifier: float        # additive value

SHOP_ITEMS = [
    ShopItemDef("shield_module", "Shield Module", "+50 max HP", 100, Health, "max_hp", 50),
    ShopItemDef("rapid_coolant", "Rapid Coolant", "Faster fire rate", 150, Weapon, "fire_rate", -0.15),
    ShopItemDef("thruster_boost", "Thruster Boost", "+80 speed", 120, Speed, "value", 80),
    ShopItemDef("overclock", "Overclock", "+5 damage", 200, Weapon, "damage", 5),
]
```

### Synergies (`data/synergies.py`)
```python
@dataclass
class SynergyDef:
    id: str
    name: str
    items: list[str]       # required item IDs
    description: str
    component: type        # component to modify
    field: str
    modifier: float        # bonus value
    active: bool = False

SYNERGIES = [
    SynergyDef("fire_storm", "Fire Storm", ["rapid_coolant", "overclock"],
               "Fire rate doubled", Weapon, "fire_rate", -0.3),
    SynergyDef("tank_build", "Tank Build", ["shield_module", "thruster_boost"],
               "Max HP +100 bonus", Health, "max_hp", 100),
]
```

### 4. Collision System (`systems/collision_system.py`)
```python
class CollisionSystem(esper.Processor):
    def __init__(self, game_widget):
        self.game = game_widget

    def process(self, dt):
        # Player bullets → enemies
        for b_ent, (b_pos, b_col, bullet) in esper.get_components(Position, Collider, Bullet):
            if bullet.owner != "player":
                continue
            for e_ent, (e_pos, e_col, health, _) in esper.get_components(Position, Collider, Health, Enemy):
                if self.aabb_overlap(b_pos, b_col, e_pos, e_col):
                    health.current -= bullet.damage
                    # Remove Kivy widget BEFORE deleting entity
                    b_rend = esper.try_component(b_ent, Renderable)
                    if b_rend and b_rend.widget:
                        self.game.remove_widget(b_rend.widget)
                    esper.delete_entity(b_ent)
                    if health.current <= 0:
                        e_rend = esper.try_component(e_ent, Renderable)
                        if e_rend and e_rend.widget:
                            self.game.remove_widget(e_rend.widget)
                        esper.delete_entity(e_ent)
                    break
```
- AABB overlap check: `pos1.x < pos2.x + w2 and pos1.x + w1 > pos2.x and ...`
- Score tracked via esper event: `esper.dispatch_event("enemy_killed", 10)`

### 5. Shop System (`systems/shop_system.py`)
```python
class ShopSystem(esper.Processor):
    """Between-wave shop. Every N waves, player spends currency on items."""

    def process(self, dt):
        # Triggered externally when wave clears + wave % SHOP_INTERVAL == 0
        pass

    def buy_item(self, player_entity: int, item: ShopItemDef) -> bool:
        currency = esper.component_for_entity(player_entity, Currency)
        if currency.gold >= item.cost:
            currency.gold -= item.cost
            inv = esper.component_for_entity(player_entity, Inventory)
            inv.items.append(item.id)
            item.apply(player_entity)  # immediate stat effect
            esper.dispatch_event("inventory_changed", player_entity)
            return True
        return False
```
- Appears when `wave_number % SHOP_INTERVAL == 0`
- Shows items from `data/shop_items.py`
- Player buys with Currency (earned from kills)
- Items stored in Inventory component
- After purchase, synergy check triggers

### 6. Synergy System (`systems/synergy_system.py`)
```python
class SynergySystem(esper.Processor):
    """Detect item combos, apply bonus effects."""

    def __init__(self):
        esper.set_handler("inventory_changed", self.check_synergies)

    def check_synergies(self, player_entity: int):
        inv = esper.component_for_entity(player_entity, Inventory)
        for synergy_def in SYNERGIES:
            # Find matching SynergyBonus component on player
            for ent, bonus in esper.get_component(SynergyBonus):
                if bonus.id == synergy_def.id:
                    has_all = all(item in inv.items for item in synergy_def.items)
                    if has_all and not bonus.active:
                        synergy_def.apply_bonus(player_entity)
                        bonus.active = True
                    elif not has_all and bonus.active:
                        synergy_def.remove_bonus(player_entity)
                        bonus.active = False
```
- After any inventory change, scan `data/synergies.py`
- If player owns items A + B → apply synergy bonus
- Bonus adds/modifies components on player
- Visual feedback: synergy name appears on HUD

### 7. Persistence System (`systems/persistence_system.py`)
- Save to JSON file in app data directory
- Track: total runs, best wave, best score, currency earned
- Meta unlocks: new starting ships (future)
- **Prototype:** just save/load best score and total currency

---

## Version Roadmap

### v0.1 — Bare Bones (get something on screen)
- Components: Position, Speed, Renderable, Player tag
- Player entity at bottom center
- InputSystem: drag-to-move (free movement, X+Y, bounded to screen)
- RenderSystem: sync Position → Kivy widget
- Game loop: esper.process() at 60fps
- **Test:** ship appears, drags freely within screen bounds

### v0.2 — Shooting
- Components: Weapon, Bullet
- WeaponSystem: auto-fire bullets upward
- Bullet factory: create_bullet()
- MovementSystem: bullets move up, enemies move down
- CleanupSystem: delete off-screen entities
- **Test:** ship auto-fires, bullets fly off screen

### v0.3 — Enemies + Collision
- Components: Health, Collider, Enemy tag
- Enemy factory: create_enemy()
- SpawnSystem: spawn enemy wave (hardcoded count)
- CollisionSystem: bullet↔enemy AABB, damage, deletion
- Score tracking via esper.dispatch_event
- **Test:** enemies spawn, bullets kill them, score increments

### v0.4 — Waves + Game Over
- Wave data: enemy counts per wave, scaling
- SpawnSystem: wave-based spawning, track wave state
- Health on player, enemies reaching bottom = damage
- GameOverScreen: show score, restart button
- HudSystem: score + HP + wave number display
- **Test:** waves progress, die → game over → restart

### v0.5 — Ship Selection (CURRENT)
- `data/ships.py`: ShipDef dataclass + 3 ships (phantom_wing, viper_scout, serpent_class)
- `ui/ship_select_screen.py`: carousel with arrows, preview image, stats display
- `ui/screen_manager.py`: selected_ship_id state, go_game(ship_id)
- `game.py`: GameWidget takes ship_id, passes to player factory
- `factories/player_factory.py`: create_player(ship_id=...) reads ShipDef
- Main menu PLAY → ship_select (was direct to game)
- Ship art at 192px in assets/ships_ascii/final/

**Pre-commit checklist:**
- [x] Ship select default image uses first SHIP_ORDER entry
- [x] Final ship PNGs exist at assets/ships_ascii/final/{phantom_wing,viper_scout,serpent_class}.png
- [x] Static Python compile checks pass
- [ ] App runs interactively: `python main.py`
- [ ] Carousel cycles 3 ships, stats update, SELECT starts game with correct ship

### v0.6 — Upgrades
- UpgradeDef dataclass + UPGRADES list
- UpgradeScreen: pick 1 of 3 between waves
- apply_upgrade(): modify player components
- Wave clear detection → show upgrade → next wave
- **Test:** wave clears, pick upgrade, stat changes apply

### v0.6b — Shop + Synergies
- ShopItemDef dataclass + SHOP_ITEMS list
- ShopSystem: buy items with currency
- ShopScreen: overlay with items + prices, appears every 5 waves
- SynergyDef dataclass + SYNERGIES list
- SynergySystem: detect item combos, apply bonuses
- Currency component on player, earned from kills
- Inventory component tracks owned items
- **Test:** wave clears → shop appears → buy item → synergy activates

### v0.6 — Polish + Settings
- Tilt input option (accelerometer)
- Settings screen: input mode toggle
- Special ability: tap for screen nuke (cooldown)
- Difficulty scaling: enemy speed/hp increases per wave
- **Test:** tilt works, special ability works, difficulty ramps

### v0.7 — APK Build
- buildozer.spec verified
- buildozer android debug
- Install + test on phone
- **Test:** APK installs, game runs on device

### Future (post-prototype)
- Multiple enemy types (fast, tank, shooter)
- Shop system (every 5 waves)
- Pickup items (drops from enemies)
- Meta-progression (persistent unlocks)
- Weapon variety (spread, laser, missile)

---

## Delta Summary (v1 → v2)

- esper 3.7 uses module-level API (`esper.create_entity()`, not `world.create_entity()`)
- Added RenderSystem to bridge esper entities → Kivy widgets
- Bullet component now has `damage` field
- Upgrades changed from lambdas to `UpgradeDef` dataclass (serializable)
- Added Kivy lifecycle (on_pause/on_resume/on_stop)
- Removed "event-driven" claim, replaced with `esper.dispatch_event`/`set_handler`
- Collision system: added `break` after hit, score via dispatch_event

---

## Design Decisions

- **Input:** Both tilt and drag-to-move. Player picks in settings. Default: drag. Free movement (X+Y+diagonal), bounded to screen.
- **Orientation:** Portrait. Enemies spawn from top, player at bottom.
- **Shooting:** Hybrid — auto-shoot main weapon, tap for special ability (screen nuke, shield, etc.)
- **Screen:** Fixed portrait resolution, scale to device.

---

## Code Style Rules

- **Type hints** on all function signatures
- **Dataclasses** for component data (not dicts)
- **Constants** in UPPER_SNAKE at top of files
- **No global state** — pass dependencies explicitly
- **Docstrings** on classes and public methods
- **Single responsibility** — each file does one thing
- **Events** — use `esper.dispatch_event` / `esper.set_handler` for cross-system communication
- **Widget cleanup** — call `game.remove_widget(rend.widget)` BEFORE `esper.delete_entity()` (deferred deletion leaves widget on screen)

---

## Kivy Lifecycle (Android)

```python
class SpaceHunterApp(App):
    def build(self):
        self.game = SpaceHunterGame()
        return self.game

    def on_pause(self):
        self.game.pause()
        return True

    def on_resume(self):
        self.game.resume()

    def on_stop(self):
        esper.clear_database()
```

---

## Verification

1. Run `python3 main.py` in Termux — game window opens
2. Touch to move ship, bullets fire automatically
3. Enemies spawn in waves, bullets kill them
4. Wave clears → upgrade screen appears
5. Pick upgrade → next wave starts with buff applied
6. Die → game over screen → restart
7. `buildozer android debug` → APK builds successfully
8. Install APK on phone → game runs
