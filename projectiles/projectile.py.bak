import pygame
import math
from typing import List

class Projectile:
    """Base class for all projectiles"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float, 
                 speed: float, damage: int):
        self.x = float(start_x)
        self.y = float(start_y)
        self.target_x = float(target_x)
        self.target_y = float(target_y)
        self.speed = speed
        self.damage = damage
        
        # Tower tracking for currency generation
        self.source_tower_id = None
        
        # Calculate direction
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        # Visual properties
        self.size = 3
        self.color = (255, 255, 0)  # Yellow by default
        
        # State
        self.should_remove = False
        self.distance_traveled = 0
        self.max_distance = 300  # Maximum travel distance
    
    def update(self):
        """Update projectile position and check for removal"""
        # Move projectile
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.distance_traveled += self.speed
        
        # Check if projectile should be removed
        if self.distance_traveled >= self.max_distance:
            self.should_remove = True
        
        # Check if projectile is off-screen
        if self.x < -50 or self.x > 1250 or self.y < -50 or self.y > 850:
            self.should_remove = True
        
        # Check collision with target area
        if self.has_reached_target():
            self.on_impact()
    
    def has_reached_target(self) -> bool:
        """Check if projectile has reached its target area"""
        distance_to_target = math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2)
        return distance_to_target < 10
    
    def on_impact(self):
        """Handle projectile impact - to be overridden by subclasses"""
        self.should_remove = True
    
    def draw(self, screen: pygame.Surface):
        """Draw the projectile on the screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size) 