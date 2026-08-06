from src.entities.entity import Entity
from src.types import Dir
from src.ui.maze import Maze
import pygame as pg


class Player(Entity):
    """The pacman player entity"""
    SIZE = 32

    def __init__(self, maze: Maze, start_cell: tuple[int, int]) -> None:
        Entity.__init__(self)
        self.maze = maze
        self.cell_x, self.cell_y = start_cell

        self.image = pg.Surface((self.SIZE, self.SIZE), pg.SRCALPHA)
        pg.draw.circle(
            self.image, pg.Color("yellow"),
            (int(self.SIZE / 2), int(self.SIZE / 2)),
            int(self.SIZE / 2)
        )
        self.rect = self.image.get_rect()
        self._sync_rect_to_cell()

    def _sync_rect_to_cell(self) -> None:
        cell_x, cell_y = self.maze.cell_position(self.cell_x, self.cell_y)
        offset = int((self.maze.CELL_SIZE - self.SIZE) / 2)
        self.rect.topleft = (cell_x + offset, cell_y + offset)

    def update(self, events: list[pg.event.Event], dt: int) -> None:
        for event in events:
            if event.type != pg.KEYDOWN:
                continue
            direction = self._key_to_direction(event.key)
            if direction is not None:
                self._try_move(direction)

    def _key_to_direction(self, key: int) -> Dir | None:
        mapping = {
            pg.K_UP: Dir.NORTH,
            pg.K_DOWN: Dir.SOUTH,
            pg.K_LEFT: Dir.WEST,
            pg.K_RIGHT: Dir.EAST,
            pg.K_w: Dir.NORTH,
            pg.K_s: Dir.SOUTH,
            pg.K_a: Dir.WEST,
            pg.K_d: Dir.EAST,
        }
        return mapping.get(key)

    def _try_move(self, direction: Dir) -> None:
        if self.maze.can_move((self.cell_x, self.cell_y), direction):
            self.cell_x, self.cell_y = self.maze.move_cell((self.cell_x, self.cell_y), direction)
            self._sync_rect_to_cell()