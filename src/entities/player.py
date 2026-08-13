from shutil import move
import math
import pygame as pg

from src.entities.entity import Entity
from src.entities.maze import Maze
from src.graphics.animation import Animation
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir


class Player(Entity):
    """The pacman player entity"""

    SIZE = 16
    FPS = 16
    # Speed in pixels per second
    DEFAULT_SPEED = 60.0
    CELL_DISTANCE = Maze.CELL_SIZE + Maze.WALL_SIZE

    def __init__(
        self,
        maze: Maze,
        start_cell: tuple[int, int],
    ) -> None:
        Entity.__init__(self)
        self.maze: Maze = maze
        self.cell: tuple[int, int] = start_cell
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.move_direction: Dir = Dir.NONE
        self.move_progress: float = 0.0
        self.target_direction: Dir = Dir.EAST
        self.speed: float = self.DEFAULT_SPEED

        self.move_animations: dict[Dir, Animation] = {
            Dir.NORTH: Animation(
                GeneralSprites.player_moving_north(), self.FPS
            ),
            Dir.EAST: Animation(GeneralSprites.player_moving_east(), self.FPS),
            Dir.SOUTH: Animation(
                GeneralSprites.player_moving_south(), self.FPS
            ),
            Dir.WEST: Animation(GeneralSprites.player_moving_west(), self.FPS),
            Dir.NONE: Animation([GeneralSprites.player_moving_east()[0]], self.FPS)
        }
        self.animation = self.move_animations[self.move_direction]
        self.image = self.animation.image
        self._sync_rect_to_cell()

    def key_to_direction(self, key: int) -> Dir:
        "Returns the direction corresponding with the input key"
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
        return mapping[key]

    def update(self, dt: int) -> None:
        # only continue to update if moving or trying to start moving
        if self.move_direction is Dir.NONE and self.target_direction is Dir.NONE:
            return

        # in cell exactly, usually when stationary
        if self.move_progress == 0.0:
            self._cell_movement()

        # player can turn around at any time
        if self.target_direction.opposite() == self.move_direction:
            self._reverse_direction()
            
        # calculate move_progress from dt and speed
        progress: float = self.speed * dt / 1000
        self.move_progress += progress
        in_next_cell: bool = self.move_progress // self.CELL_DISTANCE >= 1

        # cell threshold was crossed
        if in_next_cell:
            dx, dy = self.move_direction.delta()
            self.move_progress %= self.CELL_DISTANCE
            self.cell = (self.cell[0] + dx, self.cell[1] + dy)
            self._cell_movement()

        self._sync_rect_to_cell()

        # animations
        if self.move_direction is not Dir.NONE:
            self.animation.update_frame(dt)
            self.image = self.animation.image

    def _sync_rect_to_cell(self) -> None:
        """
        Sets the player rect postion based on current maze cell and
        movement direction/progress.
        """
        cell_x, cell_y = Maze.cell_position(self.cell)
        dx, dy = self.move_direction.delta()
        pos_x: int = round(cell_x + (dx * self.move_progress))
        pos_y: int = round(cell_y + (dy * self.move_progress))
        self.rect.topleft = (pos_x, pos_y)
    
    def _cell_movement(self) -> None:
        "Handle movement option from a cell in the maze"
        can_continue: bool = self.maze.can_move(self.cell, self.move_direction)
        can_turn: bool = self.maze.can_move(self.cell, self.target_direction)
        if not can_continue:
            self.move_direction = Dir.NONE
            self.move_progress = 0
        if self.target_direction is not Dir.NONE:
            if can_turn:
                self.move_direction = self.target_direction
                self.target_direction = Dir.NONE
                self.animation = self.move_animations[self.move_direction]

    def _reverse_direction(self) -> None:
        "Turn around, swapping the current cell with the next"
        dx, dy = self.move_direction.delta()
        next_cell = (self.cell[0] + dx, self.cell[1] + dy)
        self.cell = next_cell
        self.move_progress = 24 - self.move_progress
        self.move_direction = self.target_direction
        self.target_direction = Dir.NONE
        self.animation = self.move_animations[self.move_direction]
