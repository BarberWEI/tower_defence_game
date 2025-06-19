from typing import List, Tuple
from .enemy import Enemy
import pygame
import math

class PhaseShiftEnemy(Enemy):
    """Phasing enemy immune to sniper tower precision shots"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        super().__init__(path, wave_number)
        self.max_health = 4
        self.health = self.max_health
        self.speed = 1.4
        self.reward = 22
        self.size = 9
        self.color = (128, 0, 128)  # Purple
        
        # Force immunity to sniper towers
        self.immunities['sniper_immune'] = True
        
        # Phase properties
        self.phase_timer = 0
        self.phase_state = 0  # 0 = solid, 1 = phasing
        self.phase_cycle_duration = 120  # 2 seconds
        self.phase_duration = 30  # 0.5 seconds phased
        
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Override damage handling to implement sniper immunity"""
        if tower_type == 'sniper':
            # Completely immune to sniper damage (phases through)
            return 0
        
        # Take normal damage from other tower types
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage
    
    def update(self):
        """Update with phasing effects"""
        super().update()
        self.phase_timer += 1
        
        # Cycle between solid and phased states
        cycle_position = self.phase_timer % self.phase_cycle_duration
        if cycle_position < self.phase_duration:
            self.phase_state = 1  # Phasing
        else:
            self.phase_state = 0  # Solid
    
    def draw(self, screen: pygame.Surface):
        """Draw phase shift enemy with transparency effects"""
        # Calculate phase alpha based on state
        if self.phase_state == 1:  # Phasing
            phase_alpha = 100 + int(50 * math.sin(self.phase_timer * 0.3))
        else:  # Solid
            phase_alpha = 255
        
        # Draw main body with phase effects
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        # Create main body surface with alpha
        body_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        body_color = (*color, phase_alpha)
        pygame.draw.circle(body_surface, body_color, (self.size, self.size), self.size)
        screen.blit(body_surface, (self.x - self.size, self.y - self.size))
        
        # Draw phase ripples when phasing
        if self.phase_state == 1:
            for i in range(3):
                ripple_radius = self.size + (i + 1) * 5 + int(3 * math.sin(self.phase_timer * 0.4 + i))
                ripple_alpha = max(0, 80 - i * 30)
                
                ripple_surface = pygame.Surface((ripple_radius * 2, ripple_radius * 2), pygame.SRCALPHA)
                ripple_color = (128, 0, 128, ripple_alpha)
                pygame.draw.circle(ripple_surface, ripple_color, 
                                 (ripple_radius, ripple_radius), ripple_radius, 2)
                screen.blit(ripple_surface, (self.x - ripple_radius, self.y - ripple_radius))
        
        # Draw phase core with pulsing effect
        core_pulse = int(3 + 2 * math.sin(self.phase_timer * 0.2))
        core_surface = pygame.Surface((core_pulse * 2, core_pulse * 2), pygame.SRCALPHA)
        core_color = (255, 255, 255, phase_alpha)
        pygame.draw.circle(core_surface, core_color, (core_pulse, core_pulse), core_pulse)
        screen.blit(core_surface, (self.x - core_pulse, self.y - core_pulse))
        
        # Draw phase energy lines
        for i in range(6):
            angle = (i * 60 + self.phase_timer * 2) * math.pi / 180
            line_length = 12 + int(4 * math.sin(self.phase_timer * 0.3 + i))
            line_x = self.x + math.cos(angle) * line_length
            line_y = self.y + math.sin(angle) * line_length
            
            # Phase energy line with alpha
            line_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
            line_color = (200, 100, 200, phase_alpha // 2)
            pygame.draw.circle(line_surface, line_color, (1, 1), 1)
            screen.blit(line_surface, (line_x - 1, line_y - 1))
        
        # Draw dimensional tears when fully phasing
        if self.phase_state == 1 and phase_alpha < 150:
            for i in range(4):
                tear_angle = (i * 90 + self.phase_timer * 5) * math.pi / 180
                tear_x = self.x + math.cos(tear_angle) * 15
                tear_y = self.y + math.sin(tear_angle) * 15
                
                # Draw small dimensional tear
                pygame.draw.line(screen, (255, 0, 255), 
                               (int(tear_x - 3), int(tear_y)), 
                               (int(tear_x + 3), int(tear_y)), 1)
                pygame.draw.line(screen, (255, 0, 255), 
                               (int(tear_x), int(tear_y - 3)), 
                               (int(tear_x), int(tear_y + 3)), 1)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw wet effect overlay (water affects phasing)
        if self.wet:
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                drop_x = self.x + math.cos(rad) * (self.size + 3)
                drop_y = self.y + math.sin(rad) * (self.size + 3)
                drop_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                drop_color = (30, 144, 255, phase_alpha)
                pygame.draw.circle(drop_surface, drop_color, (2, 2), 2)
                screen.blit(drop_surface, (drop_x - 2, drop_y - 2))
        
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
        
        # Draw phase indicator
        font = pygame.font.Font(None, 12)
        phase_text = "PHASE" if self.phase_state == 1 else "SOLID"
        text_color = (255, 0, 255) if self.phase_state == 1 else (128, 0, 128)
        phase_display = font.render(phase_text, True, text_color)
        text_rect = phase_display.get_rect(center=(self.x, self.y + self.size + 8))
        screen.blit(phase_display, text_rect) 