from typing import Sequence

import pygame as pg

from src.graphics.general_sprites import GeneralSprites
from src.types import Dir


class MazeWall(pg.sprite.Sprite):
    """Represent MazeWall state and behavior."""
    def __init__(self, dir: Dir, position: Sequence[int]) -> None:
        """Initialize the object."""
        pg.sprite.Sprite.__init__(self)
        self.dir: Dir = dir
        self.position: Sequence[int] = position
        self.rect: pg.Rect = pg.Rect(position, [16, 16])
        self.image = pg.Surface((0, 0))

    def set_sprite(self) -> None:
        """Set the sprite."""
        if self.dir == Dir.ALL:
            self.image = GeneralSprites.maze_all()
        elif self.dir == Dir.NORTH | Dir.EAST | Dir.SOUTH:
            self.image = GeneralSprites.maze_t_north_east_south()
        elif self.dir == Dir.EAST | Dir.SOUTH | Dir.WEST:
            self.image = GeneralSprites.maze_t_east_south_west()
        elif self.dir == Dir.SOUTH | Dir.WEST | Dir.NORTH:
            self.image = GeneralSprites.maze_t_south_west_north()
        elif self.dir == Dir.WEST | Dir.NORTH | Dir.EAST:
            self.image = GeneralSprites.maze_t_west_north_east()
        elif self.dir == Dir.NORTH | Dir.EAST:
            self.image = GeneralSprites.maze_corner_north_east()
        elif self.dir == Dir.NORTH | Dir.WEST:
            self.image = GeneralSprites.maze_corner_north_west()
        elif self.dir == Dir.SOUTH | Dir.EAST:
            self.image = GeneralSprites.maze_corner_south_east()
        elif self.dir == Dir.SOUTH | Dir.WEST:
            self.image = GeneralSprites.maze_corner_south_west()
        elif self.dir == Dir.NORTH | Dir.SOUTH:
            self.image = GeneralSprites.maze_vertical()
        elif self.dir == Dir.EAST | Dir.WEST:
            self.image = GeneralSprites.maze_horizontal()
        elif self.dir == Dir.NORTH:
            self.image = GeneralSprites.maze_end_north()
        elif self.dir == Dir.EAST:
            self.image = GeneralSprites.maze_end_east()
        elif self.dir == Dir.SOUTH:
            self.image = GeneralSprites.maze_end_south()
        elif self.dir == Dir.WEST:
            self.image = GeneralSprites.maze_end_west()
        else:
            self.image = pg.Surface((0, 0))

    def add_dir(self, dir: Dir) -> None:
        """Add the requested add dir."""
        self.dir |= dir
