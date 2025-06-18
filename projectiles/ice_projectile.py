import pygame
import math
from typing import List
from .projectile import Projectile

class IceProjectile(Projectile):
    """Projectile that applies freeze effect in an area"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, freeze_duration: int, area_radius: int, slow_factor: float):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage)
        self.freeze_duration = freeze_duration
        self.area_radius = area_radius
        self.slow_factor = slow_factor
        self.size = 6
        self.color = (173, 216, 230)  # Light blue
    
    def check_collision(self, enemies: List) -> dict:
        """Apply freeze effect to enemies in area"""
        # Check if projectile reached target area
        target_distance = math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2)
        if target_distance < 10:  # Close enough to target
            # Apply freeze to all enemies in area
            total_damage = 0
            enemies_hit = 0
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if distance <= self.area_radius:
                    enemy.apply_freeze(self.freeze_duration)
                    if self.damage > 0:
                        actual_damage = enemy.take_damage(self.damage)
                        total_damage += actual_damage
                    enemies_hit += 1
            
            if enemies_hit > 0:
                self.should_remove = True
                return {'hit': True, 'damage': total_damage, 'tower_id': self.source_tower_id}
        
        # Also check direct collision with any enemy
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                # Apply freeze to all enemies in area around hit point
                total_damage = 0
                for other_enemy in enemies:
                    area_distance = math.sqrt((self.x - other_enemy.x)**2 + (self.y - other_enemy.y)**2)
                    if area_distance <= self.area_radius:
                        other_enemy.apply_freeze(self.freeze_duration)
                        if self.damage > 0:
                            actual_damage = other_enemy.take_damage(self.damage)
                            total_damage += actual_damage
                
                self.should_remove = True
                return {'hit': True, 'damage': total_damage, 'tower_id': self.source_tower_id}
        return {'hit': False, 'damage': 0, 'tower_id': None}
    
    def draw(self, screen: pygame.Surface):
        """Draw ice projectile with special effect"""
        # Draw main projectile
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Draw inner glow
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size - 2)
        # Draw ice sparkles
        for i in range(3):
            sparkle_x = self.x + math.cos(i * 2.1) * 3
            sparkle_y = self.y + math.sin(i * 2.1) * 3
            pygame.draw.circle(screen, (255, 255, 255), (int(sparkle_x), int(sparkle_y)), 1) 