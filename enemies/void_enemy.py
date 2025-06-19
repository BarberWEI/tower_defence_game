from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class VoidEnemy(Enemy):
    """Void enemy that absorbs energy attacks - only vulnerable to explosives and missiles"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 40
        self.health = self.max_health
        self.speed = 0.8
        self.reward = 50
        self.size = 15
        self.color = (50, 0, 100)  # Dark purple
        
        # Void properties
        self.void_rotation = 0
        self.absorption_particles = []
        self.void_distortion = 0
        
        # Only explosives and missiles can damage this enemy
        self.absorbed_types = ['basic', 'sniper', 'cannon', 'freezer', 'poison', 
                              'laser', 'lightning', 'flame', 'ice', 'antiair', 'splash']
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Only explosive and missile towers can damage void enemies"""
        # Absorb most attack types
        if tower_type in self.absorbed_types:
            # Create absorption effect
            self.create_absorption_effect()
            return 0
        
        # Only explosive and missile can damage
        if tower_type not in ['explosive', 'missile']:
            self.create_absorption_effect()
            return 0
        
        # Use parent counter system for explosive/missile damage (gets 2.5x multiplier from config)
        actual_damage = super().take_damage(damage, tower_type)
        
        # Create void disruption when damaged
        self.create_void_disruption()
        return actual_damage
    
    def create_absorption_effect(self):
        """Create absorption effect when attacked by absorbed weapons"""
        for _ in range(6):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(20, 40)
            particle = {
                'x': self.x + math.cos(angle) * distance,
                'y': self.y + math.sin(angle) * distance,
                'target_x': self.x,
                'target_y': self.y,
                'life': random.randint(25, 40),
                'color': (random.randint(100, 200), random.randint(50, 150), random.randint(150, 255))
            }
            self.absorption_particles.append(particle)
    
    def create_void_disruption(self):
        """Create void disruption when damaged by effective weapons"""
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(15, 30),
                'color': (255, 100, 0)  # Orange explosion effect
            }
            self.absorption_particles.append({
                'x': particle['x'],
                'y': particle['y'],
                'target_x': particle['x'] + particle['dx'] * 10,
                'target_y': particle['y'] + particle['dy'] * 10,
                'life': particle['life'],
                'color': particle['color']
            })
    
    def update(self):
        """Update with void effects"""
        super().update()
        
        # Update void rotation and distortion
        self.void_rotation += 3
        self.void_distortion += 0.1
        
        # Update absorption particles
        for particle in self.absorption_particles[:]:
            if 'dx' in particle:
                # Expanding disruption particle
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['dx'] *= 0.95
                particle['dy'] *= 0.95
            else:
                # Absorption particle moving toward center
                dx = particle['target_x'] - particle['x']
                dy = particle['target_y'] - particle['y']
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance > 2:
                    speed = 3.0
                    particle['x'] += (dx / distance) * speed
                    particle['y'] += (dy / distance) * speed
                else:
                    # Particle reached center, remove it
                    particle['life'] = 0
            
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.absorption_particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw void enemy with absorption effects"""
        # Draw absorption particles
        for particle in self.absorption_particles:
            alpha = particle['life'] / 40.0
            if alpha > 0:
                particle_color = (int(particle['color'][0] * alpha), 
                                int(particle['color'][1] * alpha), 
                                int(particle['color'][2] * alpha))
                size = max(1, int(3 * alpha))
                pygame.draw.circle(screen, particle_color, 
                                 (int(particle['x']), int(particle['y'])), size)
        
        # Draw void distortion rings
        for i in range(3):
            ring_radius = self.size + i * 8 + int(math.sin(self.void_distortion + i) * 4)
            ring_alpha = 0.5 - i * 0.15
            if ring_alpha > 0:
                ring_color = (int(100 * ring_alpha), 0, int(200 * ring_alpha))
                pygame.draw.circle(screen, ring_color, (int(self.x), int(self.y)), ring_radius, 2)
        
        # Main void body with swirling effect
        void_points = []
        point_count = 8
        for i in range(point_count):
            angle = (i * 45 + self.void_rotation) * math.pi / 180
            radius = self.size + math.sin(self.void_distortion + i) * 3
            point_x = self.x + math.cos(angle) * radius
            point_y = self.y + math.sin(angle) * radius
            void_points.append((int(point_x), int(point_y)))
        
        if len(void_points) >= 3:
            # Draw void body
            pygame.draw.polygon(screen, self.color, void_points)
        
        # Draw void core
        core_size = self.size - 5 + int(math.sin(self.void_distortion * 2) * 2)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), core_size)
        
        # Draw void singularity point
        pygame.draw.circle(screen, (200, 0, 255), (int(self.x), int(self.y)), 2)
        
        # Draw health bar using centralized method
        self.draw_health_bar(screen)
        
        # Draw void immunity indicator
        font = pygame.font.Font(None, 10)
        immunity_text = font.render("VOID", True, (150, 0, 200))
        text_rect = immunity_text.get_rect(center=(self.x, self.y + self.size + 12))
        screen.blit(immunity_text, text_rect) 