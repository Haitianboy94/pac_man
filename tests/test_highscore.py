"""Tests for the persistent highscore system."""

import json
from pathlib import Path

import pytest

from src.config.highscore import Highscore, InvalidHighscoreError


def test_new_highscore_is_empty(tmp_path: Path) -> None:
    """A newly created highscore table should contain no entries."""
    highscore = Highscore(str(tmp_path / "scores.json"))

    assert highscore.get() == []


def test_load_missing_file_keeps_the_current_scores(tmp_path: Path) -> None:
    """Loading a missing file should be harmless and leave scores unchanged."""
    highscore = Highscore(str(tmp_path / "missing.json"))
    assert highscore.add("Alice", 100) is None

    highscore.load()

    assert highscore.get() == [(100, "Alice")]


def test_load_reads_a_valid_json_score_table(tmp_path: Path) -> None:
    """Scores saved as a JSON object should be available after loading."""
    filename = tmp_path / "scores.json"
    filename.write_text(json.dumps({"Al ice": 500, "Bob": 250}))
    highscore = Highscore(str(filename))

    highscore.load()

    assert highscore.get() == [(500, "Al ice"), (250, "Bob")]


def test_load_invalid_json_raises_public_error(tmp_path: Path) -> None:
    """Corrupt JSON should produce the class's documented exception."""
    filename = tmp_path / "scores.json"
    filename.write_text('{"Alice": 100')
    highscore = Highscore(str(filename))

    with pytest.raises(InvalidHighscoreError):
        highscore.load()


@pytest.mark.parametrize(
    "contents",
    (
        "[]",
        "null",
        '{"Alice": "100"}',
        '{"Alice": -1}',
        '{"Alice": true}',
        '{"Alice!": 100}',
        '{"A very long name": 100}',
    ),
)
def test_load_invalid_score_format_raises_public_error(
    tmp_path: Path, contents: str
) -> None:
    """Valid JSON with an invalid score-table shape must be rejected."""
    filename = tmp_path / "scores.json"
    filename.write_text(contents)
    highscore = Highscore(str(filename))

    with pytest.raises(InvalidHighscoreError):
        highscore.load()


def test_store_and_load_round_trip(tmp_path: Path) -> None:
    """Storing scores should make them available to a new instance."""
    filename = tmp_path / "scores.json"
    highscore = Highscore(str(filename))
    highscore.add("Alice", 500)
    highscore.add("Bob", 250)

    highscore.store()

    restored = Highscore(str(filename))
    restored.load()
    assert restored.get() == [(500, "Alice"), (250, "Bob")]


def test_add_accepts_valid_boundary_values(tmp_path: Path) -> None:
    """Ten-character names and a zero score are valid inputs."""
    highscore = Highscore(str(tmp_path / "scores.json"))

    assert highscore.add("TenChars10", 0) is None
    assert highscore.add("A B", 1) is None
    assert highscore.get() == [(1, "A B"), (0, "TenChars10")]


@pytest.mark.parametrize(
    ("name", "score"),
    (
        ("", 100),
        ("A" * 11, 100),
        ("Alice!", 100),
        ("Alice-1", 100),
        ("Alice", -1),
        ("Alice", 1.5),
        ("Alice", "100"),
        ("Alice", True),
    ),
)
def test_add_rejects_invalid_values_without_mutating_scores(
    tmp_path: Path, name: str, score: int | float | str | bool
) -> None:
    """Invalid names and scores should return an error and change nothing."""
    highscore = Highscore(str(tmp_path / "scores.json"))

    with pytest.raises(InvalidHighscoreError):
        highscore.add(name, score)  # type: ignore[arg-type]

    assert highscore.get() == []


def test_add_keeps_only_the_top_ten_scores_in_descending_order(
    tmp_path: Path,
) -> None:
    """Adding more than ten scores should discard the lowest scores."""
    highscore = Highscore(str(tmp_path / "scores.json"))

    for score in range(11):
        assert highscore.add(f"P{score}", score) is None

    assert highscore.get() == [
        (10, "P10"),
        (9, "P9"),
        (8, "P8"),
        (7, "P7"),
        (6, "P6"),
        (5, "P5"),
        (4, "P4"),
        (3, "P3"),
        (2, "P2"),
        (1, "P1"),
        (0, "P0"),
    ]


def test_load_keeps_only_the_top_ten_scores(tmp_path: Path) -> None:
    """Loading scores should apply the same top-ten rule as insertion."""
    filename = tmp_path / "scores.json"
    filename.write_text(json.dumps({f"P{score}": score for score in range(11)}))
    highscore = Highscore(str(filename))

    highscore.load()

    assert highscore.get() == [
        (10, "P10"),
        (9, "P9"),
        (8, "P8"),
        (7, "P7"),
        (6, "P6"),
        (5, "P5"),
        (4, "P4"),
        (3, "P3"),
        (2, "P2"),
        (1, "P1"),
        (0, "P0"),
    ]
