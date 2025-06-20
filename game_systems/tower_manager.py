from typing import List, Tuple, Optional
from config.game_config import get_tower_config
from .tower_sizes import get_tower_size, get_tower_visual_size

class TowerManager:
    """Manages tower placement, costs, and tower-related logic"""
    
    def __init__(self):
        # Load tower configuration from centralized config
        self.config = get_tower_config()
        self.base_tower_costs = self.config['base_costs']
        self.cost_progression = self.config['cost_progression']
        self.dynamic_cost_config = self.config.get('dynamic_cost_increase', {})
        
        # Current wave number for cost calculation
        self.current_wave = 1
        
        # Track towers built for dynamic cost increases
        self.towers_built_count = {tower_type: 0 for tower_type in self.base_tower_costs}
        
        # State
        self.selected_tower_type: Optional[str] = None
        self.placing_tower = False
    
    def _get_tower_classes(self):
        """Get tower classes with lazy import to avoid circular dependency"""
        from towers import (BasicTower, SniperTower, FreezerTower, DetectorTower, 
                           AntiAirTower, PoisonTower, LaserTower, CannonTower,
                           LightningTower, FlameTower, IceTower, ExplosiveTower, MissileTower, SplashTower)
        
        return {
            "basic": BasicTower,
            "sniper": SniperTower,
            "freezer": FreezerTower,
            "detector": DetectorTower,
            "antiair": AntiAirTower,
            "poison": PoisonTower,
            "laser": LaserTower,
            "cannon": CannonTower,
            "lightning": LightningTower,
            "flame": FlameTower,
            "ice": IceTower,
            "explosive": ExplosiveTower,
            "missile": MissileTower,
            "splash": SplashTower
        }
    
    def set_current_wave(self, wave_number: int):
        """Update the current wave number for cost calculations"""
        self.current_wave = wave_number
    
    def calculate_progressive_cost(self, base_cost: int, wave_number: int) -> int:
        """Calculate tower cost with wave-based progression using config values"""
        if wave_number <= 1:
            return base_cost
        
        # Get progression config
        early_waves = self.cost_progression['early_game_waves']
        mid_waves = self.cost_progression['mid_game_waves']
        early_increase = self.cost_progression['early_increase_per_wave']
        mid_increase = self.cost_progression['mid_increase_per_wave']
        late_increase = self.cost_progression['late_increase_per_wave']
        max_multiplier = self.cost_progression['max_cost_multiplier']
        
        wave_factor = wave_number - 1
        
        # Progressive cost scaling using config values
        if wave_number <= early_waves:
            # Early game: use early_increase_per_wave
            multiplier = 1.0 + (wave_factor * early_increase)
        elif wave_number <= mid_waves:
            # Mid game: use mid_increase_per_wave
            early_multiplier = 1.0 + ((early_waves - 1) * early_increase)  # First early waves
            mid_factor = wave_number - early_waves
            multiplier = early_multiplier + (mid_factor * mid_increase)
        else:
            # Late game: use late_increase_per_wave
            early_multiplier = 1.0 + ((early_waves - 1) * early_increase)  # First early waves
            mid_multiplier = early_multiplier + ((mid_waves - early_waves) * mid_increase)  # Next mid waves
            late_factor = wave_number - mid_waves
            multiplier = mid_multiplier + (late_factor * late_increase)
        
        # Cap the cost increase using config value
        multiplier = min(multiplier, max_multiplier)
        
        return int(base_cost * multiplier)
    
    def calculate_dynamic_cost_multiplier(self, tower_type: str) -> float:
        """Calculate cost multiplier based on how many towers of this type have been built"""
        if not self.dynamic_cost_config:
            return 1.0
        
        towers_built = self.towers_built_count.get(tower_type, 0)
        per_tower_multiplier = self.dynamic_cost_config.get('per_tower_built_multiplier', 0.15)
        max_multiplier = self.dynamic_cost_config.get('max_per_tower_multiplier', 2.5)
        
        # Calculate multiplier: 1.0 + (towers_built * per_tower_multiplier)
        multiplier = 1.0 + (towers_built * per_tower_multiplier)
        
        # Cap the multiplier
        multiplier = min(multiplier, max_multiplier)
        
        return multiplier
    
    def get_tower_cost(self, tower_type: str) -> int:
        """Get the cost of a tower type with wave and usage-based progression"""
        base_cost = self.base_tower_costs.get(tower_type, 0)
        
        # Calculate wave-based cost progression
        wave_cost = self.calculate_progressive_cost(base_cost, self.current_wave)
        
        # Calculate dynamic cost increase based on towers built
        dynamic_multiplier = self.calculate_dynamic_cost_multiplier(tower_type)
        
        # Apply dynamic cost increase
        final_cost = int(wave_cost * dynamic_multiplier)
        
        return final_cost
    
    def can_afford_tower(self, tower_type: str, money: int) -> bool:
        """Check if player can afford a tower"""
        return money >= self.get_tower_cost(tower_type)
    
    def select_tower_type(self, tower_type: str):
        """Select a tower type for placement"""
        tower_classes = self._get_tower_classes()
        if tower_type in tower_classes:
            self.selected_tower_type = tower_type
            self.placing_tower = True
    
    def cancel_placement(self):
        """Cancel tower placement"""
        self.selected_tower_type = None
        self.placing_tower = False
    
    def create_tower(self, tower_type, x, y):
        """Create a new tower at the specified position"""
        # Use the same tower classes as _get_tower_classes for consistency
        tower_classes = self._get_tower_classes()
        
        if tower_type in tower_classes:
            tower_class = tower_classes[tower_type]
            tower = tower_class(x, y)
            return tower
        
        return None
    
    def attempt_tower_placement(self, pos: Tuple[int, int], money: int, 
                              existing_towers: List, map_obj) -> Tuple[bool, Optional[object], int]:
        """
        Attempt to place a tower at the given position with terrain awareness
        Returns: (success, tower_object, cost)
        """
        if not self.placing_tower or not self.selected_tower_type:
            return False, None, 0
        
        x, y = pos
        tower_type = self.selected_tower_type
        cost = self.get_tower_cost(tower_type)
        
        # Check if player can afford it
        if not self.can_afford_tower(tower_type, money):
            return False, None, 0
        
        # Check if position is valid with terrain awareness
        if map_obj.is_valid_tower_position(x, y, existing_towers, tower_type):
            # Snap to grid position
            grid_x, grid_y = map_obj.pixel_to_grid(x, y)
            
            # Calculate center position for multi-block towers
            width, height = get_tower_size(tower_type)
            center_x = map_obj.map_offset_x + (grid_x + width/2) * map_obj.cell_size
            center_y = map_obj.map_offset_y + (grid_y + height/2) * map_obj.cell_size
            
            # Create tower at calculated center
            tower = self.create_tower(tower_type, int(center_x), int(center_y))
            if tower:
                # Set references for terrain effects and currency generation
                tower.set_map_reference(map_obj)
                tower.set_grid_position(grid_x, grid_y)
                
                # Apply terrain effects to the tower (now handled by base Tower class)
                tower.apply_terrain_effects()
                
                # Increment tower built counter for dynamic cost increases
                self.towers_built_count[tower_type] = self.towers_built_count.get(tower_type, 0) + 1
                
                self.cancel_placement()  # Reset placement state
                return True, tower, cost
        
        return False, None, 0
    
    def get_tower_info(self) -> dict:
        """Get information about all available towers"""
        tower_classes = self._get_tower_classes()
        return {
            tower_type: {
                'cost': self.get_tower_cost(tower_type),
                'class': tower_classes[tower_type]
            }
            for tower_type in self.base_tower_costs
        }
    
    def get_placement_state(self) -> dict:
        """Get current placement state"""
        return {
            'placing_tower': self.placing_tower,
            'selected_tower_type': self.selected_tower_type,
            'selected_cost': self.get_tower_cost(self.selected_tower_type) if self.selected_tower_type else 0
        }
    
    def reset_tower_counts(self):
        """Reset tower build counts (for game restart)"""
        self.towers_built_count = {tower_type: 0 for tower_type in self.base_tower_costs}
    
    def reset_ui_state(self):
        """Reset all tower manager UI state to initial conditions"""
        self.selected_tower_type = None
        self.placing_tower = False 