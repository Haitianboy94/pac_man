import pygame as pg

from src.graphics.text_sprites import TextSprites


class Text(pg.sprite.Sprite):
    "A text node for the UI"

    def __init__(self, text: str, color: str = "white", scale: int = 1):
        pg.sprite.Sprite.__init__(self)

        self.color: str = color
        self.scale: int = scale
        self.position: tuple[int, int] = (0, 0)
        self.set_text(text)

    def set_pos(self, pos: tuple[int, int]) -> None:
        x, y = pos
        self.rect = self.image.get_rect(centerx=x, y=y)

    def set_text(self, text: str) -> None:
        self.image: pg.Surface = TextSprites.render(
            text, self.color, self.scale
        )
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.move_ip(self.position)
