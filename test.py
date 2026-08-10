from mazegenerator.mazegenerator import MazeGenerator

from src.maze_generator import MazeGenerationError, load_maze

# test mazegenerator provided
g = MazeGenerator(
    size=(4, 4), perfect=False, entry_cell=(0, 0), exit_cell=(3, 3), seed=1
)
print(g.maze)
print(g.shortest_path)
print(g.maze_entry, g.maze_exit)

print("=" * 80)
# test my maze_generator
dir_grid, entry, exit_, shortest_path = load_maze(
    width=6, height=6, perfect=False, entry=(0, 0), exit_=(-1, -1), seed=1
)
print(len(dir_grid), len(dir_grid[0]))
print(type(dir_grid[0][0]))
print(entry, exit_, shortest_path)

print("=" * 80)
# test error handling
try:
    load_maze(0, 0, perfect=False, entry=(0, 0), exit_=(-1, -1), seed=1)
except MazeGenerationError as e:
    print("Caught cleanly:", e)
print("=" * 10)
