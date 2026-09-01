import pygame as pg


class Animation:
    """Represent Animation state and behavior."""

    def __init__(self, frames: list[pg.Surface], fps: int) -> None:
        """Initialize the object."""
        if len(frames) < 1:
            raise ValueError("Animation must contain at least one frame")
        self.frames: list[pg.Surface] = frames
        self.ms_per_frame: int = int((1 / fps) * 1000)
        self.image: pg.Surface = frames[0]
        self.current_frame: int = 0
        self.frame_elapsed_ms: int = 0

    def reset(self) -> None:
        """Reset the object."""
        self.image = self.frames[0]
        self.current_frame = 0
        self.frame_elapsed_ms = 0

    def update_frame(self, dt: int) -> None:
        """Update the object."""
        self.frame_elapsed_ms += dt
        if self.frame_elapsed_ms > self.ms_per_frame:
            self.frame_elapsed_ms -= self.ms_per_frame
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.image = self.frames[self.current_frame]

    def is_last_frame(self) -> bool:
        """Return whether the object last frame."""
        return self.current_frame == len(self.frames) - 1
