import math
from typing import List
from .tower import Tower

class SniperTower(Tower):
    """High-range, high-damage tower with slow fire rate"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'sniper')
        self.range = 200
        self.damage = 35
        self.fire_rate = 90  # Slow but powerful
        self.projectile_speed = 12
        self.size = 15
        self.color = (0, 0, 200)  # Blue
        
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
        """Sniper targets the enemy with the most health"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                valid_targets.append((enemy, distance))
        
        if not valid_targets:
            self.target = None
            return
        
        # Target enemy with most health
        self.target = max(valid_targets, key=lambda x: x[0].health)[0]
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles: List):
        """Fire a sniper projectile"""
        if self.target:
            from projectiles import SniperProjectile
            projectile = SniperProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.tower_type
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency() 