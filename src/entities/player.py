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

    def __init__(
        self,
        maze: Maze,
        start_cell: tuple[int, int],
    ) -> None:
        Entity.__init__(self)
        self.maze: Maze = maze
        self.cell_x, self.cell_y = start_cell
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.position: tuple[float, float] = (0, 0)
        self.move_direction: Dir = Dir.NONE
        self.target_direction: Dir = Dir.NONE
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

    def _sync_rect_to_cell(self) -> None:
        cell_x, cell_y = Maze.cell_position((self.cell_x, self.cell_y))
        offset = int((Maze.CELL_SIZE - self.SIZE) / 2)
        self.position = (cell_x + offset, cell_y + offset)
        self.rect.topleft = self.position

    def update(self, dt: int) -> None:
        # only continue update if moving or trying to start moving
        if self.move_direction is Dir.NONE and self.target_direction is Dir.NONE:
            return

        # calculate next position
        x, y = prev_position = self.position
        if self.move_direction is not Dir.NONE:
            dx, dy = self.move_direction.delta()
            movement_factor = self.speed * dt / 1000
            dx, dy = dx * movement_factor, dy * movement_factor
            next_x, next_y = x+dx, y+dy
            # move to next position
            self.position = (next_x, next_y)
            self.rect.topleft = (int(next_x), int(next_y))


        # player can reverse direction at any time
        if self.target_direction.opposite() is self.move_direction:
            self._move_in_target_dir()
        # if at cell corner player can try to turn, or be stopped by a wall
        elif self.passes_cell_corner(prev_position) or self.move_direction is Dir.NONE:
            print(self.move_direction, self.target_direction)
            if (self.target_direction is not Dir.NONE
                    and self.target_direction is not self.move_direction):
                print("try to turn")
                self._try_turn()
            else:
                print("maybe stop")
                self._maybe_stop()

        # animations
        if self.move_direction is not Dir.NONE:
            self.animation.update_frame(dt)
            self.image = self.animation.image


    def passes_cell_corner(self, other_pos: tuple[float, float]) -> bool:
        cell_interval = Maze.CELL_SIZE + Maze.WALL_SIZE

        x1, y1 = self.position
        x2, y2 = other_pos
        x1, y1 = x1 - Maze.OFFSET, y1 - Maze.OFFSET
        x2, y2 = x2 - Maze.OFFSET, y2 - Maze.OFFSET
        cell_x1 = math.floor(x1 / cell_interval)
        cell_y1 = math.floor(y1 / cell_interval)
        cell_x2 = math.floor(x2 / cell_interval)
        cell_y2 = math.floor(y2 / cell_interval)

        return cell_x1 != cell_x2 or cell_y1 != cell_y2

    def _try_turn(self) -> bool:
        """
        Try to turn into to target_direction.
        Should only be called if the player is at a cell corner.
        If the player turned the function returns True and clears
        the target_direction
        """
        if self.target_direction is Dir.NONE:
            return False
        cell_offset = Maze.CELL_SIZE + Maze.WALL_SIZE
        x, y = self.position
        cell_x = math.floor(x / cell_offset)
        cell_y = math.floor(y / cell_offset)
        can_move = self.maze.can_move((cell_x, cell_y), self.target_direction)
        if can_move:
            self._move_in_target_dir()
            self.target_direction = Dir.NONE
            self.position = Maze.cell_position((cell_x, cell_y))
            return True
        if self.move_direction is Dir.NONE:
            self.target_direction = Dir.NONE
        return False

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

    def _stop_moving(self) -> None:
        "Stop player movement by clearing move_direction"
        self.move_direction = Dir.NONE

    def _move_in_target_dir(self) -> None:
        """
        Start moving towards target_direction. 
        The target_direction will be cleared
        """
        self.move_direction = self.target_direction
        self.target_direction = Dir.NONE
        self.animation = self.move_animations[self.move_direction]

    def _maybe_stop(self) -> bool:
        """
        Checks if the current cell allows movement to continue.
        Returns if the player will be moving after this function
        """
        if self.move_direction is Dir.NONE:
            return False
        cell_offset = Maze.CELL_SIZE + Maze.WALL_SIZE
        x, y = self.position
        cell_x = math.floor(x / cell_offset)
        cell_y = math.floor(y / cell_offset)
        can_move = self.maze.can_move((cell_x, cell_y), self.move_direction)
        if not can_move:
            self._stop_moving()
            return False
        return True
