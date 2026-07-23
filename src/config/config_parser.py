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
            config.width = self.clamp_int("width", kv["width"], 5, 40, 10)
            config.height = self.clamp_int("height", kv["height"], 5, 40, 10)
            config.lives = self.clamp_int("lives", kv["lives"], 1, 10, 3)
            cells: int = config.width * config.height
            config.pacgum = self.clamp_int("pacgum", kv["pacgum"], 0, cells, 10)
            config.points_per_pacgum = self.clamp_int(
                "points_per_pacgum", kv["points_per_pacgum"], 1, 10000, 10
            )
            config.points_per_super_pacgum = self.clamp_int(
                "points_per_super_pacgum", kv["points_per_super_pacgum"], 1, 1000000, 50
            )
            config.points_per_ghost = self.clamp_int(
                "points_per_ghost", kv["points_per_ghost"], 1, 1000000, 200
            )
            level_max_time = self.clamp_int(
                "level_max_time", kv["level_max_time"], 1, 1000, 90
            )
    # highscore_filename: str = "highscore.json"
    # level: list[int] = [1,2,3,4,5,6,7,8,9,10]
    # width: int = 50
    # height: int = 50
    # lives: int = 3
    # pacgum: int = 42
    # points_per_pacgum: int = 10
    # points_per_super_pacgum: int = 50
    # points_per_ghost: int = 200
    # seed: str = "42"
    # level_max_time: int = 90


            return kv
        except:
            raise InvalidConfigError('Invalid json')
            

    @staticmethod
    def is_comment(line: str) -> bool:
        return line.strip().startswith('#')

    @staticmethod
    def clamp_int(key: str, input: int | None, min: int, max: int, default: int):
        if input is None:
            print(f'{key} missing in config, defaulting to {default}')
            return default
        if input < min:
            print(f'{key} is less than mininum value {min}, clamping to {min}')
            return min
        if input > min:
            print(f'{key} is greater than maximum value {max}, clamping to {max}')
            return max
        return input
