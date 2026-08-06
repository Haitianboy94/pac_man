from src.graphics.text_sprites import TextSprites
from src.ui.text import Text
from src.game_state import GameState
import pygame as pg


class GameClock(Text):
    def __init__(self, text_sprites: TextSprites, state: GameState):
        pg.sprite.Sprite.__init__(self)
        Text.__init__(self, text_sprites, "", 'white', 1)

        self.state: GameState = state
        self._update_time()

    def update(self, events: list[pg.event.Event]) -> None:
        self._update_time()

    def _update_time(self) -> None:
        text = str(int(self.state.time_remaining_ms / 1000))
        self.set_text(text)
