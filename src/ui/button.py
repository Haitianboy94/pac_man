from typing import Callable
import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, font: pg.font.Font, text: str, color: pg.Color, hover_color: pg.Color,
                 onclick: Callable) -> None:
        pg.sprite.Sprite.__init__(self)
        self.onclick: Callable = onclick
        
        self.text: pg.Surface = font.render(text, False, color)
        self.hover_text: pg.Surface = font.render(text, False, hover_color)
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



