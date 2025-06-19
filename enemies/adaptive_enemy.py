from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class AdaptiveEnemy(Enemy):
    """Adaptive enemy that changes camouflage - only vulnerable to sniper and ice towers"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 45
        self.health = self.max_health
        self.speed = 1.1
        self.reward = 60
        self.size = 16
        self.color = (128, 128, 128)  # Base gray
        
        # Adaptive properties
        self.adaptation_timer = 0
        self.adaptation_interval = 180  # 3 seconds at 60 FPS
        self.current_adaptation = 0
        self.adaptation_particles = []
        self.camouflage_cycle = 0
        
        # Adaptation patterns (each represents different immunities)
        self.adaptations = [
            {'color': (255, 100, 100), 'name': 'FIRE', 'immune_to': ['basic', 'cannon', 'poison', 'lightning']},
            {'color': (100, 255, 100), 'name': 'NATURE', 'immune_to': ['laser', 'missile', 'flame', 'explosive']},
            {'color': (100, 100, 255), 'name': 'WATER', 'immune_to': ['freezer', 'splash', 'antiair', 'basic']},
            {'color': (255, 255, 100), 'name': 'ENERGY', 'immune_to': ['lightning', 'laser', 'cannon', 'poison']},
            {'color': (255, 100, 255), 'name': 'VOID', 'immune_to': ['missile', 'explosive', 'flame', 'antiair']}
        ]
        
        # Only sniper and ice can always damage this enemy
        self.vulnerable_to = ['sniper', 'ice']
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Only sniper and ice towers can damage adaptive enemies"""
        # Always vulnerable to sniper and ice - use counter system
        if tower_type in self.vulnerable_to:
            actual_damage = super().take_damage(damage, tower_type)
            self.create_damage_particles()
            return actual_damage
        
        # Check current adaptation immunity
        current_adapt = self.adaptations[self.current_adaptation]
        if tower_type in current_adapt['immune_to']:
            # Create adaptation reflection effect
            self.create_adaptation_reflection()
            return 0
        
        # Not immune to this tower type in current adaptation - use counter system
        actual_damage = super().take_damage(damage, tower_type)
        self.create_damage_particles()
        return actual_damage
    
    def create_adaptation_reflection(self):
        """Create reflection effect when adapted against an attack"""
        current_adapt = self.adaptations[self.current_adaptation]
        for _ in range(6):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 6)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(15, 25),
                'color': current_adapt['color']
            }
            self.adaptation_particles.append(particle)
    
    def create_damage_particles(self):
        """Create damage effect when successfully hit"""
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(10, 20),
                'color': (255, 255, 255)  # White damage particles
            }
            self.adaptation_particles.append(particle)
    
    def create_adaptation_change_effect(self):
        """Create visual effect when changing adaptations"""
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 8)
            old_color = self.adaptations[self.current_adaptation]['color']
            new_color = self.adaptations[(self.current_adaptation + 1) % len(self.adaptations)]['color']
            
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(20, 35),
                'color': random.choice([old_color, new_color])
            }
            self.adaptation_particles.append(particle)
    
    def update(self):
        """Update with adaptive effects"""
        super().update()
        
        # Update adaptation timer
        self.adaptation_timer += 1
        self.camouflage_cycle += 0.1
        
        # Change adaptation periodically
        if self.adaptation_timer >= self.adaptation_interval:
            self.create_adaptation_change_effect()
            self.current_adaptation = (self.current_adaptation + 1) % len(self.adaptations)
            self.adaptation_timer = 0
        
        # Update adaptation particles
        for particle in self.adaptation_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            particle['dx'] *= 0.96  # Friction
            particle['dy'] *= 0.96
            
            if particle['life'] <= 0:
                self.adaptation_particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw adaptive enemy with current adaptation"""
        # Draw adaptation particles
        for particle in self.adaptation_particles:
            alpha = particle['life'] / 35.0
            if alpha > 0:
                particle_color = (int(particle['color'][0] * alpha), 
                                int(particle['color'][1] * alpha), 
                                int(particle['color'][2] * alpha))
                size = max(1, int(3 * alpha))
                pygame.draw.circle(screen, particle_color, 
                                 (int(particle['x']), int(particle['y'])), size)
        
        # Get current adaptation
        current_adapt = self.adaptations[self.current_adaptation]
        
        # Draw adaptation aura
        adaptation_progress = self.adaptation_timer / self.adaptation_interval
        aura_intensity = 1.0 - adaptation_progress  # Fade as adaptation time runs out
        
        aura_radius = self.size + 6 + int(math.sin(self.camouflage_cycle * 2) * 3)
        aura_color = current_adapt['color']
        if aura_intensity > 0:
            faded_aura = (int(aura_color[0] * aura_intensity), 
                         int(aura_color[1] * aura_intensity), 
                         int(aura_color[2] * aura_intensity))
            pygame.draw.circle(screen, faded_aura, (int(self.x), int(self.y)), aura_radius, 2)
        
        # Main adaptive body with color shifting
        body_color = current_adapt['color']
        pulse = math.sin(self.camouflage_cycle) * 0.3 + 0.7
        
        # Draw multiple layers for adaptive camouflage
        for i in range(3):
            layer_size = self.size - i * 2
            if layer_size > 0:
                alpha = (3 - i) / 3.0 * pulse
                layer_color = (int(body_color[0] * alpha), 
                              int(body_color[1] * alpha), 
                              int(body_color[2] * alpha))
                pygame.draw.circle(screen, layer_color, (int(self.x), int(self.y)), layer_size)
        
        # Draw adaptation pattern
        pattern_count = 6
        for i in range(pattern_count):
            angle = (i * 60 + self.camouflage_cycle * 20) * math.pi / 180
            pattern_x = self.x + math.cos(angle) * (self.size - 6)
            pattern_y = self.y + math.sin(angle) * (self.size - 6)
            pattern_color = (255 - body_color[0], 255 - body_color[1], 255 - body_color[2])  # Inverse color
            pygame.draw.circle(screen, pattern_color, (int(pattern_x), int(pattern_y)), 2)
        
        # Draw adaptation timer indicator
        timer_progress = self.adaptation_timer / self.adaptation_interval
        timer_arc_end = int(360 * timer_progress)
        if timer_arc_end > 0:
            # Draw timer arc around enemy
            pygame.draw.arc(screen, (255, 255, 255), 
                          (int(self.x - self.size - 3), int(self.y - self.size - 3), 
                           (self.size + 3) * 2, (self.size + 3) * 2),
                          0, math.radians(timer_arc_end), 2)
        
        # Draw health bar using centralized method
        self.draw_health_bar(screen)
        
        # Draw current adaptation name
        font = pygame.font.Font(None, 10)
        adaptation_text = font.render(current_adapt['name'], True, current_adapt['color'])
        text_rect = adaptation_text.get_rect(center=(self.x, self.y + self.size + 12))
        screen.blit(adaptation_text, text_rect) 