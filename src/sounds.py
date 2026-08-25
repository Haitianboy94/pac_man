from src.resources import resource_path
from functools import cache
import pygame as pg

class Sounds:
    gum_sound = 0

    @classmethod
    def start(cls) -> pg.mixer.Sound:
        return cls._load("sounds/start.wav")

    @classmethod
    def eat_gum(cls) -> pg.mixer.Sound:
        if cls.gum_sound == 0:
            cls.gum_sound = 1
            return cls._load("sounds/eat_gum_0.wav")
        cls.gum_sound = 0
        return cls._load("sounds/eat_gum_1.wav")

    @classmethod
    def death(cls) -> pg.mixer.Sound:
        # 1.49 seconds duration
        return cls._load("sounds/death.wav")

    @classmethod
    @cache
    def _load(cls, path: str) -> pg.mixer.Sound:
        return pg.mixer.Sound(resource_path(path))


