from src.ui.spritesheet import Spritesheet
from src.types import Dir
from src.entities.entity import Entity
from src.ui.maze import Maze
import pygame as pg


class Player(Entity):
    """
    The pacman player entity
    """
    SIZE = 16

    FPS = 16
    MS_PER_FRAME = (1 / FPS) * 1000

    FRAMES = [
        [8 + 16 * 28, 0],
        [8 + 16 * 29, 0],
        [8 + 16 * 30, 0],
        [8 + 16 * 29, 0],
    ]

    def __init__(self, sprites: Spritesheet) -> None:
        pg.sprite.Sprite.__init__(self)

        self.current_frame: int = 0
        self.frame_elapsed_ms: int = 0
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.sprites = sprites

        self.direction: Dir = Dir.EAST
        self.update_frame()

    def frames(self):
        match self.direction:
            case Dir.NORTH: return Spritesheet.PLAYER_MOVING_NORTH
            case Dir.EAST: return Spritesheet.PLAYER_MOVING_EAST
            case Dir.SOUTH: return Spritesheet.PLAYER_MOVING_SOUTH
            case Dir.WEST: return Spritesheet.PLAYER_MOVING_WEST
    
    def update_frame(self):
        self.image = pg.Surface((self.SIZE, self.SIZE))
        self.image.blit(
            self.sprites.general,
            [0, 0],
            pg.Rect(self.frames()[self.current_frame], [self.SIZE, self.SIZE])
        )

    def update(self, events: list[pg.event.Event], dt: int) -> None:
        self.frame_elapsed_ms += dt
        if self.frame_elapsed_ms > self.MS_PER_FRAME:
            self.frame_elapsed_ms -= self.MS_PER_FRAME
            self.current_frame += 1
            self.current_frame %= len(self.FRAMES)
            self.update_frame()

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.set_direction(Dir.NORTH)
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.set_direction(Dir.EAST)
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.set_direction(Dir.SOUTH)
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.set_direction(Dir.WEST)

    def set_direction(self, direction: Dir) -> None:
        self.direction = direction
