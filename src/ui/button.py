from src.graphics.text_sprites import TextSprites
from typing import Callable
import pygame as pg


class Button(pg.sprite.Sprite):
    """
    UI button class which handles its own clicking behaviour.
    Calls the `onclick` argument when clicked.
    """

    def __init__(
            self,
            text_sprites: TextSprites,
            text: str,
            color: str,
            hover_color: str,
            scale: int,
            onclick: Callable
            ) -> None:
        pg.sprite.Sprite.__init__(self)
        self.onclick: Callable = onclick
        self.text: pg.Surface = text_sprites.render(text, color, scale)
        self.hover_text: pg.Surface = text_sprites.render(text, hover_color, scale)
        self.image: pg.Surface = self.text
        self.rect: pg.Rect = self.image.get_rect()

    def update(self, events: list[pg.event.Event]) -> None:
        pos: tuple[int, int] = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.hover_text
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.onclick()
        else:
            self.image = self.text

    def set_pos(self, pos: tuple[int, int]) -> None:
        x, y = pos
        self.rect = self.image.get_rect(centerx=x, y=y)
