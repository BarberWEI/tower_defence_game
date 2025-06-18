from typing import List, Tuple
from .enemy import Enemy

class FastEnemy(Enemy):
    """Fast enemy with high speed but low health"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 1
        self.health = self.max_health
        self.speed = 2.5
        self.reward = 6
        self.size = 6
        self.color = (255, 255, 0)  # Yellow
    
    def apply_freeze(self, duration: int):
        """Fast enemies are less affected by freeze"""
        super().apply_freeze(duration // 2) 