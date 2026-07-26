from abc import ABC, abstractmethod
import pygame as pg


class Entity(ABC, pg.sprite.Sprite):
    """
    An entity is a sprite which also contains its own behaviour.
    Use self.image and self.rect to set up the sprite and position.
    """

    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image: pg.Surface
        self.rect: pg.Rect

    @abstractmethod
    def update(self, events: list[pg.event.Event], dt: int) -> None:
        """
        This method is called every frame on all entities in the active scene.
        Use this method to implement the game logic for the entity.

        events: List of events which occurred in the last frame.
        dt: The amount of milliseconds since the last frame was rendered.
        """
