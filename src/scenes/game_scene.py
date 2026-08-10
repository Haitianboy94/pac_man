from src.graphics.general_sprites import GeneralSprites
import pygame as pg

from src.config.config import Config
from src.entities.ghost import Ghost
from src.entities.maze import Maze
from src.entities.player import Player
from src.game_state import GameState
from src.maze_generator import MazeGenerationError, load_maze, seed_for_level
from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId
from src.types import Dir, GhostType, PacGumType
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
        self.edible_until: int | None = None
        # self.score: int = 0
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

        self.player = Player(self.maze, self.maze.center())
        # self.ghosts_group.add(Ghost(GhostType.BLINKY, self.maze, (5, 5)))
        # self.ghosts_group.add(Ghost(GhostType.PINKY, self.maze, (4, 5)))
        # self.ghosts_group.add(Ghost(GhostType.INKY, self.maze, (5, 4)))
        # self.ghosts_group.add(Ghost(GhostType.CLYDE, self.maze, (4, 4)))
        corners = self.maze.corners()
        ghost_types = [GhostType.BLINKY, GhostType.PINKY, GhostType.INKY, GhostType.CLYDE]
        self.ghosts_group: pg.sprite.Group = pg.sprite.Group()
        for ghost_type, corner in zip(ghost_types, corners):
            self.ghosts_group.add(Ghost(ghost_type, self.maze, corner))
        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        self.entities_group.add(self.player)
        self.entities_group.add(*self.ghosts_group)
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
            self.player.target_direction = dir

    def update(self, dt: int) -> None:
        if self.is_paused:
            self.pause_group.update(dt)
            return

        eaten = pg.sprite.spritecollide(self.player, self.maze.pacgums, dokill=True)
        for gum in eaten:
            if gum.type == PacGumType.SUPER_PACGUM:
                self.state.points += self.config.points_per_super_pacgum
                self.edible_until = pg.time.get_ticks() + 8000
            else:
                self.state.points += self.config.points_per_pacgum

        edible = self.edible_until is not None and pg.time.get_ticks() < self.edible_until
        touched_ghosts = pg.sprite.spritecollide(self.player, self.ghosts_group, dokill=False)
        if touched_ghosts and not edible:
            self._handle_player_hit()
        # TODO 4.7/4.8: handle `touched_ghosts and edible` case separately

        target_cell = (self.player.cell_x, self.player.cell_y)
        self.player.update(dt)
        for ghost in self.ghosts_group:
            ghost.update(dt, target_cell)

        self.maze.pacgums.update(dt)
        self.ui_group.update(dt)
        self.state.time_remaining_ms = self.state.time_remaining_ms - dt

    def _handle_player_hit(self) -> None:
        self.state.lives -= 1
        # TODO: respawn player at center — need a method on Player for this
        # TODO: what happens when self.state.lives reaches 0? (4.10's territory)

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