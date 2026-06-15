from dataclasses import dataclass, field
from typing import Any, Optional

from kivy.uix.widget import Widget

# --- Core Components ---

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Speed:
    max_speed: float  # max pixels per second

@dataclass
class Velocity:
    dx: float
    dy: float

@dataclass
class Renderable:
    """Marks entity for rendering. RenderSystem manages Kivy widget."""
    source: str
    size: tuple = (48, 48)  # (width, height) for widget sizing
    offset: tuple = (0, 0)
    fallback_key: str = "player"
    widget: Optional[Widget] = None

# --- Tag Components ---

@dataclass
class Player:
    """Tag component for the player entity."""

@dataclass
class Enemy:
    """Enemy entity with subtype."""
    kind: str = "basic"  # "basic", "miniboss", "boss"


@dataclass
class BossAI:
    """Boss behavior state."""
    phase: int = 0
    move_timer: float = 0.0
    direction: int = 1  # 1=right, -1=left


@dataclass
class MinibossAI:
    """Miniboss behavior state."""
    strafe_timer: float = 1.5
    direction: int = 1

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
class Friction:
    """Deceleration factor per second. 5.0 = snappy stop, 1.0 = slippery."""
    value: float

@dataclass
class Pickup:
    upgrade_id: str
