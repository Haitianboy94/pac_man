from src.scenes.game_scene import GameScene
from src.scenes.main_menu import MainMenu
from src.scenes.scene_id import SceneId
from src.config.config import Config
import sys
from src.scenes.scene import Scene
import pygame as pg


class Game:
    def __init__(self, screen: pg.Surface, scene: Scene, config: Config):
        self.screen = screen
        self.active_scene: Scene = scene
        self.config = config
        self.current_level: int = 1

    def loop(self):
        clock = pg.time.Clock()
        while True:
            # delta time, the time between the last frame and the current
            dt: float = clock.tick(60)  # limits FPS to 60
            events: list[pg.event.Event] = pg.event.get()
            for event in events:
                if event.type == pg.QUIT: self._quit()
                self.active_scene.handle_event(event)
            if self._maybe_scene_transition():
                continue

            self.active_scene.update(events, dt)
            self.screen.fill("black")
            self.active_scene.draw(self.screen)
            pg.display.flip()

    def _maybe_scene_transition(self):
        next_id = self.active_scene.next_scene_id
        if next_id is not None:
            self.active_scene.next_scene_id = None
            self.active_scene = self._create_scene(next_id)
            return True
        return False
    
    def _create_scene(self, scene_id: SceneId) -> Scene:
        match scene_id:
            case SceneId.MAIN_MENU: return MainMenu(self.screen)
            case SceneId.GAME: return GameScene(self.screen, self.config, self.current_level)

    def _quit(self) -> None:
        sys.exit()

