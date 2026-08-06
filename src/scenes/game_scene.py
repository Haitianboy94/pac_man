from src.graphics.general_sprites import GeneralSprites
from src.scenes.scene_id import SceneId
from src.scenes.scene import Scene
from src.config.config import Config
from src.entities.player import Player
from src.entities.maze import Maze
from src.game_state import GameState
from src.maze_generator import load_maze, seed_for_level, MazeGenerationError
from src.types import Dir
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
        seed = seed_for_level(self.state.current_level, int(config.seed))
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
        gen_sprites = GeneralSprites()
        self.gen_sprites = gen_sprites

        self.maze: Maze = Maze(dir_grid, gen_sprites)
        self.is_paused: bool = False

        self.pause_group: pg.sprite.Group = pg.sprite.Group()
        self._init_pause_menu(screen)

        self.ui_group: pg.sprite.Group = pg.sprite.Group()
        clock_font: pg.font.Font = pg.font.Font(None, 32)
        game_clock: GameClock = GameClock(clock_font, pg.Color("white"), self.state)
        self.ui_group.add(game_clock)

        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        self.player: Player = Player(gen_sprites)
        self.player.rect.move_ip(self.maze.cell_position(0, 0))
        self.entities_group.add(self.player)
        self.game_screen: pg.Surface = pg.Surface(
            Maze.maze_size(self.config.width, self.config.height)
        )


    def handle_event(self, event: pg.event.Event) -> None:
        match event:
            case pg.event.Event(type=pg.KEYDOWN, key=pg.K_ESCAPE):
                self.is_paused = not self.is_paused
            case pg.event.Event(type=pg.KEYDOWN, key=pg.K_UP):
                self.player.set_direction(Dir.NORTH)
            case pg.event.Event(type=pg.KEYDOWN, key=pg.K_RIGHT):
                self.player.set_direction(Dir.EAST)
            case pg.event.Event(type=pg.KEYDOWN, key=pg.K_DOWN):
                self.player.set_direction(Dir.SOUTH)
            case pg.event.Event(type=pg.KEYDOWN, key=pg.K_LEFT):
                self.player.set_direction(Dir.WEST)

    def update(self, events: list[pg.event.Event], dt: int) -> None:
        if self.is_paused:
            self.pause_group.update(events)
            return
        self.entities_group.update(dt)
        self.ui_group.update(events)
        self.state.time_remaining_ms = self.state.time_remaining_ms - dt

    def draw(self, screen: pg.Surface) -> None:
        self.maze.draw(self.game_screen)
        self.maze.pacgums.draw(self.game_screen)
        self.entities_group.draw(self.game_screen)

        self.ui_group.draw(screen)

        screen.blit(self.game_screen, [50, 50])
        if self.is_paused:
            self.pause_group.draw(screen)

    def _init_pause_menu(self, screen: pg.Surface) -> None:
        title_font: pg.font.Font = pg.font.Font(None, 32)
        button_font: pg.font.Font = pg.font.Font(None, 24)

        border: Panel = Panel(pg.Rect(0, 0, 256, 206), pg.Color("white"))
        border.rect.centerx = int(screen.get_width() / 2)
        border.rect.y = 40
        self.pause_group.add(border)

        background: Panel = Panel(pg.Rect(0, 0, 250, 200), pg.Color("black"))
        background.rect.centerx = int(screen.get_width() / 2)
        background.rect.y = 43
        self.pause_group.add(background)

        title: Text = Text(title_font, "paused", pg.Color("white"))
        title.set_pos((int(screen.get_width() / 2), 100))
        self.pause_group.add(title)

        button: Button = Button(
                button_font,
                "Return to main menu",
                pg.Color("white"),
                pg.Color("blue"),
                lambda: setattr(self, 'next_scene_id', SceneId.MAIN_MENU)
                )
        button.set_pos((int(screen.get_width() / 2), 205))
        self.pause_group.add(button)
