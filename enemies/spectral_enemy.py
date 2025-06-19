from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class SpectralEnemy(Enemy):
    """Ghostly enemy that phases through physical attacks - only vulnerable to lightning and requires detection"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 25
        self.health = self.max_health
        self.speed = 1.5
        self.reward = 30
        self.size = 12
        self.color = (150, 150, 255, 128)  # Semi-transparent blue
        
        # Spectral properties
        self.invisible = True  # Requires detection
        self.phase_timer = 0
        self.phase_particles = []
        
        # Only lightning can damage this enemy
        self.spectral_immunities = ['basic', 'sniper', 'cannon', 'freezer', 'poison', 
                                   'laser', 'missile', 'flame', 'ice', 'antiair', 
                                   'explosive', 'splash']
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Only lightning towers can damage spectral enemies"""
        # Must be detected first
        if not hasattr(self, 'detected_by_detector') or not self.detected_by_detector:
            return 0
            
        # Only lightning towers can damage spectral enemies
        if tower_type != 'lightning':
            return 0
        
        # Use parent counter system for lightning damage
        return super().take_damage(damage, tower_type)
    
    def update(self):
        """Update with spectral effects"""
        super().update()
        
        # Update phase timer for visual effects
        self.phase_timer += 0.1
        
        # Create phase particles
        if random.random() < 0.3:
            particle = {
                'x': self.x + random.uniform(-self.size, self.size),
                'y': self.y + random.uniform(-self.size, self.size),
                'life': random.randint(20, 40),
                'color': (100, 100, 255)
            }
            self.phase_particles.append(particle)
        
        # Update particles
        for particle in self.phase_particles[:]:
            particle['life'] -= 1
            particle['y'] -= 0.5  # Float upward
            if particle['life'] <= 0:
                self.phase_particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw spectral enemy with ghostly effects"""
        # Draw phase particles
        for particle in self.phase_particles:
            alpha = particle['life'] / 40.0
            if alpha > 0:
                particle_color = (int(particle['color'][0] * alpha), 
                                int(particle['color'][1] * alpha), 
                                int(particle['color'][2] * alpha))
                pygame.draw.circle(screen, particle_color, 
                                 (int(particle['x']), int(particle['y'])), 2)
        
        # Main spectral body with pulsing effect
        pulse = math.sin(self.phase_timer) * 0.3 + 0.7
        body_color = (int(150 * pulse), int(150 * pulse), int(255 * pulse))
        
        # Draw multiple overlapping circles for ghostly effect
        for i in range(3):
            alpha = (3 - i) / 3.0 * pulse
            size = self.size - i * 2
            if size > 0:
                circle_color = (int(body_color[0] * alpha), 
                              int(body_color[1] * alpha), 
                              int(body_color[2] * alpha))
                pygame.draw.circle(screen, circle_color, (int(self.x), int(self.y)), size)
        
        # Draw spectral aura
        aura_radius = self.size + 5 + int(math.sin(self.phase_timer * 2) * 3)
        pygame.draw.circle(screen, (100, 100, 255), (int(self.x), int(self.y)), aura_radius, 1)
        
        # Draw detection status
        if hasattr(self, 'detected_by_detector') and self.detected_by_detector:
            # Draw detection indicator
            detection_color = (255, 255, 0)
            pygame.draw.circle(screen, detection_color, (int(self.x), int(self.y - self.size - 5)), 3)
        
        # Draw health bar using centralized method if detected
        if hasattr(self, 'detected_by_detector') and self.detected_by_detector:
            self.draw_health_bar(screen)
        
        # Draw spectral immunity indicator
        font = pygame.font.Font(None, 10)
        immunity_text = font.render("SPECTRAL", True, (150, 150, 255))
        text_rect = immunity_text.get_rect(center=(self.x, self.y + self.size + 12))
        screen.blit(immunity_text, text_rect) 