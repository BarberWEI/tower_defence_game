from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class FireElementalEnemy(Enemy):
    """Fire elemental enemy immune to flame damage"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 25
        self.health = self.max_health
        self.speed = 1.3
        self.reward = 20
        self.size = 10
        self.color = (255, 100, 0)  # Orange-red
        
        # Force immunity to flame towers
        self.immunities['flame_immune'] = True
        
        # Fire properties
        self.flame_timer = 0
        self.flame_particles = []
        self.heat_intensity = 1.0
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement flame immunity"""
        if tower_type == 'flame':
            # Completely immune to flame damage - actually heals slightly
            self.health = min(self.max_health, self.health + 1)
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def update(self):
        """Update with fire effects"""
        super().update()
        self.flame_timer += 0.3
        
        # Generate flame particles
        if len(self.flame_particles) < 15:
            for _ in range(2):
                particle = {
                    'x': self.x + random.uniform(-5, 5),
                    'y': self.y + random.uniform(-5, 5),
                    'life': random.uniform(10, 20),
                    'max_life': 20,
                    'size': random.uniform(2, 4)
                }
                self.flame_particles.append(particle)
        
        # Update flame particles
        for particle in self.flame_particles[:]:
            particle['life'] -= 1
            particle['y'] -= 1  # Rise up
            particle['x'] += random.uniform(-0.5, 0.5)  # Flicker
            
            if particle['life'] <= 0:
                self.flame_particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw fire elemental with flame effects"""
        # Draw flame particles first (behind enemy)
        for particle in self.flame_particles:
            life_ratio = particle['life'] / particle['max_life']
            
            # Color shifts from white to yellow to red as particle dies
            if life_ratio > 0.7:
                color = (255, 255, 255)  # White hot
            elif life_ratio > 0.4:
                color = (255, 255, 0)    # Yellow
            else:
                color = (255, int(100 * life_ratio), 0)  # Red
            
            alpha = int(255 * life_ratio)
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*color, alpha), 
                             (int(particle['size']), int(particle['size'])), int(particle['size']))
            screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Draw main body with flickering fire effect
        fire_intensity = 0.8 + 0.2 * math.sin(self.flame_timer)
        fire_size = int(self.size * fire_intensity)
        
        # Multiple flame layers for depth
        flame_colors = [
            (255, 255, 255),  # White core
            (255, 255, 0),    # Yellow
            (255, 150, 0),    # Orange
            (255, 50, 0)      # Red outer
        ]
        
        for i, flame_color in enumerate(flame_colors):
            layer_size = fire_size - i * 2
            if layer_size > 0:
                pygame.draw.circle(screen, flame_color, (int(self.x), int(self.y)), layer_size)
        
        # Draw flickering outer flames
        for i in range(8):
            angle = (i * 45 + self.flame_timer * 30) * math.pi / 180
            flame_length = 8 + int(4 * math.sin(self.flame_timer + i))
            flame_x = self.x + math.cos(angle) * flame_length
            flame_y = self.y + math.sin(angle) * flame_length
            
            # Draw flame tongue
            flame_points = [
                (int(self.x), int(self.y)),
                (int(flame_x), int(flame_y)),
                (int(flame_x + math.cos(angle + 0.5) * 3), int(flame_y + math.sin(angle + 0.5) * 3)),
                (int(flame_x + math.cos(angle - 0.5) * 3), int(flame_y + math.sin(angle - 0.5) * 3))
            ]
            pygame.draw.polygon(screen, (255, 100, 0), flame_points)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw health bar
        if self.health < self.max_health:
            bar_width = self.size * 2
            bar_height = 4
            bar_x = int(self.x - bar_width // 2)
            bar_y = int(self.y - self.size - 8)
            
            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Health (green)
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Draw fire indicator
        font = pygame.font.Font(None, 12)
        fire_text = font.render("FIRE", True, (255, 255, 0))
        text_rect = fire_text.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(fire_text, text_rect) 