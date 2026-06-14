import esper
from components import Position, Weapon, Player, Collider
from constants import PLAYER_SIZE
from factories.bullet_factory import create_bullet


class WeaponSystem(esper.Processor):
    """Auto-fire bullets from player weapon."""

    def process(self, dt):
        for ent, (pos, weapon, _) in esper.get_components(Position, Weapon, Player):
            weapon.fire_cooldown -= dt
            if weapon.fire_cooldown <= 0:
                # Fire bullet from top-center of player
                bullet_x = pos.x + PLAYER_SIZE / 2
                bullet_y = pos.y + PLAYER_SIZE
                create_bullet(bullet_x, bullet_y, weapon.damage, owner="player")
                weapon.fire_cooldown = weapon.fire_rate
