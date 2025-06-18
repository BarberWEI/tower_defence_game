import pygame
from typing import List, Tuple
from .enemy import Enemy

class ShieldedEnemy(Enemy):
    """Enemy with regenerating shields"""
    def __init__(self, path: List[Tuple[int, int]]):
        super().__init__(path)
        self.max_health = 2
        self.health = self.max_health
        self.max_shield = 2
        self.shield = self.max_shield
        self.shield_regen_timer = 0
        self.shield_regen_delay = 180  # 3 seconds at 60 FPS
        self.speed = 1.2
        self.reward = 10
        self.size = 10
        self.color = (0, 255, 255)  # Cyan
    
    def update(self):
        """Update with shield regeneration"""
        super().update()
        
        # Regenerate shield
        if self.shield < self.max_shield:
            self.shield_regen_timer += 1
            if self.shield_regen_timer >= self.shield_regen_delay:
                self.shield += 1
                self.shield_regen_timer = 0
    
    def take_damage(self, damage: int):
        """Damage goes to shield first, then health"""
        original_total_hp = self.shield + self.health
        
        if self.shield > 0:
            self.shield -= damage
            if self.shield < 0:
                self.health += self.shield  # Overflow damage to health
                self.shield = 0
            self.shield_regen_timer = 0  # Reset regen timer when hit
        else:
            self.health -= damage
        
        # Calculate actual damage dealt
        new_total_hp = max(0, self.shield + self.health)
        actual_damage = original_total_hp - new_total_hp
        return actual_damage
    
    def draw(self, screen: pygame.Surface):
        """Draw enemy with shield indicator"""
        super().draw(screen)
        
        # Draw shield bar
        if self.shield > 0:
            bar_width = self.size * 2
            bar_height = 3
            bar_x = int(self.x - bar_width // 2)
            bar_y = int(self.y - self.size - 15)
            
            # Shield background
            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            
            # Shield amount
            shield_width = int((self.shield / self.max_shield) * bar_width)
            pygame.draw.rect(screen, (0, 255, 255), (bar_x, bar_y, shield_width, bar_height)) 