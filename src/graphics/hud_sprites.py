import pygame as pg

from src.graphics.sprites import Sprites


class HudSprites(Sprites):
    PATH = "sprites/hud_assets.png"

    @classmethod
    def hud_lives(cls) -> pg.Surface:
        return cls._load((928, 176), (16, 16))
