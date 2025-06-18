from typing import List, Tuple, Optional
from towers import BasicTower, SniperTower, FreezerTower

class TowerManager:
    """Manages tower placement, costs, and tower-related logic"""
    
    def __init__(self):
        # Tower costs
        self.tower_costs = {
            "basic": 20,
            "sniper": 50,
            "freezer": 30
        }
        
        # Tower classes
        self.tower_classes = {
            "basic": BasicTower,
            "sniper": SniperTower,
            "freezer": FreezerTower
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
    
    def create_tower(self, tower_type: str, x: int, y: int):
        """Create a new tower of the specified type"""
        if tower_type in self.tower_classes:
            tower_class = self.tower_classes[tower_type]
            return tower_class(x, y)
        return None
    
    def attempt_tower_placement(self, pos: Tuple[int, int], money: int, 
                              is_valid_position_func) -> Tuple[bool, Optional[object], int]:
        """
        Attempt to place a tower at the given position
        Returns: (success, tower_object, cost)
        """
        if not self.placing_tower or not self.selected_tower_type:
            return False, None, 0
        
        x, y = pos
        tower_type = self.selected_tower_type
        cost = self.get_tower_cost(tower_type)
        
        # Check if position is valid and player can afford it
        if is_valid_position_func(x, y) and self.can_afford_tower(tower_type, money):
            tower = self.create_tower(tower_type, x, y)
            if tower:
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