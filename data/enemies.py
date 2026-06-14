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
        source="assets/enemy.png",
    ),
    # Future enemy types:
    # "fast": EnemyDef(name="fast", base_hp=10, base_speed=200.0, size=30, source="assets/enemy_fast.png"),
    # "tank": EnemyDef(name="tank", base_hp=80, base_speed=60.0, size=60, source="assets/enemy_tank.png"),
}

HP_SCALE_PER_WAVE = 5   # extra HP per wave
SPEED_SCALE_PER_WAVE = 10  # extra speed per wave
