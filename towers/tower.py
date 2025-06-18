import pygame
import math
import uuid
from typing import List, Optional, Dict
from game_systems.tower_upgrade_system import UpgradeType

class Tower:
    """Base class for all towers"""
    def __init__(self, x: int, y: int, tower_type: str = 'basic'):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        
        # Unique identifier for currency tracking
        self.tower_id = str(uuid.uuid4())
        
        # Grid position (will be set by tower manager)
        self.grid_x = 0
        self.grid_y = 0
        
        # Base stats - to be overridden by subclasses
        self.base_range = 100
        self.base_damage = 1
        self.base_fire_rate = 60  # frames between shots
        self.projectile_speed = 5
        self.size = 15
        self.color = (0, 255, 0)  # Green by default
        
        # Current stats (base + upgrades)
        self.range = self.base_range
        self.damage = self.base_damage
        self.fire_rate = self.base_fire_rate
        
        # Upgrade tracking
        self.upgrades: Dict[UpgradeType, int] = {
            UpgradeType.DAMAGE: 0,
            UpgradeType.RANGE: 0,
            UpgradeType.UTILITY: 0
        }
        
        # State
        self.fire_timer = 0
        self.target: Optional[object] = None
        self.angle = 0
        
        # Currency tracking
        self.total_damage_dealt = 0
        
    def update(self, enemies: List, projectiles: List):
        """Update tower state and shooting"""
        # Update fire timer
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Shoot at target if ready
        if self.target and self.fire_timer <= 0:
            self.shoot(projectiles)
            self.fire_timer = self.fire_rate
    
    def acquire_target(self, enemies: List):
        """Find the best target based on tower's targeting strategy"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range:
                valid_targets.append((enemy, distance))
        
        if not valid_targets:
            self.target = None
            return
        
        # Default targeting: closest to end of path
        self.target = max(valid_targets, key=lambda x: x[0].get_distance_from_start())[0]
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles: List):
        """Create and fire a projectile at the target"""
        if self.target:
            from projectiles import BasicProjectile
            projectile = BasicProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
    
    def add_damage_dealt(self, damage: int):
        """Track damage dealt by this tower for currency generation"""
        self.total_damage_dealt += damage
    
    def reset_stats_to_base(self):
        """Reset stats to base values before applying upgrades"""
        self.range = self.base_range
        self.damage = self.base_damage
        self.fire_rate = self.base_fire_rate
    
    def get_upgrade_level(self, upgrade_type: UpgradeType) -> int:
        """Get the current upgrade level for a specific upgrade type"""
        return self.upgrades.get(upgrade_type, 0)
    
    def set_upgrade_level(self, upgrade_type: UpgradeType, level: int):
        """Set the upgrade level for a specific upgrade type"""
        self.upgrades[upgrade_type] = level
    
    def draw(self, screen: pygame.Surface, selected: bool = False):
        """Draw the tower on the screen"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), self.range, 1)
        
        # Draw tower base
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.size, 2)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (end_x, end_y), 3) 