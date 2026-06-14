import esper
from components import Position, Velocity, Player, Friction
from constants import PLAYER_SIZE


class MovementSystem(esper.Processor):
    """Apply velocity to position. Clamp player to screen. Friction decelerates tilt input."""

    def __init__(self, game_widget):
        self.game = game_widget

    def process(self, dt):
        for ent, (pos, vel) in esper.get_components(Position, Velocity):
            pos.x += vel.dx * dt
            pos.y += vel.dy * dt

            # Apply friction (for tilt/accelerometer mode)
            friction = esper.try_component(ent, Friction)
            if friction:
                decay = max(0.0, 1.0 - friction.value * dt)
                vel.dx *= decay
                vel.dy *= decay
                if abs(vel.dx) < 0.5:
                    vel.dx = 0
                if abs(vel.dy) < 0.5:
                    vel.dy = 0

            # Clamp player to screen bounds
            if esper.has_component(ent, Player):
                pos.x = max(0, min(pos.x, self.game.width - PLAYER_SIZE))
                pos.y = max(0, min(pos.y, self.game.height - PLAYER_SIZE))
