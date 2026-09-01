import pygame as pg

from src.graphics.sprites import Sprites


class TextSprites(Sprites):
    """Represent TextSprites state and behavior."""
    PATH = "sprites/text.png"
    HEIGHT = 7
    WIDTHS = {
        "a": 7,
        "b": 7,
        "c": 7,
        "d": 7,
        "e": 6,
        "f": 7,
        "g": 7,
        "h": 7,
        "i": 6,
        "j": 7,
        "k": 7,
        "l": 6,
        "m": 7,
        "n": 7,
        "o": 7,
        "p": 7,
        "q": 7,
        "r": 7,
        "s": 7,
        "t": 6,
        "u": 7,
        "v": 7,
        "w": 7,
        "x": 7,
        "y": 6,
        "z": 7,
        "!": 5,
        "0": 7,
        "1": 6,
        "2": 7,
        "3": 7,
        "4": 7,
        "5": 7,
        "6": 7,
        "7": 7,
        "8": 7,
        "9": 7,
        " ": 5,
    }
    COLOR_OFFSET = {
        "white": 0,
        "red": 32,
        "pink": 64,
        "cyan": 96,
        "sand": 128,
        "salmon": 160,
        "yellow": 192,
    }

    @classmethod
    def render(
        cls, string: str, color: str = "white", scale: int = 1
    ) -> pg.Surface:
        # Todo: can crash if unknown character is given, such as in '-1'
        """Render the object."""
        string = string.lower()
        width = 0
        try:
            for char in string:
                width += cls.WIDTHS[char] + 1
        except KeyError as e:
            print(f"Attempted to render unknown character: {e}")
            string = "error"
            width = 50
        result = pg.Surface((width, cls.HEIGHT))
        x = 0
        for char in string:
            if char != " ":
                result.blit(cls._char(char, color), [x, 0])
            x += cls.WIDTHS[char] + 1
        return pg.transform.scale_by(result, scale)

    @classmethod
    def _char(cls, in_char: str, color: str) -> pg.Surface:
        """Perform the char operation."""
        char = in_char.lower()
        if char not in cls.WIDTHS:
            raise ValueError(f"Character {char} not found in widths")
        if color not in cls.COLOR_OFFSET:
            raise ValueError(f"Color {color} not found")
        size = (cls.WIDTHS[char], cls.HEIGHT)
        dx = cls.COLOR_OFFSET[color]

        match char:
            case "a":
                return cls._load((1, dx + 0), size)
            case "b":
                return cls._load((9, dx + 0), size)
            case "c":
                return cls._load((17, dx + 0), size)
            case "d":
                return cls._load((25, dx + 0), size)
            case "e":
                return cls._load((34, dx + 0), size)
            case "f":
                return cls._load((41, dx + 0), size)
            case "g":
                return cls._load((49, dx + 0), size)
            case "h":
                return cls._load((57, dx + 0), size)
            case "i":
                return cls._load((66, dx + 0), size)
            case "j":
                return cls._load((73, dx + 0), size)
            case "k":
                return cls._load((81, dx + 0), size)
            case "l":
                return cls._load((90, dx + 0), size)
            case "m":
                return cls._load((97, dx + 0), size)
            case "n":
                return cls._load((105, dx + 0), size)
            case "o":
                return cls._load((113, dx + 0), size)
            case "p":
                return cls._load((1, dx + 8), size)
            case "q":
                return cls._load((9, dx + 8), size)
            case "r":
                return cls._load((17, dx + 8), size)
            case "s":
                return cls._load((25, dx + 8), size)
            case "t":
                return cls._load((34, dx + 8), size)
            case "u":
                return cls._load((41, dx + 8), size)
            case "v":
                return cls._load((49, dx + 8), size)
            case "w":
                return cls._load((57, dx + 8), size)
            case "x":
                return cls._load((65, dx + 8), size)
            case "y":
                return cls._load((74, dx + 8), size)
            case "z":
                return cls._load((81, dx + 8), size)
            case "!":
                return cls._load((90, dx + 8), size)
            case "0":
                return cls._load((1, dx + 16), size)
            case "1":
                return cls._load((10, dx + 16), size)
            case "2":
                return cls._load((17, dx + 16), size)
            case "3":
                return cls._load((25, dx + 16), size)
            case "4":
                return cls._load((33, dx + 16), size)
            case "5":
                return cls._load((41, dx + 16), size)
            case "6":
                return cls._load((49, dx + 16), size)
            case "7":
                return cls._load((57, dx + 16), size)
            case "8":
                return cls._load((65, dx + 16), size)
            case "9":
                return cls._load((73, dx + 16), size)
        raise ValueError(f"Character {char} not found in font sprites")
