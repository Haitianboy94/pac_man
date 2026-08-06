from src.ui.pacgum import Pacgum
from src.ui.maze_cell import MazeCell
from src.types import Dir, PacGumType
import pygame as pg


class Maze():
    """
    Represents a maze from the `MazeGenerator` in the UI. Each cell is 
    represented as a single `MazeCell`. The maze also contains the 
    pacgums, and has methods used for positioning within the grid.
    """
    CELL_SIZE = 36

    def __init__(
            self,
            grid: list[list[Dir]],
            position: tuple[int, int] = (0, 0)
            ):
        self.grid: list[list[Dir]] = grid
        self.walls: pg.sprite.Group = pg.sprite.Group()
        self.pacgums: pg.sprite.Group = pg.sprite.Group()

        x, y = position[0], position[1]

        for row in grid:
            for col in row:
                self.walls.add(MazeCell(
                    col,
                    self.CELL_SIZE,
                    [x, y]
                    ))
                self.pacgums.add(Pacgum(
                    PacGumType.PACGUM,
                    [x + int(self.CELL_SIZE / 2), y + int(self.CELL_SIZE / 2)]
                    ))

                x = x + self.CELL_SIZE - MazeCell.WALL_SIZE
            x = position[0]
            y = y + self.CELL_SIZE - MazeCell.WALL_SIZE

    def cell_position(self, x: int, y: int) -> tuple[int, int]:
        "Returns the top-left position for the cell at x, y"
        return (
            x * self.CELL_SIZE - x * MazeCell.WALL_SIZE,
            y * self.CELL_SIZE - y * MazeCell.WALL_SIZE
        )
    _DIRECTION_DELTAS: dict[Dir, tuple[int, int]] = {
        Dir.NORTH: (0, -1),
        Dir.EAST: (1, 0),
        Dir.SOUTH: (0, 1),
        Dir.WEST: (-1, 0),
    }

    def move_cell(self, cell: tuple[int, int], direction: Dir) -> tuple[int, int]:
        "Returns the resulting cell after moving from `cell` in `direction`, without checking legality"
        dx, dy = self._DIRECTION_DELTAS[direction]
        x, y = cell
        return (x + dx, y + dy)

    def can_move(self, cell: tuple[int, int], direction: Dir) -> bool:
        "Returns whether movement from `cell` in `direction` is legal"
        x, y = cell
        if not (0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])):
            return False
        return not (self.grid[y][x] & direction)
