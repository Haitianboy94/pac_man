from src.graphics.general_sprites import GeneralSprites
from typing import Sequence
from src.types import PacGumType
import pygame as pg


class Pacgum(pg.sprite.Sprite):
    "Entity for the pacgum"
    def __init__(
            self,
            type: PacGumType,
            position: Sequence[int],
            sprites: GeneralSprites
    ):
        pg.sprite.Sprite.__init__(self)
        self.type: PacGumType = type
        self.image: pg.Surface = pg.Surface([0, 0])
        self.position: Sequence[int] = position
        self.sprites: GeneralSprites = sprites

        self._make_gum()

    def _make_gum(self) -> None:
        if self.type == PacGumType.SUPER_PACGUM:
            sprite = self.sprites.super_pacgum()
        else:
            sprite = self.sprites.pacgum()
        rect = sprite.get_rect().move([self.position[0], self.position[1]])
        self.image = sprite
        self.rect = rect
