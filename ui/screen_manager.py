"""Screen manager — handles navigation between all game screens."""

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition


class AppScreenManager(ScreenManager):
    """Central navigation. Stores selected ship_id."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.selected_ship_id = "phantom_wing"

    def go_menu(self):
        self.current = "main_menu"

    def go_ship_select(self):
        self.current = "ship_select"

    def go_game(self, ship_id: str):
        self.selected_ship_id = ship_id
        self.current = "game"

    def go_game_over(self):
        self.current = "game_over"
