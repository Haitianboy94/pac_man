from functools import cache
from dataclasses import dataclass
from src.types import Dir
import pygame as pg

class GeneralSprites:
    PATH = "sprites/general.png"
    SIZE = 16

    def __init__(self) -> None:
        self.sheet: pg.Surface = pg.image.load(self.PATH)
        self.sheet.convert_alpha()
        self.sheet.set_colorkey("black")

    @cache
    def _load(self, x: int, y: int) -> pg.Surface:
        sprite: pg.Surface = pg.Surface([self.SIZE, self.SIZE])
        sprite.blit(
            self.sheet,
            [0, 0],
            pg.Rect([x, y], [self.SIZE, self.SIZE])
        )
        return sprite
    
    def _load_all(
            self,
            offset_x: int,
            offset_y: int,
            delta_coords: list[tuple[int, int]]
    ) -> list[pg.Surface]:
        return [
            self._load(offset_x + dx, offset_y + dy)
            for [dx, dy] in delta_coords
        ]

    ##### Player sprites

    PLAYER_MOVING = [
        (0, 0),
        (SIZE * 1, 0),
        (SIZE * 2, 0),
        (SIZE * 1, 0),
    ]

    def player_moving_north(self) -> list[pg.Surface]:
        return self._load_all(
            int(self.SIZE / 2) + self.SIZE * 28,
            32,
            self.PLAYER_MOVING
        )
    def player_moving_east(self) -> list[pg.Surface]:
        return self._load_all(
            int(self.SIZE / 2) + self.SIZE * 28,
            0,
            self.PLAYER_MOVING
        )

    def player_moving_west(self) -> list[pg.Surface]:
        return self._load_all(
            int(self.SIZE / 2) + self.SIZE * 28,
            16,
            self.PLAYER_MOVING
        )

    def player_moving_south(self) -> list[pg.Surface]:
        return self._load_all(
            int(self.SIZE / 2) + self.SIZE * 28,
            48,
            self.PLAYER_MOVING
        )
    
    ##### Maze sprites
    MAZE_END_EAST = (4 + SIZE * 15, SIZE * 3)
    MAZE_END_WEST = (4 + SIZE * 16, SIZE * 3)
    MAZE_END_SOUTH = (12 + SIZE * 17, SIZE * 3)
    MAZE_END_NORTH = (12 + SIZE * 17, SIZE * 6)
    MAZE_HORIZONTAL = (12 + SIZE * 15, SIZE * 3)
    MAZE_VERTICAL = (12 + SIZE * 17, 8 + SIZE * 3)
    MAZE_CORNER_SOUTH_WEST = (4 + SIZE * 16, 8 + SIZE * 10)

    MAZE_T_BOTTOM = (12 + SIZE * 20, SIZE * 3)
    MAZE_T_RIGHT = (12 + SIZE * 17, 8 + SIZE * 4)
    MAZE_T_LEFT = (12 + SIZE * 23, 8 + SIZE * 4)
    MAZE_T_TOP = (12 + SIZE * 17, 8 + SIZE * 13)

    @cache
    def maze_all(self) -> pg.Surface:
        sprite = pg.Surface((16, 16))
        sprite.blit(self.maze_t_south_west_north(), (0, 0), pg.Rect(0, 0, 8, 16))
        sprite.blit(self.maze_t_north_east_south(), (8, 0), pg.Rect(8, 0, 8, 16))
        return sprite

    def maze_t_east_south_west(self) -> pg.Surface:
        x, y = self.MAZE_T_BOTTOM;
        return self._load(x, y)

    def maze_t_north_east_south(self) -> pg.Surface:
        x, y = self.MAZE_T_RIGHT;
        return self._load(x, y)

    def maze_t_south_west_north(self) -> pg.Surface:
        x, y = self.MAZE_T_LEFT;
        return self._load(x, y)

    def maze_t_west_north_east(self) -> pg.Surface:
        x, y = self.MAZE_T_TOP;
        return self._load(x, y)

    @cache
    def maze_corner_north_east(self) -> pg.Surface:
        sprite = self.maze_corner_south_west()
        return pg.transform.flip(sprite, flip_x=True, flip_y=True)
    
    @cache
    def maze_corner_north_west(self) -> pg.Surface:
        sprite = self.maze_corner_south_west()
        return pg.transform.flip(sprite, flip_x=False, flip_y=True)

    @cache
    def maze_corner_south_east(self) -> pg.Surface:
        sprite = self.maze_corner_south_west()
        return pg.transform.flip(sprite, flip_x=True, flip_y=False)

    def maze_corner_south_west(self) -> pg.Surface:
        x, y = self.MAZE_CORNER_SOUTH_WEST
        return self._load(x, y)

    def maze_horizontal(self) -> pg.Surface:
        x, y = self.MAZE_HORIZONTAL
        return self._load(x, y)

    def maze_vertical(self) -> pg.Surface:
        x, y = self.MAZE_VERTICAL
        return self._load(x, y)

    def maze_end_north(self) -> pg.Surface:
        x, y = self.MAZE_END_NORTH
        return self._load(x, y)

    def maze_end_east(self) -> pg.Surface:
        x, y = self.MAZE_END_EAST
        return self._load(x, y)

    def maze_end_south(self) -> pg.Surface:
        x, y = self.MAZE_END_SOUTH
        return self._load(x, y)

    def maze_end_west(self) -> pg.Surface:
        x, y = self.MAZE_END_WEST
        return self._load(x, y)

    # 8x8
    @cache
    def maze_horizontal_connector(self) -> pg.Surface:
        sprite = pg.Surface((8,8))
        sprite.blit(self.maze_horizontal(), pg.Rect(0, -4, 8, 8))
        return sprite

    @cache
    def maze_vertical_connector(self) -> pg.Surface:
        sprite = pg.Surface((8,8))
        sprite.blit(self.maze_vertical(), pg.Rect(-4, 0, 8, 8))
        return sprite
