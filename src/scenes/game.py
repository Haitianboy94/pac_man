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

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self, events: list[pg.event.Event], dt: float) -> None:
        pass

    def draw(self, screen: pg.Surface) -> None:
        self.maze.draw(screen)
