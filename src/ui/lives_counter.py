from src.graphics.hud_sprites import HudSprites
from src.game_state import GameState
import pygame as pg

class LivesCounter(pg.sprite.Sprite):
    "UI element which displays the players remaining lives"
    def __init__(self, state: GameState):
        pg.sprite.Sprite.__init__(self)
        self.state: GameState = state
        self.lives: int = state.lives
        self.sprite: pg.Surface = HudSprites.hud_lives()
        self.image: pg.Surface
        self.rect: pg.Rect = pg.Rect(0, 0, 0, 0)
        self._render()

    def update(self, dt: int):
        if self.lives != self.state.lives:
            self.lives = self.state.lives
            self._render()

    def _render(self):
        width, height = self.sprite.get_size()
        image = pg.Surface((width * self.lives, height))
        for i in range(self.lives):
            image.blit(self.sprite, (16 * i, 0))
        self.image = image
