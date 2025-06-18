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
    
    def check_collision(self, enemies: List) -> bool:
        """Check for direct hit, then explode"""
        direct_hit = False
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                direct_hit = True
                break
        
        if direct_hit or self.has_reached_target():
            self.explode(enemies)
            return True
        return False
    
    def explode(self, enemies: List):
        """Deal splash damage to all enemies in radius"""
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance <= self.splash_radius:
                # Damage decreases with distance
                damage_multiplier = 1.0 - (distance / self.splash_radius) * 0.5
                actual_damage = max(1, int(self.damage * damage_multiplier))
                enemy.take_damage(actual_damage)
        
        self.should_remove = True
    
    def draw(self, screen: pygame.Surface):
        """Draw splash projectile"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 200, 100), (int(self.x), int(self.y)), self.size - 1) 