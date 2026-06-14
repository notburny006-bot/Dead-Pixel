from kivy.app import App
from kivy.core.window import Window

import esper
from ui.screen_manager import AppScreenManager
from ui.main_menu_screen import MainMenuScreen
from ui.ship_select_screen import ShipSelectScreen
from ui.game_over_screen import GameOverScreen
from game import GameScreen


class DeadPixelApp(App):
    def build(self):
        self.sm = AppScreenManager()
        self.sm.add_widget(MainMenuScreen())
        self.sm.add_widget(ShipSelectScreen())
        self.sm.add_widget(GameScreen())
        self.sm.add_widget(GameOverScreen())
        self.sm.current = "main_menu"
        return self.sm

    def on_pause(self):
        game = self._get_game()
        if game:
            game.pause()
        return True

    def on_resume(self):
        game = self._get_game()
        if game:
            game.resume()

    def on_stop(self):
        game = self._get_game()
        if game:
            game.render_system.clear_all()
        esper.clear_database()

    def _get_game(self):
        screen = self.sm.get_screen("game") if self.sm.has_screen("game") else None
        return screen.game_widget if screen else None


if __name__ == "__main__":
    DeadPixelApp().run()
