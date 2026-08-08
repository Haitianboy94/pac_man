"""Configuration values used by the Pac-Man game."""

from dataclasses import dataclass, field
from typing import Any


DEFAULTS: dict[str, Any] = {
    "highscore_filename": "highscore.json",
    "level": list(range(1, 11)),
    "width": 20,
    "height": 20,
    "lives": 3,
    "pacgum": 10,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
}


@dataclass
class Config:
    """Game configuration with defaults."""

    UI_BORDER_X = 0
    UI_BORDER_Y = 24

    highscore_filename: str = DEFAULTS["highscore_filename"]
    level: list[int] = field(default_factory=lambda: list(DEFAULTS["level"]))
    width: int = DEFAULTS["width"]
    height: int = DEFAULTS["height"]
    lives: int = DEFAULTS["lives"]
    pacgum: int = DEFAULTS["pacgum"]
    points_per_pacgum: int = DEFAULTS["points_per_pacgum"]
    points_per_super_pacgum: int = DEFAULTS["points_per_super_pacgum"]
    points_per_ghost: int = DEFAULTS["points_per_ghost"]
    seed: int = DEFAULTS["seed"]
    level_max_time: int = DEFAULTS["level_max_time"]
