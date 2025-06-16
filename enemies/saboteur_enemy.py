import pygame
from .base_enemy import BaseEnemy
import math

class SaboteurEnemy(BaseEnemy):
    def __init__(self, path, config):
        super().__init__(path, config)
        self.type = "saboteur"
        self.health = int(config.enemy_base_health * 0.8)
        self.max_health = self.health
        self.speed = config.enemy_base_speed * 1.1
        self.reward = int(config.enemy_reward * 2)
        self.sabotage_radius = 40
        self.sabotage_damage = 20
        self.sabotage_cooldown = 1500  # ms
        self.last_sabotage_time = 0

    def get_enemy_color(self):
        return (0, 100, 0)

    def update(self, towers=None):
        super().update()
        if towers is not None:
            now = pygame.time.get_ticks()
            if now - self.last_sabotage_time >= self.sabotage_cooldown:
                for tower in towers:
                    dist = math.hypot(self.pos[0] - tower.pos[0], self.pos[1] - tower.pos[1])
                    if dist <= self.sabotage_radius:
                        if hasattr(tower, 'health'):
                            tower.health -= self.sabotage_damage
                        self.last_sabotage_time = now
                        break

    def draw(self, screen):
        pygame.draw.circle(screen, self.get_enemy_color(), (int(self.pos[0]), int(self.pos[1])), 16)
        pygame.draw.circle(screen, (0, 200, 0), (int(self.pos[0]), int(self.pos[1])), self.sabotage_radius, 1)
        # Draw S for Saboteur
        font = pygame.font.Font(None, 24)
        text = font.render("S", True, (255, 255, 255))
        text_rect = text.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(text, text_rect) 