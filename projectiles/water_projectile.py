import pygame
import math
from typing import List
from .projectile import Projectile

class WaterProjectile(Projectile):
    """Projectile that applies wet status to enemies in an area"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, wet_duration: int, splash_radius: int, lightning_multiplier: float):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage)
        self.wet_duration = wet_duration
        self.splash_radius = splash_radius
        self.lightning_multiplier = lightning_multiplier
        self.size = 6
        self.color = (30, 144, 255)  # Deep blue
        self.has_splashed = False
    
    def check_collision(self, enemies: List) -> bool:
        """Check for collision and apply wet status in area"""
        # Check if projectile reached target area
        target_distance = math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2)
        if target_distance < 8:  # Close enough to target
            self.splash_water(enemies)
            return True
        
        # Also check direct collision with any enemy
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                self.splash_water(enemies)
                return True
        return False
    
    def splash_water(self, enemies: List):
        """Apply wet status to all enemies in splash radius"""
        if self.has_splashed:
            return
        
        self.has_splashed = True
        enemies_hit = 0
        
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance <= self.splash_radius:
                # Apply wet status
                enemy.apply_wet_status(self.wet_duration, self.lightning_multiplier)
                enemies_hit += 1
        
        self.should_remove = True
    
    def draw(self, screen: pygame.Surface):
        """Draw water projectile with water effects"""
        # Draw main water droplet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Draw water highlight
        pygame.draw.circle(screen, (135, 206, 235), (int(self.x - 1), int(self.y - 1)), self.size - 2)
        
        # Draw water trail
        trail_length = 3
        for i in range(trail_length):
            trail_x = self.x - self.dx * i * 2
            trail_y = self.y - self.dy * i * 2
            trail_size = max(1, self.size - i)
            trail_alpha = 255 - (i * 80)
            if trail_alpha > 0:
                trail_color = (30, 144, 255, trail_alpha)
                pygame.draw.circle(screen, trail_color[:3], (int(trail_x), int(trail_y)), trail_size) 