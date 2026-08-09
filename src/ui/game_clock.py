import pygame as pg

from src.game_state import GameState
from src.ui.text import Text


class GameClock(Text):
    def __init__(self, state: GameState):
        pg.sprite.Sprite.__init__(self)
        Text.__init__(self, "", "white", 2)

        self.state: GameState = state
        self.time: int = int(state.time_remaining_ms / 1000)
        self._update_time()

    def update(self, dt) -> None:
        if self.time > 0:
            self._update_time()

    def _update_time(self) -> None:
        new_time: int = int(self.state.time_remaining_ms / 1000)
        if new_time != self.time:
            self.time = new_time
            self.set_text(str(new_time))
