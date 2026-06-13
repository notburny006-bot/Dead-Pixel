import esper
from components import Position, Speed, Player

# How far touch delta is scaled (pixels per pixel dragged)
TOUCH_SENSITIVITY = 1.0


class InputSystem(esper.Processor):
    """Translate touch input to player movement. Free movement, bounded to screen."""

    def __init__(self, game_widget):
        self.game = game_widget
        self.touch_pos = None
        self.screen_w = 0
        self.screen_h = 0

    def on_touch_down(self, touch):
        self.touch_pos = (touch.x, touch.y)

    def on_touch_move(self, touch):
        if self.touch_pos is None:
            return
        dx = (touch.x - self.touch_pos[0]) * TOUCH_SENSITIVITY
        dy = (touch.y - self.touch_pos[1]) * TOUCH_SENSITIVITY

        for ent, (pos, speed, _) in esper.get_components(Position, Speed, Player):
            pos.x += dx
            pos.y += dy
            # Clamp to screen bounds
            pos.x = max(0, min(pos.x, self.screen_w - 48))
            pos.y = max(0, min(pos.y, self.screen_h - 48))

        self.touch_pos = (touch.x, touch.y)

    def on_touch_up(self, touch):
        self.touch_pos = None

    def process(self, dt):
        # Update screen size each frame (resizes handled)
        self.screen_w = self.game.width
        self.screen_h = self.game.height
