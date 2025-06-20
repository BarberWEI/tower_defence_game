from .tower import Tower
import math

class BasicTower(Tower):
    """Basic tower with standard stats and targeting"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'basic')
        self.range = 80
        self.damage = 2
        self.fire_rate = 25  # Faster firing
        self.projectile_speed = 6
        self.size = 12
        self.color = (0, 200, 0)  # Green
        
        # Targeting restrictions - ground only
        self.can_target_flying = False
        self.can_target_invisible = False
        
        # Finalize initialization to update base stats
        self.finalize_initialization()
    
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
    
    def acquire_target_optimized(self, enemies):
        """Optimized targeting with targeting restrictions"""
        if not enemies:
            self.target = None
            return
        
        range_squared = self.range * self.range
        valid_targets = []
        
        # Use squared distance for initial filtering (avoids sqrt)
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance_squared = dx * dx + dy * dy
            
            if distance_squared <= range_squared and self.can_target_enemy(enemy):
                # Only calculate actual distance for valid targets
                actual_distance = math.sqrt(distance_squared)
                valid_targets.append((enemy, actual_distance))
                
                # Early termination for performance
                if len(valid_targets) >= 10:
                    break
        
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
    
    def update_with_speed_optimized(self, enemies, projectiles, speed_multiplier: float):
        """Update with speed multiplier and targeting restrictions"""
        self.acquire_target_optimized(enemies)
        
        if self.target and self.fire_timer <= 0:
            self.shoot(projectiles)
            self.fire_timer = self.fire_rate
        
        # Decrease fire timer based on speed multiplier
        if self.fire_timer > 0:
            self.fire_timer -= speed_multiplier