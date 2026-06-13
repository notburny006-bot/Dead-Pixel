import esper
from kivy.uix.widget import Widget
from kivy.clock import Clock

from components import Position, Speed, Renderable, Player
from systems.input_system import InputSystem
from systems.render_system import RenderSystem

# Player starts at bottom center
PLAYER_SIZE = 48


class SpaceHunterGame(Widget):
    """Main game widget. Manages esper ECS + Kivy rendering."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        esper.clear_database()

        # Systems (priority=0 runs first)
        self.input_system = InputSystem(self)
        esper.add_processor(self.input_system, priority=0)
        esper.add_processor(RenderSystem(self), priority=1)

        # Create player entity
        self.player_entity = esper.create_entity(
            Position(0, 0),  # set properly on first frame
            Speed(300.0),
            Renderable(source="assets/player.png"),
            Player(),
        )

        # Bind touch events to input system
        self.bind(on_touch_down=self._touch_down)
        self.bind(on_touch_move=self._touch_move)
        self.bind(on_touch_up=self._touch_up)

        # Game loop at 60fps
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)

    def _touch_down(self, widget, touch):
        self.input_system.on_touch_down(touch)

    def _touch_move(self, widget, touch):
        self.input_system.on_touch_move(touch)

    def _touch_up(self, widget, touch):
        self.input_system.on_touch_up(touch)

    def update(self, dt):
        # Center player on first frame (need valid width/height)
        pos = esper.component_for_entity(self.player_entity, Position)
        if pos.x == 0 and pos.y == 0 and self.width > 0:
            pos.x = self.width / 2 - PLAYER_SIZE / 2
            pos.y = 50

        esper.process(dt)

    def pause(self):
        self.game_loop.cancel()

    def resume(self):
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
