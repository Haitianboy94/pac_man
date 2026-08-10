import pygame as pg


class Panel(pg.sprite.Sprite):
    "A panel element for the UI"

    def __init__(self, rect: pg.Rect, color: pg.Color):
        pg.sprite.Sprite.__init__(self)

        self.image: pg.Surface = pg.Surface(rect.size)
        self.rect: pg.Rect = pg.draw.rect(self.image, color, rect)
