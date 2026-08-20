from pytest import skip
from typing import Callable
from src.game_state import GameState
from src.scenes.scene_id import SceneId
from src.ui.button import Button
from src.ui.text import Text
from src.ui.panel import Panel
import pygame as pg

class PauseMenu:
    def __init__(
            self,
            screen: pg.Surface,
            state: GameState,
            skip_level_fn: Callable
    ) -> None:
        self.state: GameState = state
        self.skip_level_fn: Callable = skip_level_fn
        self.center_x: int = int(screen.get_width() / 2) 
        self.main_group: pg.sprite.Group = self._init_main_group()
        self.cheats_group: pg.sprite.Group = self._init_cheats_group()
        self.group: pg.sprite.Group = self.main_group

    def _init_main_group(self) -> pg.sprite.Group:
        "Creates all elements for the main pause menu"
        group: pg.sprite.Group = pg.sprite.Group()

        border: Panel = Panel(pg.Rect(0, 0, 256, 206), pg.Color("white"))
        self._add_centered(group, border, 40)

        background: Panel = Panel(pg.Rect(0, 0, 250, 200), pg.Color("black"))
        self._add_centered(group, background, 43)

        title: Text = Text("paused", "white", 2)
        self._add_centered(group, title, 70)

        cheats: Button = Button(
            "cheats", "white", "yellow", 2, self._open_cheats
        )
        self._add_centered(group, cheats, 185)

        menu_button: Button = Button(
            "main menu", "white", "yellow", 2, self._return_to_main_menu
        )
        self._add_centered(group, menu_button, 205)
        return group

    def _init_cheats_group(self) -> pg.sprite.Group:
        "Creates all elements for the cheats menu"
        group: pg.sprite.Group = pg.sprite.Group()

        border: Panel = Panel(pg.Rect(0, 0, 256, 206), pg.Color("white"))
        self._add_centered(group, border, 40)

        background: Panel = Panel(pg.Rect(0, 0, 250, 200), pg.Color("black"))
        self._add_centered(group, background, 43)

        title: Text = Text("cheats", "white", 2)
        self._add_centered(group, title, 70)

        invincibility: Button = Button(
            "invincibility", "white", "yellow", 2, self.state.toggle_invincibility
        )
        self._add_centered(group, invincibility, 100)

        skip_level: Button = Button(
            "skip level", "white", "yellow", 2, self.skip_level_fn
        )
        self._add_centered(group, skip_level, 120)

        ghost_freeze: Button = Button(
            "ghost freeze", "white", "yellow", 2, self.state.toggle_freeze_ghosts
        )
        self._add_centered(group, ghost_freeze, 140)

        extra_life: Button = Button(
            "extra life", "white", "yellow", 2, self.state.extra_life
        )
        self._add_centered(group, extra_life, 160)

        super_speed: Button = Button(
            "super speed", "white", "yellow", 2, self.state.toggle_super_speed
        )
        self._add_centered(group, super_speed, 180)

        back_button: Button = Button(
            "back", "white", "yellow", 2, self._open_main
        )
        self._add_centered(group, back_button, 205)

        return group

    def _add_centered(self, group: pg.sprite.Group, sprite: pg.sprite.Sprite, y: int):
        "Add a sprite to a group with centered x position and a specified y"
        if not hasattr(sprite, "rect") or not isinstance(sprite.rect, pg.Rect):
            raise ValueError("Sprite must have rect attribute")
        sprite.rect.centerx = self.center_x
        sprite.rect.y = y
        group.add(sprite)

    def _open_cheats(self) -> None:
        "Activate the cheats menu"
        self.group = self.cheats_group

    def _open_main(self) -> None:
        "Activate the main pause menu"
        self.group = self.main_group

    def _return_to_main_menu(self) -> None:
        "Return to the main menu scene"
        self.next_scene_id = SceneId.MAIN_MENU


