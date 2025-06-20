from .tower import Tower
import pygame
import math

class PoisonTower(Tower):
    """Tower that applies poison damage over time, counters regenerating enemies"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'poison')
        self.damage = 6  # Lower direct damage
        self.range = 120
        self.fire_rate = 35  # Medium fire rate
        self.projectile_speed = 5
        self.size = 12
        self.color = (50, 205, 50)  # Lime green
        
        # Poison properties
        self.poison_damage = 2  # Reduced from 3 to 2
        self.poison_duration = 360  # Increased to 6 seconds
        self.splash_radius = 40
        
        # Targeting restrictions - ground only
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
        """Shoot poison projectile"""
        if self.target:
            # Create poison splash projectile
            projectile = PoisonProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage
            )
            projectile.splash_radius = self.splash_radius
            projectile.poison_damage = self.poison_damage
            projectile.poison_duration = self.poison_duration
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
    
    def draw(self, screen, selected: bool = False):
        """Draw poison tower"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw base
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw poison tanks
        tank_positions = [
            (self.x - 6, self.y - 6),
            (self.x + 6, self.y - 6),
            (self.x, self.y + 6)
        ]
        
        for tank_x, tank_y in tank_positions:
            pygame.draw.circle(screen, (0, 100, 0), (int(tank_x), int(tank_y)), 4)
            pygame.draw.circle(screen, (255, 255, 255), (int(tank_x), int(tank_y)), 4, 1)
        
        # Draw poison cloud effect
        cloud_radius = int(15 + math.sin(pygame.time.get_ticks() * 0.01) * 3)
        pygame.draw.circle(screen, (50, 205, 50), (int(self.x), int(self.y)), cloud_radius, 1)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 3)


    def acquire_target_optimized(self, enemies):
        """Optimized targeting with restrictions"""
        if not enemies:
            self.target = None
            return
        
        range_squared = self.range * self.range
        valid_targets = []
        
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance_squared = dx * dx + dy * dy
            
            if distance_squared <= range_squared and self.can_target_enemy(enemy):
                actual_distance = math.sqrt(distance_squared)
                valid_targets.append((enemy, actual_distance))
                if len(valid_targets) >= 10:
                    break
        
        if not valid_targets:
            self.target = None
            return
        
        # Target closest to end of path (default strategy)
        self.target = max(valid_targets, key=lambda x: x[0].get_distance_from_start())[0]
        
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def update_with_speed_optimized(self, enemies, projectiles, speed_multiplier: float):
        """Update with speed multiplier and targeting restrictions"""
        self.acquire_target_optimized(enemies)
        
        if self.target and self.fire_timer <= 0:
            self.shoot(projectiles)
            self.fire_timer = self.fire_rate
        
        if self.fire_timer > 0:
            self.fire_timer -= speed_multiplier
class PoisonProjectile:
    """Poison projectile that applies poison effect"""
    
    def __init__(self, x, y, target_x, target_y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.color = (50, 205, 50)  # Green
        self.poison_damage = 2  # Reduced tick damage
        self.poison_duration = 360  # Increased duration to 6 seconds
        self.splash_radius = 40
        
        # Calculate direction
        import math
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
        """Draw poison projectile"""
        if self.active:
            import pygame
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
            
    def check_collision(self, enemies):
        """Check collision with enemies and apply poison"""
        if not self.active:
            return {'hit': False, 'damage': 0, 'tower_id': None}
            
        import math
        total_damage = 0
        enemies_hit = 0
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.splash_radius:
                # Apply direct damage
                damage_dealt = enemy.take_damage(self.damage)
                total_damage += damage_dealt
                enemies_hit += 1
                
                # Apply poison effect
                if not hasattr(enemy, 'poison_timer'):
                    enemy.poison_timer = 0
                    enemy.poison_damage_timer = 0
                    
                enemy.poison_timer = self.poison_duration
                enemy.poison_damage = self.poison_damage
                enemy.poison_damage_timer = 0  # Reset timer for fresh poison application
                
                # Stop regeneration for regenerating enemies
                if hasattr(enemy, 'last_damage_time'):
                    enemy.last_damage_time = 0
        
        if enemies_hit > 0:
            self.active = False
            self.should_remove = True
            return {'hit': True, 'damage': total_damage, 'tower_id': getattr(self, 'source_tower_id', None)}
        
        return {'hit': False, 'damage': 0, 'tower_id': None} 