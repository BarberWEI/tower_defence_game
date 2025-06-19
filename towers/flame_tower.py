from .tower import Tower
import pygame
import math
import random

class FlameTower(Tower):
    """Tower that shoots flamethrower in a cone, causing burn damage over time"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'flame')
        self.damage = 6  # Lower direct damage
        self.range = 90  # Short range
        self.fire_rate = 20  # Very fast firing
        self.projectile_speed = 6
        self.size = 12
        self.color = (255, 69, 0)  # Red-orange
        
        # Flame properties
        self.cone_angle = 45  # Degrees
        self.burn_damage = 3  # Damage over time
        self.burn_duration = 180  # Frames (3 seconds)
        self.flame_particles = []
        
        # Ground only
        self.can_target_flying = False
        self.can_target_invisible = False
    
    def can_target_enemy(self, enemy):
        """Check if this tower can target a specific enemy"""
        # Cannot target flying enemies
        if hasattr(enemy, 'flying') and enemy.flying and not self.can_target_flying:
            return False
            
        # Cannot target invisible enemies
        # Can target invisible enemies if they've been detected by a detector tower
        if hasattr(enemy, 'invisible') and enemy.invisible and not self.can_target_invisible:
            if not hasattr(enemy, 'detected_by_detector') or not enemy.detected_by_detector:
                return False
            
        return True
    
    def acquire_target(self, enemies):
        """Find closest target"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                valid_targets.append((enemy, distance))
        
        if valid_targets:
            # Target closest enemy
            valid_targets.sort(key=lambda x: x[1])
            self.target = valid_targets[0][0]
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
    
    def shoot(self, projectiles):
        """Spray flames in a cone"""
        # Note: This tower doesn't use projectiles, it directly damages enemies
        # The enemies list will be passed through the update method
        pass
    
    def spray_flames(self, enemies):
        """Create flame cone effect"""
        if not self.target:
            return 0
            
        # Find all enemies in flame cone
        cone_angle_rad = math.radians(self.cone_angle / 2)
        total_damage = 0
        
        for enemy in enemies:
            if not self.can_target_enemy(enemy):
                continue
                
            # Check if enemy is in range
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance > self.range:
                continue
            
            # Check if enemy is in cone
            enemy_angle = math.atan2(enemy.y - self.y, enemy.x - self.x)
            angle_diff = abs(enemy_angle - self.angle)
            
            # Handle angle wraparound
            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff
            
            if angle_diff <= cone_angle_rad:
                # Apply immediate damage
                actual_damage = enemy.take_damage(self.damage)
                total_damage += actual_damage
                
                # Apply burn effect
                if not hasattr(enemy, 'burn_timer'):
                    enemy.burn_timer = 0
                    enemy.burn_damage = 0
                
                enemy.burn_timer = self.burn_duration
                enemy.burn_damage = self.burn_damage
        
        # Create visual flame particles
        self.create_flame_particles()
        return total_damage
    
    def create_flame_particles(self):
        """Create flame particle effects"""
        cone_angle_rad = math.radians(self.cone_angle / 2)
        
        for i in range(8):  # Create multiple particles
            # Random angle within cone
            particle_angle = self.angle + random.uniform(-cone_angle_rad, cone_angle_rad)
            particle_distance = random.uniform(20, self.range)
            
            particle_x = self.x + math.cos(particle_angle) * particle_distance
            particle_y = self.y + math.sin(particle_angle) * particle_distance
            
            # Random flame color
            colors = [(255, 69, 0), (255, 140, 0), (255, 215, 0), (255, 0, 0)]
            color = random.choice(colors)
            
            self.flame_particles.append({
                'x': particle_x,
                'y': particle_y,
                'color': color,
                'life': 15  # Frames to live
            })
    
    def update(self, enemies, projectiles):
        """Update flame tower"""
        # Update fire timer
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Spray flames if ready and have target
        if self.target and self.fire_timer <= 0:
            damage_dealt = self.spray_flames(enemies)
            if damage_dealt > 0:
                self.add_damage_dealt(damage_dealt)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
            
            self.fire_timer = self.fire_rate
        
        # Update flame particles
        for particle in self.flame_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.flame_particles.remove(particle)
        
        # Update burn effects on enemies
        burn_damage_dealt = 0
        for enemy in enemies:
            if hasattr(enemy, 'burn_timer') and enemy.burn_timer > 0:
                enemy.burn_timer -= 1
                if enemy.burn_timer % 20 == 0:  # Every 1/3 second
                    actual_burn_damage = enemy.take_damage(enemy.burn_damage)
                    burn_damage_dealt += actual_burn_damage
        
        # Track burn damage
        if burn_damage_dealt > 0:
            self.add_damage_dealt(burn_damage_dealt)
    
    def draw(self, screen, selected: bool = False):
        """Draw flame tower"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw flame cone outline
        if self.target:
            cone_angle_rad = math.radians(self.cone_angle / 2)
            
            # Draw cone edges
            left_angle = self.angle - cone_angle_rad
            right_angle = self.angle + cone_angle_rad
            
            left_x = self.x + math.cos(left_angle) * self.range
            left_y = self.y + math.sin(left_angle) * self.range
            right_x = self.x + math.cos(right_angle) * self.range
            right_y = self.y + math.sin(right_angle) * self.range
            
            pygame.draw.line(screen, (255, 100, 0), (int(self.x), int(self.y)), (int(left_x), int(left_y)), 1)
            pygame.draw.line(screen, (255, 100, 0), (int(self.x), int(self.y)), (int(right_x), int(right_y)), 1)
        
        # Draw flame particles
        for particle in self.flame_particles:
            alpha = particle['life'] / 15.0  # Fade out
            size = int(3 * alpha) + 1
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), size)
        
        # Draw main tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw flame nozzle
        if self.target:
            nozzle_length = self.size + 8
            end_x = self.x + math.cos(self.angle) * nozzle_length
            end_y = self.y + math.sin(self.angle) * nozzle_length
            
            pygame.draw.line(screen, (100, 100, 100), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 4)
            pygame.draw.circle(screen, (255, 0, 0), (int(end_x), int(end_y)), 2)
