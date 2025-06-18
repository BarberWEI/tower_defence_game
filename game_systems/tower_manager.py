from typing import List, Tuple, Optional
from .tower_sizes import get_tower_size, get_tower_visual_size

class TowerManager:
    """Manages tower placement, costs, and tower-related logic"""
    
    def __init__(self):
        # Base tower costs - these will be modified by wave progression
        self.base_tower_costs = {
            "basic": 15,      # Cheap starter tower
            "sniper": 45,     # Long range, high damage
            "freezer": 25,    # Utility tower - slows enemies
            "detector": 30,   # Support tower - reveals invisible
            "antiair": 55,    # Specialized for flying enemies
            "poison": 40,     # DOT specialist
            "laser": 60,      # Piercing damage
            "cannon": 75,     # Area damage, 2x2 size
            "lightning": 50,  # Chain lightning
            "flame": 35,      # Cone attack with burn
            "ice": 30,        # Area freeze
            "explosive": 100, # Massive damage, 3x3 size
            "missile": 120,   # Homing missiles with AOE
            "splash": 35      # Water-only, applies wet status
        }
        
        # Current wave number for cost calculation
        self.current_wave = 1
        
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
        """Calculate tower cost with wave-based progression"""
        if wave_number <= 1:
            return base_cost
        
        # Cost increases by 8% per wave after wave 1, with diminishing returns
        wave_factor = wave_number - 1
        
        # Progressive cost scaling with reasonable caps
        if wave_number <= 10:
            # Early game: 8% per wave
            multiplier = 1.0 + (wave_factor * 0.08)
        elif wave_number <= 20:
            # Mid game: 5% per wave (slower growth)
            early_multiplier = 1.0 + (9 * 0.08)  # First 10 waves
            mid_factor = wave_number - 10
            multiplier = early_multiplier + (mid_factor * 0.05)
        else:
            # Late game: 3% per wave (even slower)
            early_multiplier = 1.0 + (9 * 0.08)  # First 10 waves
            mid_multiplier = early_multiplier + (10 * 0.05)  # Next 10 waves
            late_factor = wave_number - 20
            multiplier = mid_multiplier + (late_factor * 0.03)
        
        # Cap the cost increase at 4x original cost
        multiplier = min(multiplier, 4.0)
        
        return int(base_cost * multiplier)
    
    def get_tower_cost(self, tower_type: str) -> int:
        """Get the cost of a tower type"""
        return self.calculate_progressive_cost(self.base_tower_costs.get(tower_type, 0), self.current_wave)
    
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
    
    def create_tower(self, tower_type: str, x: int, y: int, grid_x: int = 0, grid_y: int = 0, cell_size: int = 40):
        """Create a new tower of the specified type with multi-block support"""
        tower_classes = self._get_tower_classes()
        if tower_type in tower_classes:
            tower_class = tower_classes[tower_type]
            tower = tower_class(x, y)
            
            # Set tower type and grid position
            tower.tower_type = tower_type
            tower.grid_x = grid_x
            tower.grid_y = grid_y
            
            # Set visual size based on tower type and cell size
            tower.size = get_tower_visual_size(tower_type, cell_size)
            
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
            tower = self.create_tower(tower_type, int(center_x), int(center_y), 
                                    grid_x, grid_y, map_obj.cell_size)
            if tower:
                # Set references for terrain effects and currency generation
                tower.set_map_reference(map_obj)
                tower.set_grid_position(grid_x, grid_y)
                
                # Apply terrain effects to the tower (now handled by base Tower class)
                tower.apply_terrain_effects()
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