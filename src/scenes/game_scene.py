import pygame as pg

from src.config.config import Config
from src.entities.ghost import Ghost
from src.entities.maze import Maze
from src.entities.player import Player
from src.game_state import GameState
from src.maze_generator import MazeGenerationError, load_maze, seed_for_level
from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId
from src.types import Dir, GhostType
from src.ui.button import Button
from src.ui.game_clock import GameClock
from src.ui.panel import Panel
from src.ui.text import Text

FALLBACK_MAZE: list[list[Dir]] = [
    [
        Dir.NORTH | Dir.EAST | Dir.SOUTH,
        Dir.NORTH | Dir.WEST,
        Dir.NORTH | Dir.EAST | Dir.WEST,
    ],
    [
        Dir.NORTH | Dir.EAST | Dir.SOUTH,
        Dir.NORTH | Dir.WEST,
        Dir.NORTH | Dir.EAST | Dir.WEST,
    ],
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
                "[GameScene] Maze generation failed"
                + f", using fallback maze: {e}"
            )
            dir_grid = FALLBACK_MAZE  # small hardcoded safe grid

        self.maze: Maze = Maze(dir_grid)
        self.is_paused: bool = False

        self.pause_group: pg.sprite.Group = pg.sprite.Group()
        self._init_pause_menu(screen)

        self.ui_group: pg.sprite.Group = pg.sprite.Group()
        game_clock: GameClock = GameClock(self.state)
        game_clock.position = (16, 8)
        self.ui_group.add(game_clock)

        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        self.player: Player = Player(self.maze, (0, 0))
        self.ghosts: list[Ghost] = [
            Ghost(GhostType.BLINKY, self.maze, (5, 5)),
            Ghost(GhostType.PINKY, self.maze, (4, 5)),
            Ghost(GhostType.INKY, self.maze, (5, 4)),
            Ghost(GhostType.CLYDE, self.maze, (4, 4)),
        ]
        self.entities_group.add(self.player)
        self.entities_group.add(self.ghosts)
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

    def update(self, dt: int) -> None:
        if self.is_paused:
            self.pause_group.update(dt)
            return
        eaten = pg.sprite.spritecollide(
            self.player, self.maze.pacgums, dokill=True
        )
        self.state.points += len(eaten) * self.config.points_per_pacgum
        self.entities_group.update(dt)
        self.maze.pacgums.update(dt)
        self.ui_group.update(dt)
        self.state.time_remaining_ms = self.state.time_remaining_ms - dt

    def draw(self, screen: pg.Surface) -> None:
        self.game_screen.fill("black")
        self.maze.draw(self.game_screen)
        self.maze.pacgums.draw(self.game_screen)
        self.entities_group.draw(self.game_screen)

        self.ui_group.draw(screen)

        screen.blit(
            self.game_screen,
            [self.config.UI_BORDER_X, self.config.UI_BORDER_Y],
        )
        if self.is_paused:
            self.pause_group.draw(screen)

    def _init_pause_menu(self, screen: pg.Surface) -> None:
        center: int = int(screen.get_width() / 2)
        border: Panel = Panel(pg.Rect(0, 0, 256, 206), pg.Color("white"))
        border.rect.centerx = center
        border.rect.y = 40
        self.pause_group.add(border)

        background: Panel = Panel(pg.Rect(0, 0, 250, 200), pg.Color("black"))
        background.rect.centerx = center
        background.rect.y = 43
        self.pause_group.add(background)

        title: Text = Text("paused", "white", 2)
        title.rect.centerx = center
        title.rect.y = 100
        self.pause_group.add(title)

        button: Button = Button(
            "main menu",
            "white",
            "yellow",
            2,
            lambda: setattr(self, "next_scene_id", SceneId.MAIN_MENU),
        )
        button.rect.centerx = center
        button.rect.y = 205
        self.pause_group.add(button)
