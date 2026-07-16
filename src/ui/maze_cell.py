from src.types import Dir
from typing import Sequence
import pygame as pg

class MazeCell(pg.sprite.Sprite):
    WALL_SIZE = 1

    def __init__(self, walls: Dir, size: int, position: Sequence[int]):
        pg.sprite.Sprite.__init__(self)
        self.walls: Dir = walls
        self.size: int = size
        self.position: Sequence[int] = position
        self.image: pg.Surface = pg.Surface([self.size, self.size])
        self.rect: pg.Rect = pg.Rect(position, [0,0])

        self._place_walls()

    def _place_walls(self):
        horizontal: pg.Surface = pg.Surface([self.size, self.WALL_SIZE])
        horizontal.fill("white")
        vertical: pg.Surface = pg.Surface([self.WALL_SIZE, self.size])
        vertical.fill("white")

        if (self.walls & Dir.NORTH):
            self.image.blit(horizontal, [0,0])
            self.rect.union(pg.Rect(self.position, [self.WALL_SIZE, self.size]))
        if (self.walls & Dir.EAST):
            self.image.blit(vertical, [0, 0])
            self.rect.union(pg.Rect(self.position, [self.WALL_SIZE, self.size]))
        if (self.walls & Dir.SOUTH):
            self.image.blit(horizontal, [0, self.size - self.WALL_SIZE])
            self.rect.union(pg.Rect(self.position, [self.WALL_SIZE, self.size]))
        if (self.walls & Dir.WEST):
            self.image.blit(vertical, [self.size - self.WALL_SIZE, 0])
            self.rect.union(pg.Rect(self.position, [self.WALL_SIZE, self.size]))

