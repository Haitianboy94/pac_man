import pygame as pg

from src.entities.entity import Entity
from src.entities.maze import Maze
from src.graphics.animation import Animation
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir, GhostType


class Ghost(Entity):
    """The ghost entity"""

    SIZE = 16
    FPS = 4

    def __init__(
        self,
        type: GhostType,
        maze: Maze,
        start_cell: tuple[int, int],
    ) -> None:
        Entity.__init__(self)
        self.maze: Maze = maze
        self.cell_x, self.cell_y = start_cell
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.direction: Dir = Dir.EAST
        self.move_animations: dict[Dir, Animation] = {
            Dir.NORTH: Animation(
                GeneralSprites.ghost_moving_north(type), self.FPS
            ),
            Dir.EAST: Animation(
                GeneralSprites.ghost_moving_east(type), self.FPS
            ),
            Dir.SOUTH: Animation(
                GeneralSprites.ghost_moving_south(type), self.FPS
            ),
            Dir.WEST: Animation(
                GeneralSprites.ghost_moving_west(type), self.FPS
            ),
        }
        self.animation = self.move_animations[self.direction]
        self.image = self.animation.image
        self._sync_rect_to_cell()

    def _sync_rect_to_cell(self) -> None:
        cell_x, cell_y = self.maze.cell_position(self.cell_x, self.cell_y)
        offset = int((self.maze.CELL_SIZE - self.SIZE) / 2)
        self.rect.topleft = (cell_x + offset, cell_y + offset)

    def update(self, dt: int) -> None:
        self.animation.update_frame(dt)
        self.image = self.animation.image
