from src.types import Dir
from typing import Sequence
import pygame as pg


class MazeCell(pg.sprite.Sprite):
    """
    Represents a single maze cell in the UI.
    """

    def __init__(
            self,
            walls: Dir,
            size: int,
            wall_size: int,
            position: Sequence[int]
            ):
        pg.sprite.Sprite.__init__(self)
        self.walls: Dir = walls
        self.size: int = size + (wall_size * 2)
        self.wall_size: int = wall_size
        self.position: Sequence[int] = position
        self.image: pg.Surface = pg.Surface([self.size, self.size])
        self.image.set_colorkey("black")
        self.rect: pg.Rect = pg.Rect(position, [self.size, self.size])

        self._place_walls()

    def _place_walls(self) -> None:
        if (self.walls == Dir.ALL):
            self.image.fill("blue")

        length: int = self.size
        horizontal: pg.Surface = pg.Surface([length, self.wall_size])
        horizontal.fill("white")
        vertical: pg.Surface = pg.Surface([self.wall_size, length])
        vertical.fill("white")

        if (self.walls & Dir.NORTH):
            self.image.blit(horizontal, [0, 0])
        if (self.walls & Dir.EAST):
            self.image.blit(vertical, [self.size - self.wall_size, 0])
        if (self.walls & Dir.SOUTH):
            self.image.blit(horizontal, [0, self.size - self.wall_size])
        if (self.walls & Dir.WEST):
            self.image.blit(vertical, [0, 0])
