from src.graphics.text_sprites import TextSprites
from src.graphics.hud_sprites import HudSprites
from src.game_state import GameState
import pygame as pg

class LivesCounter(pg.sprite.Sprite):
    "UI element which displays the players remaining lives"
    def __init__(self, state: GameState):
        """Initialize the object."""
        pg.sprite.Sprite.__init__(self)
        self.state: GameState = state
        self.lives: int = state.lives
        self.sprite: pg.Surface = HudSprites.hud_lives()
        self.image: pg.Surface = pg.Surface((0, 0))
        self.rect: pg.Rect = pg.Rect(0, 0, 0, 0)
        self._render()

    def update(self, dt: int):
        """Update the object."""
        if self.lives != self.state.lives:
            self.lives = self.state.lives
            self._render()

    def _render(self):
        """Perform the render operation."""
        if self.lives < 0:
            return
        width, height = self.sprite.get_size()
        if self.lives <=5 :
            image = pg.Surface((width * self.lives, height))
            for i in range(self.lives):
                image.blit(self.sprite, (16 * i, 0))
            self.image = image
        else:
            text = TextSprites.render(str(self.lives))
            text_width: int = text.get_rect().width
            image = pg.Surface((width + text_width, height))
            image.blit(text, (0, 4))
            image.blit(self.sprite, (text_width, 0))
            self.image = image


