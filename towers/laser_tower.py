from .base_tower import BaseTower
import pygame

class LaserTower(BaseTower):
    def __init__(self, pos, config):
        super().__init__(pos, config)
        self.type = 'laser'
        self.range = 200
        self.damage = 10
        self.cooldown = 5
        self.cost = 200
        self.continuous = True
    
    def get_tower_color(self):
        return (0, 255, 255)  # Cyan
    
    def draw(self, screen):
        super().draw(screen)
        # Draw laser beam if targeting
        if self.target:
            pygame.draw.line(screen, self.color, self.pos, self.target.pos, 2) 