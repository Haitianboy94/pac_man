from src.config.highscore import Highscore
from src.ui.points_counter import PointsCounter
from src.ui.game_clock import GameClock
from src.ui.text import Text
from src.game_state import GameState
from src.ui.lives_counter import LivesCounter
import pygame as pg

class GameUI:
    def __init__(
            self,
            screen: pg.Surface,
            state: GameState,
            highscore: Highscore
    ) -> None:
        self.screen: pg.Surface = screen
        self.state: GameState = state
        self.highscore: Highscore = highscore
        self.group: pg.sprite.Group = self._init_ui()

    def _init_ui(self) -> pg.sprite.Group:
        "Creates the game ui"
        group: pg.sprite.Group = pg.sprite.Group()
        top_margin = 6

        # clock
        clock_title_text: Text = Text("time", 'white', 1)
        clock_title_text.rect.x = 8
        clock_title_text.rect.y = top_margin
        group.add(clock_title_text)
        game_clock: GameClock = GameClock(self.state)
        game_clock.position = (8, top_margin + 10)
        group.add(game_clock)

        points_title_text: Text = Text("pts", 'white', 1)
        points_title_text.rect.x = 50
        points_title_text.rect.y = top_margin
        group.add(points_title_text)
        points_counter: PointsCounter = PointsCounter(self.state)
        points_counter.position = (50, top_margin + 10)

        group.add(points_counter)

        # highscore
        highscore_title_text: Text = Text("high score", 'white', 1)
        highscore_title_text.rect.x = 130
        highscore_title_text.rect.y = top_margin
        group.add(highscore_title_text)
        if not self.highscore.scores:
            highscore_points: int = 0
        else:
            highscore_points: int = self.highscore.scores[0][0]
        highscore_points_text: Text = Text(str(highscore_points), 'white', 1)
        highscore_points_text.rect.x = 130
        highscore_points_text.rect.y = top_margin + 10
        group.add(highscore_points_text)

        # level
        level_title_text: Text = Text("lvl", 'white', 1)
        level_title_text.rect.x = 220
        level_title_text.rect.y = top_margin
        group.add(level_title_text)
        level_points_text: Text = Text(str(self.state.current_level), 'white', 1)
        level_points_text.rect.x = 220
        level_points_text.rect.y = top_margin + 10
        group.add(level_points_text)

        # lives
        lives_counter: LivesCounter = LivesCounter(self.state)
        lives_counter.rect.topleft = (8, self.screen.get_height()-24)
        group.add(lives_counter)

        return group
