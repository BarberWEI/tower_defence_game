from typing import List, Tuple, Optional
from towers import (BasicTower, SniperTower, FreezerTower, DetectorTower, 
                   AntiAirTower, PoisonTower, LaserTower, CannonTower,
                   LightningTower, FlameTower, IceTower, ExplosiveTower, MissileTower)
from .tower_sizes import get_tower_size, get_tower_visual_size

class TowerManager:
    """Manages tower placement, costs, and tower-related logic"""
    
    def __init__(self):
        # Tower costs - rebalanced for better progression
        self.tower_costs = {
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
            "missile": 120    # Homing missiles with AOE
        }
        
        # Tower classes
        self.tower_classes = {
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
            "missile": MissileTower
        }
        
        # State
        self.selected_tower_type: Optional[str] = None
        self.placing_tower = False
    
    def get_tower_cost(self, tower_type: str) -> int:
        """Get the cost of a tower type"""
        return self.tower_costs.get(tower_type, 0)
    
    def can_afford_tower(self, tower_type: str, money: int) -> bool:
        """Check if player can afford a tower"""
        return money >= self.get_tower_cost(tower_type)
    
    def select_tower_type(self, tower_type: str):
        """Select a tower type for placement"""
        if tower_type in self.tower_classes:
            self.selected_tower_type = tower_type
            self.placing_tower = True
    
    def cancel_placement(self):
        """Cancel tower placement"""
        self.selected_tower_type = None
        self.placing_tower = False
    
    def create_tower(self, tower_type: str, x: int, y: int, grid_x: int = 0, grid_y: int = 0, cell_size: int = 40):
        """Create a new tower of the specified type with multi-block support"""
        if tower_type in self.tower_classes:
            tower_class = self.tower_classes[tower_type]
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
                # Apply terrain effects to the tower
                map_obj.apply_terrain_effects_to_tower(tower, grid_x, grid_y)
                self.cancel_placement()  # Reset placement state
                return True, tower, cost
        
        return False, None, 0
    
    def get_tower_info(self) -> dict:
        """Get information about all available towers"""
        return {
            tower_type: {
                'cost': cost,
                'class': self.tower_classes[tower_type]
            }
            for tower_type, cost in self.tower_costs.items()
        }
    
    def get_placement_state(self) -> dict:
        """Get current placement state"""
        return {
            'placing_tower': self.placing_tower,
            'selected_tower_type': self.selected_tower_type,
            'selected_cost': self.get_tower_cost(self.selected_tower_type) if self.selected_tower_type else 0
        } 