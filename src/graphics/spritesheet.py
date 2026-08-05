import pygame as pg

class Spritesheet:
    GENERAL_PATH = "sprites/general.png"

    # Player sprites
    PLAYER_MOVING_EAST = [
        [8 + 16 * 28, 0],
        [8 + 16 * 29, 0],
        [8 + 16 * 30, 0],
        [8 + 16 * 29, 0],
    ]
    PLAYER_MOVING_WEST = [
        [8 + 16 * 28, 16],
        [8 + 16 * 29, 16],
        [8 + 16 * 30, 16],
        [8 + 16 * 29, 16],
    ]
    PLAYER_MOVING_NORTH = [
        [8 + 16 * 28, 32],
        [8 + 16 * 29, 32],
        [8 + 16 * 30, 32],
        [8 + 16 * 29, 32],
    ]
    PLAYER_MOVING_SOUTH = [
        [8 + 16 * 28, 48],
        [8 + 16 * 29, 48],
        [8 + 16 * 30, 48],
        [8 + 16 * 29, 48],
    ]


    def __init__(self) -> None:
        self.general: pg.Surface = self._load_sheet(self.GENERAL_PATH)

    def _load_sheet(self, path: str) -> pg.Surface:
        sheet = pg.image.load("sprites/general.png")
        sheet.convert_alpha()
        return sheet

