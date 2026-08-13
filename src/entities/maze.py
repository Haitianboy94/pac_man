import pygame as pg

from src.entities.maze_wall import MazeWall
from src.entities.pacgum import Pacgum
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir, PacGumType


class Maze:
    """
    Represents a maze from the `MazeGenerator` in the UI. Walls are represented
    using 'MazeWall. The maze also contains the pacgums, and has methods used
    for positioning within the grid.
    """

    OFFSET = 12
    CELL_SIZE = 16
    WALL_SIZE = 8

    def __init__(
        self,
        grid: list[list[Dir]],
        position: tuple[int, int] = (0, 0),
    ):
        self.grid: list[list[Dir]] = grid
        self.cells: pg.sprite.Group = pg.sprite.Group()
        self.pacgums: pg.sprite.Group = pg.sprite.Group()
        cols, rows = len(grid), len(grid[0])
        self.walls: list[list[MazeWall]] = [
            [
                MazeWall(
                    Dir.NONE,
                    [
                        row * (self.CELL_SIZE + self.WALL_SIZE),
                        col * (self.CELL_SIZE + self.WALL_SIZE),
                    ],
                )
                for row in range(rows + 1)
            ]
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

                if cell != Dir.ALL:
                    super_pos = [
                        (1, 1),
                        (1, cols - 2),
                        (rows - 2, 1),
                        (rows - 2, cols - 2),
                    ]
                    if (row_index, col_index) in super_pos:
                        type = PacGumType.SUPER_PACGUM
                    else:
                        type = PacGumType.PACGUM

                    self.pacgums.add(
                        Pacgum(type, [x + cell_center, y + cell_center])
                    )

                x = x + self.CELL_SIZE + self.WALL_SIZE
            x = position[0]
            y = y + self.CELL_SIZE + self.WALL_SIZE
        for row in self.walls:
            for wall in row:
                wall.set_sprite()
                self.cells.add(wall)

    def draw(self, surface: pg.Surface) -> None:
        self.cells.draw(surface)
        horizontal = GeneralSprites.maze_horizontal_connector()
        vertical = GeneralSprites.maze_vertical_connector()
        for row in self.walls:
            for wall in row:
                x, y = wall.position
                if wall.dir & Dir.EAST:
                    rect = pg.Rect(
                        (x + self.CELL_SIZE, y + int(self.WALL_SIZE / 2)),
                        (8, 8),
                    )
                    surface.blit(horizontal, rect)
                if wall.dir & Dir.SOUTH:
                    rect = pg.Rect(
                        (x + int(self.WALL_SIZE / 2), y + self.CELL_SIZE),
                        (8, 8),
                    )
                    surface.blit(vertical, rect)


    def move_cell(
        self, cell: tuple[int, int], direction: Dir
    ) -> tuple[int, int]:
        """
        Returns the resulting cell after moving from `cell` in `direction`
        without checking legality
        """
        dx, dy = direction.delta()
        x, y = cell
        return (x + dx, y + dy)

    def can_move(self, cell: tuple[int, int], direction: Dir) -> bool:
        "Returns whether movement from `cell` in `direction` is legal"
        if direction is Dir.NONE:
            return False
        x, y = cell
        if not (0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])):
            return False
        return not (self.grid[y][x] & direction)

    def center(self) -> tuple[int, int]:
        "Returns the approximate center cell of the maze grid"
        width = len(self.grid[0])
        height = len(self.grid)
        return (width // 2, height // 2)

    def corners(self) -> list[tuple[int, int]]:
        width = len(self.grid[0])
        height = len(self.grid)
        candidates = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]
        for x, y in candidates:
            if self.grid[y][x] == Dir.NORTH | Dir.EAST | Dir.SOUTH | Dir.WEST:
                print(f"[Maze] Warning: corner ({x},{y}) is fully sealed")
        return candidates

    @staticmethod
    def cell_position(pos: tuple[int, int]) -> tuple[int, int]:
        "Returns the top-left position for the cell at x, y"
        x, y = pos
        return (
            Maze.OFFSET + x * Maze.CELL_SIZE + x * Maze.WALL_SIZE,
            Maze.OFFSET + y * Maze.CELL_SIZE + y * Maze.WALL_SIZE,
        )

    @staticmethod
    def maze_size(width: int, height: int) -> tuple[int, int]:
        cell = Maze.CELL_SIZE
        wall = Maze.WALL_SIZE
        return (
            2 * wall + width * (cell + wall),
            2 * wall + height * (cell + wall),
        )

    @staticmethod
    def cell_size() -> int:
        "Returns pixel size for each cell, including walls"
        return Maze.CELL_SIZE + (2 * Maze.WALL_SIZE)
