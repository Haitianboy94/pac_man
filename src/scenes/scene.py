from src.scenes.scene_id import SceneId
from typing import Optional, TYPE_CHECKING
from abc import ABC, abstractmethod
import pygame as pg

if TYPE_CHECKING:
    from src.game import Game


class Scene(ABC):
    """
    A scene is a single 'screen' in the game. It is used to separate different
    parts of the game from each other. It has its own methods for drawing
    sprites to the screen, and for handling events. The update method is
    called each frame by the `Game` class.

    self.next_scene_id can be set from within the scene, to signal the `Game`
    class to transition the scene.
    """

    def __init__(self) -> None:
        self.next_scene_id: Optional[SceneId] = None

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: int) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass
