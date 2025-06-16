import pygame
import math
from .base_tower import BaseTower

class FrostTower(BaseTower):
    def __init__(self, pos, config):
        super().__init__(pos, config)
        self.type = "frost"
        self.range = 120
        self.damage = 5
        self.cooldown = 1200  # milliseconds
        self.cost = 120
        self.slow_amount = 0.5  # 50% speed
        self.slow_duration = 2000  # milliseconds
        self.last_attack_time = 0

    def get_tower_color(self):
        return (100, 200, 255)

    def attack(self, enemies):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time < self.cooldown:
            return
        for enemy in enemies:
            dist = math.hypot(enemy.pos[0] - self.pos[0], enemy.pos[1] - self.pos[1])
            if dist <= self.range:
                enemy.health -= self.damage
                # Apply slow effect
                enemy.apply_slow(self.slow_amount, self.slow_duration)
                self.last_attack_time = now
                break

    def draw(self, screen):
        pygame.draw.circle(screen, self.get_tower_color(), (int(self.pos[0]), int(self.pos[1])), 18)
        pygame.draw.circle(screen, self.get_tower_color(), (int(self.pos[0]), int(self.pos[1])), self.range, 1)
        # Draw F for Frost
        font = pygame.font.Font(None, 24)
        text = font.render("F", True, (255, 255, 255))
        text_rect = text.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(text, text_rect) 