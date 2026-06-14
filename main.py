import sys
import traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

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


def _show_error_popup(exc_type, exc_value, exc_tb):
    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    # Also log to file for reading after app closes
    with open(Path(__file__).resolve().parent / "crash.log", "w") as f:
        f.write(tb_text)
    sv = ScrollView(size_hint=(1, 1))
    lbl = Label(text=tb_text, size_hint_y=None, font_size="12sp",
                color=(1, 0.3, 0.3, 1), halign="left", valign="top")
    lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
    lbl.bind(texture_size=lambda *a: setattr(lbl, "size", lbl.texture_size))
    sv.add_widget(lbl)
    Popup(title="Dead Pixel - Error", content=sv,
          size_hint=(0.95, 0.8)).open()


if __name__ == "__main__":
    sys.excepthook = lambda t, v, tb: _show_error_popup(t, v, tb)
    DeadPixelApp().run()
