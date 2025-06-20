from .enemy import Enemy
import pygame
import math
import random

class NecromancerBoss(Enemy):
    """Ultra powerful boss that manipulates death and undeath"""
    
    def __init__(self, path, wave_number=1):
        super().__init__(path, wave_number)
        self.health = 3500
        self.max_health = 3500
        self.speed = 0.6
        self.reward = 750
        self.color = (139, 69, 19)  # Dark brown/black
        self.size = 32
        
        # Necromancy abilities
        self.resurrection_timer = 0
        self.resurrection_cooldown = 480  # 8 seconds
        self.resurrection_range = 200
        self.dead_enemies_list = []  # Track recently dead enemies
        
        # Life drain ability
        self.life_drain_timer = 0
        self.life_drain_cooldown = 360  # 6 seconds
        self.life_drain_range = 120
        self.life_drain_active = False
        self.life_drain_duration = 120  # 2 seconds
        
        # Death aura
        self.death_aura_timer = 0
        self.death_aura_interval = 60  # Every second
        self.death_aura_radius = 80
        
        # Undead minion summoning
        self.summon_timer = 0
        self.summon_cooldown = 600  # 10 seconds
        self.max_undead_minions = 6
        self.current_undead_count = 0
        
        # Boss resistances
        self.damage_reduction = 0.55  # Takes 45% damage
        self.poison_immunity = True
        self.life_steal = 0.2  # Heals for 20% of damage dealt
        
        # Phase system
        self.phase = 1
        self.max_phases = 3
        
        # Visual effects
        self.dark_particles = []
        self.soul_orbs = []
        self.aura_pulse = 0
        self.floating_offset = 0
        
    def update(self):
        """Update with necromancy abilities"""
        # Update phase based on health
        health_percentage = self.health / self.max_health
        if health_percentage > 0.66:
            self.phase = 1
        elif health_percentage > 0.33:
            self.phase = 2
        else:
            self.phase = 3  # Final phase - most dangerous
            
        # Phase-based abilities
        if self.phase >= 2:
            self.death_aura_interval = 40  # Faster death aura
        if self.phase >= 3:
            self.max_undead_minions = 10  # More minions
            
        super().update()
        
        # Update ability timers
        self.resurrection_timer += 1
        self.life_drain_timer += 1
        self.death_aura_timer += 1
        self.summon_timer += 1
        self.aura_pulse += 0.1
        self.floating_offset += 0.05
        
        # Trigger abilities
        self.update_necromancy_abilities()
        
        # Update visual effects
        self.update_dark_particles()
        self.update_soul_orbs()
        
        # Handle life drain
        if self.life_drain_active:
            self.life_drain_duration -= 1
            if self.life_drain_duration <= 0:
                self.life_drain_active = False
    
    def update_necromancy_abilities(self):
        """Update necromancy-based abilities"""
        # Resurrection ability
        if (self.resurrection_timer >= self.resurrection_cooldown and 
            len(self.dead_enemies_list) > 0):
            self.attempt_resurrection()
        
        # Life drain ability
        if self.life_drain_timer >= self.life_drain_cooldown:
            self.activate_life_drain()
        
        # Death aura (constant passive)
        if self.death_aura_timer >= self.death_aura_interval:
            self.pulse_death_aura()
            self.death_aura_timer = 0
        
        # Summon undead minions
        if (self.summon_timer >= self.summon_cooldown and 
            self.current_undead_count < self.max_undead_minions):
            self.summon_undead_minion()
    
    def attempt_resurrection(self):
        """Resurrect a recently dead enemy"""
        if len(self.dead_enemies_list) > 0:
            # Get the most recent dead enemy
            dead_enemy_data = self.dead_enemies_list.pop(0)
            
            # Create resurrection effect
            self.create_resurrection_effect(dead_enemy_data['x'], dead_enemy_data['y'])
            
            self.resurrection_timer = 0
    
    def get_resurrection_data(self):
        """Get data for enemy to resurrect (for game system to handle)"""
        if len(self.dead_enemies_list) > 0:
            return self.dead_enemies_list.pop(0)
        return None
    
    def register_dead_enemy(self, enemy_type, x, y):
        """Register a dead enemy for potential resurrection"""
        if len(self.dead_enemies_list) < 5:  # Limit memory
            self.dead_enemies_list.append({
                'type': enemy_type,
                'x': x,
                'y': y,
                'timestamp': pygame.time.get_ticks()
            })
    
    def activate_life_drain(self):
        """Drain life from nearby towers and enemies"""
        self.life_drain_active = True
        self.life_drain_duration = 120
        self.life_drain_timer = 0
        
        # Create life drain effect
        for _ in range(15):
            particle = {
                'x': self.x + random.uniform(-self.life_drain_range, self.life_drain_range),
                'y': self.y + random.uniform(-self.life_drain_range, self.life_drain_range),
                'vx': 0,
                'vy': 0,
                'life': 60,
                'max_life': 60,
                'color': (0, 255, 0),  # Green life energy
                'type': 'life_drain'
            }
            self.dark_particles.append(particle)
    
    def pulse_death_aura(self):
        """Create death aura that weakens nearby enemies and towers"""
        # Create aura particles
        for i in range(8):
            angle = (i * 45) * math.pi / 180
            particle_x = self.x + math.cos(angle) * self.death_aura_radius
            particle_y = self.y + math.sin(angle) * self.death_aura_radius
            
            particle = {
                'x': particle_x,
                'y': particle_y,
                'vx': math.cos(angle) * 2,
                'vy': math.sin(angle) * 2,
                'life': 30,
                'max_life': 30,
                'color': (139, 69, 19),  # Dark brown
                'type': 'death_aura'
            }
            self.dark_particles.append(particle)
    
    def summon_undead_minion(self):
        """Summon an undead minion"""
        self.current_undead_count += 1
        self.summon_timer = 0
        
        # Create summoning effect
        summon_x = self.x + random.uniform(-50, 50)
        summon_y = self.y + random.uniform(-50, 50)
        
        for _ in range(12):
            particle = {
                'x': summon_x,
                'y': summon_y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 45,
                'max_life': 45,
                'color': (75, 0, 130),  # Dark purple
                'type': 'summon'
            }
            self.dark_particles.append(particle)
    
    def should_summon_undead(self):
        """Check if boss should summon undead minions"""
        if (self.summon_timer >= self.summon_cooldown and 
            self.current_undead_count < self.max_undead_minions):
            self.current_undead_count += 1
            self.summon_timer = 0
            return True
        return False
    
    def minion_died(self):
        """Called when an undead minion dies"""
        self.current_undead_count = max(0, self.current_undead_count - 1)
    
    def update_dark_particles(self):
        """Update dark magic particle effects"""
        for particle in self.dark_particles[:]:
            # Different behavior based on particle type
            if particle['type'] == 'life_drain':
                # Life drain particles move toward boss
                dx = self.x - particle['x']
                dy = self.y - particle['y']
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    particle['vx'] = dx / distance * 3
                    particle['vy'] = dy / distance * 3
            
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.dark_particles.remove(particle)
    
    def update_soul_orbs(self):
        """Update floating soul orbs around boss"""
        # Maintain 3-6 soul orbs based on phase
        target_orbs = 3 + self.phase
        
        while len(self.soul_orbs) < target_orbs:
            orb = {
                'angle': random.uniform(0, 360),
                'radius': self.size + random.uniform(20, 40),
                'speed': random.uniform(0.5, 1.5),
                'size': random.randint(3, 8),
                'color': (100, 0, 100)
            }
            self.soul_orbs.append(orb)
        
        # Update existing orbs
        for orb in self.soul_orbs:
            orb['angle'] += orb['speed']
            if orb['angle'] >= 360:
                orb['angle'] -= 360
    
    def create_resurrection_effect(self, x, y):
        """Create visual effect for resurrection"""
        for _ in range(20):
            particle = {
                'x': x + random.uniform(-20, 20),
                'y': y + random.uniform(-20, 20),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-4, -1),  # Float upward
                'life': 60,
                'max_life': 60,
                'color': (255, 255, 255),  # White for resurrection
                'type': 'resurrection'
            }
            self.dark_particles.append(particle)
    
    def take_damage(self, damage, tower_type: str = 'basic'):
        """Take damage with necromancer resistances"""
        # Poison immunity
        if tower_type == 'poison':
            return 0
        
        # Apply damage reduction
        reduced_damage = damage * (1 - self.damage_reduction)
        actual_damage = min(reduced_damage, self.health)
        
        # Life steal - heal for portion of damage taken
        life_steal_amount = actual_damage * self.life_steal
        self.health = min(self.max_health, self.health + life_steal_amount - reduced_damage)
        
        return actual_damage
    
    def is_in_life_drain_range(self, x, y):
        """Check if coordinates are within life drain range"""
        if not self.life_drain_active:
            return False
        
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.life_drain_range
    
    def is_in_death_aura_range(self, x, y):
        """Check if coordinates are within death aura range"""
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.death_aura_radius
    
    def draw(self, screen):
        """Draw the Necromancer Boss with dark magic effects"""
        # Calculate floating position
        float_y = self.y + math.sin(self.floating_offset) * 3
        
        # Draw death aura
        aura_alpha = int(100 + math.sin(self.aura_pulse) * 50)
        aura_color = (139, 69, 19, aura_alpha)
        aura_surface = pygame.Surface((self.death_aura_radius * 2, 
                                     self.death_aura_radius * 2), 
                                     pygame.SRCALPHA)
        pygame.draw.circle(aura_surface, aura_color, 
                         (self.death_aura_radius, self.death_aura_radius), 
                         self.death_aura_radius)
        screen.blit(aura_surface, 
                   (self.x - self.death_aura_radius, 
                    float_y - self.death_aura_radius))
        
        # Draw life drain field
        if self.life_drain_active:
            drain_color = (0, 255, 0, 30)
            drain_surface = pygame.Surface((self.life_drain_range * 2, 
                                          self.life_drain_range * 2), 
                                          pygame.SRCALPHA)
            pygame.draw.circle(drain_surface, drain_color, 
                             (self.life_drain_range, self.life_drain_range), 
                             self.life_drain_range)
            screen.blit(drain_surface, 
                       (self.x - self.life_drain_range, 
                        float_y - self.life_drain_range))
        
        # Draw dark particles
        for particle in self.dark_particles:
            alpha = particle['life'] / particle['max_life']
            size = max(1, int(5 * alpha))
            
            # Different colors for different particle types
            color = particle['color']
            if particle['type'] == 'life_drain':
                # Pulsing green effect
                pulse = int(255 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.01)))
                color = (0, pulse, 0)
            
            pygame.draw.circle(screen, color, 
                             (int(particle['x']), int(particle['y'])), size)
        
        # Draw floating soul orbs
        for orb in self.soul_orbs:
            orb_x = self.x + math.cos(math.radians(orb['angle'])) * orb['radius']
            orb_y = float_y + math.sin(math.radians(orb['angle'])) * orb['radius']
            
            # Pulsing soul orb
            pulse_size = orb['size'] + int(math.sin(pygame.time.get_ticks() * 0.005 + orb['angle']) * 2)
            pygame.draw.circle(screen, orb['color'], 
                             (int(orb_x), int(orb_y)), pulse_size)
            pygame.draw.circle(screen, (200, 100, 200), 
                             (int(orb_x), int(orb_y)), pulse_size, 1)
        
        # Draw main boss body with phase colors
        boss_colors = [
            (139, 69, 19),   # Phase 1: Dark brown
            (75, 0, 130),    # Phase 2: Dark purple
            (0, 0, 0)        # Phase 3: Black
        ]
        boss_color = boss_colors[self.phase - 1]
        
        # Draw necromancer robe (larger circle)
        robe_size = self.size + 8
        pygame.draw.circle(screen, boss_color, (int(self.x), int(float_y)), robe_size)
        
        # Draw inner dark core
        pygame.draw.circle(screen, (50, 0, 50), (int(self.x), int(float_y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(float_y)), self.size, 3)
        
        # Draw phase indicators (skull symbols)
        for i in range(self.phase):
            angle = (i * 120) * math.pi / 180  # 3 positions around boss
            indicator_x = self.x + math.cos(angle) * (self.size - 5)
            indicator_y = float_y + math.sin(angle) * (self.size - 5)
            
            # Draw mini skull
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(indicator_x), int(indicator_y)), 4)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (int(indicator_x - 1), int(indicator_y - 1)), 1)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (int(indicator_x + 1), int(indicator_y - 1)), 1)
        
        # Draw necromancer staff
        staff_length = self.size + 15
        staff_angle = math.sin(self.floating_offset) * 0.2  # Slight sway
        staff_end_x = self.x + math.cos(staff_angle) * staff_length
        staff_end_y = float_y + math.sin(staff_angle) * staff_length
        
        pygame.draw.line(screen, (101, 67, 33), 
                        (int(self.x), int(float_y)), 
                        (int(staff_end_x), int(staff_end_y)), 4)
        
        # Draw staff crystal
        crystal_color = (148, 0, 211) if self.phase < 3 else (255, 0, 255)
        pygame.draw.circle(screen, crystal_color, 
                         (int(staff_end_x), int(staff_end_y)), 6)
        
        # Draw necromancy symbol in center
        symbol_color = (255, 255, 255) if self.phase < 3 else (255, 0, 0)
        font = pygame.font.Font(None, 20)
        symbol_text = font.render("☠", True, symbol_color)  # Skull symbol
        symbol_rect = symbol_text.get_rect(center=(int(self.x), int(float_y)))
        screen.blit(symbol_text, symbol_rect)
        
        # Draw massive health bar
        bar_width = self.size * 4
        bar_height = 12
        
        # Background
        pygame.draw.rect(screen, (50, 0, 50), 
                       (self.x - bar_width//2, float_y - self.size - 30, bar_width, bar_height))
        
        # Health
        health_percentage = self.health / self.max_health
        health_color = boss_colors[self.phase - 1]
        pygame.draw.rect(screen, health_color, 
                       (self.x - bar_width//2, float_y - self.size - 30, 
                        int(bar_width * health_percentage), bar_height))
        
        # Phase markers
        for i in range(1, self.max_phases):
            marker_x = self.x - bar_width//2 + (bar_width * (self.max_phases - i) / self.max_phases)
            pygame.draw.line(screen, (255, 255, 255), 
                           (marker_x, float_y - self.size - 30), 
                           (marker_x, float_y - self.size - 18), 3)
        
        # Draw boss title
        font = pygame.font.Font(None, 28)
        title_text = font.render("NECROMANCER BOSS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x, float_y - self.size - 50))
        screen.blit(title_text, title_rect) 