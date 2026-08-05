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

