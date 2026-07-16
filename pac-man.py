from src.game import Game
from src.scenes.main_menu import MainMenu
from src.ui.maze import MazeCell, Maze, Dir
from src.config import Config
import sys

# This to solve the recursive call in the provided mazegenerator
# Python's default recursion limit is 1000,
# Your config.width = 50, height = 50 means up to 2500 cells,
# So a long winding path can easily blow past that limit. 
# This is a known limitation of recursive-DFS maze generators at scale
sys.setrecursionlimit(10_000)

if __name__ == "__main__":
    import sys, pygame as pg
    pg.init()

    config = Config()
    size = width, height = config.width * Maze.CELL_SIZE, config.height * Maze.CELL_SIZE
    speed = [2, 2]
    black = 0, 0, 0

    screen = pg.display.set_mode(size)

    pg.display.set_caption("Pac-Man")

    initial_scene = MainMenu(screen)
    game = Game(screen, initial_scene, config)

    try:
        game.loop()
    except KeyboardInterrupt:
        sys.exit()
