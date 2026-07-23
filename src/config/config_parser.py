from typing import Any
import random
import sys
from src.config.config import Config
import json

class InvalidConfigError(Exception):
    pass

class ConfigParser:
    def __init__(self, contents: str):
        self.contents: str = contents

    def parse(self) -> Config:
        lines = [line for line in self.contents.splitlines() if not self.is_comment(line)]
        try:
            kv = json.loads(self.contents)
            config = Config()
            config.width = self.clamp_int("width", kv["width"], 5, 40, 20)
            config.height = self.clamp_int("height", kv["height"], 5, 40, 20)
            config.lives = self.clamp_int("lives", kv["lives"], 1, 10, 3)
            cells: int = config.width * config.height
            config.pacgum = self.clamp_int("pacgum", kv["pacgum"], 0, cells, 10)
            config.points_per_pacgum = self.clamp_int(
                "points_per_pacgum", kv["points_per_pacgum"], 1, 10_000, 10
            )
            config.points_per_super_pacgum = self.clamp_int(
                "points_per_super_pacgum", kv["points_per_super_pacgum"], 1, 1_000_000, 50
            )
            config.points_per_ghost = self.clamp_int(
                "points_per_ghost", kv["points_per_ghost"], 1, 1_000_000, 200
            )
            config.level_max_time = self.clamp_int(
                "level_max_time", kv["level_max_time"], 1, 1_000, 90
            )
            config.seed = self.clamp_int(
                "seed", kv["seed"], 0, sys.maxsize, self.random_seed()
            )
            config.highscore_filename  = self.get_str("highscore_filename", kv["highscore_filename"], "highscore.json")
            config.level = self.get_level("level", kv["level"], [1,2,3,4,5,6,7,8,9,10])

            return config
        except:
            raise InvalidConfigError('Invalid json')


    @staticmethod
    def is_comment(line: str) -> bool:
        return line.strip().startswith('#')

    @staticmethod
    def clamp_int(key: str, input: Any | None, min: int, max: int, default: int) -> int:
        if input is None:
            print(f'{key} missing in config, defaulting to {default}')
            return default
        if not isinstance(input, int):
            print(f'{key} must be an int, defaulting to {default}')
            return default
        if input < min:
            print(f'{key} is less than mininum value {min}, clamping to {min}')
            return min
        if input > max:
            print(f'{key} is greater than maximum value {max}, clamping to {max}')
            return max
        return input

    @staticmethod
    def get_str(key: str, input: Any | None, default: str) -> str:
        if input is None:
            print(f'{key} missing in config, defaulting to {default}')
            return default
        if not isinstance(input, str):
            print(f'{key} must be a string, defaulting to {default}')
            return default
        return input

    @staticmethod
    def get_level(key: str, input: Any | None, default: list[int]) -> list[int]:
        if input is None:
            print(f'{key} missing in config, defaulting to {default}')
            return default
        if not isinstance(input, list) or len(input) == 0:
            print(f'{key} must be a non-empty list of ints, defaulting to {default}')
            return default
        for item in input:
            if not isinstance(item, int):
                print(f'{key} must be a non-empty list of ints, defaulting to {default}')
                return default
        return input

    @staticmethod
    def random_seed() -> int:
        return random.randint(1, sys.maxsize)
