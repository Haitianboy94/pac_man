from src.scenes.scene_id import SceneId
from src.scenes.scene import Scene
import sys
import pygame as pg

class MainMenu(Scene):
    def __init__(self, screen: pg.Surface):
        Scene.__init__(self)
        self.screen: pg.Surface = screen

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.next_scene_id = SceneId.GAME

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pg.Surface) -> None:
        self._draw_title()
        pass

    def _draw_title(self):
         font = pg.font.Font(None, 32)
         text = font.render("Pac Man", False, (100, 100, 10))
         textpos = text.get_rect(centerx=self.screen.get_width() / 2, y=10)
         self.screen.blit(text, textpos)

