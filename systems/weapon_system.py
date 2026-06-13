import esper
from components import Position, Weapon, Player
from factories.bullet_factory import create_bullet


class WeaponSystem(esper.Processor):
    """Auto-fire bullets from player weapon."""

    def process(self, dt):
        for ent, (pos, weapon, _) in esper.get_components(Position, Weapon, Player):
            weapon.fire_cooldown -= dt
            if weapon.fire_cooldown <= 0:
                # Fire bullet from top of player
                bullet_x = pos.x + 20  # center of 48px sprite
                bullet_y = pos.y + 48  # top of player
                create_bullet(bullet_x, bullet_y, weapon.damage, owner="player")
                weapon.fire_cooldown = weapon.fire_rate
