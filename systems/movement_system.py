import esper
from components import Position, Velocity


class MovementSystem(esper.Processor):
    """Apply velocity to position each frame."""

    def process(self, dt):
        for ent, (pos, vel) in esper.get_components(Position, Velocity):
            pos.x += vel.dx * dt
            pos.y += vel.dy * dt
