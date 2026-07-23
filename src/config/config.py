from dataclasses import dataclass

@dataclass
class Config():
    highscore_filename: str = "highscore.json"
    level: list[int] = [1,2,3,4,5,6,7,8,9,10]
    width: int = 50
    height: int = 50
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: str = "42"
    level_max_time: int = 90


