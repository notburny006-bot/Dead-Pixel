"""Enemy type definitions. Stats scale with wave number."""

from dataclasses import dataclass


@dataclass
class EnemyDef:
    name: str
    base_hp: int
    base_speed: float
    size: int
    source: str


ENEMIES = {
    "basic": EnemyDef(
        name="basic",
        base_hp=20,
        base_speed=120.0,
        size=40,
        source="",
    ),
    "miniboss": EnemyDef(
        name="miniboss",
        base_hp=80,
        base_speed=80.0,
        size=56,
        source="",
    ),
    "boss": EnemyDef(
        name="boss",
        base_hp=200,
        base_speed=50.0,
        size=72,
        source="",
    ),
}

HP_SCALE_PER_WAVE = 5   # extra HP per wave
SPEED_SCALE_PER_WAVE = 10  # extra speed per wave
