from .tower import Tower
import pygame
import math

class SplashTower(Tower):
    """Water-based tower that applies wet status - can only be placed in water"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'splash')
        self.damage = 0  # No direct damage
        self.range = 80
        self.fire_rate = 30  # Moderate firing rate
        self.projectile_speed = 6
        self.size = 14
        self.color = (30, 144, 255)  # Deep blue
        
        # Splash properties
        self.wet_duration = 120  # 2 seconds at 60 FPS
        self.splash_radius = 35  # Area of effect
        self.lightning_damage_multiplier = 2.0  # 2x lightning damage when wet
        
        # Can target all enemy types
        self.can_target_flying = True
        self.can_target_invisible = False  # Unless detected
        
        # Placement restriction
        self.water_only = True
    
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
        
        # Target closest enemy
        self.target = min(valid_targets, key=lambda x: x[1])[0]
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles):
        """Create water projectile that applies wet status"""
        if self.target:
            from projectiles import WaterProjectile
            projectile = WaterProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.tower_type, self.wet_duration,
                self.splash_radius, self.lightning_damage_multiplier
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
    
    def draw(self, screen, selected: bool = False):
        """Draw splash tower"""
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw water ripples
        ripple_radius = int(18 + 3 * math.sin(pygame.time.get_ticks() * 0.01))
        pygame.draw.circle(screen, (100, 200, 255), (int(self.x), int(self.y)), ripple_radius, 2)
        
        # Draw main tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw water spout effect
        spout_height = 8
        for i in range(3):
            spout_y = self.y - spout_height - i * 2
            spout_size = 3 - i
            pygame.draw.circle(screen, (173, 216, 230), (int(self.x), int(spout_y)), spout_size)
        
        # Draw water drops around tower
        for angle in [0, 72, 144, 216, 288]:
            rad = math.radians(angle + pygame.time.get_ticks() * 0.1)
            drop_x = self.x + math.cos(rad) * 10
            drop_y = self.y + math.sin(rad) * 10
            pygame.draw.circle(screen, (135, 206, 235), (int(drop_x), int(drop_y)), 2) 