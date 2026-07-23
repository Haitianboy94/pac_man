from src.ui.text import Text
from src.ui.button import Button
from src.scenes.scene_id import SceneId
from src.scenes.scene import Scene
import sys
import pygame as pg

class MainMenu(Scene):
    def __init__(self, screen: pg.Surface):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        self.title_font: pg.font.Font = pg.font.Font(None, 64)
        self.button_font: pg.font.Font = pg.font.Font(None, 32)
        self.sprites: pg.sprite.Group = pg.sprite.Group()
        self._create_ui()


    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self, events: list[pg.event.Event], dt: float) -> None:
        self.sprites.update(events)

    def draw(self, screen: pg.Surface) -> None:
        self.sprites.draw(screen)

    def _create_ui(self):
        center: int = int(self.screen.get_width() / 2)

        title: Text = Text(self.title_font, "Pac-Man", pg.Color("white"))
        title.set_pos((center, 100))
        self.sprites.add(title)
        text_color: pg.Color = pg.Color('white')
        hover_color: pg.Color = pg.Color('blue')

        start_game_button: Button = Button(
                self.button_font,
                "Start game",
                text_color, 
                hover_color,
                lambda: setattr(self, "next_scene_id", SceneId.GAME)
                )
        start_game_button.set_pos((center, 200))
        self.sprites.add(start_game_button)

        highscores_button: Button = Button(
                self.button_font,
                "Highscores",
                pg.Color('white'), 
                pg.Color('blue'),
                lambda: None
                )
        highscores_button.set_pos((center, 250))
        self.sprites.add(highscores_button)

        instructions_button: Button = Button(
                self.button_font,
                "Instructions",
                pg.Color('white'), 
                pg.Color('blue'),
                lambda: None
                )
        instructions_button.set_pos((center, 300))
        self.sprites.add(instructions_button)

        exit_button: Button = Button(
                self.button_font,
                "Exit",
                pg.Color('white'), 
                pg.Color('blue'),
                lambda: pg.event.post(pg.event.Event(pg.QUIT))
                )
        exit_button.set_pos((center, 350))
        self.sprites.add(exit_button)

