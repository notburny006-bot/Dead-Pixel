"""Factory for creating the player entity."""

import esper
from components import Position, Velocity, Speed, Friction, Weapon, Health, Collider, Renderable, Player
from constants import PLAYER_SIZE, PLAYER_SPEED, PLAYER_START_Y_RATIO


def create_player(screen_width: float, screen_height: float) -> int:
    """Create player entity at center-bottom of screen."""
    return esper.create_entity(
        Position(screen_width / 2 - PLAYER_SIZE / 2, screen_height * PLAYER_START_Y_RATIO),
        Velocity(0, 0),
        Speed(PLAYER_SPEED),
        Friction(5.0),
        Weapon(damage=10, fire_rate=0.3),
        Health(current=100, max_hp=100),
        Collider(PLAYER_SIZE, PLAYER_SIZE),
        Renderable(source="assets/player.png", size=(PLAYER_SIZE, PLAYER_SIZE)),
        Player(),
    )
