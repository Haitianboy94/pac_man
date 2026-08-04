from src.entities.entity import Entity
from src.ui.maze import Maze
import pygame as pg


class Player(Entity):
    """
    The pacman player entity
    """
    SIZE = 32

    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)

        sheet = pg.image.load("sprites/general.png")
        sheet.convert_alpha()
        sheet.get_clip()

        self.image = pg.Surface((self.SIZE, self.SIZE))
        self.rect = pg.draw.circle(
                self.image,
                pg.Color("yellow"),
                (int(self.SIZE / 2), int(self.SIZE / 2)),
                int(self.SIZE / 2)
        )
        offset = int((Maze.CELL_SIZE - self.SIZE) / 2)
        self.rect.move_ip(offset, offset)

    def update(self, events: list[pg.event.Event], dt: int) -> None:
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.rect.move_ip([0, 1])
    def draw(self):
        pass
