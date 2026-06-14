from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class GameOverScreen(Screen):
    """Game over screen — score, wave, restart/menu buttons."""

    def __init__(self, **kwargs):
        super().__init__(name="game_over", **kwargs)
        self._score = 0
        self._wave = 0
        self._build_ui()
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _build_ui(self):
        layout = BoxLayout(orientation="vertical", spacing=20, padding=[50, 80])

        # Title
        layout.add_widget(Label(
            text="GAME OVER",
            font_size="36sp",
            color=(1, 0.3, 0.3, 1),
            size_hint_y=0.3,
        ))

        # Stats
        self.stats_label = Label(
            text="Score: 0\nWave: 0",
            font_size="20sp",
            color=(1, 1, 1, 1),
            size_hint_y=0.25,
        )
        layout.add_widget(self.stats_label)

        # Buttons
        btn_row = BoxLayout(orientation="horizontal", spacing=20, size_hint_y=0.2)
        size_hint_x_val = 0.5

        menu_btn = Button(
            text="MENU",
            font_size="20sp",
            background_color=(0.4, 0.1, 0.1, 1),
        )
        menu_btn.bind(on_press=self._go_menu)
        btn_row.add_widget(menu_btn)

        restart_btn = Button(
            text="RESTART",
            font_size="20sp",
            background_color=(0.0, 0.5, 0.2, 1),
        )
        restart_btn.bind(on_press=self._on_restart)
        btn_row.add_widget(restart_btn)

        layout.add_widget(btn_row)
        self.add_widget(layout)

    def show(self, score: int, wave: int):
        """Called when player dies — set stats and navigate here."""
        self._score = score
        self._wave = wave
        self.stats_label.text = f"Score: {score}\nWave: {wave}"
        self.parent.go_game_over()

    def _on_restart(self, instance):
        ship_id = self.parent.selected_ship_id
        self.parent.go_game(ship_id)

    def _go_menu(self, instance):
        self.parent.go_menu()

    def _update_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.02, 0.02, 0.08, 1)
            Rectangle(pos=self.pos, size=self.size)
