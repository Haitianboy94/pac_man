import pygame as pg

from src.graphics.sprites import Sprites


class HudSprites(Sprites):
    """Represent HudSprites state and behavior."""
    PATH = "sprites/hud_assets.png"

    @classmethod
    def hud_lives(cls) -> pg.Surface:
        """Handle hud lives."""
        return cls._load((928, 176), (16, 16))
