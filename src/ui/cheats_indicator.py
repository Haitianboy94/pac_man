from src.graphics.text_sprites import TextSprites
from src.graphics.hud_sprites import HudSprites
from src.game_state import GameState
import pygame as pg

class CheatsIndicator(pg.sprite.Sprite):
    "UI element which displays the active cheats"
    def __init__(self, state: GameState):
        """Initialize the object."""
        pg.sprite.Sprite.__init__(self)
        self.state: GameState = state
        self.lives: int = state.lives
        self.image: pg.Surface = pg.Surface((0, 0))
        self.rect: pg.Rect = pg.Rect(0, 0, 0, 0)
        self.invincibility: bool = False
        self.freeze_ghosts: bool = False
        self.super_speed: bool = False
        self._render()

    def update(self, dt: int):
        """Update the object."""
        change: bool = False
        if self.invincibility != self.state.cheats_invincibility:
            self.invincibility = self.state.cheats_invincibility
            change = True
        if self.freeze_ghosts != self.state.cheats_freeze_ghosts:
            self.freeze_ghosts = self.state.cheats_freeze_ghosts
            change = True
        if self.super_speed != self.state.cheats_super_speed:
            self.super_speed = self.state.cheats_super_speed
            change = True
        if change:
            self._render()

    def _render(self) -> None:
        """Perform the render operation."""
        active: list[str] = []
        if self.invincibility:
            active.append("godmode")
        if self.freeze_ghosts:
            active.append("freeze")
        if self.super_speed:
            active.append("speed")

        text = TextSprites.render(" ".join(active))
        self.image = text

