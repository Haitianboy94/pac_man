from src.graphics.general_sprites import GeneralSprites
from src.graphics.animation import Animation
from src.types import Dir
import pygame as pg

class PlayerAnimations:
    """Represent PlayerAnimations state and behavior."""
    def __init__(self) -> None:
        """Initialize the object."""
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
        """Handle initial."""
        self._active = self._move_animations[Dir.NONE]
        self.image = self._active.image

    def start_moving(self, dir: Dir) -> None:
        """Start the object."""
        self._active = self._move_animations[dir]
        self.loop = True
        self.play()

    def stop_moving(self) -> None:
        """Stop the object."""
        self.stop()

    def die(self) -> None:
        """Die the object."""
        self._active = self._death_animation
        self.loop = False
        self.play()

    def play(self) -> None:
        """Play the object."""
        self.playing = True

    def stop(self):
        """Stop the object."""
        self.playing = False

    def update(self, dt: int) -> None:
        """Update the object."""
        if self.playing:
            self._active.update_frame(dt)
            self.image = self._active.image
            if self._active.is_last_frame() and not self.loop:
                self.stop()
                self._active.reset()
