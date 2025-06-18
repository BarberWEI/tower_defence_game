from .tower import Tower
import pygame
import math

class CannonTower(Tower):
    """Heavy cannon tower with splash damage and long range"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'cannon')
        self.damage = 25  # High damage
        self.range = 160  # Good range
        self.fire_rate = 75  # Slow firing
        self.projectile_speed = 4.0
        self.size = 15
        self.color = (139, 69, 19)  # Brown
        
        # Cannon properties
        self.splash_radius = 40  # Area damage
        self.splash_damage = 15  # Reduced damage for splash
        
        # Targeting - ground only
        self.can_target_flying = False
        self.can_target_invisible = False
    
    def can_target_enemy(self, enemy):
        """Check if this tower can target a specific enemy"""
        # Cannot target flying enemies
        if hasattr(enemy, 'flying') and enemy.flying and not self.can_target_flying:
            return False
            
        # Can target invisible enemies if they've been detected by a detector tower
        if hasattr(enemy, 'invisible') and enemy.invisible and not self.can_target_invisible:
            if not hasattr(enemy, 'detected_by_detector') or not enemy.detected_by_detector:
                return False
            
        return True
    
    def acquire_target(self, enemies):
        """Find target - prioritize groups of enemies"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                # Count nearby enemies for splash potential
                nearby_count = 0
                for other_enemy in enemies:
                    if self.can_target_enemy(other_enemy):
                        splash_distance = math.sqrt((enemy.x - other_enemy.x)**2 + (enemy.y - other_enemy.y)**2)
                        if splash_distance <= self.splash_radius:
                            nearby_count += 1
                
                valid_targets.append((enemy, distance, nearby_count))
        
        if valid_targets:
            # Target enemy with most nearby enemies (best splash potential)
            valid_targets.sort(key=lambda x: x[2], reverse=True)
            self.target = valid_targets[0][0]
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
    
    def shoot(self, projectiles):
        """Shoot explosive cannonball"""
        if self.target:
            projectile = ExplosiveCannonball(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.splash_radius, self.splash_damage
            )
            projectiles.append(projectile)
    
    def draw(self, screen, selected: bool = False):
        """Draw cannon tower"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw base
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw cannon barrel
        if self.target:
            barrel_length = self.size + 12
            barrel_width = 4
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            
            # Draw thick barrel
            pygame.draw.line(screen, (60, 60, 60), (int(self.x), int(self.y)), (int(end_x), int(end_y)), barrel_width)
            
            # Draw muzzle
            pygame.draw.circle(screen, (40, 40, 40), (int(end_x), int(end_y)), 3)
        
        # Draw cannon wheels
        wheel_y = self.y + self.size - 3
        pygame.draw.circle(screen, (100, 50, 0), (int(self.x - 8), int(wheel_y)), 4)
        pygame.draw.circle(screen, (100, 50, 0), (int(self.x + 8), int(wheel_y)), 4)


class ExplosiveCannonball:
    """Explosive cannonball projectile with AOE damage"""
    
    def __init__(self, x, y, target_x, target_y, speed, damage, splash_radius, splash_damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.splash_radius = splash_radius
        self.splash_damage = splash_damage
        self.color = (139, 69, 19)  # Brown
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx = self.dy = 0
        
        self.active = True
        self.should_remove = False
        
    def update(self):
        """Update projectile position"""
        if self.active:
            self.x += self.dx
            self.y += self.dy
            
            # Remove if off screen
            if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
                self.active = False
                self.should_remove = True
    
    def draw(self, screen):
        """Draw cannonball"""
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 6)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), 6, 1)
            
    def check_collision(self, enemies):
        """Check collision with enemies and create explosion"""
        if not self.active:
            return
            
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= 10:  # Direct hit
                self.explode(enemies)
                return
                
    def explode(self, enemies):
        """Create explosion and damage nearby enemies"""
        # Damage all enemies in splash radius
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.splash_radius:
                # Direct hit gets full damage, splash gets reduced damage
                if distance < 15:  # Direct hit
                    enemy.take_damage(self.damage)
                else:  # Splash damage
                    enemy.take_damage(self.splash_damage)
        
        self.active = False
        self.should_remove = True