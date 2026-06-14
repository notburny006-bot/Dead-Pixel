import esper
from components import Position, Weapon, Player, Collider, Enemy
from factories.bullet_factory import create_bullet


class WeaponSystem(esper.Processor):
    """Auto-fire bullets from player weapon. Boss/miniboss shoot downward."""

    def process(self, dt):
        # Player auto-fire
        for ent, (pos, weapon, _) in esper.get_components(Position, Weapon, Player):
            weapon.fire_cooldown -= dt
            if weapon.fire_cooldown <= 0:
                collider = esper.try_component(ent, Collider)
                size = collider.width if collider else 48
                bullet_x = pos.x + size / 2
                bullet_y = pos.y + size
                create_bullet(bullet_x, bullet_y, weapon.damage, owner="player")
                weapon.fire_cooldown = weapon.fire_rate

        # Enemy shooting (boss + miniboss)
        for ent, (pos, enemy, collider) in esper.get_components(Position, Enemy, Collider):
            if enemy.kind not in ("boss", "miniboss"):
                continue

            weapon = esper.try_component(ent, Weapon)
            if not weapon:
                continue

            weapon.fire_cooldown -= dt
            if weapon.fire_cooldown <= 0:
                weapon.fire_cooldown = weapon.fire_rate
                bx = pos.x + collider.width / 2
                by = pos.y
                create_bullet(bx, by, weapon.damage, owner="enemy")
