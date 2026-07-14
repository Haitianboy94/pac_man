from typing import Callable
import pygame as pg

class Text(pg.sprite.Sprite):
    def __init__(self, font: pg.font.Font, text: str, color: pg.Color):
        pg.sprite.Sprite.__init__(self)
        
        self.text: pg.Surface = font.render(text, False, color)
        self.image: pg.Surface = self.text
        self.rect: pg.Rect = self.image.get_rect()

    def set_pos(self, pos: tuple[int, int]):
        x, y = pos
        self.rect = self.image.get_rect(centerx=x, y=y)



