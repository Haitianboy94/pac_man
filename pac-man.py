import os
import sys

from src.config.config_parser import ConfigParser, InvalidConfigError
from src.entities.maze import Maze
from src.game import Game
from src.resources import resource_path

sys.setrecursionlimit(10_000)

os.environ["SDL_VIDEO_WINDOW_POS"] = "50,50"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("usage: pac-man [config file]")
        sys.exit(1)

    config_path = (
        sys.argv[1] if len(sys.argv) == 2 else resource_path("config.json")
    )

    try:
        with open(config_path) as file:
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
    pg.mixer.init()

    screen = pg.display.set_mode(
        (x + config.UI_BORDER_X, y + config.UI_BORDER_Y * 2), flags=pg.SCALED
    )

    pg.display.set_caption("Pac-Man")

    game = Game(screen, config)

    try:
        game.loop()
    except KeyboardInterrupt:
        sys.exit()
