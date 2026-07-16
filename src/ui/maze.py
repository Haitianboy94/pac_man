from src.ui.pacgum import Pacgum
from src.ui.maze_cell import MazeCell
from src.types import Dir, PacGumType
import pygame as pg


class Maze():
    CELL_SIZE = 36
    def __init__(self, grid: list[list[Dir]], position: tuple[int, int] = (0, 0)):
        self.walls: pg.sprite.Group = pg.sprite.Group()
        self.pacgums: pg.sprite.Group = pg.sprite.Group()

        x, y = position[0], position[1]

        for row in grid:
            for col in row:
                self.walls.add(MazeCell(
                    col,
                    self.CELL_SIZE,
                    [x,y]
                    ))
                self.pacgums.add(Pacgum(
                    PacGumType.PACGUM,
                    [x + int(self.CELL_SIZE / 2), y + int(self.CELL_SIZE / 2)]
                    ))

                x = x + self.CELL_SIZE - MazeCell.WALL_SIZE
            x = position[0]
            y = y + self.CELL_SIZE - MazeCell.WALL_SIZE

    def cell_position(self, x: int, y: int) -> tuple[int, int]:
        return (
            x * self.CELL_SIZE - x * MazeCell.WALL_SIZE,
            y * self.CELL_SIZE - y * MazeCell.WALL_SIZE
        )

