import esper
from components import Position, Weapon, Player, Collider
from factories.bullet_factory import create_bullet


class WeaponSystem(esper.Processor):
    """Auto-fire bullets from player weapon."""

    def process(self, dt):
        for ent, (pos, weapon, _) in esper.get_components(Position, Weapon, Player):
            weapon.fire_cooldown -= dt
            if weapon.fire_cooldown <= 0:
                collider = esper.try_component(ent, Collider)
                size = collider.width if collider else 48
                bullet_x = pos.x + size / 2
                bullet_y = pos.y + size
                create_bullet(bullet_x, bullet_y, weapon.damage, owner="player")
                weapon.fire_cooldown = weapon.fire_rate
