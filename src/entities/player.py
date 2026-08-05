from src.graphics.animation import Animation
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir
from src.entities.entity import Entity
from src.entities.maze import Maze
import pygame as pg


class Player(Entity):
    """
    The pacman player entity
    """
    SIZE = 16
    FPS = 16

    def __init__(self, sprites: GeneralSprites) -> None:
        pg.sprite.Sprite.__init__(self)

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

    def update(self, dt: int) -> None:
        self.animation.update_frame(dt)
        self.image = self.animation.image

    def set_direction(self, direction: Dir) -> None:
        self.direction = direction
        self.animation = self.move_animations[self.direction]
