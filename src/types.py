from typing import TypeIs, Any
import enum


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

    def __str__(self) -> str:
        i = int(self)
        if i == 0:
            return "Dir(None)"
        if i == self.ALL:
            return "Dir(All)"
        dirs = []
        if i & self.NORTH:
            dirs.append("North")
        if i & self.EAST:
            dirs.append("East")
        if i & self.SOUTH:
            dirs.append("South")
        if i & self.WEST:
            dirs.append("West")
        return f"Dir({"|".join(dirs)})"


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
