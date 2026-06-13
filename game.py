import esper
from kivy.uix.widget import Widget
from kivy.clock import Clock

from components import Position, Speed, Renderable, Player, Weapon
from constants import PLAYER_SIZE, PLAYER_SPEED, PLAYER_START_Y
from systems.input_system import InputSystem
from systems.render_system import RenderSystem
from systems.weapon_system import WeaponSystem
from systems.movement_system import MovementSystem
from systems.cleanup_system import CleanupSystem


class SpaceHunterGame(Widget):
    """Main game widget. Manages esper ECS + Kivy rendering."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        esper.clear_database()

        # Systems (priority=0 runs first)
        self.input_system = InputSystem(self)
        self.render_system = RenderSystem(self)
        esper.add_processor(self.input_system, priority=0)
        esper.add_processor(WeaponSystem(), priority=1)
        esper.add_processor(MovementSystem(), priority=2)
        esper.add_processor(self.render_system, priority=3)
        esper.add_processor(CleanupSystem(self), priority=4)

        # Create player entity
        self.player_entity = esper.create_entity(
            Position(0, PLAYER_START_Y),
            Speed(PLAYER_SPEED),
            Weapon(damage=10, fire_rate=0.3),
            Renderable(source="assets/player.png"),
            Player(),
        )
        self._player_initialized = False

        # Bind touch events to input system
        self.bind(on_touch_down=self._touch_down)
        self.bind(on_touch_move=self._touch_move)
        self.bind(on_touch_up=self._touch_up)

        # Game loop at 60fps
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _touch_down(self, widget, touch):
        self.input_system.on_touch_down(touch)

    def _touch_move(self, widget, touch):
        self.input_system.on_touch_move(touch)

    def _touch_up(self, widget, touch):
        self.input_system.on_touch_up(touch)

    def update(self, dt):
        # Center player on first frame (need valid width/height)
        if not self._player_initialized and self.width > 0:
            pos = esper.component_for_entity(self.player_entity, Position)
            pos.x = self.width / 2 - PLAYER_SIZE / 2
            self._player_initialized = True

        esper.process(dt)

    def pause(self):
        self.game_loop.cancel()
        self._paused = True

    def resume(self):
        if self._paused:
            self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
            self._paused = False
