import pygame
import math

class BaseTower:
    def __init__(self, pos, config):
        self.pos = pos
        self.config = config
        self.cooldown_timer = 0
        self.target = None
        self.color = self.get_tower_color()
    
    def get_tower_color(self):
        return (100, 100, 100)  # Default gray color
    
    def update(self, enemies):
        if self.cooldown_timer > 0 and not self.continuous:
            self.cooldown_timer -= 1
            return
        
        # Find closest enemy in range
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((enemy.pos[0] - self.pos[0])**2 + 
                               (enemy.pos[1] - self.pos[1])**2)
            if distance <= self.range and distance < min_distance:
                closest_enemy = enemy
                min_distance = distance
        
        # Attack if enemy found
        if closest_enemy:
            self.attack(closest_enemy, enemies)
            if not self.continuous:
                self.cooldown_timer = self.cooldown
    
    def attack(self, target, enemies):
        # Base implementation - single target damage
        target.health -= self.damage
    
    def draw(self, screen):
        # Draw tower base
        pygame.draw.circle(screen, self.color, self.pos, 20)
        
        # Draw range circle (for debugging)
        pygame.draw.circle(screen, (*self.color, 50), self.pos, self.range, 1)
        
        # Draw tower top
        pygame.draw.circle(screen, (150, 150, 150), self.pos, 15)
        
        # Draw tower type indicator
        type_text = pygame.font.Font(None, 20).render(self.type[0].upper(), True, (255, 255, 255))
        text_rect = type_text.get_rect(center=self.pos)
        screen.blit(type_text, text_rect) 