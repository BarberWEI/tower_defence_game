from .enemy import Enemy
import pygame
import math
import random

class TimeLordBoss(Enemy):
    """Ultra powerful boss that manipulates time and space"""
    
    def __init__(self, path, wave_number=1):
        super().__init__(path, wave_number)
        self.health = 4000
        self.max_health = 4000
        self.speed = 0.8
        self.reward = 800
        self.color = (75, 0, 130)  # Indigo
        self.size = 30
        
        # Time manipulation abilities
        self.time_distortion_active = False
        self.time_distortion_timer = 0
        self.time_distortion_duration = 180  # 3 seconds
        self.time_distortion_cooldown = 600  # 10 seconds
        self.time_distortion_radius = 150
        
        # Damage rewind ability
        self.damage_history = []  # Store recent damage taken
        self.rewind_timer = 0
        self.rewind_cooldown = 480  # 8 seconds
        self.rewind_amount = 0.3  # Rewinds 30% of recent damage
        
        # Temporal rift ability
        self.rift_timer = 0
        self.rift_cooldown = 720  # 12 seconds
        self.active_rifts = []
        
        # Boss resistances
        self.damage_reduction = 0.6  # Takes 40% damage
        self.magic_immunity_timer = 0  # Periods of magic immunity
        
        # Phase system
        self.phase = 1
        self.max_phases = 4
        
        # Visual effects
        self.time_particles = []
        self.aura_rotation = 0
        self.pulse_timer = 0
        
    def update(self):
        """Update with time manipulation abilities"""
        # Update phase based on health
        health_percentage = self.health / self.max_health
        if health_percentage > 0.75:
            self.phase = 1
        elif health_percentage > 0.5:
            self.phase = 2
        elif health_percentage > 0.25:
            self.phase = 3
        else:
            self.phase = 4  # Final phase - most dangerous
            
        # Phase-based speed and abilities
        self.speed = 0.8 + (self.phase - 1) * 0.15
        
        super().update()
        
        # Update ability timers
        self.time_distortion_timer += 1
        self.rewind_timer += 1
        self.rift_timer += 1
        self.aura_rotation += 2
        self.pulse_timer += 0.1
        
        # Update magic immunity (phase 3+)
        if self.phase >= 3:
            self.magic_immunity_timer += 1
        
        # Trigger abilities based on phase and timers
        self.update_time_abilities()
        
        # Update visual effects
        self.update_time_particles()
        self.update_temporal_rifts()
    
    def update_time_abilities(self):
        """Update time-based abilities"""
        # Time distortion ability
        if (self.time_distortion_timer >= self.time_distortion_cooldown and 
            not self.time_distortion_active):
            self.activate_time_distortion()
        
        if self.time_distortion_active:
            self.time_distortion_timer += 1
            if self.time_distortion_timer >= self.time_distortion_duration:
                self.deactivate_time_distortion()
        
        # Damage rewind ability (phase 2+)
        if (self.phase >= 2 and self.rewind_timer >= self.rewind_cooldown and 
            len(self.damage_history) > 0):
            self.activate_damage_rewind()
        
        # Temporal rift ability (phase 3+)
        if (self.phase >= 3 and self.rift_timer >= self.rift_cooldown):
            self.create_temporal_rift()
    
    def activate_time_distortion(self):
        """Slow down all projectiles and towers in range"""
        self.time_distortion_active = True
        self.time_distortion_timer = 0
        
        # Create time distortion particles
        for _ in range(20):
            particle = {
                'x': self.x + random.uniform(-self.time_distortion_radius, self.time_distortion_radius),
                'y': self.y + random.uniform(-self.time_distortion_radius, self.time_distortion_radius),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'life': 60,
                'max_life': 60,
                'color': (150, 0, 255)
            }
            self.time_particles.append(particle)
    
    def deactivate_time_distortion(self):
        """End time distortion effect"""
        self.time_distortion_active = False
        self.time_distortion_timer = 0
    
    def activate_damage_rewind(self):
        """Rewind recent damage taken"""
        if len(self.damage_history) > 0:
            # Calculate total recent damage
            recent_damage = sum(self.damage_history[-5:])  # Last 5 damage instances
            rewind_health = int(recent_damage * self.rewind_amount)
            
            # Restore health (but not above max)
            self.health = min(self.max_health, self.health + rewind_health)
            
            # Clear damage history
            self.damage_history = []
            self.rewind_timer = 0
            
            # Create rewind effect
            self.create_rewind_effect()
    
    def create_temporal_rift(self):
        """Create a temporal rift that spawns echo enemies"""
        # Create rift at random location near boss
        rift_x = self.x + random.uniform(-100, 100)
        rift_y = self.y + random.uniform(-100, 100)
        
        rift = {
            'x': rift_x,
            'y': rift_y,
            'life': 300,  # 5 seconds
            'spawn_timer': 0,
            'spawn_interval': 60,  # Spawn every second
            'radius': 25
        }
        
        self.active_rifts.append(rift)
        self.rift_timer = 0
    
    def update_temporal_rifts(self):
        """Update all active temporal rifts"""
        for rift in self.active_rifts[:]:
            rift['life'] -= 1
            rift['spawn_timer'] += 1
            
            if rift['life'] <= 0:
                self.active_rifts.remove(rift)
            elif rift['spawn_timer'] >= rift['spawn_interval']:
                # This would spawn an echo enemy in the game
                rift['spawn_timer'] = 0
    
    def should_spawn_echoes(self):
        """Check if rifts should spawn echo enemies"""
        spawnable_rifts = []
        for rift in self.active_rifts:
            if rift['spawn_timer'] >= rift['spawn_interval']:
                spawnable_rifts.append(rift)
                rift['spawn_timer'] = 0
        return spawnable_rifts
    
    def update_time_particles(self):
        """Update time manipulation visual effects"""
        for particle in self.time_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Gravity effect towards boss
            dx = self.x - particle['x']
            dy = self.y - particle['y']
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                particle['vx'] += dx / distance * 0.1
                particle['vy'] += dy / distance * 0.1
            
            if particle['life'] <= 0:
                self.time_particles.remove(particle)
    
    def create_rewind_effect(self):
        """Create visual effect for damage rewind"""
        for _ in range(15):
            particle = {
                'x': self.x + random.uniform(-self.size, self.size),
                'y': self.y + random.uniform(-self.size, self.size),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 40,
                'max_life': 40,
                'color': (0, 255, 255)  # Cyan for rewind
            }
            self.time_particles.append(particle)
    
    def take_damage(self, damage, tower_type: str = 'basic'):
        """Take damage with time lord resistances"""
        # Check magic immunity (lightning/ice towers)
        if (self.phase >= 3 and tower_type in ['lightning', 'ice'] and 
            self.magic_immunity_timer % 240 < 120):  # Immune 50% of the time
            return 0
        
        # Apply damage reduction
        reduced_damage = damage * (1 - self.damage_reduction)
        actual_damage = min(reduced_damage, self.health)
        
        # Store damage in history for rewind ability
        self.damage_history.append(actual_damage)
        if len(self.damage_history) > 10:  # Keep only recent damage
            self.damage_history.pop(0)
        
        self.health -= reduced_damage
        return actual_damage
    
    def get_time_distortion_effect(self):
        """Get the current time distortion multiplier for nearby objects"""
        if self.time_distortion_active:
            return 0.3  # Slow everything to 30% speed
        return 1.0
    
    def is_in_time_distortion_range(self, x, y):
        """Check if coordinates are within time distortion range"""
        if not self.time_distortion_active:
            return False
        
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.time_distortion_radius
    
    def draw(self, screen):
        """Draw the TimeLord Boss with temporal effects"""
        # Draw time distortion field
        if self.time_distortion_active:
            distortion_color = (100, 0, 200, 50)
            distortion_surface = pygame.Surface((self.time_distortion_radius * 2, 
                                               self.time_distortion_radius * 2), 
                                               pygame.SRCALPHA)
            pygame.draw.circle(distortion_surface, distortion_color, 
                             (self.time_distortion_radius, self.time_distortion_radius), 
                             self.time_distortion_radius)
            screen.blit(distortion_surface, 
                       (self.x - self.time_distortion_radius, 
                        self.y - self.time_distortion_radius))
        
        # Draw temporal rifts
        for rift in self.active_rifts:
            # Pulsing rift effect
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5 + rift['radius']
            pygame.draw.circle(screen, (200, 0, 255), 
                             (int(rift['x']), int(rift['y'])), int(pulse), 3)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(rift['x']), int(rift['y'])), int(pulse - 10), 1)
        
        # Draw time particles
        for particle in self.time_particles:
            alpha = particle['life'] / particle['max_life']
            size = max(1, int(4 * alpha))
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)
        
        # Draw rotating time aura
        aura_points = []
        for i in range(8):
            angle = self.aura_rotation + i * 45
            rad = math.radians(angle)
            aura_x = self.x + math.cos(rad) * (self.size + 15)
            aura_y = self.y + math.sin(rad) * (self.size + 15)
            aura_points.append((int(aura_x), int(aura_y)))
        
        # Draw aura lines
        for i in range(len(aura_points)):
            next_i = (i + 1) % len(aura_points)
            pygame.draw.line(screen, (150, 0, 255), aura_points[i], aura_points[next_i], 2)
        
        # Draw main boss body with phase colors
        boss_colors = [
            (75, 0, 130),    # Phase 1: Indigo
            (128, 0, 255),   # Phase 2: Purple
            (255, 0, 255),   # Phase 3: Magenta
            (255, 255, 255)  # Phase 4: White (ultimate)
        ]
        boss_color = boss_colors[self.phase - 1]
        
        # Pulsing effect based on abilities
        pulse_size = self.size
        if self.time_distortion_active:
            pulse_size += int(math.sin(self.pulse_timer) * 5)
        
        pygame.draw.circle(screen, boss_color, (int(self.x), int(self.y)), pulse_size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), pulse_size, 4)
        
        # Draw phase indicators (clock-like)
        for i in range(self.phase):
            angle = (i * 90) * math.pi / 180  # 4 quarters like a clock
            indicator_x = self.x + math.cos(angle) * (self.size - 8)
            indicator_y = self.y + math.sin(angle) * (self.size - 8)
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(indicator_x), int(indicator_y)), 5)
        
        # Draw time symbols
        time_symbols = ['∞', '⟲', '⧖', '⌛']  # Infinity, rewind, hourglass, etc.
        symbol_color = (255, 255, 255)
        if self.phase >= 4:
            symbol_color = (255, 255, 0)
        
        font = pygame.font.Font(None, 24)
        symbol_text = font.render(time_symbols[min(self.phase - 1, 3)], True, symbol_color)
        symbol_rect = symbol_text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(symbol_text, symbol_rect)
        
        # Draw massive health bar
        bar_width = self.size * 4
        bar_height = 12
        
        # Background
        pygame.draw.rect(screen, (50, 0, 50), 
                       (self.x - bar_width//2, self.y - self.size - 25, bar_width, bar_height))
        
        # Health
        health_percentage = self.health / self.max_health
        health_color = boss_colors[self.phase - 1]
        pygame.draw.rect(screen, health_color, 
                       (self.x - bar_width//2, self.y - self.size - 25, 
                        int(bar_width * health_percentage), bar_height))
        
        # Phase markers
        for i in range(1, self.max_phases):
            marker_x = self.x - bar_width//2 + (bar_width * (self.max_phases - i) / self.max_phases)
            pygame.draw.line(screen, (255, 255, 255), 
                           (marker_x, self.y - self.size - 25), 
                           (marker_x, self.y - self.size - 13), 3)
        
        # Draw boss title
        font = pygame.font.Font(None, 28)
        title_text = font.render("TIMELORD BOSS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x, self.y - self.size - 45))
        screen.blit(title_text, title_rect) 