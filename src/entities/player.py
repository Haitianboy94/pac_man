from src.graphics.animation import Animation
from src.graphics.general_sprites import GeneralSprites
from src.entities.entity import Entity
from src.types import Dir
from src.entities.maze import Maze
import pygame as pg


class Player(Entity):
    """The pacman player entity"""
    SIZE = 16
    FPS = 16

    def __init__(
        self,
        maze: Maze,
        start_cell: tuple[int, int],
        sprites: GeneralSprites
) -> None:
        Entity.__init__(self)
        self.maze: Maze = maze
        self.cell_x, self.cell_y = start_cell
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.sprites = sprites
        self.direction: Dir = Dir.EAST
        self.move_animations: dict[Dir, Animation] = {
            Dir.NORTH: Animation(self.sprites.player_moving_north(), self.FPS),
            Dir.EAST: Animation(self.sprites.player_moving_east(), self.FPS),
            Dir.SOUTH: Animation(self.sprites.player_moving_south(), self.FPS),
            Dir.WEST: Animation(self.sprites.player_moving_west(), self.FPS),
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

    def key_to_direction(self, key: int) -> Dir:
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

    def try_move(self, direction: Dir) -> None:
        if self.maze.can_move((self.cell_x, self.cell_y), direction):
            self.direction = direction
            self.animation = self.move_animations[self.direction]
            self.cell_x, self.cell_y = self.maze.move_cell((self.cell_x, self.cell_y), direction)
            self._sync_rect_to_cell()
