from src.entities.entity import Entity
from src.entities.pacgum import Pacgum
from src.entities.maze_cell import MazeCell
from src.types import Dir, PacGumType
import pygame as pg


class Maze():
    """
    Represents a maze from the `MazeGenerator` in the UI. Each cell is 
    represented as a single `MazeCell`. The maze also contains the 
    pacgums, and has methods used for positioning within the grid.
    """
    CELL_SIZE = 16
    WALL_SIZE = 4

    def __init__(
            self,
            grid: list[list[Dir]],
            position: tuple[int, int] = (0, 0)
            ):
        self.walls: pg.sprite.Group = pg.sprite.Group()
        self.pacgums: pg.sprite.Group = pg.sprite.Group()

        x, y = position[0], position[1]
        cell_center: int = int(self.cell_size() / 2)

        for row in grid:
            for col in row:
                self.walls.add(MazeCell(
                    col,
                    self.CELL_SIZE,
                    self.WALL_SIZE,
                    [x, y]
                    ))
                
                if col != Dir.ALL:
                    self.pacgums.add(Pacgum(
                        PacGumType.PACGUM,
                        [x + cell_center, y + cell_center]
                        ))

                x = x + self.CELL_SIZE + self.WALL_SIZE
            x = position[0]
            y = y + self.CELL_SIZE + self.WALL_SIZE

    def cell_position(self, x: int, y: int) -> tuple[int, int]:
        "Returns the top-left position for the cell at x, y"
        return (
            x * self.CELL_SIZE - (x - 1) * self.WALL_SIZE,
            y * self.CELL_SIZE - (y - 1) * self.WALL_SIZE
        )

    @staticmethod
    def cell_size() -> int:
        "Returns pixel size for each cell, including walls"
        return Maze.CELL_SIZE + (2 * Maze.WALL_SIZE)
