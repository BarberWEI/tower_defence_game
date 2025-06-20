from .enemy import Enemy
import pygame
import math
import random

class ShadowKing(Enemy):
    """Ultra powerful boss that manipulates shadows and dimensions"""
    
    def __init__(self, path, wave_number=1):
        super().__init__(path, wave_number)
        self.health = 4500
        self.max_health = 4500
        self.speed = 0.7
        self.reward = 850
        self.color = (30, 30, 30)  # Very dark gray
        self.size = 33
        
        # Shadow abilities
        self.phase_shift_timer = 0
        self.phase_shift_cooldown = 420  # 7 seconds
        self.phase_shift_active = False
        self.phase_shift_duration = 180  # 3 seconds
        
        # Shadow duplicate ability
        self.duplicate_timer = 0
        self.duplicate_cooldown = 600  # 10 seconds
        self.active_duplicates = []
        self.max_duplicates = 3
        
        # Darkness manipulation
        self.darkness_aura_radius = 120
        self.darkness_timer = 0
        self.darkness_interval = 90  # Every 1.5 seconds
        
        # Boss resistances
        self.damage_reduction = 0.65  # Takes 35% damage
        self.projectile_dodge_chance = 0.3  # 30% chance to dodge
        
        # Phase system
        self.phase = 1
        self.max_phases = 3
        
        # Visual effects
        self.shadow_particles = []
        self.transparency = 255  # Full opacity when not phased
        self.shadow_tendrils = []
        
    def update(self):
        """Update with shadow abilities"""
        # Update phase based on health
        health_percentage = self.health / self.max_health
        if health_percentage > 0.66:
            self.phase = 1
        elif health_percentage > 0.33:
            self.phase = 2  
        else:
            self.phase = 3
            
        super().update()
        
        # Update ability timers
        self.phase_shift_timer += 1
        self.duplicate_timer += 1
        self.darkness_timer += 1
        
        # Handle phase shift
        if self.phase_shift_active:
            self.phase_shift_duration -= 1
            self.transparency = 100  # Semi-transparent when phased
            if self.phase_shift_duration <= 0:
                self.phase_shift_active = False
                self.transparency = 255
        
        # Trigger abilities
        self.update_shadow_abilities()
        self.update_shadow_particles()
        
    def update_shadow_abilities(self):
        """Update shadow-based abilities"""
        # Phase shift ability
        if self.phase_shift_timer >= self.phase_shift_cooldown:
            self.activate_phase_shift()
        
        # Shadow duplicate ability
        if (self.duplicate_timer >= self.duplicate_cooldown and 
            len(self.active_duplicates) < self.max_duplicates):
            self.create_shadow_duplicate()
        
        # Darkness aura
        if self.darkness_timer >= self.darkness_interval:
            self.pulse_darkness()
            self.darkness_timer = 0
    
    def activate_phase_shift(self):
        """Enter shadow dimension - become harder to hit"""
        self.phase_shift_active = True
        self.phase_shift_duration = 180
        self.phase_shift_timer = 0
        
        # Create phase shift effect
        for _ in range(25):
            particle = {
                'x': self.x + random.uniform(-self.size, self.size),
                'y': self.y + random.uniform(-self.size, self.size),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 50,
                'max_life': 50,
                'color': (100, 0, 200),  # Purple shadow
                'type': 'phase_shift'
            }
            self.shadow_particles.append(particle)
    
    def create_shadow_duplicate(self):
        """Create a shadow duplicate"""
        duplicate_x = self.x + random.uniform(-80, 80)
        duplicate_y = self.y + random.uniform(-80, 80)
        
        duplicate = {
            'x': duplicate_x,
            'y': duplicate_y,
            'life': 300,  # 5 seconds
            'max_life': 300,
            'size': self.size * 0.7,
            'alpha': 150
        }
        
        self.active_duplicates.append(duplicate)
        self.duplicate_timer = 0
    
    def pulse_darkness(self):
        """Create expanding ring of darkness"""
        for i in range(12):
            angle = (i * 30) * math.pi / 180
            particle = {
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * 4,
                'vy': math.sin(angle) * 4,
                'life': 60,
                'max_life': 60,
                'color': (20, 20, 20),
                'type': 'darkness'
            }
            self.shadow_particles.append(particle)
    
    def update_shadow_particles(self):
        """Update shadow particle effects"""
        for particle in self.shadow_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Particle-specific behavior
            if particle['type'] == 'darkness':
                # Darkness particles expand outward
                particle['vx'] *= 1.05
                particle['vy'] *= 1.05
            
            if particle['life'] <= 0:
                self.shadow_particles.remove(particle)
        
        # Update duplicates
        for duplicate in self.active_duplicates[:]:
            duplicate['life'] -= 1
            if duplicate['life'] <= 0:
                self.active_duplicates.remove(duplicate)
    
    def should_create_duplicates(self):
        """Check if boss should create new duplicates"""
        return (self.duplicate_timer >= self.duplicate_cooldown and 
                len(self.active_duplicates) < self.max_duplicates)
    
    def take_damage(self, damage, tower_type: str = 'basic'):
        """Take damage with shadow resistances"""
        # Increased dodge chance when phase shifted
        dodge_chance = self.projectile_dodge_chance
        if self.phase_shift_active:
            dodge_chance = 0.7  # 70% dodge when phased
        
        if random.random() < dodge_chance:
            return 0  # Dodged the attack
        
        # Apply damage reduction
        reduced_damage = damage * (1 - self.damage_reduction)
        actual_damage = min(reduced_damage, self.health)
        
        self.health -= reduced_damage
        return actual_damage
    
    def draw(self, screen):
        """Draw the Shadow King with shadow effects"""
        # Draw darkness aura
        aura_alpha = 80 if not self.phase_shift_active else 40
        aura_surface = pygame.Surface((self.darkness_aura_radius * 2, 
                                     self.darkness_aura_radius * 2), 
                                     pygame.SRCALPHA)
        pygame.draw.circle(aura_surface, (0, 0, 0, aura_alpha), 
                         (self.darkness_aura_radius, self.darkness_aura_radius), 
                         self.darkness_aura_radius)
        screen.blit(aura_surface, (self.x - self.darkness_aura_radius, 
                                  self.y - self.darkness_aura_radius))
        
        # Draw shadow particles
        for particle in self.shadow_particles:
            alpha = particle['life'] / particle['max_life']
            size = max(1, int(6 * alpha))
            color = list(particle['color'])
            
            pygame.draw.circle(screen, color, 
                             (int(particle['x']), int(particle['y'])), size)
        
        # Draw shadow duplicates
        for duplicate in self.active_duplicates:
            alpha = int(duplicate['alpha'] * (duplicate['life'] / duplicate['max_life']))
            duplicate_surface = pygame.Surface((duplicate['size'] * 2, duplicate['size'] * 2), 
                                             pygame.SRCALPHA)
            
            # Draw duplicate as semi-transparent shadow
            pygame.draw.circle(duplicate_surface, (50, 50, 50, alpha), 
                             (int(duplicate['size']), int(duplicate['size'])), 
                             int(duplicate['size']))
            
            screen.blit(duplicate_surface, 
                       (duplicate['x'] - duplicate['size'], 
                        duplicate['y'] - duplicate['size']))
        
        # Draw main boss with transparency effects
        boss_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        
        # Shadow King appearance - multiple shadow layers
        for i in range(3):
            layer_size = self.size - i * 3
            layer_alpha = int(self.transparency * (0.8 - i * 0.2))
            layer_color = (30 + i * 20, 30 + i * 20, 30 + i * 20, layer_alpha)
            
            pygame.draw.circle(boss_surface, layer_color, 
                             (self.size * 1.5, self.size * 1.5), layer_size)
        
        # Draw crown/spikes
        crown_points = []
        for i in range(8):
            angle = i * 45 * math.pi / 180
            spike_length = self.size + 10 if i % 2 == 0 else self.size + 5
            spike_x = self.size * 1.5 + math.cos(angle) * spike_length
            spike_y = self.size * 1.5 + math.sin(angle) * spike_length
            crown_points.append((int(spike_x), int(spike_y)))
        
        # Draw shadow crown
        for point in crown_points:
            pygame.draw.line(boss_surface, (100, 100, 100, self.transparency), 
                           (self.size * 1.5, self.size * 1.5), point, 3)
        
        # Blit the boss surface to screen
        screen.blit(boss_surface, (self.x - self.size * 1.5, self.y - self.size * 1.5))
        
        # Draw glowing eyes
        eye_color = (255, 0, 0) if self.phase < 3 else (255, 255, 0)  # Red eyes, yellow in final phase
        eye_alpha = self.transparency
        
        left_eye_x = self.x - 8
        right_eye_x = self.x + 8
        eye_y = self.y - 5
        
        eye_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(eye_surface, (*eye_color, eye_alpha), (3, 3), 3)
        
        screen.blit(eye_surface, (left_eye_x - 3, eye_y - 3))
        screen.blit(eye_surface, (right_eye_x - 3, eye_y - 3))
        
        # Draw health bar
        bar_width = self.size * 4
        bar_height = 12
        
        pygame.draw.rect(screen, (20, 20, 20), 
                       (self.x - bar_width//2, self.y - self.size - 30, bar_width, bar_height))
        
        health_percentage = self.health / self.max_health
        health_color = (100, 0, 100) if not self.phase_shift_active else (150, 0, 200)
        pygame.draw.rect(screen, health_color, 
                       (self.x - bar_width//2, self.y - self.size - 30, 
                        int(bar_width * health_percentage), bar_height))
        
        # Draw boss title
        font = pygame.font.Font(None, 28)
        phase_text = " (PHASED)" if self.phase_shift_active else ""
        title_text = font.render(f"SHADOW KING{phase_text}", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x, self.y - self.size - 50))
        screen.blit(title_text, title_rect) 