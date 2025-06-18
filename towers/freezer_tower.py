import math
from typing import List
from .tower import Tower

class FreezerTower(Tower):
    """Tower that slows enemies with freeze effect"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.range = 70
        self.damage = 0  # No damage, just freeze
        self.fire_rate = 45  # ~1.3 shots per second at 60 FPS
        self.projectile_speed = 4
        self.size = 13
        self.color = (100, 200, 255)  # Light blue
        self.freeze_duration = 90  # 1.5 seconds at 60 FPS
    
    def acquire_target(self, enemies: List):
        """Freezer targets the fastest enemy"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and not enemy.frozen:
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
            projectiles.append(projectile) 