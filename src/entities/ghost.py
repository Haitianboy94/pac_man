import pygame as pg
from collections import deque
from src.entities.entity import Entity
from src.entities.maze import Maze
from src.graphics.animation import Animation
from src.graphics.general_sprites import GeneralSprites
from src.types import Dir, GhostType
import random


class Ghost(Entity):
    """The ghost entity"""

    SIZE = 16
    FPS = 4
    MOVE_INTERVAL_MS = 500  # how often the ghost decides to move

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
        self.respawn_at: int | None = None
        self.rect = pg.Rect(0, 0, self.SIZE, self.SIZE)
        self.direction: Dir = Dir.EAST
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
        self.animation = self.move_animations[self.direction]
        self.image = self.animation.image
        self._sync_rect_to_cell()
        self.move_timer: int = random.randint(0, self.MOVE_INTERVAL_MS)
        self.player_cell: tuple[int, int]
        self.player_direction: Dir
        self.edible: bool

    def _sync_rect_to_cell(self) -> None:
        cell_x, cell_y = Maze.cell_position((self.cell_x, self.cell_y))
        offset = int((Maze.CELL_SIZE - self.SIZE) / 2)
        self.rect.topleft = (cell_x + offset, cell_y + offset)

    def is_eaten(self) -> bool:
        return self.respawn_at is not None

    def get_eaten(self, respawn_delay_ms: int) -> None:
        self.cell_x, self.cell_y = self.start_cell
        self._sync_rect_to_cell()
        self.respawn_at = pg.time.get_ticks() + respawn_delay_ms
        print(f"[{self.type.name}] eaten at {pg.time.get_ticks()}, respawn_at={self.respawn_at}")

    def update(self, dt: int) -> None:
        if self.is_eaten() and self.respawn_at is not None:
            if pg.time.get_ticks() >= self.respawn_at:
                self.respawn_at = None
            else:
                return
        self.animation.update_frame(dt)
        self.image = self.animation.image
        self.move_timer += dt
        if self.move_timer >= self.MOVE_INTERVAL_MS:
            self.move_timer = 0
            target_cell = self._get_target_cell()
            self._chase(target_cell)

    def _find_path_direction(self, target_cell: tuple[int, int]) -> Dir | None:
        """BFS from current cell to target_cell; returns the first step's direction, or None if unreachable"""
        start = (self.cell_x, self.cell_y)
        if start == target_cell:
            return None

        visited = {start}
        queue = deque([(start, None)])

        while queue:
            cell, first_dir = queue.popleft()
            for direction in (Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST):
                if not self.maze.can_move(cell, direction):
                    continue
                next_cell = self.maze.move_cell(cell, direction)
                if next_cell in visited:
                    continue
                next_first_dir = first_dir if first_dir is not None else direction
                if next_cell == target_cell:
                    return next_first_dir
                visited.add(next_cell)
                queue.append((next_cell, next_first_dir))

        return None

    def _get_target_cell(self) -> tuple[int, int]:
        if self.edible:
            width = len(self.maze.grid[0])
            height = len(self.maze.grid)
            candidates = self.maze.corners()
            return max(candidates, key=lambda c: (c[0]-self.player_cell[0])**2 + (c[1]-self.player_cell[1])**2)
        if self.type == GhostType.BLINKY:
            return self.player_cell
        elif self.type == GhostType.PINKY:
            dx, dy = self.player_direction.delta() if self.player_direction != Dir.NONE else (0, 0)
            return (self.player_cell[0] + dx * 4, self.player_cell[1] + dy * 4)
        elif self.type == GhostType.CLYDE:
            dist = (self.cell_x - self.player_cell[0]) ** 2 + (self.cell_y - self.player_cell[1]) ** 2
            if dist < 64:
                width = len(self.maze.grid[0])
                height = len(self.maze.grid)
                return (random.randint(0, width - 1), random.randint(0, height - 1))
            return self.player_cell
        else:
            return (
                self.player_cell[0] + random.randint(-3, 3),
                self.player_cell[1] + random.randint(-3, 3),
            )

    def _chase(self, target_cell: tuple[int, int]) -> None:
        direction = self._find_path_direction(target_cell)
        if direction is None:
            return
        self.cell_x, self.cell_y = self.maze.move_cell((self.cell_x, self.cell_y), direction)
        self.direction = direction
        self.animation = self.move_animations[self.direction]
        self._sync_rect_to_cell()
