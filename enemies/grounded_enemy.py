from typing import List, Tuple
from .enemy import Enemy
import pygame
import math

class GroundedEnemy(Enemy):
    """Electrically grounded enemy immune to lightning damage"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 20
        self.health = self.max_health
        self.speed = 0.9
        self.reward = 16
        self.size = 12
        self.color = (139, 69, 19)  # Brown/earthy
        
        # Force immunity to lightning towers
        self.immunities['lightning_immune'] = True
        
        # Grounding properties
        self.spark_timer = 0
        self.ground_spikes = 8
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement lightning immunity"""
        if tower_type == 'lightning':
            # Completely immune to lightning damage
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def update(self):
        """Update with grounding effects"""
        super().update()
        self.spark_timer += 0.2
    
    def draw(self, screen: pygame.Surface):
        """Draw grounded enemy with electrical grounding effects"""
        # Draw main body
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw grounding spikes extending from enemy
        for i in range(self.ground_spikes):
            angle = (i * 45) * math.pi / 180
            spike_length = 8 + int(3 * math.sin(self.spark_timer + i))
            spike_x = self.x + math.cos(angle) * spike_length
            spike_y = self.y + math.sin(angle) * spike_length
            
            # Draw grounding spike
            pygame.draw.line(screen, (160, 82, 45), 
                           (int(self.x), int(self.y)), 
                           (int(spike_x), int(spike_y)), 2)
            
            # Draw spike tip
            pygame.draw.circle(screen, (200, 100, 50), (int(spike_x), int(spike_y)), 2)
        
        # Draw central grounding conductor
        pygame.draw.circle(screen, (100, 50, 25), (int(self.x), int(self.y)), 6)
        pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), 3)  # Copper core
        
        # Draw occasional spark discharge (grounding effect)
        if int(self.spark_timer * 10) % 30 < 5:  # Spark every 3 seconds for 0.5 seconds
            for i in range(3):
                spark_angle = (i * 120 + self.spark_timer * 50) * math.pi / 180
                spark_x = self.x + math.cos(spark_angle) * (self.size + 5)
                spark_y = self.y + math.sin(spark_angle) * (self.size + 5)
                pygame.draw.circle(screen, (255, 255, 0), (int(spark_x), int(spark_y)), 1)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw wet effect overlay
        if self.wet:
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
        
        # Draw grounding indicator
        font = pygame.font.Font(None, 12)
        ground_text = font.render("GND", True, (255, 215, 0))
        text_rect = ground_text.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(ground_text, text_rect) 