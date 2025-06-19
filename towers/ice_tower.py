from .tower import Tower
import pygame
import math

class IceTower(Tower):
    """Advanced freezing tower that slows enemies in an area"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'ice')
        self.damage = 0  # No damage, just freeze (swapped with freezer)
        self.range = 90   # Slightly reduced range (was 100)
        self.fire_rate = 60  # Much slower firing (was 45)
        self.projectile_speed = 5
        self.size = 12
        self.color = (173, 216, 230)  # Light blue
        
        # Ice properties - significantly nerfed
        self.freeze_duration = 40  # Even shorter freeze (was 60 frames)
        self.slow_factor = 0.5  # Less severe slow - 50% speed (was 30%)
        self.area_effect_radius = 40  # Smaller area (was 50)
        
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
        """Create ice blast with area freeze effect"""
        if self.target:
            from projectiles import IceProjectile
            projectile = IceProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.tower_type, self.freeze_duration,
                self.area_effect_radius, self.slow_factor
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
    
    def draw(self, screen, selected: bool = False):
        """Draw ice tower"""
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw ice crystals
        for angle in [0, 60, 120, 180, 240, 300]:
            rad = math.radians(angle)
            crystal_x = self.x + math.cos(rad) * 8
            crystal_y = self.y + math.sin(rad) * 8
            points = [
                (crystal_x, crystal_y - 4),
                (crystal_x - 2, crystal_y + 2),
                (crystal_x + 2, crystal_y + 2)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), points)
