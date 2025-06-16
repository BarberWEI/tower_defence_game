from .base_enemy import BaseEnemy
import pygame

class BossEnemy(BaseEnemy):
    def __init__(self, path, config):
        super().__init__(path, config)
        self.type = 'boss'
        self.health = int(config.enemy_base_health * 3.0)
        self.max_health = self.health
        self.speed = config.enemy_base_speed * 0.5
        self.reward = int(config.enemy_reward * 2.0)
    
    def get_enemy_color(self):
        return (255, 0, 255)  # Magenta
    
    def draw(self, screen):
        super().draw(screen)
        # Draw boss aura
        pygame.draw.circle(screen, (*self.color, 30), 
                         (int(self.pos[0]), int(self.pos[1])), 25) 