"""Ship type definitions. Each ship has unique stats and appearance."""

from dataclasses import dataclass


@dataclass
class ShipDef:
    name: str
    display_name: str
    source: str
    hp: int
    speed: float
    weapon_damage: int
    fire_rate: float
    size: int


SHIPS = {
    "phantom_wing": ShipDef(
        name="phantom_wing",
        display_name="PHANTOM WING",
        source="assets/ships_ascii/final/phantom_wing.png",
        hp=100,
        speed=300.0,
        weapon_damage=10,
        fire_rate=0.3,
        size=48,
    ),
    "viper_scout": ShipDef(
        name="viper_scout",
        display_name="VIPER SCOUT",
        source="assets/ships_ascii/final/viper_scout.png",
        hp=60,
        speed=450.0,
        weapon_damage=8,
        fire_rate=0.2,
        size=40,
    ),
    "serpent_class": ShipDef(
        name="serpent_class",
        display_name="SERPENT CLASS",
        source="assets/ships_ascii/final/serpent_class.png",
        hp=200,
        speed=180.0,
        weapon_damage=20,
        fire_rate=0.5,
        size=56,
    ),
}
