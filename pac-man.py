from src.ui.maze import MazeCell, Maze, Dir

if __name__ == "__main__":
    import sys, pygame as pg
    pg.init()

    size = width, height = 800, 600
    speed = [2, 2]
    black = 0, 0, 0
    clock = pg.time.Clock()

    screen = pg.display.set_mode(size)


    maze = Maze([
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

    try:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT: sys.exit()

            screen.fill(black)

            maze.draw(screen)

            # pg.display.flip()
            clock.tick(60)  # limits FPS to 60
    except KeyboardInterrupt:
        sys.exit()
