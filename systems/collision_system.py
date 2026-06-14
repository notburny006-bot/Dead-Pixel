import esper
from components import Position, Collider, Bullet, Health, Player, Enemy, Renderable


class CollisionSystem(esper.Processor):
    """AABB collision: player bullets→enemies, enemy bullets→player. Damage + widget cleanup."""

    def __init__(self, game_widget, render_system):
        self.game = game_widget
        self.render_system = render_system

    def process(self, dt):
        to_delete = []  # (entity_id, is_enemy, score_or_None)
        hit_enemies = {}  # enemy_ent → damage taken

        # Player bullets → enemies
        for b_ent, (b_pos, b_col, bullet) in esper.get_components(Position, Collider, Bullet):
            if bullet.owner != "player":
                continue
            for e_ent, (e_pos, e_col, health, _) in esper.get_components(Position, Collider, Health, Enemy):
                if self._aabb_overlap(b_pos, b_col, e_pos, e_col):
                    health.current -= bullet.damage
                    to_delete.append((b_ent, False, None))
                    if health.current <= 0:
                        score_map = {"basic": 10, "miniboss": 50, "boss": 200}
                        enemy = esper.try_component(e_ent, Enemy)
                        score = score_map.get(enemy.kind, 10) if enemy else 10
                        to_delete.append((e_ent, True, score))
                    break

        # Enemy bullets → player
        for b_ent, (b_pos, b_col, bullet) in esper.get_components(Position, Collider, Bullet):
            if bullet.owner != "enemy":
                continue
            for p_ent, (p_pos, p_col, health, _) in esper.get_components(Position, Collider, Health, Player):
                if self._aabb_overlap(b_pos, b_col, p_pos, p_col):
                    health.current -= bullet.damage
                    to_delete.append((b_ent, False, None))
                    if health.current <= 0:
                        esper.dispatch_event("player_died")
                    break

        # Defer all deletions until after iteration
        for ent, is_enemy, score in to_delete:
            self.render_system.remove_widget(ent)
            esper.delete_entity(ent)
            if is_enemy and score:
                esper.dispatch_event("enemy_killed", score)

    @staticmethod
    def _aabb_overlap(pos_a, col_a, pos_b, col_b) -> bool:
        return (pos_a.x < pos_b.x + col_b.width and
                pos_a.x + col_a.width > pos_b.x and
                pos_a.y < pos_b.y + col_b.height and
                pos_a.y + col_a.height > pos_b.y)
