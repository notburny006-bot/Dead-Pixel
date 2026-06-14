import esper
from components import Position, Velocity, Speed, Player, Collider


class InputSystem(esper.Processor):
    """Set player velocity toward touch position. Release = instant stop."""

    def __init__(self, game_widget):
        self.game = game_widget
        self.touch_pos = None

    def on_touch_down(self, touch):
        self.touch_pos = (touch.x, touch.y)

    def on_touch_move(self, touch):
        self.touch_pos = (touch.x, touch.y)

    def on_touch_up(self, touch):
        self.touch_pos = None

    def process(self, dt):
        for ent, (pos, vel, speed, _) in esper.get_components(Position, Velocity, Speed, Player):
            if self.touch_pos is None:
                vel.dx = 0
                vel.dy = 0
                continue

            collider = esper.try_component(ent, Collider)
            size = collider.width if collider else 48

            center_x = pos.x + size / 2
            center_y = pos.y + size / 2
            dx = self.touch_pos[0] - center_x
            dy = self.touch_pos[1] - center_y
            dist = (dx * dx + dy * dy) ** 0.5

            if dist < 5:
                vel.dx = 0
                vel.dy = 0
            else:
                vel.dx = (dx / dist) * speed.max_speed
                vel.dy = (dy / dist) * speed.max_speed
