import pygame
import math
from typing import List, Optional

class Tower:
    """Base class for all towers"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
        # Base stats - to be overridden by subclasses
        self.range = 100
        self.damage = 1
        self.fire_rate = 60  # frames between shots
        self.projectile_speed = 5
        self.size = 15
        self.color = (0, 255, 0)  # Green by default
        
        # State
        self.fire_timer = 0
        self.target: Optional[object] = None
        self.angle = 0
        
    def update(self, enemies: List, projectiles: List):
        """Update tower state and shooting"""
        # Update fire timer
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Shoot at target if ready
        if self.target and self.fire_timer <= 0:
            self.shoot(projectiles)
            self.fire_timer = self.fire_rate
    
    def acquire_target(self, enemies: List):
        """Find the best target based on tower's targeting strategy"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range:
                valid_targets.append((enemy, distance))
        
        if not valid_targets:
            self.target = None
            return
        
        # Default targeting: closest to end of path
        self.target = max(valid_targets, key=lambda x: x[0].get_distance_from_start())[0]
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles: List):
        """Create and fire a projectile at the target"""
        if self.target:
            from projectiles import BasicProjectile
            projectile = BasicProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage
            )
            projectiles.append(projectile)
    
    def draw(self, screen: pygame.Surface):
        """Draw the tower on the screen"""
        # Draw range circle when selected (simplified - always show for demo)
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), self.range, 1)
        
        # Draw tower base
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.size, 2)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (end_x, end_y), 3) 