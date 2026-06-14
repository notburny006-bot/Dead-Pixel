import sys
import traceback
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, BASE_DIR)


def _get_crash_log_paths():
    paths = []
    try:
        from android.storage import app_storage_path
        paths.append(Path(app_storage_path()) / "crash.log")
    except Exception:
        pass
    for raw in (
        "/sdcard/deadpixel_crash.log",
        "/storage/emulated/0/deadpixel_crash.log",
        str(Path(BASE_DIR) / "crash.log"),
    ):
        paths.append(Path(raw))
    return paths


def _write_crash(text):
    print(text, file=sys.stderr)
    for path in _get_crash_log_paths():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                f.write(text)
        except Exception:
            pass


def _patch_kivy_clock():
    from kivy.clock import Clock
    orig_tick = Clock._tick

    def safe_tick(*args, **kwargs):
        try:
            return orig_tick(*args, **kwargs)
        except BaseException:
            text = traceback.format_exc()
            _write_crash(text)
            try:
                _show_crash_screen(text)
            except Exception:
                pass
            return False

    Clock._tick = safe_tick


def _show_crash_screen(text):
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView

    app = App.get_running_app()
    if not app or not app.root:
        return

    root = BoxLayout(orientation="vertical", padding=10, spacing=10)
    title = Label(text="DEAD PIXEL CRASH", size_hint_y=None, height=40,
                  color=(1, 0.2, 0.2, 1), font_size="20sp")
    sv = ScrollView(size_hint=(1, 1))
    lbl = Label(text=text, size_hint_y=None, font_size="12sp",
                color=(1, 0.3, 0.3, 1), halign="left", valign="top")
    lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
    lbl.bind(texture_size=lambda *a: setattr(lbl, "size", lbl.texture_size))
    sv.add_widget(lbl)
    close = Button(text="Close App", size_hint_y=None, height=50)
    close.bind(on_press=lambda *a: app.stop())
    root.add_widget(title)
    root.add_widget(sv)
    root.add_widget(close)
    app.root.clear_widgets()
    app.root.add_widget(root)


def _clear_old_crash_logs():
    for path in _get_crash_log_paths():
        try:
            if path.exists():
                path.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    _clear_old_crash_logs()
    try:
        from kivy.app import App
        import esper
        from ui.screen_manager import AppScreenManager
        from ui.main_menu_screen import MainMenuScreen
        from ui.ship_select_screen import ShipSelectScreen
        from ui.game_over_screen import GameOverScreen
        from game import GameScreen

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
                if game and hasattr(game, "render_system"):
                    game.render_system.clear_all()
                esper.clear_database()

            def _get_game(self):
                screen = self.sm.get_screen("game") if self.sm.has_screen("game") else None
                return screen.game_widget if screen else None

        DeadPixelApp().run()

    except BaseException:
        _write_crash(traceback.format_exc())
