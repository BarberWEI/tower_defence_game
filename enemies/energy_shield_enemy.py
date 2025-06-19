from typing import List, Tuple
from .enemy import Enemy
import pygame
import math

class EnergyShieldEnemy(Enemy):
    """Enemy with energy shields immune to laser damage"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 6
        self.health = self.max_health
        self.speed = 1.2
        self.reward = 18
        self.size = 10
        self.color = (0, 255, 255)  # Cyan
        
        # Force immunity to laser towers
        self.immunities['laser_immune'] = True
        
        # Shield properties
        self.shield_pulse_timer = 0
        self.shield_radius = 15
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement laser immunity"""
        if tower_type == 'laser':
            # Completely immune to laser damage
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def update(self):
        """Update with shield effects"""
        super().update()
        self.shield_pulse_timer += 0.15
    
    def draw(self, screen: pygame.Surface):
        """Draw enemy with energy shield effects"""
        # Draw pulsing energy shield
        shield_alpha = 100 + int(50 * math.sin(self.shield_pulse_timer))
        shield_size = self.shield_radius + int(3 * math.sin(self.shield_pulse_timer * 2))
        
        # Create shield surface with transparency
        shield_surface = pygame.Surface((shield_size * 2, shield_size * 2), pygame.SRCALPHA)
        shield_color = (0, 255, 255, shield_alpha)
        pygame.draw.circle(shield_surface, shield_color, (shield_size, shield_size), shield_size, 3)
        screen.blit(shield_surface, (self.x - shield_size, self.y - shield_size))
        
        # Draw main body
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw energy core
        core_pulse = int(3 + 2 * math.sin(self.shield_pulse_timer * 3))
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), core_pulse)
        
        # Draw shield generators around enemy
        for i in range(4):
            angle = (i * 90) * math.pi / 180
            gen_x = self.x + math.cos(angle) * 8
            gen_y = self.y + math.sin(angle) * 8
            pygame.draw.circle(screen, (0, 200, 255), (int(gen_x), int(gen_y)), 2)
        
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
        
        # Draw shield indicator
        font = pygame.font.Font(None, 12)
        shield_text = font.render("SHLD", True, (0, 255, 255))
        text_rect = shield_text.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(shield_text, text_rect) 