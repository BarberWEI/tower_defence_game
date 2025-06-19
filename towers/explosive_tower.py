from .tower import Tower
import pygame
import math

class ExplosiveTower(Tower):
    """Tower that fires explosive rockets with large splash damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'explosive')
        self.damage = 35  # Very high damage
        self.range = 180  # Long range
        self.fire_rate = 100  # Very slow firing
        self.projectile_speed = 3.5
        self.size = 14
        self.color = (255, 165, 0)  # Orange
        
        # Explosive properties
        self.splash_radius = 60  # Large splash
        self.splash_damage = 20
        
        # Can only target ground enemies
        self.can_target_flying = False
        self.can_target_invisible = False
    
    def can_target_enemy(self, enemy):
        """Check if this tower can target a specific enemy"""
        if hasattr(enemy, 'flying') and enemy.flying and not self.can_target_flying:
            return False
        # Can target invisible enemies if they've been detected by a detector tower
        if hasattr(enemy, 'invisible') and enemy.invisible and not self.can_target_invisible:
            if not hasattr(enemy, 'detected_by_detector') or not enemy.detected_by_detector:
                return False
        return True
    
    def acquire_target(self, enemies):
        """Find target using targeting restrictions"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                valid_targets.append((enemy, distance))
        
        if not valid_targets:
            self.target = None
            return
        
        # Target closest to end of path
        self.target = max(valid_targets, key=lambda x: x[0].get_distance_from_start())[0]
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles):
        """Fire explosive rocket"""
        if self.target:
            projectile = ExplosiveRocket(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.splash_radius, self.splash_damage
            )
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
    
    def draw(self, screen, selected: bool = False):
        """Draw explosive tower"""
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw missile launcher
        launcher_rect = pygame.Rect(self.x - 6, self.y - 10, 12, 8)
        pygame.draw.rect(screen, (100, 100, 100), launcher_rect)
        
        # Draw missiles
        for i in range(2):
            missile_x = self.x - 3 + i * 6
            missile_y = self.y - 8
            pygame.draw.circle(screen, (255, 0, 0), (int(missile_x), int(missile_y)), 2)


class ExplosiveRocket:
    """Explosive rocket projectile with massive AOE damage"""
    
    def __init__(self, x, y, target_x, target_y, speed, damage, splash_radius, splash_damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.splash_radius = splash_radius
        self.splash_damage = splash_damage
        self.color = (255, 165, 0)  # Orange
        
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
        self.trail_positions = []
        
    def update(self):
        """Update projectile position"""
        if self.active:
            self.x += self.dx
            self.y += self.dy
            
            # Add to trail
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > 6:
                self.trail_positions.pop(0)
            
            # Remove if off screen
            if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
                self.active = False
                self.should_remove = True
    
    def draw(self, screen):
        """Draw rocket with trail"""
        if self.active:
            # Draw trail
            for i, (trail_x, trail_y) in enumerate(self.trail_positions):
                alpha = (i + 1) / len(self.trail_positions)
                trail_color = (int(255 * alpha), int(165 * alpha), 0)
                pygame.draw.circle(screen, trail_color, (int(trail_x), int(trail_y)), max(1, int(4 * alpha)))
            
            # Draw rocket
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 3)
            
    def check_collision(self, enemies):
        """Check collision with enemies and create explosion"""
        if not self.active:
            return {'hit': False, 'damage': 0, 'tower_id': None}
            
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= 12:  # Direct hit
                total_damage = 0
                # Damage all enemies in splash radius
                for enemy_in_range in enemies:
                    explosion_distance = math.sqrt((enemy_in_range.x - self.x)**2 + (enemy_in_range.y - self.y)**2)
                    if explosion_distance <= self.splash_radius:
                        if explosion_distance < 20:  # Direct hit
                            damage_dealt = enemy_in_range.take_damage(self.damage)
                        else:  # Splash damage
                            damage_dealt = enemy_in_range.take_damage(self.splash_damage)
                        total_damage += damage_dealt
                
                self.active = False
                self.should_remove = True
                return {'hit': True, 'damage': total_damage, 'tower_id': getattr(self, 'source_tower_id', None)}
        
        return {'hit': False, 'damage': 0, 'tower_id': None}
                
    def explode(self, enemies):
        """Create massive explosion and damage all nearby enemies"""
        # Damage all enemies in splash radius
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.splash_radius:
                # Direct hit gets full damage, splash gets reduced damage
                if distance < 20:  # Direct hit
                    enemy.take_damage(self.damage)
                else:  # Splash damage
                    enemy.take_damage(self.splash_damage)
        
        self.active = False
        self.should_remove = True
