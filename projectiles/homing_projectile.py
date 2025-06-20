import pygame
import math
from typing import List
from .projectile import Projectile

class HomingProjectile(Projectile):
    """Projectile that homes in on the nearest enemy"""
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float,
                 speed: float, damage: int, tower_type: str = "basic"):
        super().__init__(start_x, start_y, target_x, target_y, speed, damage, tower_type)
        self.size = 4
        self.color = (255, 0, 255)  # Magenta
        self.turning_speed = 0.1
        self.current_target = None
        self.max_distance = 500
    
    def update(self):
        """Update with homing behavior"""
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
    
    def update_homing(self, enemies: List):
        """Update homing behavior towards nearest enemy"""
        if not enemies:
            # Still move forward if no enemies
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.distance_traveled += self.speed
            
            # Check removal conditions
            if self.distance_traveled >= self.max_distance:
                self.should_remove = True
            return
        
        # Find nearest enemy
        nearest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        
        if nearest_enemy:
            # Calculate desired direction
            dx = nearest_enemy.x - self.x
            dy = nearest_enemy.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                desired_vel_x = (dx / distance) * self.speed
                desired_vel_y = (dy / distance) * self.speed
                
                # Gradually turn towards target
                self.velocity_x += (desired_vel_x - self.velocity_x) * self.turning_speed
                self.velocity_y += (desired_vel_y - self.velocity_y) * self.turning_speed
                
                # Normalize velocity to maintain speed
                vel_magnitude = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
                if vel_magnitude > 0:
                    self.velocity_x = (self.velocity_x / vel_magnitude) * self.speed
                    self.velocity_y = (self.velocity_y / vel_magnitude) * self.speed
        
        # Move projectile
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.distance_traveled += self.speed
        
        # Check removal conditions
        if self.distance_traveled >= self.max_distance:
            self.should_remove = True
        
        if self.x < -50 or self.x > 1250 or self.y < -50 or self.y > 850:
            self.should_remove = True
    
    def update_homing_with_speed(self, enemies: List, speed_multiplier: float):
        """Update homing behavior with speed multiplier for performance optimization"""
        if not enemies:
            # Still move forward if no enemies
            self.x += self.velocity_x * speed_multiplier
            self.y += self.velocity_y * speed_multiplier
            self.distance_traveled += self.speed * speed_multiplier
            
            # Check removal conditions
            if self.distance_traveled >= self.max_distance:
                self.should_remove = True
            return
        
        # Find nearest enemy
        nearest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        
        if nearest_enemy:
            # Calculate desired direction
            dx = nearest_enemy.x - self.x
            dy = nearest_enemy.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                desired_vel_x = (dx / distance) * self.speed
                desired_vel_y = (dy / distance) * self.speed
                
                # Gradually turn towards target
                self.velocity_x += (desired_vel_x - self.velocity_x) * self.turning_speed
                self.velocity_y += (desired_vel_y - self.velocity_y) * self.turning_speed
                
                # Normalize velocity to maintain speed
                vel_magnitude = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
                if vel_magnitude > 0:
                    self.velocity_x = (self.velocity_x / vel_magnitude) * self.speed
                    self.velocity_y = (self.velocity_y / vel_magnitude) * self.speed
        
        # Move projectile faster
        self.x += self.velocity_x * speed_multiplier
        self.y += self.velocity_y * speed_multiplier
        self.distance_traveled += self.speed * speed_multiplier
        
        # Check removal conditions
        if self.distance_traveled >= self.max_distance:
            self.should_remove = True
        
        if self.x < -50 or self.x > 1250 or self.y < -50 or self.y > 850:
            self.should_remove = True
    
    def check_collision(self, enemies: List) -> dict:
        """Check collision and apply damage"""
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance < (self.size + enemy.size):
                actual_damage = enemy.take_damage(self.damage, self.tower_type)
                self.should_remove = True
                return {'hit': True, 'damage': actual_damage, 'tower_id': self.source_tower_id}
        return {'hit': False, 'damage': 0, 'tower_id': None}
    
    def draw(self, screen: pygame.Surface):
        """Draw homing projectile with trail effect"""
        # Draw main projectile
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Draw trail
        trail_x = self.x - self.velocity_x * 0.5
        trail_y = self.y - self.velocity_y * 0.5
        pygame.draw.circle(screen, (128, 0, 128), (int(trail_x), int(trail_y)), self.size - 1) 