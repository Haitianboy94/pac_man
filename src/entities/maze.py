from src.entities.maze_wall import MazeWall
from src.graphics.general_sprites import GeneralSprites
from src.entities.entity import Entity
from src.entities.pacgum import Pacgum
from src.types import Dir, PacGumType
import pygame as pg


class Maze():
    """
    Represents a maze from the `MazeGenerator` in the UI. Walls are represented
    using 'MazeWall. The maze also contains the pacgums, and has methods used
    for positioning within the grid.
    """
    CELL_SIZE = 16
    WALL_SIZE = 8

    def __init__(
            self,
            grid: list[list[Dir]],
            sprites: GeneralSprites,
            position: tuple[int, int] = (0, 0),
            ):
        self.cells: pg.sprite.Group = pg.sprite.Group()
        self.pacgums: pg.sprite.Group = pg.sprite.Group()
        self.sprites: GeneralSprites = sprites
        cols, rows = len(grid), len(grid[0])
        self.walls: list[list[MazeWall]] = [
            [
                MazeWall(
                    Dir.NONE,
                    [
                        row * (self.CELL_SIZE + self.WALL_SIZE),
                        col * (self.CELL_SIZE + self.WALL_SIZE),
                    ],
                    sprites
                )
                for row in range(rows + 1)] 
            for col in range(cols + 1)
        ]

        x, y = position[0], position[1]
        cell_center: int = int(self.cell_size() / 2)

        for row_index, row in enumerate(grid):
            for col_index, cell in enumerate(row):
                if cell & Dir.NORTH:
                    self.walls[row_index][col_index].add_dir(Dir.EAST)
                    self.walls[row_index][col_index + 1].add_dir(Dir.WEST)
                if cell & Dir.EAST:
                    self.walls[row_index][col_index + 1].add_dir(Dir.SOUTH)
                    self.walls[row_index + 1][col_index + 1].add_dir(Dir.NORTH)
                if cell & Dir.SOUTH:
                    self.walls[row_index + 1][col_index + 1].add_dir(Dir.WEST)
                    self.walls[row_index + 1][col_index].add_dir(Dir.EAST)
                if cell & Dir.WEST:
                    self.walls[row_index + 1][col_index].add_dir(Dir.NORTH)
                    self.walls[row_index][col_index].add_dir(Dir.SOUTH)

                # if cell != Dir.ALL:
                #     self.pacgums.add(Pacgum(
                #         PacGumType.PACGUM,
                #         [x + cell_center, y + cell_center]
                #         ))

                x = x + self.CELL_SIZE + self.WALL_SIZE
            x = position[0]
            y = y + self.CELL_SIZE + self.WALL_SIZE
        for row in self.walls:
            for wall in row:
                wall.set_sprite()
                self.cells.add(wall)
                

    def cell_position(self, x: int, y: int) -> tuple[int, int]:
        "Returns the top-left position for the cell at x, y"
        offset = int(self.WALL_SIZE / 2)
        return (
            offset + x * self.CELL_SIZE - (x - 1) * self.WALL_SIZE,
            offset + y * self.CELL_SIZE - (y - 1) * self.WALL_SIZE
        )

    @staticmethod
    def cell_size() -> int:
        "Returns pixel size for each cell, including walls"
        return Maze.CELL_SIZE + (2 * Maze.WALL_SIZE)
