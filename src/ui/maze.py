import enum
from typing import Sequence
import pygame as pg

class Dir(enum.IntFlag):
    """Wall directions using bit flags for efficient set operations.

    IntFlag allows bitwise operations (|, &, ~) to combine/remove walls
    in a single cell. Power-of-2 values enable representing any wall
    combination (0-15) as a single integer for compact storage.
    """
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

class Maze(pg.sprite.Group):
    SIZE = 16
    def __init__(self, grid: list[list[Dir]]):
        pg.sprite.Group.__init__(self)

        x, y = self.SIZE, self.SIZE
        for row in grid:
            for col in row:
                self.add(MazeCell(col, self.SIZE, [x,y]))
                x = x + self.SIZE - MazeCell.WIDTH
            x = self.SIZE
            y = y + self.SIZE - MazeCell.WIDTH

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

