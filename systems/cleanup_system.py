import esper
from components import Position, Renderable, Player


class CleanupSystem(esper.Processor):
    """Remove off-screen entities and their widgets. Never deletes the player."""

    def __init__(self, game_widget, render_system):
        self.game = game_widget
        self.render_system = render_system

    def process(self, dt):
        to_delete = []

        for ent, (pos, rend) in esper.get_components(Position, Renderable):
            # Never delete the player
            if esper.has_component(ent, Player):
                continue

            # Off-screen check with margin (use actual widget size)
            margin = 100
            w = self.game.width
            h = self.game.height
            if (pos.y > h + margin or
                pos.y < -margin or
                pos.x < -margin or
                pos.x > w + margin):
                to_delete.append(ent)

        for ent in to_delete:
            self.render_system.remove_widget(ent)
            esper.delete_entity(ent)
