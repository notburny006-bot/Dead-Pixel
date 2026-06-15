from pathlib import Path

import esper
from components import Position, Renderable
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.image import Image
from kivy.uix.widget import Widget


BASE_DIR = Path(__file__).resolve().parents[1]


class FallbackSprite(Widget):
    """Simple built-in sprite used until real enemy/bullet art is added."""

    COLORS = {
        "enemy": (1.0, 0.15, 0.15, 1),
        "bullet": (1.0, 0.9, 0.15, 1),
        "player": (0.0, 0.8, 1.0, 1),
    }

    def __init__(self, fallback_key: str, **kwargs):
        super().__init__(**kwargs)
        self.fallback_key = fallback_key
        with self.canvas:
            Color(*self.COLORS.get(fallback_key, self.COLORS["player"]))
            if fallback_key == "bullet":
                self.shape = Ellipse(pos=self.pos, size=self.size)
            else:
                self.shape = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_shape, size=self._update_shape)

    def _update_shape(self, *args):
        self.shape.pos = self.pos
        self.shape.size = self.size


class RenderSystem(esper.Processor):
    """Sync Position components to Kivy widgets. Manages widget lifecycle."""

    def __init__(self, game_widget):
        self.game = game_widget
        self._widget_map: dict[int, Widget] = {}  # entity_id → widget

    def _create_widget(self, rend: Renderable) -> Widget:
        if rend.source and (BASE_DIR / rend.source).exists():
            image = Image(
                source=rend.source,
                size=rend.size,
                fit_mode="contain",
            )
            image.bind(texture=self._sharpen_texture)
            if image.texture:
                self._sharpen_texture(image, image.texture)
            return image
        return FallbackSprite(rend.fallback_key, size=rend.size)

    @staticmethod
    def _sharpen_texture(instance, texture):
        texture.mag_filter = "nearest"
        texture.min_filter = "nearest"

    def process(self, dt):
        for ent, (pos, rend) in esper.get_components(Position, Renderable):
            if rend.widget is None:
                rend.widget = self._create_widget(rend)
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
