from typing import List, Tuple
from .enemy import Enemy
import pygame
import math

class ArmoredEnemy(Enemy):
    """Heavily armored enemy immune to basic tower damage"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 8
        self.health = self.max_health
        self.speed = 0.8
        self.reward = 15
        self.size = 11
        self.color = (120, 120, 120)  # Steel gray
        
        # Force immunity to basic towers
        self.immunities['basic_immune'] = True
        
        # Armor properties
        self.armor_thickness = 3
        self.armor_segments = 6
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement basic tower immunity"""
        if tower_type == 'basic':
            # Completely immune to basic tower damage
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def draw(self, screen: pygame.Surface):
        """Draw armored enemy with armor plating"""
        # Draw main body
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw armor segments
        for i in range(self.armor_segments):
            angle = (i * 60) * math.pi / 180  # 6 segments at 60-degree intervals
            armor_x = self.x + math.cos(angle) * (self.size - 2)
            armor_y = self.y + math.sin(angle) * (self.size - 2)
            
            # Draw armor plate
            armor_size = 4
            pygame.draw.circle(screen, (80, 80, 80), (int(armor_x), int(armor_y)), armor_size)
            pygame.draw.circle(screen, (200, 200, 200), (int(armor_x), int(armor_y)), armor_size, 1)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw wet effect overlay
        if self.wet:
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                drop_x = self.x + math.cos(rad) * (self.size + 3)
                drop_y = self.y + math.sin(rad) * (self.size + 3)
                pygame.draw.circle(screen, (30, 144, 255), (int(drop_x), int(drop_y)), 2)
        
        # Draw health bar using the centralized method
        self.draw_health_bar(screen)
        
        # Draw armor indicator
        font = pygame.font.Font(None, 12)
        armor_text = font.render("ARM", True, (255, 255, 255))
        text_rect = armor_text.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(armor_text, text_rect) 