from src.scenes.scene_id import SceneId
from typing import Optional
from abc import ABC, abstractmethod
import pygame as pg

class Scene(ABC):
    def __init__(self):
        self.next_scene_id: Optional[SceneId] = None

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass
