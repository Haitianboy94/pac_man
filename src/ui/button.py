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
        """Initialize the object."""
        pg.sprite.Sprite.__init__(self)
        self.onclick: Callable = onclick
        self.text: pg.Surface = TextSprites.render(text, color, scale)
        self.hover_text: pg.Surface = TextSprites.render(
            text, hover_color, scale
        )
        self.image: pg.Surface = self.text
        self.rect: pg.Rect = self.image.get_rect()
        self.hovering: bool = False

    def hover(self) -> None:
        """Hover the object."""
        self.hovering = True
        self.image = self.hover_text

    def unhover(self) -> None:
        """Unhover the object."""
        self.hovering = False
        self.image = self.text

    def handle_event(self, event: pg.event.Event) -> None:
        """Handle handle event."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovering:
                self.onclick()

    def update(self, events: list[pg.event.Event]) -> None:
        """Update the object."""
        pos: tuple[int, int] = pg.mouse.get_pos()
        hovering: bool = self.rect.collidepoint(pos)
        clicked = False
        if hovering:
            if not self.hovering:
                self.hover()
        else:
            if self.hovering:
                self.unhover()
