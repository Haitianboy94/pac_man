from src.ui.pause_menu import PauseMenu
from src.ui.lives_counter import LivesCounter
from src.graphics.hud_sprites import HudSprites
from src.ui.points_counter import PointsCounter
from src.config.highscore import Highscore
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

    def __init__(self,
                 screen: pg.Surface,
                 config: Config,
                 highscore: Highscore,
                 state: GameState,
                 game: "Game"
                 ):
        Scene.__init__(self, game)
        self.screen: pg.Surface = screen
        self.config: Config = config
        self.highscore: Highscore = highscore
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

        self.pause_menu: PauseMenu = PauseMenu(screen, state, self._finish_level)

        self.ui_group: pg.sprite.Group = pg.sprite.Group()
        self._init_game_ui(screen)

        self.player = Player(self.maze, self.maze.center())
        corners = self.maze.corners()
        ghost_types = [GhostType.BLINKY, GhostType.PINKY, GhostType.INKY, GhostType.CLYDE]
        self.ghosts_group: pg.sprite.Group = pg.sprite.Group()
        for ghost_type, corner in zip(ghost_types, corners):
            self.ghosts_group.add(Ghost(ghost_type, self.maze, corner))
        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        self.entities_group.add(*self.ghosts_group)
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
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.is_paused = not self.is_paused
        elif event.type == pg.KEYDOWN and event.key in direction_keys:
            dir = self.player.key_to_direction(event.key)
            self.player.target_direction = dir
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for sprite in self.pause_menu.group:
                print(sprite)
                if isinstance(sprite, Button):
                    sprite.handle_event(event)

    def update(self, dt: int) -> None:
        self.ui_group.update(dt)
        if self.is_paused:
            self.pause_menu.group.update(dt)
            return

        eaten = pg.sprite.spritecollide(self.player, self.maze.pacgums, dokill=True)
        for gum in eaten:
            if gum.type == PacGumType.SUPER_PACGUM:
                self.state.points += self.config.points_per_super_pacgum
                self.edible_until = pg.time.get_ticks() + 7000
                for ghost in self.ghosts_group:
                    ghost.set_edible(True)
            else:
                self.state.points += self.config.points_per_pacgum

        if len(self.maze.pacgums) == 0:
            self._finish_level()
            return

        edible_expired = self.edible_until and pg.time.get_ticks() > self.edible_until
        if edible_expired:
            self.edible_until = None
            for ghost in self.ghosts_group:
                ghost.set_edible(False)

        edible = self.edible_until is not None and pg.time.get_ticks() < self.edible_until
        touched_ghosts = pg.sprite.spritecollide(self.player, self.ghosts_group, dokill=False)
        if touched_ghosts:
            if edible:
                for ghost in touched_ghosts:
                    if not ghost.is_eaten():
                        self.state.points += self.config.points_per_ghost
                        ghost.get_eaten(respawn_delay_ms=7000)
            else:
                self._handle_player_hit()

        self.player.update(dt)
        for ghost in self.ghosts_group:
            ghost.player_cell = self.player.cell
            ghost.player_direction = self.player.move_direction
            ghost.update(dt)

        self.maze.pacgums.update(dt)
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
            self.pause_menu.group.draw(screen)

    def _finish_level(self) -> None:
        self.game.pending_game_over = (True, self.state.points)
        self.next_scene_id = SceneId.GAME_OVER

    def _handle_player_hit(self) -> None:
        self.state.lives -= 1
        self.player.respawn(self.maze.center())
        if self.state.lives <= 0:
            self.game.pending_game_over = (False, self.state.points)
            self.next_scene_id = SceneId.GAME_OVER

    def _init_game_ui(self, screen: pg.Surface) -> None:
        "Creates the game ui"
        top_margin = 6

        # clock
        clock_title_text: Text = Text("time", 'white', 1)
        clock_title_text.rect.x = 8
        clock_title_text.rect.y = top_margin
        self.ui_group.add(clock_title_text)
        game_clock: GameClock = GameClock(self.state)
        game_clock.position = (8, top_margin + 10)
        self.ui_group.add(game_clock)

        points_title_text: Text = Text("pts", 'white', 1)
        points_title_text.rect.x = 50
        points_title_text.rect.y = top_margin
        self.ui_group.add(points_title_text)
        points_counter: PointsCounter = PointsCounter(self.state)
        points_counter.position = (50, top_margin + 10)

        self.ui_group.add(points_counter)

        # highscore
        highscore_title_text: Text = Text("high score", 'white', 1)
        highscore_title_text.rect.x = 130
        highscore_title_text.rect.y = top_margin
        self.ui_group.add(highscore_title_text)
        if not self.highscore.scores:
            highscore_points: int = 0
        else:
            highscore_points: int = self.highscore.scores[0][0]
        highscore_points_text: Text = Text(str(highscore_points), 'white', 1)
        highscore_points_text.rect.x = 130
        highscore_points_text.rect.y = top_margin + 10
        self.ui_group.add(highscore_points_text)

        # level
        level_title_text: Text = Text("lvl", 'white', 1)
        level_title_text.rect.x = 220
        level_title_text.rect.y = top_margin
        self.ui_group.add(level_title_text)
        level_points_text: Text = Text(str(self.state.current_level), 'white', 1)
        level_points_text.rect.x = 220
        level_points_text.rect.y = top_margin + 10
        self.ui_group.add(level_points_text)

        # lives
        lives_counter: LivesCounter = LivesCounter(self.state)
        lives_counter.rect.topleft = (8, screen.get_height()-24)
        self.ui_group.add(lives_counter)
