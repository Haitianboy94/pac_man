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

        font = pg.font.Font(None, 32)
        paused = Text(font, "paused", pg.Color("white"))
        paused.set_pos((int(screen.get_width() / 2), 200))
        self.pause_group = pg.sprite.Group(paused)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.is_paused = not self.is_paused
        pass

    def update(self, events: list[pg.event.Event], dt: float) -> None:
        if self.is_paused:
            return

    def draw(self, screen: pg.Surface) -> None:
        self.maze.draw(screen)

        if self.is_paused:
            self.pause_group.draw(screen)

