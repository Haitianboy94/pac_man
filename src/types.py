import enum
from typing import Any, TypeIs


class Dir(enum.IntFlag):
    """Wall directions using bit flags for efficient set operations.

    IntFlag allows bitwise operations (|, &, ~) to combine/remove walls
    in a single cell. Power-of-2 values enable representing any wall
    combination (0-15) as a single integer for compact storage.
    """

    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = 15

    def delta(self) -> tuple[int, int]:
        """
        Returns a unit difference on x-y coordinates for the direction.
        Only supports cardinal directions
        """
        if self == Dir.NORTH:
            return (0, -1)
        if self == Dir.EAST:
            return (1, 0)
        if self == Dir.SOUTH:
            return (0, 1)
        if self == Dir.WEST:
            return (-1, 0)
        return (0, 0)

    def opposite(self) -> "Dir":
        """
        Returns the opposite direction.
        Only supports cardinal directions.
        """
        if self == Dir.NORTH:
            return Dir.SOUTH
        if self == Dir.EAST:
            return Dir.WEST
        if self == Dir.SOUTH:
            return Dir.NORTH
        if self == Dir.WEST:
            return Dir.EAST
        return Dir.NONE

    def __str__(self) -> str:
        """Return the object as a string."""
        if self is Dir.NONE:
            return "Dir(None)"
        if self is self.ALL:
            return "Dir(All)"
        dirs = []
        if self & self.NORTH:
            dirs.append("North")
        if self & self.EAST:
            dirs.append("East")
        if self & self.SOUTH:
            dirs.append("South")
        if self & self.WEST:
            dirs.append("West")
        return f"Dir({'|'.join(dirs)})"


class PacGumType(enum.IntEnum):
    "Enum for the different Pacgum types"

    NONE = 0
    PACGUM = 1
    SUPER_PACGUM = 2


class GhostType(enum.IntEnum):
    "Enum for the different ghost types"

    BLINKY = 1
    PINKY = 2
    INKY = 3
    CLYDE = 4


def is_nonempty_int_list(value: Any) -> TypeIs[list[int]]:
    """
    Type predicate which asserts the list[int] type.
    """
    return (
        isinstance(value, list)
        and len(value) > 0
        and all(isinstance(item, int) for item in value)
    )
