import pygame as pg

from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId
from src.ui.button import Button
from src.ui.text import Text


class MainMenu(Scene):
    "Main menu scene"

    def __init__(self, screen: pg.Surface):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        self.sprites: pg.sprite.Group = pg.sprite.Group()
        self._create_ui()

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self._start()

    def update(self, dt: int) -> None:
        self.sprites.update(dt)

    def draw(self, screen: pg.Surface) -> None:
        self.sprites.draw(screen)

    def _start(self) -> None:
        "Starts the game"
        self.next_scene_id = SceneId.GAME


    def _create_ui(self) -> None:
        "Sets up all ui elements for the main menu"
        center: int = int(self.screen.get_width() / 2)
        text_color = "white"
        hover_color = "yellow"

        title: Text = Text("pac man", "yellow", 3)
        title.rect.centerx = center
        title.rect.y = 50
        self.sprites.add(title)

        start_game_button: Button = Button(
            "Start game",
            text_color,
            hover_color,
            2,
            self._start
        )
        start_game_button.rect.centerx = center
        start_game_button.rect.y = 80
        self.sprites.add(start_game_button)

        highscores_button: Button = Button(
            "Highscores", text_color, hover_color, 2, lambda: None
        )
        highscores_button.rect.centerx = center
        highscores_button.rect.y = 100
        self.sprites.add(highscores_button)

        instructions_button: Button = Button(
            "Instructions", text_color, hover_color, 2, lambda: None
        )
        instructions_button.rect.centerx = center
        instructions_button.rect.y = 120
        self.sprites.add(instructions_button)

        exit_button: Button = Button(
            "Exit",
            text_color,
            hover_color,
            2,
            lambda: pg.event.post(pg.event.Event(pg.QUIT)),
        )
        exit_button.rect.centerx = center
        exit_button.rect.y = 140
        self.sprites.add(exit_button)
