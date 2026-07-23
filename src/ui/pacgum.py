from typing import Sequence
from src.types import PacGumType
import pygame as pg

class Pacgum(pg.sprite.Sprite):
    def __init__(self, type: PacGumType, position: Sequence[int]):
        pg.sprite.Sprite.__init__(self)
        self.type: PacGumType = type
        self.image: pg.Surface = pg.Surface([0,0])
        self.position: Sequence[int] = position

        if self.type == PacGumType.PACGUM:
            self._make_gum(4)
        elif self.type == PacGumType.SUPER_PACGUM:
            self._make_gum(8)
        
    def _make_gum(self, radius: int):
        surface: pg.Surface = pg.Surface([radius * 2, radius * 2])
        gum: pg.Rect = pg.draw.circle(surface, "white", [radius, radius], radius)
        gum.move_ip([self.position[0] - radius, self.position[1] - radius])
        self.image = surface
        self.rect = gum

