from typing import List, Tuple
from .enemy import Enemy
import pygame
import math
import random

class ToxicMutantEnemy(Enemy):
    """Toxic mutant enemy immune to physical damage - only vulnerable to poison and flame"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 30
        self.health = self.max_health
        self.speed = 1.3
        self.reward = 35
        self.size = 14
        self.color = (100, 255, 50)  # Toxic green
        
        # Toxic properties
        self.mutation_timer = 0
        self.toxic_bubbles = []
        self.pulsation = 0
        
        # Only poison and flame can damage this enemy
        self.physical_immunities = ['basic', 'sniper', 'cannon', 'laser', 'lightning', 
                                   'missile', 'ice', 'antiair', 'explosive', 'splash']
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Only poison and flame towers can damage toxic mutants"""
        # Immune to all physical and energy attacks
        if tower_type in self.physical_immunities:
            # Create toxic splash when attacked
            self.create_toxic_splash()
            return 0
        
        # Only poison and flame can damage
        if tower_type not in ['poison', 'flame']:
            self.create_toxic_splash()
            return 0
        
        # Use parent counter system for poison/flame damage (gets 2x multiplier from config)
        actual_damage = super().take_damage(damage, tower_type)
        
        # Create mutation particles when damaged
        self.create_mutation_particles()
        return actual_damage
    
    def create_toxic_splash(self):
        """Create toxic splash effect when attacked by immune weapons"""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(20, 35),
                'color': (50, 200, 50)
            }
            self.toxic_bubbles.append(particle)
    
    def create_mutation_particles(self):
        """Create mutation effect when damaged by effective weapons"""
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(15, 25),
                'color': (200, 100, 50)  # Orange for flame/poison reaction
            }
            self.toxic_bubbles.append(particle)
    
    def update(self):
        """Update with toxic effects"""
        super().update()
        
        # Update mutation timer for visual effects
        self.mutation_timer += 0.15
        self.pulsation += 0.2
        
        # Create random toxic bubbles
        if random.random() < 0.2:
            bubble = {
                'x': self.x + random.uniform(-self.size/2, self.size/2),
                'y': self.y + random.uniform(-self.size/2, self.size/2),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-2, 0),
                'life': random.randint(30, 50),
                'color': (random.randint(50, 150), random.randint(200, 255), random.randint(50, 100))
            }
            self.toxic_bubbles.append(bubble)
        
        # Update toxic bubbles
        for bubble in self.toxic_bubbles[:]:
            bubble['x'] += bubble['dx']
            bubble['y'] += bubble['dy']
            bubble['life'] -= 1
            bubble['dy'] -= 0.1  # Gravity effect
            
            if bubble['life'] <= 0:
                self.toxic_bubbles.remove(bubble)
    
    def draw(self, screen: pygame.Surface):
        """Draw toxic mutant enemy with mutation effects"""
        # Draw toxic bubbles
        for bubble in self.toxic_bubbles:
            alpha = bubble['life'] / 50.0
            if alpha > 0:
                bubble_color = (int(bubble['color'][0] * alpha), 
                              int(bubble['color'][1] * alpha), 
                              int(bubble['color'][2] * alpha))
                size = max(1, int(3 * alpha))
                pygame.draw.circle(screen, bubble_color, 
                                 (int(bubble['x']), int(bubble['y'])), size)
        
        # Main toxic body with pulsing effect
        pulse = math.sin(self.pulsation) * 0.2 + 0.8
        body_size = int(self.size * pulse)
        
        # Draw multiple layers for toxic effect
        for i in range(3):
            layer_size = body_size - i * 2
            if layer_size > 0:
                alpha = (3 - i) / 3.0
                layer_color = (int(100 * alpha), int(255 * alpha), int(50 * alpha))
                pygame.draw.circle(screen, layer_color, (int(self.x), int(self.y)), layer_size)
        
        # Draw mutation spots
        spot_count = 4 + int(math.sin(self.mutation_timer) * 2)
        for i in range(spot_count):
            angle = (i * 360 / spot_count + self.mutation_timer * 10) * math.pi / 180
            spot_x = self.x + math.cos(angle) * (self.size - 4)
            spot_y = self.y + math.sin(angle) * (self.size - 4)
            spot_size = 2 + int(math.sin(self.mutation_timer + i) * 1)
            pygame.draw.circle(screen, (200, 100, 200), (int(spot_x), int(spot_y)), spot_size)
        
        # Draw toxic aura
        aura_radius = self.size + 8 + int(math.sin(self.mutation_timer * 2) * 4)
        pygame.draw.circle(screen, (50, 200, 50), (int(self.x), int(self.y)), aura_radius, 1)
        
        # Draw health bar using centralized method
        self.draw_health_bar(screen)
        
        # Draw toxic immunity indicator
        font = pygame.font.Font(None, 10)
        immunity_text = font.render("TOXIC", True, (100, 255, 50))
        text_rect = immunity_text.get_rect(center=(self.x, self.y + self.size + 12))
        screen.blit(immunity_text, text_rect) 