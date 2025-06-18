from typing import List, Tuple
from .enemy import Enemy

class TankEnemy(Enemy):
    """Tank enemy with high health but slow speed"""
    def __init__(self, path: List[Tuple[int, int]]):
        super().__init__(path)
        self.max_health = 5
        self.health = self.max_health
        self.speed = 0.5
        self.reward = 15
        self.size = 12
        self.color = (100, 50, 50)  # Dark red
    
    def take_damage(self, damage: int):
        """Tank enemies have armor that reduces damage"""
        armor_reduction = 0.8 if damage > 1 else 1.0
        actual_damage = max(1, int(damage * armor_reduction))
        self.health -= actual_damage 