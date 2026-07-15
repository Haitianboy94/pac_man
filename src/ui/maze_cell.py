from src.types import Dir
from typing import Sequence
import pygame as pg

class MazeCell(pg.sprite.Sprite):
    WIDTH = 1

    def __init__(self, walls: Dir, size: int, position: Sequence[int]):
        pg.sprite.Sprite.__init__(self)
        self.walls: Dir = walls
        self.size: int = size
        self.position: Sequence[int] = position
        self.image: pg.Surface = pg.Surface([self.size, self.size])
        self.rect: pg.Rect = pg.Rect(position, [0,0])

        self._place_walls()

    def _place_walls(self):
        horizontal: pg.Surface = pg.Surface([self.size, self.WIDTH])
        horizontal.fill("white")
        vertical: pg.Surface = pg.Surface([self.WIDTH, self.size])
        vertical.fill("white")

        if (self.walls & Dir.NORTH):
            self.image.blit(horizontal, [0,0])
            self.rect.union(pg.Rect(self.position, [self.WIDTH, self.size]))
        if (self.walls & Dir.EAST):
            self.image.blit(vertical, [0, 0])
            self.rect.union(pg.Rect(self.position, [self.WIDTH, self.size]))
        if (self.walls & Dir.SOUTH):
            self.image.blit(horizontal, [0, self.size - self.WIDTH])
            self.rect.union(pg.Rect(self.position, [self.WIDTH, self.size]))
        if (self.walls & Dir.WEST):
            self.image.blit(vertical, [self.size - self.WIDTH, 0])
            self.rect.union(pg.Rect(self.position, [self.WIDTH, self.size]))

