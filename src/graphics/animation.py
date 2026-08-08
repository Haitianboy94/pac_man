import pygame as pg

class Animation:

    def __init__(self, frames: list[pg.Surface], fps: int):
        if len(frames) < 1:
            raise ValueError("Animation must contain at least one frame")
        self.frames: list[pg.Surface] = frames
        self.image: pg.Surface = frames[0]
        self.fps: int = fps
        self.current_frame: int = 0
        self.frame_elapsed_ms: int = 0

    def update_frame(self, dt: int):
        ms_per_frame: int = int((1 / self.fps) * 1000)

        self.frame_elapsed_ms += dt
        if self.frame_elapsed_ms > ms_per_frame:
            self.frame_elapsed_ms -= ms_per_frame
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.image = self.frames[self.current_frame]



