import pygame as pg
from collections import deque
from src.entities.entity import Entity
from src.entities.maze import Maze
from src.graphics.animation import Animation
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir, GhostType
import random


class Ghost(Entity):
    """The ghost entity."""
    SIZE = 16
    FPS = 4
    CELL_DISTANCE = Maze.CELL_SIZE + Maze.WALL_SIZE
    SPEED = 45.0  # pixels per second

    def __init__(
        self,
        type: GhostType,
        maze: Maze,
        start_cell: tuple[int, int],
    ) -> None:
        Entity.__init__(self)

        self.maze: Maze = maze
        self.type: GhostType = type
        self.start_cell: tuple[int, int] = start_cell
        self.cell_x, self.cell_y = start_cell
        self.move_progress: float = 0.0
        self.respawn_at: int | None = None
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.moving: bool = True
        self.direction: Dir = Dir.EAST
        self.player_cell: tuple[int, int] = start_cell
        self.player_direction: Dir = Dir.NONE
        self.edible: bool = False
        self.move_animations: dict[Dir, Animation] = {
            Dir.NORTH: Animation(
                GeneralSprites.ghost_moving_north(type), self.FPS
            ),
            Dir.EAST: Animation(
                GeneralSprites.ghost_moving_east(type), self.FPS
            ),
            Dir.SOUTH: Animation(
                GeneralSprites.ghost_moving_south(type), self.FPS
            ),
            Dir.WEST: Animation(
                GeneralSprites.ghost_moving_west(type), self.FPS
            ),
        }
        self.scared_animation = Animation(
            GeneralSprites.ghost_scared(), self.FPS
        )
        self.image = self._get_animation().image
        self._sync_rect_to_cell()

    def set_player_state(
        self,
        player_cell: tuple[int, int],
        player_direction: Dir,
    ) -> None:
        """Update the information used by the ghost AI."""
        self.player_cell = player_cell
        self.player_direction = player_direction

    def _sync_rect_to_cell(self) -> None:
        """Synchronize the sprite position with the current cell."""
        cell_x, cell_y = Maze.cell_position((self.cell_x, self.cell_y))
        offset = int((Maze.CELL_SIZE - self.SIZE) / 2)
        dx, dy = self.direction.delta()
        pos_x = round(
            cell_x + offset + (dx * self.move_progress)
        )
        pos_y = round(
            cell_y + offset + (dy * self.move_progress)
        )
        self.rect.topleft = (pos_x, pos_y)

    def set_edible(self, edible: bool) -> None:
        self.edible = edible

    def is_eaten(self) -> bool:
        return self.respawn_at is not None

    def respawn(self) -> None:
        self.cell_x, self.cell_y = self.start_cell
        self.move_progress = 0.0
        self._sync_rect_to_cell()
        self.moving = True

    def get_eaten(self, respawn_delay_ms: int) -> None:
        self.cell_x, self.cell_y = self.start_cell
        self.move_progress = 0.0
        self._sync_rect_to_cell()
        self.respawn_at = (
            pg.time.get_ticks() + respawn_delay_ms
        )
        self.set_edible(False)

    def update(self, dt: int) -> None:
        if self.is_eaten():
            if pg.time.get_ticks() >= self.respawn_at:
                self.respawn_at = None
            else:
                return
        self._get_animation().update_frame(dt)
        self.image = self._get_animation().image

        # Convert delta time to movement distance.
        remaining = self.SPEED * dt / 1000.0

        # Process movement in cell-sized chunks. This is important:
        # whenever the ghost reaches a new cell, it immediately runs
        # pathfinding again and can turn at a junction.
        while remaining > 0 and self.moving:
            current_cell = (self.cell_x, self.cell_y)

            # Pick a direction whenever we are exactly at a cell.
            if self.move_progress == 0.0:
                target_cell = self._get_target_cell()
                self._decide_direction(target_cell)

            # If our selected direction is blocked, recalculate.
            if not self.maze.can_move(current_cell, self.direction):
                self.move_progress = 0.0
                target_cell = self._get_target_cell()
                self._decide_direction(target_cell)

                # No legal direction available.
                if not self.maze.can_move(
                    current_cell,
                    self.direction,
                ):
                    break
            distance_to_next_cell = (
                self.CELL_DISTANCE - self.move_progress
            )
            distance = min(
                remaining,
                distance_to_next_cell,
            )
            self.move_progress += distance
            remaining -= distance

            # We reached the next cell.
            if self.move_progress >= self.CELL_DISTANCE:
                self.move_progress = 0.0

                self.cell_x, self.cell_y = self.maze.move_cell(
                    current_cell,
                    self.direction,
                )

                # Immediately recalculate the path at the new cell.
                # This makes ghosts turn at intersections instead of
                # continuing straight until they hit a wall.
                target_cell = self._get_target_cell()
                self._decide_direction(target_cell)

        self._sync_rect_to_cell()

    def _decide_direction(
        self,
        target_cell: tuple[int, int],
    ) -> None:
        """Choose the next direction using BFS."""
        direction = self._find_path_direction(target_cell)

        if direction is not None:
            self.direction = direction
            self.animation = self.move_animations[self.direction]
            return

        # BFS returns None when the target is the current cell or when
        # it cannot be reached. Try a legal fallback direction.
        fallback = self._greedy_direction(target_cell)

        if fallback is not None:
            self.direction = fallback
            self.animation = self.move_animations[self.direction]

    def _greedy_direction(
        self,
        target_cell: tuple[int, int],
    ) -> Dir | None:
        """
        Fallback direction when BFS cannot provide a route.

        Prefer a non-reversing legal direction that gets closer to the
        target. Reverse only when there is no other legal option.
        """
        current_cell = (self.cell_x, self.cell_y)
        reverse = self.direction.opposite()

        best_direction: Dir | None = None
        best_distance: int | None = None

        for direction in (
            Dir.NORTH,
            Dir.EAST,
            Dir.SOUTH,
            Dir.WEST,
        ):
            if direction is reverse:
                continue

            if not self.maze.can_move(
                current_cell,
                direction,
            ):
                continue

            candidate = self.maze.move_cell(
                current_cell,
                direction,
            )

            distance = (
                (candidate[0] - target_cell[0]) ** 2
                + (candidate[1] - target_cell[1]) ** 2
            )

            if (
                best_distance is None
                or distance < best_distance
            ):
                best_direction = direction
                best_distance = distance

        if best_direction is not None:
            return best_direction

        # At a dead end, reversing is necessary.
        if self.maze.can_move(
            current_cell,
            reverse,
        ):
            return reverse

        return None

    def _get_animation(self) -> Animation:
        """Return the active animation for the ghost."""
        if self.edible:
            return self.scared_animation

        return self.move_animations[self.direction]

    def _find_path_direction(
        self,
        target_cell: tuple[int, int],
    ) -> Dir | None:
        """
        BFS from the ghost's current cell to the target.
        Returns the first direction of the shortest path.
        """
        start = (self.cell_x, self.cell_y)
        if start == target_cell:
            return None
        visited = {start}
        queue = deque([(start, None)])
        while queue:
            cell, first_direction = queue.popleft()
            for direction in (
                Dir.NORTH,
                Dir.EAST,
                Dir.SOUTH,
                Dir.WEST,
            ):
                if not self.maze.can_move(
                    cell,
                    direction,
                ):
                    continue
                next_cell = self.maze.move_cell(
                    cell,
                    direction,
                )
                if next_cell in visited:
                    continue
                next_first_direction = (
                    first_direction
                    if first_direction is not None
                    else direction
                )
                if next_cell == target_cell:
                    return next_first_direction
                visited.add(next_cell)
                queue.append(
                    (next_cell, next_first_direction)
                )
        return None

    def _get_target_cell(self) -> tuple[int, int]:
        """Return the cell the ghost should currently chase."""
        if self.edible:
            candidates = self.maze.corners()
            if not candidates:
                return self.player_cell
            return max(
                candidates,
                key=lambda c: (
                    (c[0] - self.player_cell[0]) ** 2
                    + (c[1] - self.player_cell[1]) ** 2
                ),
            )
        if self.type == GhostType.BLINKY:
            # Blinky directly targets Pac-Man.
            return self.player_cell

        elif self.type == GhostType.PINKY:
            # Target four cells ahead of Pac-Man.
            dx, dy = (
                self.player_direction.delta()
                if self.player_direction != Dir.NONE
                else (0, 0)
            )
            target = (
                self.player_cell[0] + dx * 4,
                self.player_cell[1] + dy * 4,
            )
            return self._clamp_to_grid(target)
        elif self.type == GhostType.CLYDE:
            dist = (
                (self.cell_x - self.player_cell[0]) ** 2
                + (self.cell_y - self.player_cell[1]) ** 2
            )
            if dist < 64:
                width = len(self.maze.grid[0])
                height = len(self.maze.grid)

                return (
                    random.randint(0, width - 1),
                    random.randint(0, height - 1),
                )
            return self.player_cell
        else:
            # Random/chase hybrid.
            return self._clamp_to_grid(
                (
                    self.player_cell[0] + random.randint(-3, 3),
                    self.player_cell[1] + random.randint(-3, 3),
                )
            )

    def _clamp_to_grid(
        self,
        cell: tuple[int, int],
    ) -> tuple[int, int]:
        """Keep a target cell inside the maze grid."""
        width = len(self.maze.grid[0])
        height = len(self.maze.grid)
        x = max(0, min(cell[0], width - 1))
        y = max(0, min(cell[1], height - 1))
        return (x, y)

    def refresh_image(self) -> None:
        "Update the displayed sprite without moving (used when frozen)"
        self.image = self._get_animation().image
