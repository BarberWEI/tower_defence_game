import pygame
import math

class Tower:
    def __init__(self, pos):
        self.pos = pos
        self.range = 150
        self.damage = 20
        self.cooldown = 30
        self.cooldown_timer = 0
        self.target = None
    
    def update(self, enemies):
        if self.cooldown_timer > 0:
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
            closest_enemy.health -= self.damage
            self.cooldown_timer = self.cooldown
    
    def draw(self, screen):
        # Draw tower base
        pygame.draw.circle(screen, (100, 100, 100), self.pos, 20)
        
        # Draw range circle (for debugging)
        pygame.draw.circle(screen, (100, 100, 100, 50), self.pos, self.range, 1)
        
        # Draw tower top
        pygame.draw.circle(screen, (150, 150, 150), self.pos, 15) 