from typing import Callable
import pygame as pg

class Timer:
    """Represent Timer state and behavior."""
    def __init__(self, duration: int, on_end: Callable | None = None):
        """Initialize the object."""
        self.duration: int = duration
        self.ends_at: None | int = None
        self.on_end: Callable | None = on_end

    def update(self) -> None:
        """Update the object."""
        if self.ends_at is None:
            return
        if pg.time.get_ticks() > self.ends_at:
            if self.on_end:
                self.on_end()
            self.ends_at = None

    def start(self) -> None:
        """Start the object."""
        self.ends_at = pg.time.get_ticks() + self.duration

    def is_active(self) -> bool:
        """Return whether the object active."""
        return self.ends_at is not None
