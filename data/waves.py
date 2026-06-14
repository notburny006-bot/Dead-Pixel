"""Wave composition definitions. Each wave defines enemy types + counts."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class WaveDef:
    wave: int
    enemies: Dict[str, int]  # enemy_type → count


def get_wave_enemies(wave: int) -> Dict[str, int]:
    """Return enemy composition for a given wave. Scales with wave number."""
    base = 3 + wave
    return {"basic": base}
