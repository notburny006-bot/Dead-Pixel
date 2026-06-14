from kivy.app import App

import esper
from game import DeadPixelGame


class DeadPixelApp(App):
    def build(self):
        self.game = DeadPixelGame()
        return self.game

    def on_pause(self):
        self.game.pause()
        return True

    def on_resume(self):
        self.game.resume()

    def on_stop(self):
        self.game.render_system.clear_all()
        esper.clear_database()


if __name__ == "__main__":
    DeadPixelApp().run()
