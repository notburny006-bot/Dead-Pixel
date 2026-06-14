"""Factory for creating the player entity."""

import esper
from components import Position, Velocity, Speed, Friction, Weapon, Health, Collider, Renderable, Player
from data.ships import SHIPS
from constants import PLAYER_START_Y_RATIO


def create_player(screen_width: float, screen_height: float, ship_id: str = "phantom_wing") -> int:
    """Create player entity at center-bottom of screen using ship stats."""
    ship = SHIPS[ship_id]
    return esper.create_entity(
        Position(screen_width / 2 - ship.size / 2, screen_height * PLAYER_START_Y_RATIO),
        Velocity(0, 0),
        Speed(ship.speed),
        Friction(5.0),
        Weapon(damage=ship.weapon_damage, fire_rate=ship.fire_rate),
        Health(current=ship.hp, max_hp=ship.hp),
        Collider(ship.size, ship.size),
        Renderable(source=ship.source, size=(ship.size, ship.size)),
        Player(),
    )
