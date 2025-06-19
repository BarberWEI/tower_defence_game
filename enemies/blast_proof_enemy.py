from typing import List, Tuple
from .enemy import Enemy
import pygame
import math

class BlastProofEnemy(Enemy):
    """Heavily reinforced enemy immune to explosive damage"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 25
        self.health = self.max_health
        self.speed = 0.7
        self.reward = 25
        self.size = 13
        self.color = (64, 64, 64)  # Dark gray
        
        # Force immunity to explosive towers
        self.immunities['explosive_immune'] = True
        self.immunities['cannon_immune'] = True  # Also immune to cannon
        self.immunities['missile_immune'] = True  # Also immune to missiles
        
        # Blast-proof properties
        self.armor_timer = 0
        self.armor_plates = 8
        self.blast_deflector_angle = 0
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement explosive immunity"""
        if tower_type in ['explosive', 'cannon', 'missile']:
            # Completely immune to explosive damage types
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def update(self):
        """Update with armor effects"""
        super().update()
        self.armor_timer += 0.1
        self.blast_deflector_angle += 2
    
    def draw(self, screen: pygame.Surface):
        """Draw blast-proof enemy with heavy armor"""
        # Draw main body
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw blast-resistant armor plates
        for i in range(self.armor_plates):
            angle = (i * 45) * math.pi / 180
            plate_x = self.x + math.cos(angle) * (self.size - 1)
            plate_y = self.y + math.sin(angle) * (self.size - 1)
            
            # Draw armor plate with rivets
            plate_size = 5
            pygame.draw.circle(screen, (100, 100, 100), (int(plate_x), int(plate_y)), plate_size)
            pygame.draw.circle(screen, (200, 200, 200), (int(plate_x), int(plate_y)), plate_size, 2)
            
            # Draw rivets on armor plate
            for j in range(3):
                rivet_angle = angle + (j - 1) * 0.3
                rivet_x = plate_x + math.cos(rivet_angle) * 2
                rivet_y = plate_y + math.sin(rivet_angle) * 2
                pygame.draw.circle(screen, (150, 150, 150), (int(rivet_x), int(rivet_y)), 1)
        
        # Draw central blast deflector
        deflector_size = 8
        deflector_points = []
        for i in range(6):
            angle = (i * 60 + self.blast_deflector_angle) * math.pi / 180
            point_x = self.x + math.cos(angle) * deflector_size
            point_y = self.y + math.sin(angle) * deflector_size
            deflector_points.append((int(point_x), int(point_y)))
        
        pygame.draw.polygon(screen, (150, 150, 150), deflector_points)
        pygame.draw.polygon(screen, (255, 255, 255), deflector_points, 2)
        
        # Draw reinforcement bands
        for ring_radius in [6, 9]:
            ring_thickness = 2
            pygame.draw.circle(screen, (80, 80, 80), (int(self.x), int(self.y)), ring_radius, ring_thickness)
        
        # Draw blast warning symbols
        warning_symbols = 4
        for i in range(warning_symbols):
            angle = (i * 90 + self.armor_timer * 10) * math.pi / 180
            symbol_x = self.x + math.cos(angle) * (self.size + 8)
            symbol_y = self.y + math.sin(angle) * (self.size + 8)
            
            # Draw warning triangle
            triangle_size = 3
            triangle_points = [
                (int(symbol_x), int(symbol_y - triangle_size)),
                (int(symbol_x - triangle_size), int(symbol_y + triangle_size)),
                (int(symbol_x + triangle_size), int(symbol_y + triangle_size))
            ]
            pygame.draw.polygon(screen, (255, 255, 0), triangle_points)
            pygame.draw.polygon(screen, (255, 0, 0), triangle_points, 1)
            
            # Draw "!" in center
            pygame.draw.circle(screen, (255, 0, 0), (int(symbol_x), int(symbol_y)), 1)
        
        # Draw blast impact marks (scorch marks from deflected explosions)
        for i in range(6):
            mark_angle = (i * 60 + self.armor_timer * 5) * math.pi / 180
            mark_x = self.x + math.cos(mark_angle) * (self.size + 3)
            mark_y = self.y + math.sin(mark_angle) * (self.size + 3)
            
            # Small burn marks
            pygame.draw.circle(screen, (40, 40, 40), (int(mark_x), int(mark_y)), 2)
            pygame.draw.circle(screen, (20, 20, 20), (int(mark_x), int(mark_y)), 1)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw wet effect overlay
        if self.wet:
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                drop_x = self.x + math.cos(rad) * (self.size + 3)
                drop_y = self.y + math.sin(rad) * (self.size + 3)
                pygame.draw.circle(screen, (30, 144, 255), (int(drop_x), int(drop_y)), 2)
        
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
        
        # Draw blast-proof indicator
        font = pygame.font.Font(None, 12)
        blast_text = font.render("BLAST", True, (255, 255, 0))
        text_rect = blast_text.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(blast_text, text_rect) 