from dataclasses import dataclass

WAVES_PER_ZONE = 6
MINIBOSS_WAVE = 3
BOSS_WAVE = 6


@dataclass
class ZoneDef:
    name: str
    subtitle: str
    bg_color: tuple
    hp_mult: float
    speed_mult: float
    spawn_mult: float


ZONES = [
    ZoneDef(
        "Neon Ruins",
        "Abandoned satellite graveyard",
        (0.02, 0.02, 0.08, 1.0),
        hp_mult=1.0,
        speed_mult=1.0,
        spawn_mult=1.0,
    ),
]

# Fallback: after last zone, reuse last zone stats with progressive scaling.
# Add more ZoneDefs to ZONES list for more biomes.


def get_zone_index(global_wave: int) -> int:
    return (global_wave - 1) // WAVES_PER_ZONE


def get_zone(global_wave: int) -> ZoneDef:
    idx = get_zone_index(global_wave)
    if idx < len(ZONES):
        return ZONES[idx]
    # Fallback: last zone with escalating multipliers
    last = ZONES[-1]
    extra = idx - len(ZONES) + 1
    return ZoneDef(
        name=last.name,
        subtitle=last.subtitle,
        bg_color=last.bg_color,
        hp_mult=last.hp_mult + extra * 0.3,
        speed_mult=last.speed_mult + extra * 0.15,
        spawn_mult=last.spawn_mult + extra * 0.2,
    )


def get_wave_in_zone(global_wave: int) -> int:
    return ((global_wave - 1) % WAVES_PER_ZONE) + 1


def is_miniboss_wave(global_wave: int) -> bool:
    return get_wave_in_zone(global_wave) == MINIBOSS_WAVE


def is_boss_wave(global_wave: int) -> bool:
    return get_wave_in_zone(global_wave) == BOSS_WAVE
