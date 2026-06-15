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


def _append_crash_log(text):
    for path in _get_crash_log_paths():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a") as f:
                f.write(text + "\n")
        except Exception:
            pass


def _show_crash_screen(text):
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView

    class CrashApp(App):
        def build(self):
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
            close.bind(on_press=lambda *a: self.stop())
            root.add_widget(title)
            root.add_widget(sv)
            root.add_widget(close)
            return root

    CrashApp().run()


def _install_kivy_exception_handler():
    try:
        from kivy.base import ExceptionHandler, ExceptionManager

        class DeadPixelExceptionHandler(ExceptionHandler):
            def handle_exception(self, inst):
                text = "".join(
                    traceback.format_exception(type(inst), inst, inst.__traceback__)
                )
                _write_crash(text)
                return ExceptionManager.PASS

        ExceptionManager.add_handler(DeadPixelExceptionHandler())
    except Exception:
        _append_crash_log("Failed to install Kivy exception handler:")
        _append_crash_log(traceback.format_exc())


def main():
    try:
        _append_crash_log("startup: begin")
        import esper
        _append_crash_log("startup: imported esper")
        from kivy.app import App
        _append_crash_log("startup: imported kivy App")
        from ui.screen_manager import AppScreenManager
        from ui.main_menu_screen import MainMenuScreen
        from ui.ship_select_screen import ShipSelectScreen
        from ui.game_over_screen import GameOverScreen
        from game import GameScreen
        _append_crash_log("startup: imported screens")

        _install_kivy_exception_handler()
        _append_crash_log("startup: installed exception handler")

        class DeadPixelApp(App):
            def build(self):
                _append_crash_log("startup: build begin")
                self.sm = AppScreenManager()
                self.sm.add_widget(MainMenuScreen())
                self.sm.add_widget(ShipSelectScreen())
                self.sm.add_widget(GameScreen())
                self.sm.add_widget(GameOverScreen())
                self.sm.current = "main_menu"
                _append_crash_log("startup: build complete")
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
                    game.destroy()

            def _get_game(self):
                screen = self.sm.get_screen("game") if self.sm.has_screen("game") else None
                return screen.game_widget if screen else None

        _append_crash_log("startup: run app")
        DeadPixelApp().run()
        _append_crash_log("startup: app stopped normally")

    except BaseException:
        text = traceback.format_exc()
        _write_crash(text)
        try:
            _show_crash_screen(text)
        except BaseException:
            pass


if __name__ == "__main__":
    main()
