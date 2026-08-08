from src.graphics.sprites import Sprites
import pygame as pg

class TextSprites(Sprites):
    PATH = "sprites/text.png"
    HEIGHT = 7
    WIDTHS = {
        'a': 7,
        'b': 7,
        'c': 7,
        'd': 7,
        'e': 6,
        'f': 7,
        'g': 7,
        'h': 7,
        'i': 6,
        'j': 7,
        'k': 7,
        'l': 6,
        'm': 7,
        'n': 7,
        'o': 7,
        'p': 7,
        'q': 7,
        'r': 7,
        's': 7,
        't': 6,
        'u': 7,
        'v': 7,
        'w': 7,
        'x': 7,
        'y': 6,
        'z': 7,
        '!': 5,
        '0': 7,
        '1': 6,
        '2': 7,
        '3': 7,
        '4': 7,
        '5': 7,
        '6': 7,
        '7': 7,
        '8': 7,
        '9': 7,
        ' ': 5,
    }
    COLOR_OFFSET = {
        'white': 0,
        'red': 32,
        'pink': 64,
        'cyan': 96,
        'sand': 128,
        'salmon': 160,
        'yellow': 192,
    }

    def __init__(self) -> None:
        Sprites.__init__(self, self.PATH)

    def render(self, string: str, color: str = 'white', scale: int = 1) -> pg.Surface:
        string = string.lower()
        width = 0
        for char in string:
            width += self.WIDTHS[char] + 1
        width
        height = self.HEIGHT

        result = pg.Surface((width, height))
        x = 0
        for char in string:
            if char != ' ':
                result.blit(self.char(char, color), [x, 0])
            x += self.WIDTHS[char] + 1
        return pg.transform.scale_by(result, scale)


    def char(self, in_char: str, color: str) -> pg.Surface:
        char = in_char.lower()
        if char not in self.WIDTHS:
            raise ValueError(f'Character {char} not found in widths')
        if color not in self.COLOR_OFFSET:
            raise ValueError(f'Color {color} not found')
        width = self.WIDTHS[char]
        height = self.HEIGHT
        h_offset = self.COLOR_OFFSET[color]

        match char:
            case 'a': return self._load(1, h_offset + 0, width, height)
            case 'b': return self._load(9, h_offset + 0, width, height)
            case 'c': return self._load(17, h_offset + 0, width, height)
            case 'd': return self._load(25, h_offset + 0, width, height)
            case 'e': return self._load(34, h_offset + 0, width, height)
            case 'f': return self._load(41, h_offset + 0, width, height)
            case 'g': return self._load(49, h_offset + 0, width, height)
            case 'h': return self._load(57, h_offset + 0, width, height)
            case 'i': return self._load(66, h_offset + 0, width, height)
            case 'j': return self._load(73, h_offset + 0, width, height)
            case 'k': return self._load(81, h_offset + 0, width, height)
            case 'l': return self._load(90, h_offset + 0, width, height)
            case 'm': return self._load(97, h_offset + 0, width, height)
            case 'n': return self._load(105, h_offset + 0, width, height)
            case 'o': return self._load(113, h_offset + 0, width, height)
            case 'p': return self._load(1, h_offset + 8, width, height)
            case 'q': return self._load(9, h_offset + 8, width, height)
            case 'r': return self._load(17, h_offset + 8, width, height)
            case 's': return self._load(25, h_offset + 8, width, height)
            case 't': return self._load(34, h_offset + 8, width, height)
            case 'u': return self._load(41, h_offset + 8, width, height)
            case 'v': return self._load(49, h_offset + 8, width, height)
            case 'w': return self._load(57, h_offset + 8, width, height)
            case 'x': return self._load(65, h_offset + 8, width, height)
            case 'y': return self._load(74, h_offset + 8, width, height)
            case 'z': return self._load(81, h_offset + 8, width, height)
            case '!': return self._load(90, h_offset + 8, width, height)
            case '0': return self._load(1, h_offset + 16, width, height)
            case '1': return self._load(10, h_offset + 16, width, height)
            case '2': return self._load(17, h_offset + 16, width, height)
            case '3': return self._load(25, h_offset + 16, width, height)
            case '4': return self._load(33, h_offset + 16, width, height)
            case '5': return self._load(41, h_offset + 16, width, height)
            case '6': return self._load(49, h_offset + 16, width, height)
            case '7': return self._load(57, h_offset + 16, width, height)
            case '8': return self._load(65, h_offset + 16, width, height)
            case '9': return self._load(73, h_offset + 16, width, height)
        raise ValueError(f'Character {char} not found in font sprites')
