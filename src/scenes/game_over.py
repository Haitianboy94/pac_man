from src.config.highscore import Highscore
from src.game_state import GameState
import pygame as pg

from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId
from src.ui.text import Text

MAX_NAME_LENGTH = 10


class GameOverScene(Scene):
    "Scene shown when the player wins or loses the game"

    def __init__(
            self,
            screen: pg.Surface,
            state: GameState,
            highscore: Highscore
    ):
        """Initialize the object."""
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        if state.pending_game_over is None:
            raise RuntimeError("Pending game over should be set")
        self.won: bool = state.pending_game_over
        self.score: int = state.points
        self.name: str = ""
        self.highscore: Highscore = highscore

        self.sprites: pg.sprite.Group = pg.sprite.Group()
        center = int(screen.get_width() / 2)

        title_text = "YOU WIN!" if self.won else "GAME OVER"
        self.title = Text(title_text, "yellow" if self.won else "red", 3)
        self.title.position = (center - 80, 80)
        self.title.rect.topleft = self.title.position
        self.sprites.add(self.title)

        self.score_text = Text(f"score {self.score}", "white", 2)
        self.score_text.position = (center - 60, 160)
        self.score_text.rect.topleft = self.score_text.position
        self.sprites.add(self.score_text)

        self.prompt = Text("enter your name", "white", 2)
        self.prompt.position = (center - 90, 220)
        self.prompt.rect.topleft = self.prompt.position
        self.sprites.add(self.prompt)

        self.name_text = Text(" ", "white", 2)
        self.name_text.position = (self.prompt.rect.left, self.prompt.rect.bottom + 20)
        self.name_text.rect.topleft = self.name_text.position
        self.sprites.add(self.name_text)

    def handle_event(self, event: pg.event.Event) -> None:
        """Handle handle event."""
        if event.type != pg.KEYDOWN:
            return
        if event.key == pg.K_RETURN:
            self._submit()
        elif event.key == pg.K_BACKSPACE:
            self.name = self.name[:-1]
            self._update_name_display()
        elif len(self.name) < MAX_NAME_LENGTH:
            char = event.unicode
            if char.isalnum() or char == " ":
                self.name += char
                self._update_name_display()

    def _update_name_display(self) -> None:
        """Perform the update name display operation."""
        self.name_text.set_text(self.name if self.name else " ")

    def _submit(self) -> None:
        """Perform the submit operation."""
        name = self.name.strip()
        if len(name) == 0:
            return
        self.highscore.add(name, self.score)
        self.highscore.store()
        self.next_scene_id = SceneId.MAIN_MENU

    def update(self, dt: int) -> None:
        """Update the object."""
        self.sprites.update(dt)

    def draw(self, screen: pg.Surface) -> None:
        """Draw the object."""
        screen.fill("black")
        self.sprites.draw(screen)