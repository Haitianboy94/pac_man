import pygame as pg

from src.game_state import GameState
from src.ui.text import Text


class PointsCounter(Text):
    """Represent PointsCounter state and behavior."""
    def __init__(self, state: GameState):
        """Initialize the object."""
        pg.sprite.Sprite.__init__(self)
        Text.__init__(self, "", "white", 1)

        self.state: GameState = state
        self.points: int = 0

    def update(self, dt) -> None:
        """Update the object."""
        if self.state.points != self.points:
            self.points = self.state.points
            self.set_text(str(self.state.points))
