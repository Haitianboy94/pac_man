from src.ui.pacgum import Pacgum
from src.ui.maze_cell import MazeCell
from src.types import Dir, PacGumType
import pygame as pg


class Maze():
    SIZE = 32
    def __init__(self, grid: list[list[Dir]]):
        self.walls: pg.sprite.Group = pg.sprite.Group()
        self.pacgums: pg.sprite.Group = pg.sprite.Group()

        x, y = self.SIZE, self.SIZE
        for row in grid:
            for col in row:
                self.walls.add(MazeCell(
                    col,
                    self.SIZE,
                    [x,y]
                    ))
                self.pacgums.add(Pacgum(
                    PacGumType.PACGUM,
                    [x + int(self.SIZE / 2), y + int(self.SIZE / 2)]
                    ))

                x = x + self.SIZE - MazeCell.WIDTH
            x = self.SIZE
            y = y + self.SIZE - MazeCell.WIDTH

