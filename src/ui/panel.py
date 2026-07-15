from typing import Sequence
import pygame as pg

class Panel(pg.sprite.Sprite):
    def __init__(self, rect: pg.Rect, color: pg.Color):
        pg.sprite.Sprite.__init__(self)
        
        self.image: pg.Surface = pg.Surface(rect.size)
        self.rect: pg.Rect = pg.draw.rect(
                self.image,
                color,
                rect
                )

    def set_pos(self, pos: tuple[int, int]):
        x, y = pos
        self.rect = self.image.get_rect(centerx=x, y=y)



