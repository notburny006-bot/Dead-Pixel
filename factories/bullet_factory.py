import esper
from components import Position, Velocity, Renderable, Bullet, Collider
from constants import BULLET_SIZE

BULLET_SPEED = 600.0  # pixels per second, upward


def create_bullet(x: float, y: float, damage: int, owner: str = "player") -> int:
    """Create a bullet entity. Player bullets go up, enemy bullets go down."""
    dy = BULLET_SPEED if owner == "player" else -BULLET_SPEED
    return esper.create_entity(
        Position(x, y),
        Velocity(0, dy),
        Collider(BULLET_SIZE[0], BULLET_SIZE[1]),
        Bullet(owner=owner, damage=damage),
        Renderable(source="assets/bullet.png", size=BULLET_SIZE),
    )
