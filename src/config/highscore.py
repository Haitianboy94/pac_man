import heapq
import json
class InvalidHighscoreError(Exception):
    """Raised when highscore data does not meet the required format."""


class Highscore:
    """Manage player high scores stored in a JSON file."""

    def __init__(self, filename: str) -> None:
        """Create a highscore table backed by ``filename``."""
        self.filename: str = filename
        self.scores: list[tuple[int, str]] = []

    def load(self) -> None:
        """
        Loads the highscore values from the JSON file.
        Does nothing if the file does not exist.
        Ignores file contents if the format is invalid
        """
        try:
            with open(self.filename) as file:
                contents = file.read()
                kv: dict[str, int] = json.loads(contents)
                if not isinstance(kv, dict):
                    raise InvalidHighscoreError('Json is not a key-value pair')
                for name, score in kv.items():
                    self.add(name, score)
        except FileNotFoundError:
            print('No highscore file found, proceeding with empty scores')
            pass
        except json.JSONDecodeError as e:
            raise InvalidHighscoreError('Invalid json') from e

    def store(self) -> None:
        """Commits the internal highscore values to the JSON file."""
        try:
            with open(self.filename, 'w') as file:
                score_dict: dict[str, int] = {name: score for score, name in self.scores}
                file.write(json.dumps(score_dict))
        except:
            print('Failed to write highscore')

    def add(self, name: str, score: int) -> None:
        """
        Records a new highscore.
        Raises InvalidHighscoreError if the input was invalid.
        """
        if not isinstance(name, str):
            raise InvalidHighscoreError('Name must be a string')
        if isinstance(score, bool):
            raise InvalidHighscoreError('Score must be an int')
        if not isinstance(score, int):
            raise InvalidHighscoreError('Score must be an int')
        if len(name) == 0:
            raise InvalidHighscoreError('Name must be at least 1 character')
        if len(name) > 10:
            raise InvalidHighscoreError('Name must be at most 10 character')
        for char in name:
            if not char.isalnum() and not char == " ":
                raise InvalidHighscoreError('Name must be alphanumeric')
        if score < 0:
            raise InvalidHighscoreError('Score must not be negative')
        heapq.heappush(self.scores, (score, name))

    def get(self) -> list[tuple[int, str]]:
        """Returns the current highscores."""
        return list(reversed(self.scores))
