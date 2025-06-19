import pygame
import math
from typing import List
from .projectile import Projectile

class FreezeProjectile(Projectile):
    """Projectile that applies freeze effect"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, tower_type: str, freeze_duration: int):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage, tower_type)
        self.freeze_duration = freeze_duration
        self.size = 4
        self.color = (100, 200, 255)  # Light blue
    
    def check_collision(self, enemies: List) -> dict:
        """Apply freeze effect to enemies"""
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                enemy.apply_freeze(self.freeze_duration)
                actual_damage = 0
                if self.damage > 0:
                    actual_damage = enemy.take_damage(self.damage, self.tower_type)
                self.should_remove = True
                return {'hit': True, 'damage': actual_damage, 'tower_id': self.source_tower_id}
        return {'hit': False, 'damage': 0, 'tower_id': None}
    
    def draw(self, screen: pygame.Surface):
        """Draw freeze projectile with special effect"""
        # Draw main projectile
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Draw inner glow
        pygame.draw.circle(screen, (200, 255, 255), (int(self.x), int(self.y)), self.size - 1) 