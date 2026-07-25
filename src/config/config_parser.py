"""Parse and validate the Pac-Man JSON configuration."""

import json
import sys
from typing import Any

from src.config.config import DEFAULTS, Config


class InvalidConfigError(Exception):
    """Raised when configuration contents are not a valid JSON object."""


class ConfigParser:
    """Convert JSON configuration contents into a validated ``Config``."""

    def __init__(self, contents: str):
        """Initialize the parser with raw configuration contents."""
        self.contents: str = contents
        self.kv: dict[str, Any] = {}

    def parse(self) -> Config:
        """
        Parse the configuration, applying defaults to faulty values.
        Raises InvalidConfigError when the JSON is invalid.
        """
        self._load_kv()
        config = Config()
        config.width = self.clamp_int("width", 5, 40)
        config.height = self.clamp_int("height", 5, 40)
        config.lives = self.clamp_int("lives", 1, 10)
        cells = config.width * config.height
        config.pacgum = self.clamp_int("pacgum", 0, cells)
        config.points_per_pacgum = self.clamp_int("points_per_pacgum", 1, 10_000)
        config.points_per_super_pacgum = self.clamp_int("points_per_super_pacgum", 1, 1_000_000)
        config.points_per_ghost = self.clamp_int("points_per_ghost", 1, 1_000_000)
        config.level_max_time = self.clamp_int("level_max_time", 1, 1_000)
        config.seed = self.clamp_int("seed", 0, sys.maxsize)
        config.highscore_filename = self.get_str("highscore_filename")
        config.level = self.get_level("level")
        return config

    def _load_kv(self) -> None:
        uncommented = "\n".join(
            line
            for line in self.contents.splitlines()
            if not line.strip().startswith(("#", "//"))
        )
        try:
            kv = json.loads(uncommented)
            if not isinstance(kv, dict):
                raise InvalidConfigError("Invalid json")
            self.kv = kv
        except (json.JSONDecodeError, TypeError) as error:
            raise InvalidConfigError("Invalid json") from error

    def clamp_int(self, key: str, minimum: int, maximum: int) -> int:
        """Validate an integer and clamp it to its supported range."""
        value = self.kv.get(key)
        default: int = DEFAULTS[key]
        if value is None:
            print(f"{key} missing in config, defaulting to {default}")
            return default
        if type(value) is not int:
            print(f"{key} must be an int, defaulting to {default}")
            return default
        if value < minimum:
            print(
                f"{key} is less than minimum value {minimum}, "
                f"clamping to {minimum}"
            )
            return minimum
        if value > maximum:
            print(
                f"{key} is greater than maximum value {maximum}, "
                f"clamping to {maximum}"
            )
            return maximum
        return value

    def get_str(self, key: str) -> str:
        """Validate a string configuration value."""
        input_value = self.kv.get(key)
        default: str = DEFAULTS[key]
        if input_value is None:
            print(f"{key} missing in config, defaulting to {default}")
            return default
        if not isinstance(input_value, str):
            print(f"{key} must be a string, defaulting to {default}")
            return default
        return input_value

    def get_level(self, key: str) -> list[int]:
        """Validate a non-empty list of integer level identifiers."""
        input_value = self.kv.get(key)
        default: list[int] = DEFAULTS[key]
        if input_value is None:
            print(f"{key} missing in config, defaulting to {default}")
            return list(default)
        if (
            not isinstance(input_value, list)
            or not input_value
            or any(type(item) is not int for item in input_value)
        ):
            print(
                f"{key} must be a non-empty list of ints, "
                f"defaulting to {default}"
            )
            return list(default)
        return input_value
