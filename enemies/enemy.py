import pygame
import math
from typing import List, Tuple

class Enemy:
    """Base class for all enemies"""
    def __init__(self, path: List[Tuple[int, int]]):
        self.path = path
        self.path_index = 0
        self.x = float(path[0][0])
        self.y = float(path[0][1])
        
        # Base stats - to be overridden by subclasses
        self.max_health = 1
        self.health = self.max_health
        self.speed = 1.0
        self.reward = 5
        self.size = 10
        self.color = (255, 0, 0)  # Red by default
        
        # Status effects
        self.frozen = False
        self.freeze_timer = 0
        self.wet = False
        self.wet_timer = 0
        self.lightning_damage_multiplier = 1.0
        
        # State
        self.reached_end = False
        self.distance_traveled = 0
    
    def update(self):
        """Update enemy position and state"""
        # Handle freeze effect
        if self.frozen:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.frozen = False
        
        # Handle wet effect
        if self.wet:
            self.wet_timer -= 1
            if self.wet_timer <= 0:
                self.wet = False
                self.lightning_damage_multiplier = 1.0
        
        # Move along path if not frozen
        if not self.frozen:
            self.move_along_path()
    
    def move_along_path(self):
        """Move the enemy along the predefined path"""
        if self.path_index >= len(self.path) - 1:
            self.reached_end = True
            return
        
        # Get current and next waypoints
        current_point = self.path[self.path_index]
        next_point = self.path[self.path_index + 1]
        
        # Calculate direction to next waypoint
        dx = next_point[0] - current_point[0]
        dy = next_point[1] - current_point[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            self.path_index += 1
            return
        
        # Normalize direction and apply speed
        dx = (dx / distance) * self.speed
        dy = (dy / distance) * self.speed
        
        # Move towards next waypoint
        self.x += dx
        self.y += dy
        self.distance_traveled += self.speed
        
        # Check if we've reached the next waypoint
        if math.sqrt((self.x - next_point[0])**2 + (self.y - next_point[1])**2) < 5:
            self.path_index += 1
    
    def take_damage(self, damage: int):
        """Apply damage to the enemy"""
        actual_damage = min(damage, self.health)  # Can't deal more damage than remaining health
        self.health -= damage
        return actual_damage
    
    def apply_freeze(self, duration: int):
        """Apply freeze effect to the enemy"""
        self.frozen = True
        self.freeze_timer = max(self.freeze_timer, duration)
    
    def apply_wet_status(self, duration: int, lightning_multiplier: float):
        """Apply wet status to the enemy"""
        self.wet = True
        self.wet_timer = max(self.wet_timer, duration)
        self.lightning_damage_multiplier = lightning_multiplier
    
    def get_distance_from_start(self) -> float:
        """Get the total distance traveled along the path"""
        return self.distance_traveled
    
    def draw(self, screen: pygame.Surface):
        """Draw the enemy on the screen"""
        # Draw main enemy circle with status effects
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            # Slightly darker and more saturated when wet
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw wet effect overlay
        if self.wet:
            # Draw water droplets around enemy
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                drop_x = self.x + math.cos(rad) * (self.size + 3)
                drop_y = self.y + math.sin(rad) * (self.size + 3)
                pygame.draw.circle(screen, (30, 144, 255), (int(drop_x), int(drop_y)), 2)
        
        # Draw health bar
        if self.health < self.max_health:
            bar_width = self.size * 2
            bar_height = 4
            bar_x = int(self.x - bar_width // 2)
            bar_y = int(self.y - self.size - 8)
            
            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Health (green)
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height)) 