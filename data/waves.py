"""Wave composition definitions. Zone-aware: miniboss wave 3, boss wave 6."""

from typing import Dict

from data.zones import get_zone, get_wave_in_zone, is_miniboss_wave, is_boss_wave


def get_wave_enemies(global_wave: int) -> Dict[str, int]:
    """Return enemy composition for a given global wave number."""
    zone = get_zone(global_wave)
    wiz = get_wave_in_zone(global_wave)
    sm = zone.spawn_mult

    if is_boss_wave(global_wave):
        return {"boss": 1, "basic": int(4 * sm)}
    elif is_miniboss_wave(global_wave):
        return {"miniboss": 1, "basic": int(3 * sm)}
    else:
        return {"basic": int((2 + wiz) * sm)}
