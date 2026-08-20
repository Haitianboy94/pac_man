from functools import cache

import pygame as pg

from src.graphics.sprites import Sprites
from src.types import GhostType


class GeneralSprites(Sprites):
    PATH = "sprites/general.png"
    SIZE = 16

    #
    # Player sprites
    #
    PLAYER_MOVING = [
        (0, 0),
        (SIZE * 1, 0),
        (SIZE * 2, 0),
        (SIZE * 1, 0),
    ]

    @classmethod
    @cache
    def player_moving_north(cls) -> list[pg.Surface]:
        sprites = cls._load_all(
            (int(cls.SIZE / 2) + cls.SIZE * 28, 32),
            (16, 16),
            cls.PLAYER_MOVING,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def player_moving_east(cls) -> list[pg.Surface]:
        sprites = cls._load_all(
            (int(cls.SIZE / 2) + cls.SIZE * 28, 0), (16, 16), cls.PLAYER_MOVING
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def player_moving_west(cls) -> list[pg.Surface]:
        sprites = cls._load_all(
            (int(cls.SIZE / 2) + cls.SIZE * 28, 16),
            (16, 16),
            cls.PLAYER_MOVING,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def player_moving_south(cls) -> list[pg.Surface]:
        sprites = cls._load_all(
            (int(cls.SIZE / 2) + cls.SIZE * 28, 48),
            (16, 16),
            cls.PLAYER_MOVING,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def player_death(cls) -> list[pg.Surface]:
        frames = [(i * cls.SIZE, 0) for i in range(0, 11)]
        sprites = cls._load_all(
            (8 + cls.SIZE * 32, 0), (16, 16), frames
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    #
    # Ghost sprites
    #
    GHOST_BLINKY_OFFSET = (456, 64)
    GHOST_PINKY_OFFSET = (456, 80)
    GHOST_INKY_OFFSET = (456, 96)
    GHOST_CLYDE_OFFSET = (456, 112)
    GHOST_MOVE_EAST = [(0, 0), (16, 0)]
    GHOST_MOVE_WEST = [(32, 0), (48, 0)]
    GHOST_MOVE_NORTH = [(64, 0), (80, 0)]
    GHOST_MOVE_SOUTH = [(96, 0), (112, 0)]

    GHOST_OFFSETS = {
        GhostType.BLINKY: GHOST_BLINKY_OFFSET,
        GhostType.PINKY: GHOST_PINKY_OFFSET,
        GhostType.INKY: GHOST_INKY_OFFSET,
        GhostType.CLYDE: GHOST_CLYDE_OFFSET,
    }

    GHOST_SCARED_OFFSET = (584, 64)
    GHOST_SCARED = [(0, 0), (16, 0)]

    @classmethod
    @cache
    def ghost_moving_east(cls, type: GhostType) -> list[pg.Surface]:
        sprites = cls._load_all(
            cls.GHOST_OFFSETS[type],
            (16, 16),
            cls.GHOST_MOVE_EAST,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def ghost_moving_west(cls, type: GhostType) -> list[pg.Surface]:
        sprites = cls._load_all(
            cls.GHOST_OFFSETS[type],
            (16, 16),
            cls.GHOST_MOVE_WEST,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def ghost_moving_north(cls, type: GhostType) -> list[pg.Surface]:
        sprites = cls._load_all(
            cls.GHOST_OFFSETS[type],
            (16, 16),
            cls.GHOST_MOVE_NORTH,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def ghost_moving_south(cls, type: GhostType) -> list[pg.Surface]:
        sprites = cls._load_all(
            cls.GHOST_OFFSETS[type],
            (16, 16),
            cls.GHOST_MOVE_SOUTH,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    @classmethod
    @cache
    def ghost_scared(cls) -> list[pg.Surface]:
        sprites = cls._load_all(
            cls.GHOST_SCARED_OFFSET,
            (16, 16),
            cls.GHOST_SCARED,
        )
        for sprite in sprites:
            sprite.set_colorkey('black')
        return sprites

    #
    # Maze sprites
    #
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

    @classmethod
    def maze_color(cls) -> pg.Color:
        return pg.Color(33, 33, 255, 255)

    @classmethod
    @cache
    def maze_all(cls) -> pg.Surface:
        sprite = pg.Surface((16, 16))
        sprite.blit(
            cls.maze_t_south_west_north(), (0, 0), pg.Rect(0, 0, 8, 16)
        )
        sprite.blit(
            cls.maze_t_north_east_south(), (8, 0), pg.Rect(8, 0, 8, 16)
        )
        return sprite

    @classmethod
    def maze_t_east_south_west(cls) -> pg.Surface:
        return cls._load(cls.MAZE_T_BOTTOM, (16, 16))

    @classmethod
    def maze_t_north_east_south(cls) -> pg.Surface:
        return cls._load(cls.MAZE_T_RIGHT, (16, 16))

    @classmethod
    def maze_t_south_west_north(cls) -> pg.Surface:
        return cls._load(cls.MAZE_T_LEFT, (16, 16))

    @classmethod
    def maze_t_west_north_east(cls) -> pg.Surface:
        return cls._load(cls.MAZE_T_TOP, (16, 16))

    @classmethod
    @cache
    def maze_corner_north_east(cls) -> pg.Surface:
        sprite = cls.maze_corner_south_west()
        return pg.transform.flip(sprite, flip_x=True, flip_y=True)

    @classmethod
    @cache
    def maze_corner_north_west(cls) -> pg.Surface:
        sprite = cls.maze_corner_south_west()
        return pg.transform.flip(sprite, flip_x=False, flip_y=True)

    @classmethod
    @cache
    def maze_corner_south_east(cls) -> pg.Surface:
        sprite = cls.maze_corner_south_west()
        return pg.transform.flip(sprite, flip_x=True, flip_y=False)

    @classmethod
    def maze_corner_south_west(cls) -> pg.Surface:
        return cls._load(cls.MAZE_CORNER_SOUTH_WEST, (16, 16))

    @classmethod
    def maze_horizontal(cls) -> pg.Surface:
        return cls._load(cls.MAZE_HORIZONTAL, (16, 16))

    @classmethod
    def maze_vertical(cls) -> pg.Surface:
        return cls._load(cls.MAZE_VERTICAL, (16, 16))

    @classmethod
    def maze_end_north(cls) -> pg.Surface:
        return cls._load(cls.MAZE_END_NORTH, (16, 16))

    @classmethod
    def maze_end_east(cls) -> pg.Surface:
        return cls._load(cls.MAZE_END_EAST, (16, 16))

    @classmethod
    def maze_end_south(cls) -> pg.Surface:
        return cls._load(cls.MAZE_END_SOUTH, (16, 16))

    @classmethod
    def maze_end_west(cls) -> pg.Surface:
        return cls._load(cls.MAZE_END_WEST, (16, 16))

    # 8x8
    @classmethod
    @cache
    def maze_horizontal_connector(cls) -> pg.Surface:
        sprite = pg.Surface((8, 8))
        sprite.blit(cls.maze_horizontal(), pg.Rect(0, -4, 8, 8))
        return sprite

    @classmethod
    @cache
    def maze_vertical_connector(cls) -> pg.Surface:
        sprite = pg.Surface((8, 8))
        sprite.blit(cls.maze_vertical(), pg.Rect(-4, 0, 8, 8))
        return sprite

    @classmethod
    def pacgum(cls) -> pg.Surface:
        return cls._load((8, 8), (8, 8))

    @classmethod
    def super_pacgum(cls) -> pg.Surface:
        return cls._load((8, 24), (8, 8))
