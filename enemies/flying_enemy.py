from .enemy import Enemy
import pygame
import math

class FlyingEnemy(Enemy):
    """Enemy that flies and can only be hit by anti-air towers"""
    
    def __init__(self, path, wave_number=1):
        super().__init__(path, wave_number)
        self.health = 40
        self.max_health = 40
        self.speed = 2.0
        self.reward = 10
        self.color = (255, 165, 0)  # Orange
        self.flying = True
        self.hover_offset = 0  # For hovering animation
        
    def update(self):
        """Update flying enemy with hovering animation"""
        super().update()
        self.hover_offset += 0.2
        
    def draw(self, screen):
        """Draw the flying enemy with hovering effect"""
        # Calculate hover position
        hover_y = self.y + math.sin(self.hover_offset) * 3
        
        # Draw shadow on ground
        shadow_color = (50, 50, 50, 100)
        pygame.draw.ellipse(screen, shadow_color, 
                          (self.x - 6, self.y - 3, 12, 6))
        
        # Draw flying enemy (elevated)
        pygame.draw.circle(screen, self.color, (int(self.x), int(hover_y - 10)), 8)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(hover_y - 10)), 8, 2)
        
        # Draw wings
        wing_color = (200, 200, 200)
        pygame.draw.ellipse(screen, wing_color, 
                          (self.x - 12, hover_y - 15, 8, 4))
        pygame.draw.ellipse(screen, wing_color, 
                          (self.x + 4, hover_y - 15, 8, 4))
        
        # Draw health bar using centralized method with hover offset
        # Temporarily adjust y position for health bar calculation
        original_y = self.y
        self.y = hover_y - 10  # Set to the actual drawn position
        self.draw_health_bar(screen, y_offset=-7)  # Additional offset to clear wings
        self.y = original_y  # Restore original position
    
    def can_be_hit_by_tower(self, tower_type):
        """Check if this flying enemy can be hit by a tower type"""
        return tower_type in ["antiair", "sniper"]  # Only anti-air and sniper can hit flying 