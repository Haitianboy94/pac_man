from src.graphics.text_sprites import TextSprites
from src.ui.text import Text
from src.ui.button import Button
from src.scenes.scene_id import SceneId
from src.scenes.scene import Scene
import pygame as pg


class MainMenu(Scene):
    "Main menu scene"

    def __init__(self, screen: pg.Surface):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        self.sprites: pg.sprite.Group = pg.sprite.Group()
        self.text_sprites: TextSprites = TextSprites()
        self._create_ui()

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self, events: list[pg.event.Event], dt: int) -> None:
        self.sprites.update(events)

    def draw(self, screen: pg.Surface) -> None:
        self.sprites.draw(screen)

    def _create_ui(self) -> None:
        "Sets up all ui elements for the main menu"
        center: int = int(self.screen.get_width() / 2)

        title: Text = Text(self.text_sprites, "pac man", 'yellow', 3)
        title.set_pos((center, 50))
        self.sprites.add(title)
        text_color = 'white'
        hover_color = 'yellow'

        start_game_button: Button = Button(
                self.text_sprites,
                "Start game",
                text_color,
                hover_color,
                2,
                lambda: setattr(self, "next_scene_id", SceneId.GAME)
                )
        start_game_button.set_pos((center, 80))
        self.sprites.add(start_game_button)
        print(start_game_button.rect)
        
        highscores_button: Button = Button(
                self.text_sprites,
                "Highscores",
                text_color,
                hover_color,
                2,
                lambda: None
                )
        highscores_button.set_pos((center, 100))
        self.sprites.add(highscores_button)

        instructions_button: Button = Button(
                self.text_sprites,
                "Instructions",
                text_color,
                hover_color,
                2,
                lambda: None
                )
        instructions_button.set_pos((center, 120))
        self.sprites.add(instructions_button)

        exit_button: Button = Button(
                self.text_sprites,
                "Exit",
                text_color,
                hover_color,
                2,
                lambda: pg.event.post(pg.event.Event(pg.QUIT))
                )
        exit_button.set_pos((center, 140))
        self.sprites.add(exit_button)
