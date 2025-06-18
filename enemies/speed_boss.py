from .enemy import Enemy
import pygame
import math

class SpeedBoss(Enemy):
    """Boss that becomes faster as it takes damage"""
    
    def __init__(self, path):
        super().__init__(path)
        self.health = 800
        self.max_health = 800
        self.base_speed = 1.0
        self.speed = self.base_speed
        self.reward = 160
        self.color = (255, 255, 0)  # Yellow
        self.size = 18
        
        # Speed boost mechanics
        self.speed_multiplier = 1.0
        self.max_speed_multiplier = 4.0
        self.trail_positions = []  # For speed trail effect
        self.dash_timer = 0
        self.dash_cooldown = 240  # 4 seconds
        self.is_dashing = False
        self.dash_duration = 30  # 0.5 seconds
        
    def update(self):
        """Update with speed mechanics"""
        super().update()
        
        # Calculate speed multiplier based on health lost
        health_percentage = self.health / self.max_health
        self.speed_multiplier = 1.0 + (1.0 - health_percentage) * (self.max_speed_multiplier - 1.0)
        
        # Handle dash ability
        self.dash_timer += 1
        if self.dash_timer >= self.dash_cooldown and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = 0
            
        if self.is_dashing:
            if self.dash_timer < self.dash_duration:
                self.speed = self.base_speed * self.speed_multiplier * 3  # Triple speed during dash
            else:
                self.is_dashing = False
                self.speed = self.base_speed * self.speed_multiplier
        else:
            self.speed = self.base_speed * self.speed_multiplier
            
        # Update trail positions
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > 10:
            self.trail_positions.pop(0)
            
    def draw(self, screen):
        """Draw speed boss with trail effects"""
        # Draw speed trail
        for i, (trail_x, trail_y) in enumerate(self.trail_positions[:-1]):
            alpha = int(255 * (i / len(self.trail_positions)))
            trail_color = (255, 255, 0, alpha)
            trail_size = int(self.size * (0.3 + 0.7 * i / len(self.trail_positions)))
            
            # Create surface for trail with alpha
            trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (trail_size, trail_size), trail_size)
            screen.blit(trail_surface, (trail_x - trail_size, trail_y - trail_size))
        
        # Draw main boss
        boss_color = self.color
        if self.is_dashing:
            boss_color = (255, 255, 255)  # White during dash
            
        pygame.draw.circle(screen, boss_color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw speed indicators (lightning bolts)
        speed_level = int(self.speed_multiplier)
        for i in range(min(speed_level, 4)):
            bolt_x = self.x - self.size + 5 + i * 8
            bolt_y = self.y - self.size + 5
            self.draw_lightning_bolt(screen, bolt_x, bolt_y, 6)
        
        # Draw health bar
        bar_width = self.size * 2.5
        bar_height = 6
        
        pygame.draw.rect(screen, (100, 0, 0), 
                       (self.x - bar_width//2, self.y - self.size - 15, bar_width, bar_height))
        
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (255, 255, 0), 
                       (self.x - bar_width//2, self.y - self.size - 15, 
                        int(bar_width * health_percentage), bar_height))
        
        # Draw boss title
        font = pygame.font.Font(None, 20)
        title_text = font.render("SPEED BOSS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x, self.y - self.size - 25))
        screen.blit(title_text, title_rect)
        
    def draw_lightning_bolt(self, screen, x, y, size):
        """Draw a small lightning bolt indicator"""
        points = [
            (x, y),
            (x + size//2, y + size//3),
            (x + size//3, y + size//3),
            (x + size, y + size),
            (x + size//2, y + 2*size//3),
            (x + 2*size//3, y + 2*size//3),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points) 