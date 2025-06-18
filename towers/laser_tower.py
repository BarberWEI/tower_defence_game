from .tower import Tower
import pygame
import math

class LaserTower(Tower):
    """Tower that fires continuous laser beam through multiple enemies"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage = 20  # High damage
        self.range = 160
        self.fire_rate = 20  # Fast firing
        self.projectile_speed = 10  # Not used for laser but needed for inheritance
        self.size = 12
        self.color = (255, 0, 255)  # Magenta
        
        # Laser properties
        self.laser_width = 4
        self.laser_duration = 10  # Frames the laser is visible
        self.laser_timer = 0
        self.laser_target = None
        self.laser_end_point = None
        self.charging = False
        self.charge_time = 30  # Frames to charge
        self.charge_timer = 0
        
    def update(self, enemies, projectiles):
        """Update laser tower"""
        super().update(enemies, projectiles)
        
        # Update laser timer
        if self.laser_timer > 0:
            self.laser_timer -= 1
            
        # Update charge timer
        if self.charging:
            self.charge_timer += 1
            if self.charge_timer >= self.charge_time:
                self.fire_laser(enemies)
                self.charging = False
                self.charge_timer = 0
    
    def acquire_target(self, enemies):
        """Find target for laser"""
        targets_in_range = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range:
                targets_in_range.append((enemy, distance))
        
        if targets_in_range:
            # Target enemy with most health
            targets_in_range.sort(key=lambda x: x[0].health, reverse=True)
            self.target = targets_in_range[0][0]
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
    
    def shoot(self, projectiles):
        """Start charging laser"""
        if self.target and not self.charging:
            self.laser_target = self.target
            self.charging = True
            self.charge_timer = 0
    
    def fire_laser(self, enemies):
        """Fire laser beam"""
        if not self.laser_target:
            return
            
        # Calculate laser direction
        dx = self.laser_target.x - self.x
        dy = self.laser_target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Find all enemies in laser path
            laser_length = self.range
            hit_enemies = []
            
            for enemy in enemies:
                # Check if enemy is in laser path
                enemy_dx = enemy.x - self.x
                enemy_dy = enemy.y - self.y
                enemy_distance = math.sqrt(enemy_dx**2 + enemy_dy**2)
                
                if enemy_distance <= laser_length:
                    # Calculate perpendicular distance from laser line
                    cross_product = abs(enemy_dx * dy - enemy_dy * dx)
                    if cross_product <= self.laser_width:
                        # Check if enemy is in front of tower
                        dot_product = enemy_dx * dx + enemy_dy * dy
                        if dot_product > 0:
                            hit_enemies.append((enemy, enemy_distance))
            
            # Sort by distance and apply damage
            hit_enemies.sort(key=lambda x: x[1])
            for enemy, _ in hit_enemies:
                enemy.take_damage(self.damage)
                
                # Prevent teleporting enemies from teleporting when hit by laser
                if hasattr(enemy, 'teleport_timer'):
                    enemy.teleport_timer = 0  # Reset teleport cooldown
            
            # Set laser visual effect
            self.laser_timer = self.laser_duration
            if hit_enemies:
                furthest_enemy = hit_enemies[-1][0]
                self.laser_end_point = (furthest_enemy.x, furthest_enemy.y)
            else:
                self.laser_end_point = (self.x + dx * laser_length, self.y + dy * laser_length)
    
    def draw(self, screen):
        """Draw laser tower"""
        # Draw range circle
        pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw charging effect
        if self.charging:
            charge_progress = self.charge_timer / self.charge_time
            charge_radius = int(15 * charge_progress)
            charge_color = (255, int(255 * charge_progress), 255)
            
            for i in range(3):
                pygame.draw.circle(screen, charge_color, (int(self.x), int(self.y)), 
                                 charge_radius - i * 2, 1)
        
        # Draw laser beam
        if self.laser_timer > 0 and self.laser_end_point:
            # Draw laser beam
            pygame.draw.line(screen, (255, 0, 255), 
                           (int(self.x), int(self.y)), 
                           (int(self.laser_end_point[0]), int(self.laser_end_point[1])), 
                           self.laser_width)
        
        # Draw main tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw laser emitter
        emitter_points = [
            (self.x - 4, self.y - 8),
            (self.x + 4, self.y - 8),
            (self.x + 2, self.y - 12),
            (self.x - 2, self.y - 12)
        ]
        pygame.draw.polygon(screen, (200, 200, 200), emitter_points)
        
        # Draw crystal
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y - 10)), 3)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 3) 