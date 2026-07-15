from src.game import Game
from src.scenes.main_menu import MainMenu
from src.ui.maze import MazeCell, Maze, Dir

if __name__ == "__main__":
    import sys, pygame as pg
    pg.init()

    size = width, height = 800, 600
    speed = [2, 2]
    black = 0, 0, 0

    screen = pg.display.set_mode(size)

    pg.display.set_caption("Pac-Man")


    initial_scene = MainMenu(screen)
    game = Game(screen, initial_scene)

    try:
        game.loop()
    except KeyboardInterrupt:
        sys.exit()
