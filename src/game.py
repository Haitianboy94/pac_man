from src.config.highscore import Highscore
import sys

import pygame as pg

from src.config.config import Config
from src.game_state import GameState
from src.scenes.game_over import GameOverScene
from src.scenes.game_scene import GameScene
from src.scenes.main_menu import MainMenu
from src.scenes.scene import Scene
from src.scenes.scene_id import SceneId


class Game:
    """
    This class represents the main game process. It runs the game loop
    and owns the config and pygame screen. It also contains the active scene
    and handles scene transisitons.
    """

    def __init__(self, screen: pg.Surface, config: Config):
        """Initialize the object."""
        self.screen = screen
        self.config = config
        self.current_level: int = 1
        self.highscore: Highscore = Highscore(config.highscore_filename)
        self.highscore.load()
        self.active_scene: Scene = self._create_scene(SceneId.MAIN_MENU)
        self.state: GameState = GameState(self.config)

    def loop(self) -> None:
        """
        The main game loop. The main steps are:

        - Handling scene transitions
        - FPS limiting via clock.tick()
        - Retrieving all events from the last frame and passing them to
          the active scene, as well as calling the update method
        - Rendering the active scene to the screen
        """
        clock = pg.time.Clock()
        while True:
            if self._maybe_scene_transition():
                continue
            dt: int = clock.tick(60)  # limits FPS to 60
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()
                self.active_scene.handle_event(event)

            self.active_scene.update(dt)
            self.screen.fill("black")
            self.active_scene.draw(self.screen)
            pg.display.flip()

    def _maybe_scene_transition(self) -> bool:
        "Polling method which handles scene transitions"
        next_id = self.active_scene.next_scene_id
        if next_id is not None:
            self.active_scene.next_scene_id = None
            self.active_scene = self._create_scene(next_id)
            return True
        return False

    def _create_scene(self, scene_id: SceneId) -> Scene:
        "Factory method which constructs new scenes"
        match scene_id:
            case SceneId.MAIN_MENU:
                self.state = GameState(self.config)
                return MainMenu(self.screen, self.config, self.highscore)
            case SceneId.GAME:
                return GameScene(
                    self.screen,
                    self.config,
                    self.highscore,
                    self.state,
                )
            case SceneId.GAME_OVER:
                won = self.state.pending_game_over
                return GameOverScene(self.screen, self.state, self.highscore)

    def _quit(self) -> None:
        "Exits the game"
        sys.exit()
