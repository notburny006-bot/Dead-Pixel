import esper
from components import Position, Renderable
from kivy.uix.image import Image


class RenderSystem(esper.Processor):
    """Sync Position components to Kivy widgets."""

    def __init__(self, game_widget):
        self.game = game_widget

    def process(self, dt):
        for ent, (pos, rend) in esper.get_components(Position, Renderable):
            if rend.widget is None:
                rend.widget = Image(
                    source=rend.source,
                    size=(48, 48),
                    allow_stretch=True,
                )
                self.game.add_widget(rend.widget)
            rend.widget.pos = (pos.x, pos.y)
