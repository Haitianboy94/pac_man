from src.config.config import Config


class GameState:
    """
    Contains information about the state of the game.
    """
    def __init__(self, config: Config):
        self.lives: int = config.lives
        self.current_level: int = 1
        self.points: int = 0
        self.time_remaining_ms: int = config.level_max_time * 1000
