import pygame
import math
import uuid
from typing import List, Optional, Dict
from config.game_config import get_balance_config
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
        
        # Current stats (base + upgrades + terrain effects)
        self.range = self.base_range
        self.damage = self.base_damage
        self.fire_rate = self.base_fire_rate
        
        # Terrain effects tracking
        self.terrain_effects_applied = False
        self.terrain_type = None
        
        # Flag to track if subclass has finished initialization
        self._initialization_complete = False
        
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
        
        # Reference to game systems (set by tower manager)
        self.map_reference = None
        self.upgrade_system_reference = None
        
    def set_grid_position(self, grid_x: int, grid_y: int):
        """Set the grid position and apply terrain effects"""
        self.grid_x = grid_x
        self.grid_y = grid_y
        # Reset terrain effects and reapply for new position
        if self.map_reference and self._initialization_complete:
            self.terrain_effects_applied = False
            self.apply_terrain_effects()
    
    def set_map_reference(self, map_obj):
        """Set reference to map for terrain effects"""
        self.map_reference = map_obj
        if not self.terrain_effects_applied and self._initialization_complete:
            self.apply_terrain_effects()
    
    def finalize_initialization(self):
        """Call this after subclass sets its stats to update base values"""
        self.base_range = self.range
        self.base_damage = self.damage
        self.base_fire_rate = self.fire_rate
        self._initialization_complete = True
        
        # Apply terrain effects if map reference is already set
        if self.map_reference and not self.terrain_effects_applied:
            self.apply_terrain_effects()
    
    def set_upgrade_system_reference(self, upgrade_system):
        """Set reference to upgrade system for currency generation"""
        self.upgrade_system_reference = upgrade_system
    
    def apply_terrain_effects(self):
        """Apply terrain-specific effects to this tower"""
        if not self.map_reference or self.terrain_effects_applied:
            return
            
        from game_systems.terrain_types import get_terrain_property
        
        terrain_type = self.map_reference.get_terrain_at_grid(self.grid_x, self.grid_y)
        self.terrain_type = terrain_type
        special_rules = get_terrain_property(terrain_type, 'special_rules')
        
        if special_rules == 'reduced_range':
            # Forest reduces tower range by 20% but increases damage by 30%
            self.range = int(self.base_range * 0.8)
            self.damage = int(self.base_damage * 1.3)
        elif special_rules == 'water_only':
            # Water terrain gives special bonuses to certain towers
            if hasattr(self, 'freeze_duration'):
                self.freeze_duration = int(self.freeze_duration * 1.5)
            # Water also increases range by 10% for water-compatible towers
            self.range = int(self.base_range * 1.1)
        
        self.terrain_effects_applied = True
    
    def track_damage_and_generate_currency(self, damage_dealt: int):
        """Track damage and generate currency - centralized for all towers using config values"""
        if damage_dealt > 0:
            self.add_damage_dealt(damage_dealt)
            
            # Generate currency using config value
            config = get_balance_config()
            currency_amount = max(1, damage_dealt // config['currency']['damage_divisor'])
            
            if self.upgrade_system_reference:
                self.upgrade_system_reference.add_tower_currency(
                    self.tower_id, self.tower_type, currency_amount
                )
    
    def track_utility_hit(self):
        """Track utility hit for support towers - centralized using config values"""
        # Support towers get minimal currency for successful hits
        config = get_balance_config()
        currency_amount = config['currency']['utility_hit_reward']
        
        if self.upgrade_system_reference:
            self.upgrade_system_reference.add_tower_currency(
                self.tower_id, self.tower_type, currency_amount
            )

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
    
    def generate_firing_currency(self):
        """Generate currency immediately when tower fires a projectile"""
        config = get_balance_config()
        currency_amount = config['currency']['firing_reward']
        
        if self.upgrade_system_reference:
            self.upgrade_system_reference.add_tower_currency(
                self.tower_id, self.tower_type, currency_amount
            )

    def shoot(self, projectiles: List):
        """Create and fire a projectile at the target"""
        if self.target:
            from projectiles import BasicProjectile
            projectile = BasicProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.tower_type
            )
            # Link projectile to tower for damage tracking
            projectile.source_tower_id = self.tower_id
            projectiles.append(projectile)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
    
    def add_damage_dealt(self, damage: int):
        """Track damage dealt by this tower for currency generation"""
        self.total_damage_dealt += damage
    
    def reset_stats_to_base(self):
        """Reset stats to base values before applying upgrades and terrain effects"""
        self.range = self.base_range
        self.damage = self.base_damage
        self.fire_rate = self.base_fire_rate
        
        # Reapply terrain effects after reset
        self.terrain_effects_applied = False
        self.apply_terrain_effects()
    
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