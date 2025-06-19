import math
from typing import List
from .projectile import Projectile

class BasicProjectile(Projectile):
    """Standard projectile that deals direct damage"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, tower_type: str = "basic"):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage, tower_type)
        self.size = 3
        self.color = (255, 255, 0)  # Yellow
        self.target_enemy = None
    
    def update(self):
        """Update with enemy collision detection"""
        super().update()
        
        # Check collision with enemies (this will be handled by the game loop)
        # The game loop will check collisions and apply damage
    
    def check_collision(self, enemies: List) -> bool:
        """Check collision with enemies and apply damage"""
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                actual_damage = enemy.take_damage(self.damage, self.tower_type)
                self.should_remove = True
                # Return the actual damage dealt and source tower for currency tracking
                return {'hit': True, 'damage': actual_damage, 'tower_id': self.source_tower_id}
        return {'hit': False, 'damage': 0, 'tower_id': None} 