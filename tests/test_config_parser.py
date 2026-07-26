"""Tests for the Pac-Man configuration parser."""

import json

import pytest

from src.config.config import DEFAULTS, Config
from src.config.config_parser import ConfigParser, InvalidConfigError


def valid_config() -> dict[str, object]:
    """Return a complete configuration containing valid non-default values."""
    return {
        "highscore_filename": "scores.json",
        "level": [10, 20, 30],
        "width": 15,
        "height": 12,
        "lives": 5,
        "pacgum": 75,
        "points_per_pacgum": 25,
        "points_per_super_pacgum": 100,
        "points_per_ghost": 500,
        "seed": 1234,
        "level_max_time": 120,
    }


def parse(payload: dict[str, object]) -> Config:
    """Serialize and parse a configuration dictionary."""
    return ConfigParser(json.dumps(payload)).parse()


def test_parse_complete_valid_config() -> None:
    """Every supported key should be loaded from a valid JSON object."""
    config = parse(valid_config())

    assert config.highscore_filename == "scores.json"
    assert config.level == [10, 20, 30]
    assert config.width == 15
    assert config.height == 12
    assert config.lives == 5
    assert config.pacgum == 75
    assert config.points_per_pacgum == 25
    assert config.points_per_super_pacgum == 100
    assert config.points_per_ghost == 500
    assert config.seed == 1234
    assert config.level_max_time == 120


@pytest.mark.parametrize(("missing_key", "expected"), DEFAULTS.items())
def test_missing_key_uses_default_and_continues(
    missing_key: str,
    expected: object,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A missing key should be reported without rejecting the whole file."""
    payload = valid_config()
    del payload[missing_key]

    config = parse(payload)

    assert getattr(config, missing_key) == expected
    message = capsys.readouterr().out.lower()
    assert missing_key in message
    assert "default" in message


INVALID_VALUES: tuple[tuple[str, object], ...] = (
    ("highscore_filename", 123),
    ("level", [1, "two", 3]),
    ("width", "wide"),
    ("height", [12]),
    ("lives", 3.5),
    ("pacgum", "many"),
    ("points_per_pacgum", {}),
    ("points_per_super_pacgum", []),
    ("points_per_ghost", "200"),
    ("seed", "random"),
    ("level_max_time", 90.5),
)


@pytest.mark.parametrize(("key", "bad_value"), INVALID_VALUES)
def test_bad_type_uses_default_and_continues(
    key: str,
    bad_value: object,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A wrongly typed value should be reported and replaced by its default."""
    payload = valid_config()
    payload[key] = bad_value

    config = parse(payload)

    assert getattr(config, key) == DEFAULTS[key]
    message = capsys.readouterr().out.lower()
    assert key in message
    assert "default" in message


@pytest.mark.parametrize(
    "key",
    (
        "width",
        "height",
        "lives",
        "pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "seed",
        "level_max_time",
    ),
)
def test_boolean_is_not_accepted_as_an_integer(key: str) -> None:
    """JSON booleans must not silently become numeric configuration values."""
    payload = valid_config()
    payload[key] = True

    config = parse(payload)

    assert getattr(config, key) == DEFAULTS[key]


@pytest.mark.parametrize("key", tuple(DEFAULTS))
def test_json_null_uses_default(key: str) -> None:
    """A JSON null value should be treated as absent and use the default."""
    payload = valid_config()
    payload[key] = None

    config = parse(payload)

    assert getattr(config, key) == DEFAULTS[key]


def test_hash_comment_lines_are_ignored() -> None:
    """Full comment lines, including indented ones, should be ignored."""
    contents = json.dumps(valid_config(), indent=2)
    contents = contents.replace("{\n", "{\n  # level settings\n", 1)
    contents = "# Pac-Man configuration\n" + contents

    config = ConfigParser(contents).parse()

    assert config.width == 15
    assert config.level == [10, 20, 30]


def test_double_slash_comment_lines_are_ignored() -> None:
    """Full comment lines, including indented ones, should be ignored."""
    contents = json.dumps(valid_config(), indent=2)
    contents = contents.replace("{\n", "{\n  // level settings\n", 1)
    contents = "// Pac-Man configuration\n" + contents

    config = ConfigParser(contents).parse()

    assert config.width == 15
    assert config.level == [10, 20, 30]


def test_unknown_keys_are_ignored() -> None:
    """Additional defense-time keys should not invalidate the config."""
    payload = valid_config()
    payload["future_option"] = {"enabled": True}

    config = parse(payload)

    assert config.width == 15
    assert not hasattr(config, "future_option")


@pytest.mark.parametrize(
    "contents",
    (
        "",
        "{",
        '{"width": 15,}',
        '{"width": fifteen}',
        "[]",
        "null",
    ),
)
def test_malformed_or_non_object_json_raises_clear_config_error(
    contents: str,
) -> None:
    """Invalid JSON input should be converted to the parser's public error."""
    with pytest.raises(InvalidConfigError, match="Invalid json"):
        ConfigParser(contents).parse()
