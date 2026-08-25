from src.sounds import Sounds
import pygame as pg

from src.config.config import Config
from src.config.highscore import Highscore
from src.entities.ghost import Ghost
from src.entities.maze import Maze
from src.entities.player import Player
from src.game_state import GameState
from src.graphics.general_sprites import GeneralSprites
from src.graphics.hud_sprites import HudSprites
from src.maze_generator import MazeGenerationError, load_maze, seed_for_level
from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId
from src.types import Dir, GhostType, PacGumType
from src.ui.button import Button
from src.ui.game_clock import GameClock
from src.ui.game_ui import GameUI
from src.ui.lives_counter import LivesCounter
from src.ui.panel import Panel
from src.ui.pause_menu import PauseMenu
from src.ui.points_counter import PointsCounter
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
    DEATH_PAUSE: int = 1000
    DEATH_ANIM: int = 2000
    START_PAUSE: int = 4000
    """
    The game scene where pacman actually takes place.
    Calls `MazeGenerator` to create the level.
    """

    def __init__(self,
                 screen: pg.Surface,
                 config: Config,
                 highscore: Highscore,
                 state: GameState,
                 ):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        self.config: Config = config
        self.highscore: Highscore = highscore
        self.state: GameState = state
        self.edible_until: int | None = None

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
        self.show_pause_menu: bool = False

        self.pause_menu: PauseMenu = PauseMenu(
            screen,
            state,
            self._finish_level,
            self._to_main_menu
        )
        self.game_ui: GameUI = GameUI(screen, state, highscore)

        self.player = Player(self.maze, self.maze.center())
        self.start_pause_until: int | None = None
        self.death_pause_until: int | None = None
        self.death_anim_until: int | None = None
        self.corners: list[tuple[int, int]] = self.maze.corners()
        ghost_types = [GhostType.BLINKY, GhostType.PINKY, GhostType.INKY, GhostType.CLYDE]
        self.ghosts_group: pg.sprite.Group = pg.sprite.Group()
        for ghost_type, corner in zip(ghost_types, self.corners):
            self.ghosts_group.add(Ghost(ghost_type, self.maze, corner))
        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        self.entities_group.add(*self.ghosts_group)
        self.entities_group.add(self.player)
        self.game_screen: pg.Surface = pg.Surface(
            Maze.maze_size(self.config.width, self.config.height)
        )

    def handle_event(self, event: pg.event.Event) -> None:
        if self.death_pause_until or self.death_anim_until:
            return
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
            self.show_pause_menu = not self.show_pause_menu
        elif event.type == pg.KEYDOWN and event.key == pg.K_k:
            self._handle_player_hit()
        elif event.type == pg.KEYDOWN and event.key in direction_keys:
            dir = self.player.key_to_direction(event.key)
            self.player.target_direction = dir
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for sprite in self.pause_menu.group:
                if isinstance(sprite, Button):
                    sprite.handle_event(event)

    def update(self, dt: int) -> None:
        self.game_ui.group.update(dt)

        time: int = pg.time.get_ticks()
        if self.start_pause_until is None:
            Sounds.start().play()
            self.start_pause_until = time + self.START_PAUSE
        if time < self.start_pause_until:
            return
        if self.death_pause_until:
            if time > self.death_pause_until:
                self._start_death_anim()
                self.death_pause_until = None
        if self.death_anim_until:
            if time > self.death_anim_until:
                self._respawn_or_end()
                self.death_anim_until = None
                return
        if self.show_pause_menu:
            self.pause_menu.group.update(dt)
            return

        eaten = pg.sprite.spritecollide(self.player, self.maze.pacgums, dokill=True)
        for gum in eaten:
            Sounds.eat_gum().play()
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
        if self.state.time_remaining_ms <= 0:
            self._handle_player_hit()

    def draw(self, screen: pg.Surface) -> None:
        self.game_screen.fill("black")
        self.maze.draw(self.game_screen)
        self.maze.pacgums.draw(self.game_screen)
        self.entities_group.draw(self.game_screen)

        self.game_ui.group.draw(screen)

        screen.blit(
            self.game_screen,
            [self.config.UI_BORDER_X, self.config.UI_BORDER_Y],
        )
        if self.show_pause_menu:
            self.pause_menu.group.draw(screen)

    def _finish_level(self) -> None:
        self.state.current_level += 1
        if self.state.current_level > self.state.total_levels:
            self.state.pending_game_over = True
            self.next_scene_id = SceneId.GAME_OVER
        else:
            self.state.time_remaining_ms = self.config.level_max_time * 1000
            self.next_scene_id = SceneId.GAME

    def _to_main_menu(self) -> None:
        self.next_scene_id = SceneId.MAIN_MENU

    def _handle_player_hit(self) -> None:
        if not self.death_pause_until and not self.death_anim_until:
            self.death_pause_until = pg.time.get_ticks() + self.DEATH_PAUSE
            self.player.moving = False
            self.player.animations.stop()
            for ghost in self.ghosts_group:
                ghost.moving = False

    def _start_death_anim(self) -> None:
        self.death_anim_until = pg.time.get_ticks() + self.DEATH_ANIM
        self.player.die()

    def _respawn_or_end(self) -> None:
        self.state.lives -= 1
        self.state.time_remaining_ms = self.config.level_max_time * 1000
        self.player.respawn(self.maze.center())
        for ghost in self.ghosts_group:
            ghost.respawn()
        if self.state.lives <= 0:
            self.state.pending_game_over = False
            self.next_scene_id = SceneId.GAME_OVER


