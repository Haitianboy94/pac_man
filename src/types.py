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


class PacGumType(enum.IntEnum):
    """
    Enum for the different Pacgum types.
    """
    NONE = 0
    PACGUM = 1
    SUPER_PACGUM = 2


def is_nonempty_int_list(value: Any) -> TypeIs[list[int]]:
    """
    Type predicate which asserts the list[int] type.
    """
    return (
        isinstance(value, list)
        and len(value) > 0
        and all(isinstance(item, int) for item in value)
    )
