from functools import cache
from abc import ABC, abstractmethod
import pygame as pg

class Sprites(ABC):
    def __init__(self, path: str) -> None:
        self.sheet: pg.Surface = pg.image.load(path).convert_alpha()

    @cache
    def _load(self, x: int, y: int, size_x: int, size_y: int) -> pg.Surface:
        sprite: pg.Surface = pg.Surface([size_x, size_y])
        sprite.blit(
            self.sheet,
            [0, 0],
            pg.Rect([x, y], [size_x, size_y])
        )
        return sprite.convert_alpha()
    
    def _load_all(
            self,
            offset_x: int,
            offset_y: int,
            size_x: int,
            size_y: int,
            delta_coords: list[tuple[int, int]]
    ) -> list[pg.Surface]:
        return [
            self._load(offset_x + dx, offset_y + dy, size_x, size_y)
            for [dx, dy] in delta_coords
        ]
