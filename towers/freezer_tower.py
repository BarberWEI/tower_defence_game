import math
from typing import List
from .tower import Tower

class FreezerTower(Tower):
    """Tower that slows enemies with freeze effect"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'freezer')
        self.range = 70
        self.damage = 2  # Low damage (swapped with ice tower)
        self.fire_rate = 50  # Much slower firing (was 20)
        self.projectile_speed = 5
        self.size = 13
        self.color = (100, 200, 255)  # Light blue
        self.freeze_duration = 90  # 1.5 seconds at 60 FPS
        
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
    
    def acquire_target(self, enemies: List):
        """Freezer targets the fastest enemy"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and not getattr(enemy, 'frozen', False) and self.can_target_enemy(enemy):
                valid_targets.append((enemy, distance))
        
        if not valid_targets:
            self.target = None
            return
        
        # Target fastest enemy that's not already frozen
        self.target = max(valid_targets, key=lambda x: x[0].speed)[0]
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles: List):
        """Fire a freeze projectile"""
        if self.target:
            from projectiles import FreezeProjectile
            projectile = FreezeProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.tower_type, self.freeze_duration
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency() 

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