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
                self.projectile_speed, self.damage, self.freeze_duration
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile) 