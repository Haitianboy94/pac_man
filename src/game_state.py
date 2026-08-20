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
        self.cheats_invincibility: bool = False
        self.cheats_freeze_ghosts: bool = False
        self.cheats_super_speed: bool = False

    def toggle_invincibility(self) -> None:
        "Toggle invincibility"
        self.cheats_invincibility = not self.cheats_invincibility

    def toggle_freeze_ghosts(self) -> None:
        "Toggle ghost freeze"
        self.cheats_freeze_ghosts = not self.cheats_freeze_ghosts

    def extra_life(self) -> None:
        "Add an extra life"
        self.lives += 1

    def toggle_super_speed(self) -> None:
        "Toggle super speed"
        self.cheats_super_speed = not self.cheats_super_speed
