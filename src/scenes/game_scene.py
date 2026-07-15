from src.ui.text import Text
from src.ui.maze import Maze, Dir
from src.scenes.scene import Scene
import pygame as pg

class GameScene(Scene):
    def __init__(self, screen: pg.Surface):
        Scene.__init__(self)
        self.screen: pg.Surface = screen
        self.maze: Maze = Maze([
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
            ])
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
        self.maze.walls.draw(screen)
        self.maze.pacgums.draw(screen)

        if self.is_paused:
            self.pause_group.draw(screen)

