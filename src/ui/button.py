from typing import Callable

import pygame as pg

from src.graphics.text_sprites import TextSprites


class Button(pg.sprite.Sprite):
    """
    UI button class which handles its own clicking behaviour.
    Calls the `onclick` argument when clicked.
    """

    def __init__(
        self,
        text: str,
        color: str,
        hover_color: str,
        scale: int,
        onclick: Callable,
    ) -> None:
        pg.sprite.Sprite.__init__(self)
        self.onclick: Callable = onclick
        self.text: pg.Surface = TextSprites.render(text, color, scale)
        self.hover_text: pg.Surface = TextSprites.render(
            text, hover_color, scale
        )
        self.image: pg.Surface = self.text
        self.rect: pg.Rect = self.image.get_rect()
        self.selected: bool = False

    def select(self) -> None:
        self.selected = True
        self.image = self.hover_text

    def unselect(self) -> None:
        self.selected = False
        self.image = self.text

    def update(self, events: list[pg.event.Event]) -> None:
        pos: tuple[int, int] = pg.mouse.get_pos()
        hovering: bool = self.rect.collidepoint(pos)
        if hovering:
            if not self.selected:
                self.select()
            if pg.mouse.get_pressed()[0]:
                self.onclick()
        else:
            if self.selected:
                self.unselect()
