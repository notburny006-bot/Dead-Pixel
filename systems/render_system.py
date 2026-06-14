import esper
from components import Position, Renderable
from kivy.uix.image import Image


class RenderSystem(esper.Processor):
    """Sync Position components to Kivy widgets. Manages widget lifecycle."""

    def __init__(self, game_widget):
        self.game = game_widget
        self._widget_map: dict[int, Image] = {}  # entity_id → widget

    def process(self, dt):
        for ent, (pos, rend) in esper.get_components(Position, Renderable):
            if rend.widget is None:
                rend.widget = Image(
                    source=rend.source,
                    size=rend.size,
                    fit_mode="contain",
                )
                self.game.add_widget(rend.widget)
                self._widget_map[ent] = rend.widget
            rend.widget.pos = (pos.x, pos.y)

    def remove_widget(self, entity: int) -> None:
        """Remove Kivy widget for a deleted entity."""
        widget = self._widget_map.pop(entity, None)
        if widget and widget.parent:
            self.game.remove_widget(widget)

    def clear_all(self) -> None:
        """Remove all widgets. Call before clearing esper database."""
        for entity, widget in list(self._widget_map.items()):
            if widget and widget.parent:
                self.game.remove_widget(widget)
        self._widget_map.clear()
