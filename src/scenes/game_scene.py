from src.entities.player import Player
from src.scenes.scene_id import SceneId
from src.ui.panel import Panel
from pygame.locals import Color
from src.ui.button import Button
from src.ui.text import Text
from src.ui.maze import Maze, Dir
from src.scenes.scene import Scene
from src.maze_generator import load_maze, seed_for_level, MazeGenerationError
from src.config import Config
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
    def __init__(self, screen: pg.Surface, config: Config, current_level: int):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        seed = seed_for_level(current_level, int(config.seed))
        try:
            dir_grid, entry, exit_, shortest_path = load_maze(
                width=config.width,
                height=config.height,
                perfect=False,
                entry=(0, 0),
                exit_=(-1, -1),
                seed=seed,
            )
        except MazeGenerationError as e:
            print(f"[GameScene] Maze generation failed, using fallback maze: {e}")
            dir_grid = FALLBACK_MAZE   # small hardcoded safe grid
            entry, exit_, shortest_path = (0, 0), (0, 0), ''

        self.maze: Maze = Maze(dir_grid)
        self.is_paused: bool = False

        self.pause_group: pg.sprite.Group = pg.sprite.Group()
        self._init_pause_menu(screen)

        self.entities_group: pg.sprite.Group = pg.sprite.Group()
        player = Player()
        player.rect.move_ip(self.maze.cell_position(9, 9))
        self.entities_group.add(player)


    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.is_paused = not self.is_paused
        pass

    def update(self, events: list[pg.event.Event], dt: float) -> None:
        if self.is_paused:
            self.pause_group.update(events)
            return

    def draw(self, screen: pg.Surface) -> None:
        self.maze.walls.draw(screen)
        self.maze.pacgums.draw(screen)
        self.entities_group.draw(screen)

        if self.is_paused:
            self.pause_group.draw(screen)

    def _init_pause_menu(self, screen: pg.Surface) -> None:
        title_font: pg.font.Font = pg.font.Font(None, 64)
        button_font: pg.font.Font = pg.font.Font(None, 32)

        border: Panel = Panel(pg.Rect(0, 0, 510, 410), pg.Color("white"))
        border.rect.centerx = int(screen.get_width() / 2)
        border.rect.y = 95
        self.pause_group.add(border)

        background: Panel = Panel(pg.Rect(0, 0, 500, 400), pg.Color("black"))
        background.rect.centerx = int(screen.get_width() / 2)
        background.rect.y = 100
        self.pause_group.add(background)

        title: Text = Text(title_font, "paused", pg.Color("white"))
        title.set_pos((int(screen.get_width() / 2), 200))
        self.pause_group.add(title)

        button: Button = Button(
                button_font,
                "Return to main menu",
                Color("white"),
                Color("blue"),
                lambda: setattr(self, 'next_scene_id', SceneId.MAIN_MENU)
                )
        button.set_pos((int(screen.get_width() / 2), 410))
        self.pause_group.add(button)

