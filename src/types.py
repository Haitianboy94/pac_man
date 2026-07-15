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
    NONE = 0
    PACGUM = 1
    SUPER_PACGUM = 2
