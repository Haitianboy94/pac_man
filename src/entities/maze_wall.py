from typing import Sequence
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir
import pygame as pg


class MazeWall(pg.sprite.Sprite):
    def __init__(self, dir: Dir, position: Sequence[int], sprites: GeneralSprites) -> None:
        pg.sprite.Sprite.__init__(self)
        self.dir: Dir = dir
        self.sprites: GeneralSprites = sprites
        self.position: Sequence[int] = position
        self.rect: pg.Rect = pg.Rect(position, [16, 16])
        self.image = pg.Surface((0,0))

    def set_sprite(self) -> None:
        if self.dir == Dir.ALL:
            self.image = self.sprites.maze_all()
        elif self.dir == Dir.NORTH | Dir.EAST | Dir.SOUTH: 
            self.image = self.sprites.maze_t_north_east_south()
        elif self.dir == Dir.EAST | Dir.SOUTH | Dir.WEST: 
            self.image = self.sprites.maze_t_east_south_west()
        elif self.dir == Dir.SOUTH | Dir.WEST | Dir.NORTH: 
            self.image = self.sprites.maze_t_south_west_north()
        elif self.dir == Dir.WEST | Dir.NORTH | Dir.EAST: 
            self.image = self.sprites.maze_t_west_north_east()
        elif self.dir == Dir.NORTH | Dir.EAST: 
            self.image = self.sprites.maze_corner_north_east()
        elif self.dir == Dir.NORTH | Dir.WEST: 
            self.image = self.sprites.maze_corner_north_west()
        elif self.dir == Dir.SOUTH | Dir.EAST: 
            self.image = self.sprites.maze_corner_south_east()
        elif self.dir == Dir.SOUTH | Dir.WEST: 
            self.image = self.sprites.maze_corner_south_west()
        elif self.dir == Dir.NORTH | Dir.SOUTH:
            self.image = self.sprites.maze_vertical()
        elif self.dir == Dir.EAST | Dir.WEST:
            self.image = self.sprites.maze_horizontal()
        elif self.dir == Dir.NORTH:
            self.image = self.sprites.maze_end_north()
        elif self.dir == Dir.EAST:
            self.image = self.sprites.maze_end_east()
        elif self.dir == Dir.SOUTH:
            self.image = self.sprites.maze_end_south()
        elif self.dir == Dir.WEST:
            self.image = self.sprites.maze_end_west()
        else:
            self.image = pg.Surface((0,0))

    def add_dir(self, dir: Dir) -> None:
        self.dir |= dir


