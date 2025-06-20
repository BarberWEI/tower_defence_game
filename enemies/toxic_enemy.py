from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class ToxicEnemy(Enemy):
    """Toxic enemy immune to poison damage"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 30
        self.health = self.max_health
        self.speed = 1.1
        self.reward = 17
        self.size = 11
        self.color = (76, 175, 80)  # Toxic green
        
        # Force immunity to poison towers
        self.immunities['poison_immune'] = True
        
        # Toxic properties
        self.toxic_timer = 0
        self.toxic_bubbles = []
        self.poison_aura_radius = 20
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement poison immunity"""
        if tower_type == 'poison':
            # Completely immune to poison damage
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def update(self):
        """Update with toxic effects"""
        super().update()
        self.toxic_timer += 0.2
        
        # Generate toxic bubbles
        if len(self.toxic_bubbles) < 10:
            if random.random() < 0.3:  # 30% chance each frame
                bubble = {
                    'x': self.x + random.uniform(-8, 8),
                    'y': self.y + random.uniform(-8, 8),
                    'life': random.uniform(15, 30),
                    'max_life': 30,
                    'size': random.uniform(1, 3),
                    'float_speed': random.uniform(0.5, 1.5)
                }
                self.toxic_bubbles.append(bubble)
        
        # Update toxic bubbles
        for bubble in self.toxic_bubbles[:]:
            bubble['life'] -= 1
            bubble['y'] -= bubble['float_speed']  # Float up
            bubble['x'] += random.uniform(-0.3, 0.3)  # Drift
            
            if bubble['life'] <= 0:
                self.toxic_bubbles.remove(bubble)
    
    def draw(self, screen: pygame.Surface):
        """Draw toxic enemy with poison effects"""
        # Draw toxic aura
        aura_alpha = 50 + int(20 * math.sin(self.toxic_timer))
        aura_surface = pygame.Surface((self.poison_aura_radius * 2, self.poison_aura_radius * 2), pygame.SRCALPHA)
        aura_color = (76, 175, 80, aura_alpha)
        pygame.draw.circle(aura_surface, aura_color, 
                         (self.poison_aura_radius, self.poison_aura_radius), self.poison_aura_radius)
        screen.blit(aura_surface, (self.x - self.poison_aura_radius, self.y - self.poison_aura_radius))
        
        # Draw toxic bubbles
        for bubble in self.toxic_bubbles:
            life_ratio = bubble['life'] / bubble['max_life']
            bubble_alpha = int(150 * life_ratio)
            
            # Toxic green bubbles with varying opacity
            bubble_surface = pygame.Surface((bubble['size'] * 2, bubble['size'] * 2), pygame.SRCALPHA)
            bubble_color = (0, 255, 0, bubble_alpha)
            pygame.draw.circle(bubble_surface, bubble_color, 
                             (int(bubble['size']), int(bubble['size'])), int(bubble['size']))
            screen.blit(bubble_surface, (bubble['x'] - bubble['size'], bubble['y'] - bubble['size']))
        
        # Draw main body
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw toxic core with pulsing effect
        core_pulse = int(5 + 2 * math.sin(self.toxic_timer * 2))
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), core_pulse)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)
        
        # Draw poison symbols around enemy
        for i in range(6):
            angle = (i * 60 + self.toxic_timer * 20) * math.pi / 180
            symbol_x = self.x + math.cos(angle) * 8
            symbol_y = self.y + math.sin(angle) * 8
            
            # Draw small poison symbol (skull shape)
            pygame.draw.circle(screen, (0, 200, 0), (int(symbol_x), int(symbol_y)), 2)
            pygame.draw.circle(screen, (0, 100, 0), (int(symbol_x), int(symbol_y)), 1)
        
        # Draw dripping toxic effect
        drip_offset = int(3 * math.sin(self.toxic_timer))
        for i in range(3):
            drip_x = self.x + (i - 1) * 4
            drip_y = self.y + self.size + drip_offset
            pygame.draw.circle(screen, (0, 255, 0), (int(drip_x), int(drip_y)), 1)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw wet effect overlay (poison doesn't mix well with water)
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
        
        # Draw toxic indicator
        font = pygame.font.Font(None, 12)
        toxic_text = font.render("TOX", True, (0, 255, 0))
        text_rect = toxic_text.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(toxic_text, text_rect) 