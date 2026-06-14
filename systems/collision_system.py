import esper
from components import Position, Collider, Bullet, Health, Player, Enemy, Renderable


class CollisionSystem(esper.Processor):
    """AABB collision: player bullets→enemies, enemy bullets→player. Damage + widget cleanup."""

    def __init__(self, game_widget, render_system):
        self.game = game_widget
        self.render_system = render_system

    def process(self, dt):
        # Player bullets → enemies
        for b_ent, (b_pos, b_col, bullet) in esper.get_components(Position, Collider, Bullet):
            if bullet.owner != "player":
                continue
            for e_ent, (e_pos, e_col, health, _) in esper.get_components(Position, Collider, Health, Enemy):
                if self._aabb_overlap(b_pos, b_col, e_pos, e_col):
                    health.current -= bullet.damage
                    # Remove bullet
                    self.render_system.remove_widget(b_ent)
                    esper.delete_entity(b_ent)
                    # Remove enemy if dead
                    if health.current <= 0:
                        self.render_system.remove_widget(e_ent)
                        esper.delete_entity(e_ent)
                        esper.dispatch_event("enemy_killed", 10)
                    break  # Bullet already consumed

        # Enemy bullets → player (future: when enemies shoot)
        for b_ent, (b_pos, b_col, bullet) in esper.get_components(Position, Collider, Bullet):
            if bullet.owner != "enemy":
                continue
            for p_ent, (p_pos, p_col, health, _) in esper.get_components(Position, Collider, Health, Player):
                if self._aabb_overlap(b_pos, b_col, p_pos, p_col):
                    health.current -= bullet.damage
                    self.render_system.remove_widget(b_ent)
                    esper.delete_entity(b_ent)
                    if health.current <= 0:
                        esper.dispatch_event("player_died")
                    break

    @staticmethod
    def _aabb_overlap(pos_a, col_a, pos_b, col_b) -> bool:
        return (pos_a.x < pos_b.x + col_b.width and
                pos_a.x + col_a.width > pos_b.x and
                pos_a.y < pos_b.y + col_b.height and
                pos_a.y + col_a.height > pos_b.y)
