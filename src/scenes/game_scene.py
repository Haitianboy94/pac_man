from src.entities.ghost import Ghost
from src.graphics.text_sprites import TextSprites
from src.graphics.general_sprites import GeneralSprites
from src.scenes.scene_id import SceneId
from src.scenes.scene import Scene
from src.config.config import Config
from src.entities.player import Player
from src.entities.maze import Maze
from src.game_state import GameState
from src.maze_generator import load_maze, seed_for_level, MazeGenerationError
from src.types import Dir, GhostType
from src.ui.button import Button
from src.ui.panel import Panel
from src.ui.text import Text
from src.ui.game_clock import GameClock
import pygame as pg

FALLBACK_MAZE: list[list[Dir]] = [
            [
                Dir.NORTH | Dir.EAST | Dir.SOUTH,
                Dir.NORTH | Dir.WEST,
                Dir.NORTH | Dir.EAST | Dir.WEST
                ],
            [
                Dir.NORTH | Dir.EAST | Dir.SOUTH,
                Dir.NORTH | Dir.WEST,
                Dir.NORTH | Dir.EAST | Dir.WEST
                ]
            ]


class GameScene(Scene):
    """
    The game scene where pacman actually takes place.
    Calls `MazeGenerator` to create the level.
    """
    def __init__(self, screen: pg.Surface, config: Config, state: GameState):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        self.config: Config = config
        self.state: GameState = state
        seed = seed_for_level(state.current_level, config.seed)
        try:
            dir_grid, _, _, _ = load_maze(
                width=config.width,
                height=config.height,
                perfect=False,
                entry=(0, 0),
                exit_=(-1, -1),
                seed=seed,
            )
        except MazeGenerationError as e:
            print(
                    "[GameScene] Maze generation failed" +
                    f", using fallback maze: {e}"
                    )
            dir_grid = FALLBACK_MAZE   # small hardcoded safe grid

        self.maze: Maze = Maze(dir_grid)
        self.is_paused: bool = False

        self.pause_group: pg.sprite.Group = pg.sprite.Group()
        self._init_pause_menu(screen)

        self.ui_group: pg.sprite.Group = pg.sprite.Group()
        game_clock: GameClock = GameClock(self.state)
        game_clock.position = (16, 8)
        self.ui_group.add(game_clock)

        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        self.player = Player(self.maze, (0, 0))
        self.entities_group.add(Ghost(GhostType.BLINKY, self.maze, (5, 5)))
        self.entities_group.add(Ghost(GhostType.PINKY, self.maze, (4, 5)))
        self.entities_group.add(Ghost(GhostType.INKY, self.maze, (5, 4)))
        self.entities_group.add(Ghost(GhostType.CLYDE, self.maze, (4, 4)))
        self.entities_group.add(self.player)
        self.game_screen: pg.Surface = pg.Surface(
            Maze.maze_size(self.config.width, self.config.height)
        )

    def handle_event(self, event: pg.event.Event) -> None:
        direction_keys = [
            pg.K_UP,
            pg.K_DOWN,
            pg.K_LEFT,
            pg.K_RIGHT,
            pg.K_w,
            pg.K_s,
            pg.K_a,
            pg.K_d,
        ]
        if event.type != pg.KEYDOWN:
            return
        if event.key == pg.K_ESCAPE:
            self.is_paused = not self.is_paused
        elif event.key in direction_keys:
            dir = self.player.key_to_direction(event.key)
            self.player.try_move(dir)

    def update(self, events: list[pg.event.Event], dt: int) -> None:
        if self.is_paused:
            self.pause_group.update(events)
            return
        eaten = pg.sprite.spritecollide(self.player, self.maze.pacgums, dokill=True)
        self.state.points += len(eaten) * self.config.points_per_pacgum
        self.entities_group.update(dt)
        self.ui_group.update(events)
        self.state.time_remaining_ms = self.state.time_remaining_ms - dt

    def draw(self, screen: pg.Surface) -> None:
        self.game_screen.fill('black')
        self.maze.draw(self.game_screen)
        self.maze.pacgums.draw(self.game_screen)
        self.entities_group.draw(self.game_screen)

        self.ui_group.draw(screen)

        screen.blit(
            self.game_screen,
            [self.config.UI_BORDER_X, self.config.UI_BORDER_Y]
        )
        if self.is_paused:
            self.pause_group.draw(screen)

    def _init_pause_menu(self, screen: pg.Surface) -> None:
        border: Panel = Panel(pg.Rect(0, 0, 256, 206), pg.Color("white"))
        border.rect.centerx = int(screen.get_width() / 2)
        border.rect.y = 40
        self.pause_group.add(border)

        background: Panel = Panel(pg.Rect(0, 0, 250, 200), pg.Color("black"))
        background.rect.centerx = int(screen.get_width() / 2)
        background.rect.y = 43
        self.pause_group.add(background)

        title: Text = Text("paused", 'white', 2)
        title.set_pos((int(screen.get_width() / 2), 100))
        self.pause_group.add(title)

        button: Button = Button(
                "main menu",
                'white',
                'yellow',
                2,
                lambda: setattr(self, 'next_scene_id', SceneId.MAIN_MENU)
                )
        button.set_pos((int(screen.get_width() / 2), 205))
        self.pause_group.add(button)
