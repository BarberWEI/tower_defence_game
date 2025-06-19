import math
from typing import List
from .projectile import Projectile

class SniperProjectile(Projectile):
    """High-speed, high-damage projectile"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, tower_type: str = "basic"):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage, tower_type)
        self.size = 2
        self.color = (0, 100, 255)  # Blue
        self.max_distance = 500  # Longer range
    
    def check_collision(self, enemies: List) -> dict:
        """Sniper projectiles pierce through enemies"""
        hit_count = 0
        total_damage = 0
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                actual_damage = enemy.take_damage(self.damage, self.tower_type)
                total_damage += actual_damage
                hit_count += 1
                if hit_count >= 2:  # Pierce through up to 2 enemies
                    self.should_remove = True
                    break
        
        if hit_count > 0:
            return {'hit': True, 'damage': total_damage, 'tower_id': self.source_tower_id}
        return {'hit': False, 'damage': 0, 'tower_id': None} 