import sys
import traceback
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, BASE_DIR)

CRASH_LOG = Path(BASE_DIR) / "crash.log"


def _write_crash(text):
    """Always write crash to file — this never fails."""
    try:
        with open(CRASH_LOG, "w") as f:
            f.write(text)
    except Exception:
        pass
    print(text, file=sys.stderr)


def _patch_kivy_clock():
    """Wrap Clock._tick to catch exceptions from scheduled callbacks.

    Kivy silently swallows exceptions in Clock.schedule_interval callbacks.
    This patch catches them, writes to crash.log, and shows a popup.
    """
    from kivy.clock import Clock
    _orig_tick = Clock._tick

    def _safe_tick(self, *args, **kwargs):
        try:
            return _orig_tick(self, *args, **kwargs)
        except Exception:
            text = traceback.format_exc()
            _write_crash(text)
            try:
                _show_crash_popup(text)
            except Exception:
                pass
            return False

    Clock._tick = _safe_tick


def _show_crash_popup(text):
    """Show scrollable traceback in a Kivy popup."""
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView
    sv = ScrollView(size_hint=(1, 1))
    lbl = Label(text=text, size_hint_y=None, font_size="12sp",
                color=(1, 0.3, 0.3, 1), halign="left", valign="top")
    lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
    lbl.bind(texture_size=lambda *a: setattr(lbl, "size", lbl.texture_size))
    sv.add_widget(lbl)
    Popup(title="DEAD PIXEL - CRASH", content=sv,
          size_hint=(0.95, 0.8)).open()


if __name__ == "__main__":
    # Delete old crash log on fresh start
    if CRASH_LOG.exists():
        CRASH_LOG.unlink()

    try:
        from kivy.app import App
        from kivy.clock import Clock
        import esper
        from ui.screen_manager import AppScreenManager
        from ui.main_menu_screen import MainMenuScreen
        from ui.ship_select_screen import ShipSelectScreen
        from ui.game_over_screen import GameOverScreen
        from game import GameScreen

        # Patch Clock BEFORE app starts so all callbacks are covered
        _patch_kivy_clock()

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
                if game and hasattr(game, 'render_system'):
                    game.render_system.clear_all()
                esper.clear_database()

            def _get_game(self):
                screen = self.sm.get_screen("game") if self.sm.has_screen("game") else None
                return screen.game_widget if screen else None

        DeadPixelApp().run()

    except Exception:
        # Catches import errors and build() failures
        text = traceback.format_exc()
        _write_crash(text)
