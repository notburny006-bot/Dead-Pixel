from itertools import count

import esper
from kivy.app import App
from kivy.graphics import Color, Rectangle
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


_WORLD_COUNTER = count(1)


class GameWidget(Widget):
    """Game rendering + ECS logic. Embedded inside GameScreen."""

    def __init__(self, ship_id: str, **kwargs):
        super().__init__(**kwargs)
        self.ship_id = ship_id
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        self._world_name = self._make_world_name()
        self._activate_world()
        self._setup_systems()
        self.player_entity = None
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _make_world_name(self):
        return f"game_{id(self)}_{next(_WORLD_COUNTER)}"

    def _activate_world(self):
        esper.switch_world(self._world_name)

    def _delete_world(self, world_name):
        try:
            if esper.current_world == world_name:
                esper.switch_world("default")
            esper.delete_world(world_name)
        except KeyError:
            pass

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def _reset(self):
        """Reset ECS for a new run without re-creating GameWidget."""
        self.pause()
        self._activate_world()
        if hasattr(self, "render_system"):
            self.render_system.clear_all()
        old_world = self._world_name
        self._world_name = self._make_world_name()
        self._delete_world(old_world)
        self._activate_world()
        self._setup_systems()
        self.player_entity = None
        self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
        self._paused = False

    def _setup_systems(self):
        self._activate_world()
        self.input_system = InputSystem(self)
        self.render_system = RenderSystem(self)
        self.hud_system = HudSystem(self)
        esper.add_processor(self.input_system, priority=70)
        esper.add_processor(WeaponSystem(), priority=60)
        esper.add_processor(MovementSystem(self), priority=50)
        esper.add_processor(CollisionSystem(self, self.render_system), priority=40)
        esper.add_processor(SpawnSystem(self), priority=30)
        esper.add_processor(CleanupSystem(self, self.render_system), priority=20)
        esper.add_processor(self.render_system, priority=10)
        esper.add_processor(self.hud_system, priority=0)
        esper.set_handler("player_died", self._on_player_died)

    def _create_player(self):
        self._activate_world()
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
        if self._paused:
            return

        self._activate_world()
        if self.player_entity is None and self.width > 0 and self.height > 0:
            self._create_player()
        esper.process(dt)

    def pause(self):
        if self.game_loop is not None:
            self.game_loop.cancel()
            self.game_loop = None
        self._paused = True

    def resume(self):
        if self._paused and self.game_loop is None:
            self.game_loop = Clock.schedule_interval(self.update, 1 / 60)
            self._paused = False

    def destroy(self):
        self.pause()
        self._activate_world()
        if hasattr(self, "render_system"):
            self.render_system.clear_all()
        self._delete_world(self._world_name)


class GameScreen(Screen):
    """Screen wrapper — creates fresh GameWidget on enter."""

    def __init__(self, **kwargs):
        super().__init__(name="game", **kwargs)
        self.game_widget = None

    def on_enter(self, *args):
        if not self.parent:
            return
        ship_id = self.parent.selected_ship_id

        if self.game_widget:
            self.game_widget.ship_id = ship_id
            self.game_widget._reset()
        else:
            self.game_widget = GameWidget(ship_id)
            self.add_widget(self.game_widget)

    def on_leave(self, *args):
        if self.game_widget:
            self.game_widget.pause()
