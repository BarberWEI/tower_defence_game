from typing import List, Tuple
from .enemy import Enemy

class BasicEnemy(Enemy):
    """Basic enemy with standard stats"""
    def __init__(self, path: List[Tuple[int, int]]):
        super().__init__(path)
        self.max_health = 1
        self.health = self.max_health
        self.speed = 1.0
        self.reward = 4
        self.size = 8
        self.color = (255, 100, 100)  # Light red 