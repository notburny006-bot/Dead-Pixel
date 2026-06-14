import esper
from components import Position, Velocity, Player, Friction, Collider, Enemy, BossAI, MinibossAI


class MovementSystem(esper.Processor):
    """Apply velocity to position. Clamp player to screen. Enemy behavior by kind."""

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

            # Enemy behavior overrides
            enemy = esper.try_component(ent, Enemy)
            if enemy:
                self._enemy_behavior(ent, pos, vel, enemy, dt)

            # Clamp player to screen bounds
            if esper.has_component(ent, Player):
                collider = esper.try_component(ent, Collider)
                size = collider.width if collider else 48
                pos.x = max(0, min(pos.x, self.game.width - size))
                pos.y = max(0, min(pos.y, self.game.height - size))

    def _enemy_behavior(self, ent, pos, vel, enemy, dt):
        if enemy.kind == "basic":
            return

        if enemy.kind == "miniboss":
            ai = esper.try_component(ent, MinibossAI)
            if ai and pos.y < self.game.height * 0.7:
                vel.dy = 0
                ai.strafe_timer -= dt
                if ai.strafe_timer <= 0:
                    ai.direction *= -1
                    ai.strafe_timer = 1.5
                vel.dx = 80 * ai.direction
                # Clamp to screen
                collider = esper.try_component(ent, Collider)
                size = collider.width if collider else 56
                if pos.x <= 0 or pos.x >= self.game.width - size:
                    ai.direction *= -1

        elif enemy.kind == "boss":
            ai = esper.try_component(ent, BossAI)
            if ai and pos.y < self.game.height * 0.6:
                vel.dy = 0
                ai.move_timer -= dt
                if ai.move_timer <= 0:
                    ai.direction *= -1
                    ai.move_timer = 2.0
                vel.dx = 60 * ai.direction
                # Clamp to screen
                collider = esper.try_component(ent, Collider)
                size = collider.width if collider else 72
                if pos.x <= 0 or pos.x >= self.game.width - size:
                    ai.direction *= -1
