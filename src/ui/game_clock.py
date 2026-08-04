from src.game_state import GameState
from src.ui.text import Text
import pygame as pg


class GameClock(Text):
    ""
    def __init__(self, font: pg.font.Font, color: pg.Color, state: GameState):
        pg.sprite.Sprite.__init__(self)

        self.font: pg.font.Font = font
        self.color: pg.Color = color
        self.state: GameState = state

        self._update_time()

    def update(self, events: list[pg.event.Event]) -> None:
        self._update_time()


    def _update_time(self) -> None:
        text = str(int(self.state.time_remaining_ms / 1000))
        self.set_text(text)

