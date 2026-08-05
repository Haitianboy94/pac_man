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

        self.current_frame: int = 0
        self.frame_elapsed_ms: int = 0
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.sprites = sprites

        self.direction: Dir = Dir.EAST
        self.frames = self.sprites.player_moving_east()
        self.image = self.frames[0]

    def update_frame(self, dt: int):
        ms_per_frame: int = int((1 / self.FPS) * 1000)

        self.frame_elapsed_ms += dt
        if self.frame_elapsed_ms > ms_per_frame:
            self.frame_elapsed_ms -= ms_per_frame
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.image = self.frames[self.current_frame]

    def update(self, dt: int) -> None:
        self.update_frame(dt)

    def set_direction(self, direction: Dir) -> None:
        self.direction = direction
        match direction:
            case Dir.NORTH: self.frames = self.sprites.player_moving_north()
            case Dir.EAST: self.frames = self.sprites.player_moving_east()
            case Dir.SOUTH: self.frames = self.sprites.player_moving_south()
            case Dir.WEST: self.frames = self.sprites.player_moving_west()
