import esper
from components import Position, Velocity, Renderable, Bullet, Collider
from constants import BULLET_SIZE

BULLET_SPEED = 600.0  # pixels per second, upward


def create_bullet(x: float, y: float, damage: int, owner: str = "player") -> int:
    """Create a bullet entity at the given position moving upward."""
    return esper.create_entity(
        Position(x, y),
        Velocity(0, BULLET_SPEED),  # positive Y = upward in Kivy
        Collider(BULLET_SIZE[0], BULLET_SIZE[1]),
        Bullet(owner=owner, damage=damage),
        Renderable(source="assets/bullet.png"),
    )
