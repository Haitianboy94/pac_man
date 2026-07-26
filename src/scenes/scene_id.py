import enum


class SceneId(enum.Enum):
    """
    An enum containing the ID of a scene. Used for scene transitions.
    """
    MAIN_MENU = enum.auto()
    GAME = enum.auto()
