## Review

- **Correct:** `Dir.delta()` and `Dir.opposite()` correctly map cardinal directions (`src/types.py:20-48`). The `speed * dt / 1000` conversion also correctly interprets `dt` as milliseconds (`src/entities/player.py:75-79`).
- **Correct:** For exact cell anchors, the player’s stride and inverse conversion agree: `CELL_SIZE + WALL_SIZE == 24`, matching `Maze.cell_position()` (`src/entities/player.py:64-67`, `src/entities/maze.py:144-151`).
- **Correct:** A topological grid collision model is appropriate; sprite-vs-wall collision is unnecessary if every traversed edge is authorized correctly. `Maze.can_move()` correctly reads a cardinal wall bit from `grid[y][x]` (`src/entities/maze.py:117-122`).

### Immediate bugs

- **Blocker: NORTH/WEST movement uses the wrong cell state.**  
  `floor((position - OFFSET) / 24)` partitions space at each cell anchor (`src/entities/player.py:63-67`, `121-131`). Moving WEST from cell 1’s anchor, `x=36`, to `x=35.04` immediately yields cell 0, while moving EAST does not change cells until the next anchor is reached. Consequently, NORTH/WEST traversal does not process arrival at the actual neighboring cell and can continue through its wall until reaching another cell or even an out-of-bounds index.

- **Blocker: queued turns are evaluated at the cell being left rather than the cell being reached.**  
  When an EAST/SOUTH candidate crosses the next anchor, `self.cell_x/y` still describe the old cell. `_try_turn()` checks and snaps to that old cell (`src/entities/player.py:84-98`, `133-147`). A legal turn can therefore rewind almost an entire 24-pixel edge and turn at the wrong intersection. Conversely, a turn legal only at the destination is missed.

- **Blocker: a blocked queued turn suppresses forward-wall handling.**  
  When `target_direction` differs from the current direction, only `_try_turn()` runs. If it fails, `_maybe_stop()` is skipped because it is in the `else` branch (`src/entities/player.py:88-107`). The candidate position is then committed at lines 111-115. Thus a buffered perpendicular input can let the player depart the newly reached cell through a forward wall.

- **Blocker: large `dt` tunnels across cells and walls.**  
  Only the final projected cell is examined once (`src/entities/player.py:73-107`). A large displacement can cross several grid edges, but intermediate walls are never checked. If the final check blocks, `_maybe_stop()` snaps to that final cell anyway (`src/entities/player.py:179-191`), potentially beyond multiple walls.

- **Blocker: stopping leaves three representations inconsistent.**  
  `_maybe_stop()` changes `self.position` and direction but not `rect` or `cell_x/y` (`src/entities/player.py:188-191`). Because the commit block only runs while direction is non-`NONE` (`src/entities/player.py:111-118`) and future idle updates return early (`src/entities/player.py:59-61`), the float position, rendered/collision rectangle, and reported grid cell can remain permanently different until another input occurs.

- **Blocker: turning reuses the entire frame’s movement budget.**  
  After detecting that a candidate reached a waypoint, a successful turn resets position and reapplies `speed * dt` in full (`src/entities/player.py:91-98`). It does not subtract the distance already consumed reaching the turn. This produces rewinds, speed variation, and frame-rate-dependent behavior.

### Coordinate and grid risks

- **Note:** `Maze(position=...)` does not define one coherent coordinate space. Pacgums use `position` (`src/entities/maze.py:43-79`), while walls begin at `(0, 0)` (`src/entities/maze.py:29-40`) and `cell_position()` always uses the global `OFFSET` (`src/entities/maze.py:144-151`). This is dormant in `GameScene`, which uses the default origin, but any nonzero maze position separates walls, entities, and pickups.

- **Note:** `_sync_rect_to_cell()` applies a sprite-centering offset, but turn/stop snapping uses raw `Maze.cell_position()` (`src/entities/player.py:52-56`, `146`, `190`). The offset is currently zero because both sizes are 16, but changing player size would reintroduce misalignment.

- **Note:** There are conflicting size concepts: movement stride is 24, while `Maze.cell_size()` returns 32 (`src/entities/maze.py:171-174`). Its current pacgum placement happens to center an 8-pixel gum correctly, but the naming invites future offset/stride mistakes.

- **Note:** `Maze.can_move()` verifies only that the source is in bounds, not that the destination is (`src/entities/maze.py:117-122`). It therefore permits leaving the grid if boundary wall data is missing. Explicit portal/tunnel behavior should use a neighbor mapping rather than accidental out-of-bounds movement.

- **Note:** `Dir.delta()` silently returns `(0, 0)` for combined `IntFlag` values (`src/types.py:20-33`). Current input supplies cardinal values, but movement APIs should reject anything other than the four cardinals rather than silently freezing.

### Recommended movement model

Use a discrete **edge-progress model**, not `floor()` on arbitrary float positions:

1. Store a canonical cell waypoint and, while moving, an authorized edge:
   - `edge_start`
   - `edge_end`
   - `progress` from `0..stride`
   - `direction`
   - buffered `desired_direction`
2. Represent world position consistently, preferably by the player’s center. Derive `rect` from that float position with rounding; never derive logical cells from the integer `rect`.
3. At a cell waypoint:
   - Take the buffered direction if it is legal.
   - Otherwise continue forward if legal.
   - Otherwise stop exactly at the waypoint.
   - Keep a blocked perpendicular request buffered if Pac-Man-style early turning is desired.
4. Between waypoints, perpendicular turns wait. An opposite request reverses immediately by swapping edge endpoints and replacing `progress` with `stride - progress`; this retraces an already-authorized edge.
5. Consume `remaining_distance = speed * dt / 1000` in a loop:
   - Move at most to the current edge endpoint.
   - Commit the reached cell exactly.
   - Subtract consumed distance.
   - Select and authorize the next edge.
   - Continue until distance is exhausted or a wall stops movement.
6. Check every crossed edge, so a large `dt` behaves like many small updates. A defensive `dt` cap can still be used, but must not replace edge-by-edge collision handling.
7. Make coordinate conversion an instance responsibility, such as `maze.cell_center(cell)`, incorporating the maze origin. Either support a nonzero origin everywhere or remove the constructor’s `position` option.

Useful regression cases are all four directions from identical layouts, blocked and legal queued turns, midpoint reversals, stopping-state synchronization, and equivalence between one large update and many smaller updates up to the first wall.

No files were edited.