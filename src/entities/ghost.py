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
    MOVE_INTERVAL_MS = 500  # how often the ghost decides to move

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
        self.move_timer: int = 0

    def _sync_rect_to_cell(self) -> None:
        cell_x, cell_y = Maze.cell_position((self.cell_x, self.cell_y))
        offset = int((Maze.CELL_SIZE - self.SIZE) / 2)
        self.rect.topleft = (cell_x + offset, cell_y + offset)

    # def update(self, dt: int) -> None:
    #     self.animation.update_frame(dt)
    #     self.image = self.animation.image
    def update(self, dt: int, target_cell: tuple[int, int]) -> None:
        self.animation.update_frame(dt)
        self.image = self.animation.image

        self.move_timer += dt
        if self.move_timer >= self.MOVE_INTERVAL_MS:
            self.move_timer = 0
            self._chase(target_cell)

    def _chase(self, target_cell: tuple[int, int]) -> None:
        best_direction: Dir | None = None
        best_cell: tuple[int, int] | None = None
        best_distance: int | None = None

        for direction in (Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST):
            if not self.maze.can_move((self.cell_x, self.cell_y), direction):
                continue
            candidate_cell = self.maze.move_cell((self.cell_x, self.cell_y), direction)
            distance = (
                (candidate_cell[0] - target_cell[0]) ** 2 +
                (candidate_cell[1] - target_cell[1]) ** 2
            )

            if best_distance is None or distance < best_distance:
                best_direction = direction
                best_cell = candidate_cell
                best_distance = distance

        if best_cell is not None and best_direction is not None:
            self.cell_x, self.cell_y = best_cell
            self.direction = best_direction
            self.animation = self.move_animations[self.direction]
            self._sync_rect_to_cell()