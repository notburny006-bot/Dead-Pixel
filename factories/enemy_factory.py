"""Factory for creating enemy entities from enemy definitions."""

import random
import esper
from components import (
    Position, Velocity, Health, Enemy, Collider, Renderable,
    BossAI, MinibossAI, Weapon,
)
from data.enemies import ENEMIES, HP_SCALE_PER_WAVE, SPEED_SCALE_PER_WAVE
from data.zones import get_zone
from constants import MAX_ENEMY_SPEED


def create_enemy(enemy_type: str, x: float, y: float, wave: int) -> int:
    """Create an enemy entity. Stats scale with wave number and zone."""
    defn = ENEMIES[enemy_type]
    zone = get_zone(wave)

    hp = (defn.base_hp + (wave - 1) * HP_SCALE_PER_WAVE) * zone.hp_mult
    speed = min((defn.base_speed + (wave - 1) * SPEED_SCALE_PER_WAVE) * zone.speed_mult, MAX_ENEMY_SPEED)

    enemy_comp = Enemy(kind=enemy_type)
    extra = []

    if enemy_type == "miniboss":
        extra.append(MinibossAI())
        extra.append(Weapon(damage=5 + wave, fire_rate=2.0))

    elif enemy_type == "boss":
        extra.append(BossAI())
        extra.append(Weapon(damage=10 + wave * 2, fire_rate=1.5))

    return esper.create_entity(
        Position(x, y),
        Velocity(0, -speed),
        Health(current=int(hp), max_hp=int(hp)),
        Collider(defn.size, defn.size),
        Renderable(source=defn.source, size=(defn.size, defn.size), fallback_key="enemy"),
        enemy_comp,
        *extra,
    )
