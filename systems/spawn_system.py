import random
import esper
from components import Position, Enemy
from factories.enemy_factory import create_enemy
from data.enemies import ENEMIES


BASE_ENEMIES_PER_WAVE = 5
ENEMIES_PER_WAVE_INCREMENT = 2
SPAWN_INTERVAL = 0.8  # seconds between spawns


class SpawnSystem(esper.Processor):
    """Wave-based enemy spawning using enemy definitions + factory."""

    def __init__(self, game_widget):
        self.game = game_widget
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_per_wave = BASE_ENEMIES_PER_WAVE
        self.spawn_timer = 2.0
        self.wave_active = True

    def process(self, dt):
        if not self.wave_active:
            self._check_wave_clear()
            return

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._spawn_enemy()
            self.spawn_timer = SPAWN_INTERVAL
            self.enemies_spawned += 1

            if self.enemies_spawned >= self.enemies_per_wave:
                self.wave_active = False

    def _check_wave_clear(self):
        """Start next wave when all enemies from current wave are dead."""
        enemy_count = len(list(esper.get_components(Position, Enemy)))
        if enemy_count == 0:
            self.wave += 1
            self.enemies_spawned = 0
            self.enemies_per_wave = BASE_ENEMIES_PER_WAVE + (self.wave - 1) * ENEMIES_PER_WAVE_INCREMENT
            self.spawn_timer = 2.0
            self.wave_active = True

    def _spawn_enemy(self):
        """Spawn a random enemy type at top of screen."""
        enemy_type = random.choice(list(ENEMIES.keys()))
        defn = ENEMIES[enemy_type]
        max_x = max(0, self.game.width - defn.size)
        x = random.uniform(0, max_x)
        y = self.game.height + 10
        create_enemy(enemy_type, x, y, self.wave)
