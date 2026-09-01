from src.resources import resource_path
from functools import cache
import pygame as pg

class Sounds:
    """Represent Sounds state and behavior."""
    gum_sound = 0

    @classmethod
    def start(cls) -> pg.mixer.Sound:
        """Start the object."""
        return cls._load("sounds/start.wav")

    @classmethod
    def eat_gum(cls) -> pg.mixer.Sound:
        """Handle eat gum."""
        if cls.gum_sound == 0:
            cls.gum_sound = 1
            return cls._load("sounds/eat_gum_0.wav")
        cls.gum_sound = 0
        return cls._load("sounds/eat_gum_1.wav")

    @classmethod
    def eat_ghost(cls) -> pg.mixer.Sound:
        """Handle eat ghost."""
        return cls._load("sounds/eat_ghost.wav")

    @classmethod
    def death(cls) -> pg.mixer.Sound:
        # 1.49 seconds duration
        """Handle death."""
        return cls._load("sounds/death.wav")

    @classmethod
    @cache
    def _load(cls, path: str) -> pg.mixer.Sound:
        """Perform the load operation."""
        return pg.mixer.Sound(resource_path(path))


