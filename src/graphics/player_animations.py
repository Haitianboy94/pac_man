from src.graphics.general_sprites import GeneralSprites
from src.graphics.animation import Animation
from src.types import Dir
import pygame as pg

class PlayerAnimations:
    def __init__(self) -> None:
        self.playing: bool = True
        self.loop: bool = True
        self._move_animations: dict[Dir, Animation] = {
            Dir.NORTH: Animation(GeneralSprites.player_moving_north(), 16),
            Dir.EAST: Animation(GeneralSprites.player_moving_east(), 16),
            Dir.SOUTH: Animation(GeneralSprites.player_moving_south(), 16),
            Dir.WEST: Animation(GeneralSprites.player_moving_west(), 16),
            Dir.NONE: Animation([GeneralSprites.player_moving_east()[0]], 16)
        }
        self._death_animation = Animation(GeneralSprites.player_death(), 8)
        self._active: Animation 
        self.image: pg.Surface
        self.initial()

    def initial(self) -> None:
        self._active = self._move_animations[Dir.NONE]
        self.image = self._active.image

    def start_moving(self, dir: Dir) -> None:
        self._active = self._move_animations[dir]
        self.loop = True
        self.play()

    def stop_moving(self) -> None:
        self.stop()

    def die(self) -> None:
        self._active = self._death_animation
        self.loop = False
        self.play()

    def play(self) -> None:
        self.playing = True

    def stop(self):
        self.playing = False

    def update(self, dt: int) -> None:
        if self.playing:
            self._active.update_frame(dt)
            self.image = self._active.image
            if self._active.is_last_frame() and not self.loop:
                self.stop()
                self._active.reset()
