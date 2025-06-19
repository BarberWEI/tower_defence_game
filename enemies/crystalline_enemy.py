from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class CrystallineEnemy(Enemy):
    """Crystal enemy that reflects all attacks except laser beams"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 40
        self.health = self.max_health
        self.speed = 0.9
        self.reward = 40
        self.size = 13
        self.color = (200, 255, 255)  # Crystal blue
        
        # Crystal properties
        self.crystal_faces = 6
        self.rotation = 0
        self.reflection_particles = []
        
        # Only laser can damage this enemy
        self.crystal_immunities = ['basic', 'sniper', 'cannon', 'freezer', 'poison', 
                                  'lightning', 'missile', 'flame', 'ice', 'antiair', 
                                  'explosive', 'splash']
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Only laser towers can damage crystalline enemies"""
        # Only laser towers can penetrate crystal structure
        if tower_type != 'laser':
            # Create reflection particles when attacked
            self.create_reflection_particles()
            return 0
        
        # Use parent counter system for laser damage (gets 3x multiplier from config)
        actual_damage = super().take_damage(damage, tower_type)
        
        # Create shatter particles when damaged
        self.create_shatter_particles()
        return actual_damage
    
    def create_reflection_particles(self):
        """Create reflection effect when attacked by non-laser weapons"""
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 6)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(15, 25),
                'color': (255, 255, 255)
            }
            self.reflection_particles.append(particle)
    
    def create_shatter_particles(self):
        """Create crystal shatter effect when damaged by laser"""
        for _ in range(3):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(10, 20),
                'color': (200, 255, 255)
            }
            self.reflection_particles.append(particle)
    
    def update(self):
        """Update with crystal effects"""
        super().update()
        
        # Rotate crystal
        self.rotation += 2
        
        # Update reflection particles
        for particle in self.reflection_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            particle['dx'] *= 0.98  # Friction
            particle['dy'] *= 0.98
            
            if particle['life'] <= 0:
                self.reflection_particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw crystalline enemy with crystal structure"""
        # Draw reflection particles
        for particle in self.reflection_particles:
            alpha = particle['life'] / 25.0
            if alpha > 0:
                particle_color = (int(particle['color'][0] * alpha), 
                                int(particle['color'][1] * alpha), 
                                int(particle['color'][2] * alpha))
                pygame.draw.circle(screen, particle_color, 
                                 (int(particle['x']), int(particle['y'])), 2)
        
        # Draw crystal facets
        crystal_points = []
        for i in range(self.crystal_faces):
            angle = (i * 60 + self.rotation) * math.pi / 180
            point_x = self.x + math.cos(angle) * self.size
            point_y = self.y + math.sin(angle) * self.size
            crystal_points.append((int(point_x), int(point_y)))
        
        if len(crystal_points) >= 3:
            # Draw crystal body
            pygame.draw.polygon(screen, self.color, crystal_points)
            pygame.draw.polygon(screen, (150, 200, 255), crystal_points, 2)
        
        # Draw inner crystal core
        inner_points = []
        for i in range(self.crystal_faces):
            angle = (i * 60 - self.rotation) * math.pi / 180
            point_x = self.x + math.cos(angle) * (self.size - 4)
            point_y = self.y + math.sin(angle) * (self.size - 4)
            inner_points.append((int(point_x), int(point_y)))
        
        if len(inner_points) >= 3:
            pygame.draw.polygon(screen, (255, 255, 255), inner_points)
        
        # Draw crystal gleam
        gleam_offset = math.sin(self.rotation * math.pi / 180) * 3
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(self.x + gleam_offset), int(self.y - gleam_offset)), 2)
        
        # Draw health bar using centralized method
        self.draw_health_bar(screen)
        
        # Draw crystal immunity indicator
        font = pygame.font.Font(None, 10)
        immunity_text = font.render("CRYSTAL", True, (200, 255, 255))
        text_rect = immunity_text.get_rect(center=(self.x, self.y + self.size + 12))
        screen.blit(immunity_text, text_rect) 