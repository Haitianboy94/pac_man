from typing import Callable
import pygame as pg

class Timer:
    def __init__(self, duration: int, on_end: Callable | None = None):
        self.duration: int = duration
        self.ends_at: None | int = None
        self.on_end: Callable | None = on_end

    def update(self) -> None:
        if self.ends_at is None:
            return
        if pg.time.get_ticks() > self.ends_at:
            if self.on_end:
                self.on_end()
            self.ends_at = None

    def start(self) -> None:
        self.ends_at = pg.time.get_ticks() + self.duration

    def is_active(self) -> bool:
        return self.ends_at is not None
