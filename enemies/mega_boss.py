from .enemy import Enemy
import pygame
import math
import random

class MegaBoss(Enemy):
    """Massive boss enemy with multiple phases and abilities"""
    
    def __init__(self, path):
        super().__init__(path)
        self.health = 2000
        self.max_health = 2000
        self.speed = 0.5
        self.reward = 400
        self.color = (128, 0, 128)  # Purple
        self.size = 25
        
        # Boss-specific properties
        self.phase = 1
        self.max_phases = 3
        self.damage_reduction = 0.5  # Takes 50% less damage
        self.ability_timer = 0
        self.ability_cooldown = 300  # 5 seconds
        self.minion_spawn_timer = 0
        self.minion_spawn_cooldown = 600  # 10 seconds
        
        # Visual effects
        self.pulse_timer = 0
        self.aura_radius = 30
        
    def update(self):
        """Update boss with special abilities"""
        super().update()
        
        # Update phase based on health
        health_percentage = self.health / self.max_health
        if health_percentage > 0.66:
            self.phase = 1
        elif health_percentage > 0.33:
            self.phase = 2
        else:
            self.phase = 3
            
        # Update ability timers
        self.ability_timer += 1
        self.minion_spawn_timer += 1
        self.pulse_timer += 0.1
        
        # Phase-based speed increase
        self.speed = 0.5 + (self.phase - 1) * 0.2
        
    def take_damage(self, damage):
        """Take reduced damage"""
        reduced_damage = damage * (1 - self.damage_reduction)
        actual_damage = min(reduced_damage, self.health)  # Can't deal more than remaining health
        self.health -= reduced_damage
        return actual_damage
        
    def should_spawn_minions(self):
        """Check if boss should spawn minions"""
        if self.minion_spawn_timer >= self.minion_spawn_cooldown:
            self.minion_spawn_timer = 0
            return True
        return False
        
    def get_minion_count(self):
        """Get number of minions to spawn based on phase"""
        return self.phase * 2
        
    def draw(self, screen):
        """Draw the mega boss with phase-based effects"""
        # Draw pulsing aura
        aura_size = self.aura_radius + math.sin(self.pulse_timer) * 5
        aura_color = [128, 0, 128, 30]  # Semi-transparent purple
        
        # Phase-based aura color
        if self.phase == 2:
            aura_color = [255, 128, 0, 40]  # Orange
        elif self.phase == 3:
            aura_color = [255, 0, 0, 50]  # Red
            
        # Draw main boss body
        boss_color = self.color
        if self.phase == 2:
            boss_color = (255, 128, 0)  # Orange
        elif self.phase == 3:
            boss_color = (255, 0, 0)  # Red
            
        pygame.draw.circle(screen, boss_color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 3)
        
        # Draw phase indicators
        for i in range(self.phase):
            angle = (i * 120) * math.pi / 180
            indicator_x = self.x + math.cos(angle) * (self.size - 5)
            indicator_y = self.y + math.sin(angle) * (self.size - 5)
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(indicator_x), int(indicator_y)), 4)
        
        # Draw health bar (larger for boss)
        bar_width = self.size * 3
        bar_height = 8
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), 
                       (self.x - bar_width//2, self.y - self.size - 20, bar_width, bar_height))
        
        # Health
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                       (self.x - bar_width//2, self.y - self.size - 20, 
                        int(bar_width * health_percentage), bar_height))
        
        # Phase markers on health bar
        for i in range(1, self.max_phases):
            marker_x = self.x - bar_width//2 + (bar_width * (self.max_phases - i) / self.max_phases)
            pygame.draw.line(screen, (255, 255, 255), 
                           (marker_x, self.y - self.size - 20), 
                           (marker_x, self.y - self.size - 12), 2)
        
        # Draw boss title
        font = pygame.font.Font(None, 24)
        title_text = font.render("MEGA BOSS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x, self.y - self.size - 35))
        screen.blit(title_text, title_rect) 