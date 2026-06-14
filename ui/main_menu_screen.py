"""Main menu screen — title + PLAY button."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="main_menu", **kwargs)
        self._build_ui()
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _build_ui(self):
        layout = BoxLayout(orientation="vertical", spacing=30, padding=[50, 100])

        # Title
        title = Label(
            text="DEAD PIXEL",
            font_size="48sp",
            color=(0.0, 0.8, 1.0, 1),
            size_hint_y=0.5,
        )
        layout.add_widget(title)

        # Subtitle
        subtitle = Label(
            text="SPACE SHOOTER",
            font_size="18sp",
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.15,
        )
        layout.add_widget(subtitle)

        # Spacer
        layout.add_widget(Label(size_hint_y=0.15))

        # Play button
        play_btn = Button(
            text="PLAY",
            font_size="24sp",
            size_hint=(0.5, None),
            height=70,
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            background_color=(0.0, 0.5, 0.8, 1),
        )
        play_btn.bind(on_press=self._on_play)
        layout.add_widget(play_btn)

        self.add_widget(layout)

    def _on_play(self, instance):
        self.parent.go_ship_select()

    def _update_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.02, 0.02, 0.08, 1)
            Rectangle(pos=self.pos, size=self.size)
