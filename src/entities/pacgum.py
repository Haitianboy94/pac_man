from src.graphics.animation import Animation
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
    ):
        pg.sprite.Sprite.__init__(self)
        self.type: PacGumType = type
        self.position: Sequence[int] = position
        empty_frame = pg.Surface((8, 8))
        empty_frame.fill('black')
        self.animation: Animation = Animation(
            [
                GeneralSprites.super_pacgum(),
                empty_frame,
            ],
            4
        )

        self._make_gum()

    def update(self, dt: int) -> None:
        if self.type == PacGumType.SUPER_PACGUM:
            self.animation.update_frame(dt)
            self.image = self.animation.image

    def _make_gum(self) -> None:
        if self.type == PacGumType.SUPER_PACGUM:
            sprite = GeneralSprites.super_pacgum()
        else:
            sprite = GeneralSprites.pacgum()
        rect = sprite.get_rect().move([self.position[0], self.position[1]])
        self.image = sprite
        self.rect = rect
