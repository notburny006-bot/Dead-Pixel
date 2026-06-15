"""Ship selection screen — carousel with ship preview, name, stats."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from data.ships import SHIPS, ShipDef

SHIP_ORDER = ["phantom_wing", "viper_scout", "serpent_class"]


class ShipSelectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="ship_select", **kwargs)
        self._ship_index = 0
        with self.canvas.before:
            Color(0.02, 0.02, 0.08, 1)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self._build_ui()
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _build_ui(self):
        root = BoxLayout(
            orientation="vertical",
            padding=[30, 40],
            spacing=20,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )

        # Header
        header = Label(
            text="SELECT YOUR SHIP",
            font_size="28sp",
            color=(0.0, 0.8, 1.0, 1),
            size_hint_y=0.1,
        )
        root.add_widget(header)

        # Ship preview area — image center, arrows sides
        preview_row = BoxLayout(orientation="horizontal", size_hint_y=0.45)

        left_btn = Button(
            text="<",
            font_size="32sp",
            size_hint_x=0.15,
            background_color=(0.2, 0.2, 0.4, 1),
        )
        left_btn.bind(on_press=self._prev_ship)

        self.ship_image = Image(
            source=SHIPS[SHIP_ORDER[0]].source,
            fit_mode="contain",
            size_hint_x=0.7,
        )

        right_btn = Button(
            text=">",
            font_size="32sp",
            size_hint_x=0.15,
            background_color=(0.2, 0.2, 0.4, 1),
        )
        right_btn.bind(on_press=self._next_ship)

        preview_row.add_widget(left_btn)
        preview_row.add_widget(self.ship_image)
        preview_row.add_widget(right_btn)
        root.add_widget(preview_row)

        # Ship name
        self.ship_name = Label(
            text=SHIPS[SHIP_ORDER[0]].display_name,
            font_size="32sp",
            color=(1, 1, 1, 1),
            size_hint_y=0.1,
            bold=True,
        )
        root.add_widget(self.ship_name)

        # Stats
        self.stats_layout = GridLayout(cols=3, size_hint_y=0.2, spacing=10)
        self._build_stats()
        root.add_widget(self.stats_layout)

        # Buttons row
        btn_row = BoxLayout(orientation="horizontal", size_hint_y=0.15, spacing=20)

        back_btn = Button(
            text="BACK",
            font_size="20sp",
            background_color=(0.4, 0.1, 0.1, 1),
        )
        back_btn.bind(on_press=self._go_back)

        select_btn = Button(
            text="SELECT",
            font_size="22sp",
            background_color=(0.0, 0.6, 0.2, 1),
        )
        select_btn.bind(on_press=self._on_select)

        btn_row.add_widget(back_btn)
        btn_row.add_widget(select_btn)
        root.add_widget(btn_row)

        self.add_widget(root)

    def _build_stats(self):
        self.stats_layout.clear_widgets()
        ship = self._current_ship()
        stats = [
            ("HP", str(ship.hp), self._bar_color(ship.hp, 60, 200)),
            ("SPEED", str(int(ship.speed)), self._bar_color(ship.speed, 180, 450)),
            ("DAMAGE", str(ship.weapon_damage), self._bar_color(ship.weapon_damage, 8, 20)),
        ]
        for label, value, color in stats:
            col = BoxLayout(orientation="vertical")
            col.add_widget(Label(text=label, font_size="14sp", color=(0.7, 0.7, 0.7, 1)))
            col.add_widget(Label(text=value, font_size="20sp", color=color, bold=True))
            self.stats_layout.add_widget(col)

    def _bar_color(self, value, low, high):
        ratio = (value - low) / (high - low) if high != low else 0.5
        ratio = max(0, min(1, ratio))
        return (1 - ratio, ratio * 0.8, 0.2, 1)

    def _current_ship(self) -> ShipDef:
        return SHIPS[SHIP_ORDER[self._ship_index]]

    def _update_display(self):
        ship = self._current_ship()
        self.ship_image.source = ship.source
        self.ship_name.text = ship.display_name
        self._build_stats()

    def _prev_ship(self, instance):
        self._ship_index = (self._ship_index - 1) % len(SHIP_ORDER)
        self._update_display()

    def _next_ship(self, instance):
        self._ship_index = (self._ship_index + 1) % len(SHIP_ORDER)
        self._update_display()

    def _on_select(self, instance):
        ship = self._current_ship()
        self.parent.go_game(ship.name)

    def _go_back(self, instance):
        self.parent.go_menu()

    def on_enter(self, *args):
        self._ship_index = SHIP_ORDER.index(self.parent.selected_ship_id)
        self._update_display()

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
