import pygame
import math
from typing import List
from .projectile import Projectile

class SplashProjectile(Projectile):
    """Projectile that deals area damage on impact"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, splash_radius: float):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage)
        self.splash_radius = splash_radius
        self.size = 5
        self.color = (255, 100, 0)  # Orange
        self.has_exploded = False
    
    def on_impact(self):
        """Explode and deal area damage"""
        self.has_exploded = True
        self.should_remove = True
    
    def check_collision(self, enemies: List) -> dict:
        """Check for direct hit, then explode"""
        direct_hit = False
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                direct_hit = True
                break
        
        if direct_hit or self.has_reached_target():
            total_damage = self.explode(enemies)
            return {'hit': total_damage > 0, 'damage': total_damage, 'tower_id': self.source_tower_id}
        return {'hit': False, 'damage': 0, 'tower_id': None}
    
    def explode(self, enemies: List):
        """Deal splash damage to all enemies in radius"""
        total_damage = 0
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance <= self.splash_radius:
                # Damage decreases with distance
                damage_multiplier = 1.0 - (distance / self.splash_radius) * 0.5
                actual_damage = max(1, int(self.damage * damage_multiplier))
                damage_dealt = enemy.take_damage(actual_damage)
                total_damage += damage_dealt
        
        self.should_remove = True
        return total_damage
    
    def draw(self, screen: pygame.Surface):
        """Draw splash projectile"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 200, 100), (int(self.x), int(self.y)), self.size - 1) 