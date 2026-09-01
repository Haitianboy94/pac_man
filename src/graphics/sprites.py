from functools import cache

import pygame as pg

from src.resources import resource_path


class Sprites:
    """Represent Sprites state and behavior."""

    PATH: str

    @classmethod
    @cache
    def sheet(cls) -> pg.Surface:
        """Handle sheet."""
        return pg.image.load(resource_path(cls.PATH)).convert_alpha()

    @classmethod
    @cache
    def _load(cls, pos: tuple[int, int], size: tuple[int, int]) -> pg.Surface:
        """Perform the load operation."""
        sprite: pg.Surface = pg.Surface(size, pg.SRCALPHA)
        sprite.blit(cls.sheet(), [0, 0], pg.Rect(pos, size))
        return sprite

    @classmethod
    def _load_all(
        cls,
        offset: tuple[int, int],
        size: tuple[int, int],
        delta_coords: list[tuple[int, int]],
    ) -> list[pg.Surface]:
        """Perform the load all operation."""
        return [
            cls._load((offset[0] + dx, offset[1] + dy), size)
            for [dx, dy] in delta_coords
        ]
