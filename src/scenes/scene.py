from src.scenes.scene_id import SceneId
from typing import Optional
from abc import ABC, abstractmethod
import pygame as pg

class Scene(ABC):
    def __init__(self):
        # next_scene_id is polled by the game process to switch to another scene.
        self.next_scene_id: Optional[SceneId] = None
        self.quit: bool = False

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, events: list[pg.event.Event], dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass
