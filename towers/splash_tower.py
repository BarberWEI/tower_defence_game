import math
from .base_tower import BaseTower
import pygame

class SplashTower(BaseTower):
    def __init__(self, pos, config):
        super().__init__(pos, config)
        self.type = 'splash'
        self.range = 100
        self.damage = 15
        self.cooldown = 45
        self.cost = 150
        self.splash_radius = 50
        self.continuous = False
    
    def get_tower_color(self):
        return (255, 255, 0)  # Yellow
    
    def attack(self, target, enemies):
        # Deal splash damage to all enemies in radius
        for enemy in enemies:
            distance = math.sqrt((enemy.pos[0] - target.pos[0])**2 + 
                               (enemy.pos[1] - target.pos[1])**2)
            if distance <= self.splash_radius:
                enemy.health -= self.damage
    
    def draw(self, screen):
        super().draw(screen)
        # Draw splash radius
        pygame.draw.circle(screen, (*self.color, 30), self.pos, self.splash_radius, 1) 