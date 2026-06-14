import esper
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class GameOverScreen(BoxLayout):
    """Overlay shown on player death. Score, wave reached, restart button."""

    def __init__(self, game_widget, hud_system, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.game = game_widget
        self.hud = hud_system

        # Styling
        self.spacing = 20
        self.padding = [50, 80]

        # Title
        self.add_widget(Label(
            text="GAME OVER",
            font_size="32sp",
            color=(1, 0.3, 0.3, 1),
            size_hint_y=0.3,
        ))

        # Stats
        self.stats_label = Label(
            text="",
            font_size="18sp",
            color=(1, 1, 1, 1),
            size_hint_y=0.3,
        )
        self.add_widget(self.stats_label)

        # Restart button
        restart_btn = Button(
            text="RESTART",
            font_size="20sp",
            size_hint=(0.6, None),
            height=60,
            size_hint_x=0.6,
            pos_hint={"center_x": 0.5},
        )
        restart_btn.bind(on_press=self._on_restart)
        self.add_widget(restart_btn)

        # Register for death event
        esper.set_handler("player_died", self._on_player_died)

        # Hide by default
        self.opacity = 0
        self.disabled = True

    def _on_player_died(self):
        """Called when player HP reaches 0."""
        self.stats_label.text = f"Score: {self.hud.score}\nWave: {self.hud.wave}"
        self.opacity = 1
        self.disabled = False
        self.game.pause()

    def _on_restart(self, instance):
        """Reset game state and start fresh."""
        self.opacity = 0
        self.disabled = True
        self.game.restart()
