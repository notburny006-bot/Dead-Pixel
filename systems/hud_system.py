import esper
from components import Health, Player
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from data.zones import get_zone, get_wave_in_zone, WAVES_PER_ZONE


class HudSystem(esper.Processor):
    """Overlay: score, HP bar, zone + wave. Registers for esper events."""

    def __init__(self, game_widget):
        self.game = game_widget
        self.score = 0
        self.wave = 1
        self.zone_name = ""
        self.wave_in_zone = 1

        # Score label (top-left)
        self.score_label = Label(
            text="Score: 0",
            size_hint=(None, None),
            pos=(10, 0),
            font_size="16sp",
            color=(1, 1, 1, 1),
        )
        self.game.add_widget(self.score_label)

        # Wave label (top-center)
        self.wave_label = Label(
            text="Wave 1",
            size_hint=(None, None),
            pos=(0, 0),
            font_size="16sp",
            color=(1, 1, 1, 1),
        )
        self.game.add_widget(self.wave_label)

        # HP bar
        self.hp_bar = ProgressBar(
            max=100,
            value=100,
            size_hint=(0.3, None),
            height=20,
            pos=(10, 0),
        )
        self.game.add_widget(self.hp_bar)

        # Register for score + wave events
        esper.set_handler("enemy_killed", self._on_enemy_killed)

    def _on_enemy_killed(self, points: int):
        self.score += points

    def process(self, dt):
        # Update position relative to game widget size
        top = self.game.height - 30
        self.score_label.pos = (10, top)
        self.wave_label.pos = (self.game.width / 2 - 30, top)
        self.hp_bar.pos = (10, top - 30)

        # Update score text
        self.score_label.text = f"Score: {self.score}"
        self.wave_label.text = f"{self.zone_name} - Wave {self.wave_in_zone}/{WAVES_PER_ZONE}"

        # Update HP bar from player Health
        for ent, (health, _) in esper.get_components(Health, Player):
            self.hp_bar.max = health.max_hp
            self.hp_bar.value = max(0, health.current)

    def set_wave(self, wave: int):
        self.wave = wave
        zone = get_zone(wave)
        self.zone_name = zone.name
        self.wave_in_zone = get_wave_in_zone(wave)
