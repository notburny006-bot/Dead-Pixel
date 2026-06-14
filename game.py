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
from systems.hud_system import HudSystem
from ui.game_over_screen import GameOverScreen
from factories.player_factory import create_player


class DeadPixelGame(Widget):
    """Main game widget. Manages esper ECS + Kivy rendering."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        esper.clear_database()

        # Systems
        self._setup_systems()

        # Game over screen (overlay)
        self.game_over_screen = GameOverScreen(self, self.hud_system)
        self.add_widget(self.game_over_screen)

        # Player entity created on first update (need width/height)
        self.player_entity = None

        # Game loop at 60fps
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _setup_systems(self):
        """Register all ECS processors."""
        self.input_system = InputSystem(self)
        self.render_system = RenderSystem(self)
        self.hud_system = HudSystem(self)
        esper.add_processor(self.input_system, priority=0)
        esper.add_processor(WeaponSystem(), priority=1)
        esper.add_processor(MovementSystem(self), priority=2)
        esper.add_processor(self.render_system, priority=3)
        esper.add_processor(CollisionSystem(self, self.render_system), priority=4)
        esper.add_processor(SpawnSystem(self), priority=5)
        esper.add_processor(CleanupSystem(self, self.render_system), priority=6)
        esper.add_processor(self.hud_system, priority=7)

    def _create_player(self):
        """Create player using factory."""
        self.player_entity = create_player(self.width, self.height)

    def on_touch_down(self, touch):
        if self._paused:
            return
        self.input_system.on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._paused:
            return
        self.input_system.on_touch_move(touch)

    def on_touch_up(self, touch):
        if self._paused:
            return
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

    def restart(self):
        """Full game reset. Called from GameOverScreen."""
        self.render_system.clear_all()
        esper.clear_database()

        self._setup_systems()
        self.player_entity = None
        self.hud_system.score = 0
        self.hud_system.wave = 1

        # Re-register game over handler
        esper.set_handler("player_died", self.game_over_screen._on_player_died)

        self.resume()
