"""Factory for creating enemy entities from enemy definitions."""

import random
import esper
from components import Position, Velocity, Health, Enemy, Collider, Renderable
from data.enemies import ENEMIES, HP_SCALE_PER_WAVE, SPEED_SCALE_PER_WAVE


def create_enemy(enemy_type: str, x: float, y: float, wave: int) -> int:
    """Create an enemy entity. Stats scale with wave number."""
    defn = ENEMIES[enemy_type]

    hp = defn.base_hp + (wave - 1) * HP_SCALE_PER_WAVE
    speed = defn.base_speed + (wave - 1) * SPEED_SCALE_PER_WAVE

    return esper.create_entity(
        Position(x, y),
        Velocity(0, -speed),
        Health(current=hp, max_hp=hp),
        Collider(defn.size, defn.size),
        Renderable(source=defn.source, size=(defn.size, defn.size)),
        Enemy(),
    )
