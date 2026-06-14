import esper
from kivy.app import App
from kivy.uix.screenmanager import Screen
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
from factories.player_factory import create_player
from data.ships import SHIPS


class GameWidget(Widget):
    """Game rendering + ECS logic. Embedded inside GameScreen."""

    def __init__(self, ship_id: str, **kwargs):
        super().__init__(**kwargs)
        self.ship_id = ship_id
        esper.clear_database()
        self._setup_systems()
        self.player_entity = None
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _reset(self):
        """Reset ECS for a new run without re-creating GameWidget."""
        esper.clear_database()
        self._setup_systems()
        self.player_entity = None
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _setup_systems(self):
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
        esper.set_handler("player_died", self._on_player_died)

    def _create_player(self):
        self.player_entity = create_player(self.width, self.height, ship_id=self.ship_id)

    def _on_player_died(self):
        self.pause()
        sm = App.get_running_app().root
        game_over = sm.get_screen("game_over")
        game_over.show(self.hud_system.score, self.hud_system.wave)

    def on_touch_down(self, touch):
        if not self._paused:
            self.input_system.on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self._paused:
            self.input_system.on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self._paused:
            self.input_system.on_touch_up(touch)

    def update(self, dt):
        if self.player_entity is None and self.width > 0 and self.height > 0:
            self._create_player()
        esper.process(dt)

    def pause(self):
        self.game_loop.cancel()
        self._paused = True

    def resume(self):
        if self._paused:
            self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
            self._paused = False


class GameScreen(Screen):
    """Screen wrapper — creates fresh GameWidget on enter."""

    def __init__(self, **kwargs):
        super().__init__(name="game", **kwargs)
        self.game_widget = None

    def on_enter(self, *args):
        ship_id = self.parent.selected_ship_id

        if self.game_widget:
            self.game_widget._reset()
        else:
            self.game_widget = GameWidget(ship_id)
            self.add_widget(self.game_widget)

    def on_leave(self, *args):
        if self.game_widget:
            self.game_widget.pause()
