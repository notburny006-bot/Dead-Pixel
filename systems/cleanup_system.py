import esper
from components import Position, Renderable, Player, Enemy, Health


ENEMY_BOTTOM_DAMAGE = 10  # damage to player when enemy reaches bottom


class CleanupSystem(esper.Processor):
    """Remove off-screen entities and their widgets. Never deletes the player.
    Enemies reaching the bottom damage the player before being removed."""

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
            # Enemy reaching bottom = player takes damage
            if esper.has_component(ent, Enemy):
                pos = esper.try_component(ent, Position)
                if pos and pos.y < 0:
                    self._damage_player(ENEMY_BOTTOM_DAMAGE)

            self.render_system.remove_widget(ent)
            esper.delete_entity(ent)

    def _damage_player(self, damage: int):
        """Deal damage to the player entity."""
        player = self.game.player_entity
        if player is None:
            return
        health = esper.try_component(player, Health)
        if health is None:
            return
        health.current -= damage
        if health.current <= 0:
            health.current = 0
            esper.dispatch_event("player_died")
