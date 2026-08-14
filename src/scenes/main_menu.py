from src.config.config import Config
from src.config.highscore import Highscore
from enum import Enum
import pygame as pg

from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId
from src.ui.button import Button
from src.ui.text import Text


class MainMenu(Scene):
    "Main menu scene"

    def __init__(self, screen: pg.Surface, game: "Game"):
        Scene.__init__(self, game)
        self.screen: pg.Surface = screen
        self.config: Config = game.config
        self.highscore: Highscore = game.highscore
        self.main_group: pg.sprite.Group = pg.sprite.Group()
        self.highscores_group: pg.sprite.Group = pg.sprite.Group()
        self.instructions_group: pg.sprite.Group = pg.sprite.Group()
        self.active_group: pg.sprite.Group = self.main_group
        self._init_main()
        self._init_highscores()
        self._init_instructions()

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self._start()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for sprite in self.active_group:
                if isinstance(sprite, Button):
                    sprite.handle_event(event)

    def update(self, dt: int) -> None:
        self.active_group.update(dt)

    def draw(self, screen: pg.Surface) -> None:
        self.active_group.draw(screen)

    def _start(self) -> None:
        "Starts the game"
        self.next_scene_id = SceneId.GAME


    def _init_main(self) -> None:
        "Sets up all ui elements for the main menu"
        center: int = int(self.screen.get_width() / 2)
        text_color = "white"
        hover_color = "yellow"

        title: Text = Text("pac man", "yellow", 3)
        title.rect.centerx = center
        title.rect.y = 50
        self.main_group.add(title)

        start_game_button: Button = Button(
            "Start game",
            text_color,
            hover_color,
            2,
            self._start
        )
        start_game_button.rect.centerx = center
        start_game_button.rect.y = 80
        self.main_group.add(start_game_button)

        highscores_button: Button = Button(
            "Highscores",
            text_color,
            hover_color,
            2,
            lambda: setattr(self, 'active_group', self.highscores_group)
        )
        highscores_button.rect.centerx = center
        highscores_button.rect.y = 100
        self.main_group.add(highscores_button)

        instructions_button: Button = Button(
            "Instructions",
            text_color,
            hover_color,
            2,
            lambda: setattr(self, 'active_group', self.instructions_group)
        )
        instructions_button.rect.centerx = center
        instructions_button.rect.y = 120
        self.main_group.add(instructions_button)

        exit_button: Button = Button(
            "Exit",
            text_color,
            hover_color,
            2,
            lambda: pg.event.post(pg.event.Event(pg.QUIT)),
        )
        exit_button.rect.centerx = center
        exit_button.rect.y = 140
        self.main_group.add(exit_button)

    def _init_highscores(self) -> None:
        center: int = int(self.screen.get_width() / 2)
        title: Text = Text("highscores", "yellow", 2)
        title.rect.centerx = center
        title.rect.y = 50
        self.highscores_group.add(title)

        y = 74
        for score, name in self.highscore.get():
            name: Text = Text(name, "white")
            name.rect.x = center - 76
            name.rect.y = y
            self.highscores_group.add(name)

            score: Text = Text(str(score), "white")
            score.rect.x = center + 30
            score.rect.y = y
            self.highscores_group.add(score)
            y += 12

        back_button: Button = Button(
            "back",
            "white",
            "yellow",
            2,
            lambda: setattr(self, 'active_group', self.main_group)
        )
        y += 32
        back_button.rect.centerx = center
        back_button.rect.y = y
        self.highscores_group.add(back_button)

    def _init_instructions(self) -> None:
        """Set up the controls and game-rules overview."""
        center: int = self.screen.get_width() // 2

        def add_centered(
            label: str,
            y: int,
            color: str = "white",
            scale: int = 1,
        ) -> None:
            text = Text(label, color, scale)
            text.rect.centerx = center
            text.rect.y = y
            self.instructions_group.add(text)

        add_centered("instructions", 24, "yellow", 2)

        add_centered("how to play", 54, "cyan")
        add_centered("eat pacgums and avoid ghosts", 68)
        add_centered("getting caught costs one life", 80)
        add_centered(f"you start with {self.config.lives} lives", 92)
        add_centered("power pacgums turn ghosts blue", 104)
        add_centered("eat blue ghosts for bonus points", 116)
        add_centered("power lasts 7 seconds", 128, "cyan")

        add_centered("scoring", 150, "yellow")
        add_centered(
            f"pacgum {self.config.points_per_pacgum} points",
            164,
        )
        add_centered(
            f"power pacgum {self.config.points_per_super_pacgum} points",
            176,
        )
        add_centered(
            f"blue ghost {self.config.points_per_ghost} points",
            188,
        )

        add_centered("controls", 210, "yellow")
        add_centered("move with wasd or arrow keys", 224)
        add_centered("pause and resume with esc", 236)

        back_button = Button(
            "back",
            "white",
            "yellow",
            2,
            lambda: setattr(self, 'active_group', self.main_group)
        )
        back_button.rect.centerx = center
        back_button.rect.y = 258
        self.instructions_group.add(back_button)
