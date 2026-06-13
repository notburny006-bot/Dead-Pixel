from dataclasses import dataclass
from typing import Any

# --- Core Components ---

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Speed:
    value: float  # pixels per second

@dataclass
class Velocity:
    dx: float
    dy: float

@dataclass
class Renderable:
    """Marks entity for rendering. RenderSystem manages Kivy widget."""
    source: str
    widget: Any = None

# --- Tag Components ---

@dataclass
class Player:
    """Tag component for the player entity."""

@dataclass
class Enemy:
    """Tag component for enemy entities."""

@dataclass
class Bullet:
    owner: str      # "player" or "enemy"
    damage: int

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
class Collider:
    width: float
    height: float

@dataclass
class Pickup:
    upgrade_id: str
