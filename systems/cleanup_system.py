import esper
from components import Position, Renderable, Bullet, Collider
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BULLET_SIZE


class CleanupSystem(esper.Processor):
    """Remove off-screen entities and their widgets."""

    def __init__(self, game_widget):
        self.game = game_widget

    def process(self, dt):
        to_delete = []

        for ent, (pos, rend) in esper.get_components(Position, Renderable):
            # Off-screen check with margin
            margin = 100
            if (pos.y > SCREEN_HEIGHT + margin or
                pos.y < -margin or
                pos.x < -margin or
                pos.x > SCREEN_WIDTH + margin):
                to_delete.append(ent)

        for ent in to_delete:
            rend = esper.try_component(ent, Renderable)
            if rend and rend.widget and rend.widget.parent:
                self.game.remove_widget(rend.widget)
            esper.delete_entity(ent)
