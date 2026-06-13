from kivy.app import App
from kivy.core.window import Window

import esper
from game import SpaceHunterGame

# Portrait mode
Window.size = (400, 700)


class SpaceHunterApp(App):
    def build(self):
        self.game = SpaceHunterGame()
        return self.game

    def on_pause(self):
        self.game.pause()
        return True

    def on_resume(self):
        self.game.resume()

    def on_stop(self):
        esper.clear_database()


if __name__ == "__main__":
    SpaceHunterApp().run()
