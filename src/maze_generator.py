from mazegenerator.mazegenerator import MazeGenerator
from src.ui.maze import Dir


class MazeGenerationError(Exception):
    """Raised when a maze cannot be generated."""
    pass


def load_maze(width, height, perfect, entry, exit_, seed, max_retries=3):
    last_error = None
    for attempt in range(max_retries):
        try:
            generator = MazeGenerator(size=(width, height), perfect=perfect,
                                      entry_cell=entry, exit_cell=exit_,
                                      seed=seed if attempt == 0 else 0
                                      )

        except Exception as e:
            last_error = e
            continue

        if generator.shortest_path is False:
            last_error = RuntimeError("no path found")
            continue

        dir_grid = [[Dir(cell) for cell in row] for row in generator.maze]
        return dir_grid, generator.maze_entry, generator.maze_exit, generator.shortest_path

    print(f"Maze generation failed after {max_retries} attempts: {last_error}")

    raise MazeGenerationError(
        f"Failed after {max_retries} attempts: {last_error}"
    )


def seed_for_level(level: int, base_seed: int) -> int:
    if level == 1:
        return base_seed
    return 0
