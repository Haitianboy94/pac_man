import os
import sys

from src.config.config_parser import ConfigParser, InvalidConfigError
from src.entities.maze import Maze
from src.game import Game
from src.scenes.main_menu import MainMenu

# This to solve the recursive call in the provided mazegenerator
# Python's default recursion limit is 1000,
# Your config.width = 50, height = 50 means up to 2500 cells,
# So a long winding path can easily blow past that limit.
# This is a known limitation of recursive-DFS maze generators at scale
sys.setrecursionlimit(10_000)

# Position the window on the left side of the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: uv run pac-man.py [config file]")
        sys.exit(1)

    try:
        with open(sys.argv[1]) as file:
            parser = ConfigParser(file.read())
            config = parser.parse()
    except InvalidConfigError as e:
        print(f"Config file is invalid: {e.args[0]}")
        exit(1)
    except FileNotFoundError as e:
        print(f"Config file at {e.filename} does not exist")
        exit(1)
    except Exception:
        print("Unknown exception when parsing config file")
        exit(1)

    import pygame as pg

    pg.init()

    x, y = Maze.maze_size(config.width, config.height)

    screen = pg.display.set_mode(
        (x + config.UI_BORDER_X, y + config.UI_BORDER_Y * 2), flags=pg.SCALED
    )

    pg.display.set_caption("Pac-Man")

    initial_scene = MainMenu(screen)
    game = Game(screen, initial_scene, config)

    try:
        game.loop()
    except KeyboardInterrupt:
        sys.exit()
