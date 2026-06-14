import random
import esper
from components import Position, Enemy
from factories.enemy_factory import create_enemy
from data.enemies import ENEMIES
from data.waves import get_wave_enemies


SPAWN_INTERVAL = 0.8  # seconds between spawns


class SpawnSystem(esper.Processor):
    """Wave-based enemy spawning using wave data + enemy factory."""

    def __init__(self, game_widget):
        self.game = game_widget
        self.wave = 1
        self.spawn_queue = []  # list of enemy types to spawn this wave
        self.spawn_timer = 2.0
        self.wave_active = True
        self._build_wave_queue()
        self.game.hud_system.set_wave(self.wave)

    def process(self, dt):
        if not self.wave_active:
            self._check_wave_clear()
            return

        if not self.spawn_queue:
            self.wave_active = False
            return

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._spawn_next()
            self.spawn_timer = SPAWN_INTERVAL

    def _check_wave_clear(self):
        """Start next wave when all enemies from current wave are dead."""
        enemy_count = len(list(esper.get_components(Position, Enemy)))
        if enemy_count == 0:
            self.wave += 1
            self.spawn_timer = 2.0
            self.wave_active = True
            self._build_wave_queue()
            self.game.hud_system.set_wave(self.wave)

    def _build_wave_queue(self):
        """Build spawn queue from wave data."""
        wave_def = get_wave_enemies(self.wave)
        self.spawn_queue = []
        for enemy_type, count in wave_def.items():
            self.spawn_queue.extend([enemy_type] * count)
        random.shuffle(self.spawn_queue)

    def _spawn_next(self):
        """Spawn next enemy from queue at top of screen."""
        if not self.spawn_queue:
            return
        enemy_type = self.spawn_queue.pop(0)
        defn = ENEMIES[enemy_type]
        max_x = max(0, self.game.width - defn.size)
        x = random.uniform(0, max_x)
        y = self.game.height + 10
        create_enemy(enemy_type, x, y, self.wave)
