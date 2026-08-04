import pygame as pg


class Text(pg.sprite.Sprite):
    "A text node for the UI"
    def __init__(self, font: pg.font.Font, text: str, color: pg.Color):
        pg.sprite.Sprite.__init__(self)

        self.font: pg.font.Font = font
        self.color: pg.Color = color
        self.set_text(text)

    def set_pos(self, pos: tuple[int, int]) -> None:
        x, y = pos
        self.rect = self.image.get_rect(centerx=x, y=y)

    def set_text(self, text: str) -> None:
        self.image: pg.Surface = self.font.render(text, False, self.color)
        self.rect: pg.Rect = self.image.get_rect()
