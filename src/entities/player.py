from src.ui.maze import Maze
from typing import Callable
import pygame as pg

class Player(pg.sprite.Sprite):
    SIZE = 32
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image: pg.Surface = pg.Surface((self.SIZE, self.SIZE))
        self.rect: pg.Rect = pg.draw.circle(
                self.image,
                pg.Color("yellow"),
                (int(self.SIZE / 2), int(self.SIZE / 2)),
                int(self.SIZE / 2)
        )
        offset: int = int((Maze.CELL_SIZE - self.SIZE) / 2)
        self.rect.move_ip(offset, offset)

    def update(self, events: list[pg.event.Event]) -> None:
        pass
