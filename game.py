import esper
from kivy.uix.widget import Widget
from kivy.clock import Clock

from systems.input_system import InputSystem
from systems.render_system import RenderSystem
from systems.weapon_system import WeaponSystem
from systems.movement_system import MovementSystem
from systems.collision_system import CollisionSystem
from systems.spawn_system import SpawnSystem
from systems.cleanup_system import CleanupSystem
from factories.player_factory import create_player


class DeadPixelGame(Widget):
    """Main game widget. Manages esper ECS + Kivy rendering."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        esper.clear_database()

        # Systems (priority=0 runs first)
        self.input_system = InputSystem(self)
        self.render_system = RenderSystem(self)
        esper.add_processor(self.input_system, priority=0)
        esper.add_processor(WeaponSystem(), priority=1)
        esper.add_processor(MovementSystem(self), priority=2)
        esper.add_processor(self.render_system, priority=3)
        esper.add_processor(CollisionSystem(self, self.render_system), priority=4)
        esper.add_processor(SpawnSystem(self), priority=5)
        esper.add_processor(CleanupSystem(self, self.render_system), priority=6)

        # Player entity created on first update (need width/height)
        self.player_entity = None

        # Game loop at 60fps
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _create_player(self):
        """Create player using factory."""
        self.player_entity = create_player(self.width, self.height)

    def on_touch_down(self, touch):
        self.input_system.on_touch_down(touch)

    def on_touch_move(self, touch):
        self.input_system.on_touch_move(touch)

    def on_touch_up(self, touch):
        self.input_system.on_touch_up(touch)

    def update(self, dt):
        # Create player on first frame when dimensions are valid
        if self.player_entity is None and self.width > 0:
            self._create_player()

        esper.process(dt)

    def pause(self):
        self.game_loop.cancel()
        self._paused = True

    def resume(self):
        if self._paused:
            self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
            self._paused = False
