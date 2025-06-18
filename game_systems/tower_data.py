"""
Tower Data Management - Centralized tower information
"""

class TowerDataManager:
    """Manages tower information and provides data to UI and game systems"""
    
    def __init__(self, tower_manager):
        self.tower_manager = tower_manager
        
        # Tower type mapping (order matters for UI display)
        self.tower_types = [
            'basic', 'sniper', 'freezer', 'detector', 'antiair', 'poison', 
            'laser', 'cannon', 'lightning', 'flame', 'ice', 'explosive', 
            'missile', 'splash'
        ]
        
        # Tower display names
        self.tower_names = {
            'basic': 'Basic Tower',
            'sniper': 'Sniper Tower', 
            'freezer': 'Freezer Tower',
            'detector': 'Detector Tower',
            'antiair': 'Anti-Air Tower',
            'poison': 'Poison Tower',
            'laser': 'Laser Tower',
            'cannon': 'Cannon Tower',
            'lightning': 'Lightning Tower',
            'flame': 'Flame Tower',
            'ice': 'Ice Tower',
            'explosive': 'Explosive Tower',
            'missile': 'Missile Tower',
            'splash': 'Splash Tower'
        }
        
        # Tower descriptions
        self.tower_descriptions = {
            'basic': 'Cheap starter tower',
            'sniper': 'Long range, high damage',
            'freezer': 'Slows enemies with damage',
            'detector': 'Reveals invisible enemies',
            'antiair': 'Targets flying enemies',
            'poison': 'Poison damage over time',
            'laser': 'Pierces through enemies',
            'cannon': 'Splash damage, 2x2 size',
            'lightning': 'Chains between enemies',
            'flame': 'Cone attack with burn',
            'ice': 'Area freeze, no damage',
            'explosive': 'Massive splash, 3x3 size',
            'missile': 'Homing missiles, AOE, 2x2 size',
            'splash': 'Water-only, makes enemies wet'
        }
        
        # Tower colors for UI display
        self.tower_colors = {
            'basic': (0, 200, 0),
            'sniper': (0, 0, 255),
            'freezer': (0, 255, 255),
            'detector': (255, 255, 0),
            'antiair': (0, 191, 255),
            'poison': (50, 205, 50),
            'laser': (255, 0, 255),
            'cannon': (139, 69, 19),
            'lightning': (255, 255, 0),
            'flame': (255, 69, 0),
            'ice': (173, 216, 230),
            'explosive': (255, 165, 0),
            'missile': (128, 128, 128),
            'splash': (30, 144, 255)
        }
    
    def get_tower_count(self) -> int:
        """Get total number of tower types"""
        return len(self.tower_types)
    
    def get_tower_type_by_index(self, index: int) -> str:
        """Get tower type by index"""
        if 0 <= index < len(self.tower_types):
            return self.tower_types[index]
        return None
    
    def get_tower_data(self, tower_type: str) -> dict:
        """Get complete tower data for UI display"""
        if tower_type not in self.tower_types:
            return None
            
        # Get cost from tower manager
        cost = self.tower_manager.get_tower_cost(tower_type)
        
        # Get tower instance to read stats
        tower_class = self.tower_manager.tower_classes.get(tower_type)
        if tower_class:
            # Create temporary instance to read stats
            temp_tower = tower_class(0, 0)
            stats = self._extract_tower_stats(temp_tower)
        else:
            stats = {}
        
        return {
            'type': tower_type,
            'name': self.tower_names.get(tower_type, tower_type.title()),
            'cost': cost,
            'color': self.tower_colors.get(tower_type, (128, 128, 128)),
            'description': self.tower_descriptions.get(tower_type, 'Tower'),
            'stats': stats
        }
    
    def get_all_tower_data(self) -> list:
        """Get data for all towers for UI display"""
        return [self.get_tower_data(tower_type) for tower_type in self.tower_types]
    
    def _extract_tower_stats(self, tower) -> dict:
        """Extract displayable stats from a tower instance"""
        stats = {}
        
        # Damage
        if hasattr(tower, 'damage'):
            stats['Damage'] = tower.damage
        
        # Range
        if hasattr(tower, 'range'):
            stats['Range'] = tower.range
            
        # Speed (convert fire rate to readable format)
        if hasattr(tower, 'fire_rate'):
            if tower.fire_rate <= 20:
                speed = 'Very Fast'
            elif tower.fire_rate <= 35:
                speed = 'Fast'
            elif tower.fire_rate <= 50:
                speed = 'Medium'
            elif tower.fire_rate <= 70:
                speed = 'Slow'
            elif tower.fire_rate <= 100:
                speed = 'Very Slow'
            else:
                speed = 'Ultra Slow'
            stats['Speed'] = speed
        
        return stats 