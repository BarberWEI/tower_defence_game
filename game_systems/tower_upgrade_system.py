"""
Tower Upgrade System - Manages tower upgrades with three paths and tower-specific currencies
"""
from typing import Dict, List, Tuple, Optional
from enum import Enum

class UpgradeType(Enum):
    DAMAGE = "damage"
    RANGE = "range" 
    UTILITY = "utility"

class TowerUpgradeSystem:
    """Manages tower upgrades with three simultaneous upgrade paths"""
    
    def __init__(self):
        # Tower-specific currencies (gained by using towers)
        self.tower_currencies = {}
        
        # Upgrade definitions for each tower type
        self.upgrade_definitions = {
            'basic': {
                UpgradeType.DAMAGE: {
                    'name': 'Power',
                    'description': 'Increases damage',
                    'max_level': 5,
                    'base_cost': 10,
                    'effects': [
                        {'damage': 1},   # Level 1: +1 damage
                        {'damage': 2},   # Level 2: +2 damage  
                        {'damage': 3},   # Level 3: +3 damage
                        {'damage': 4},   # Level 4: +4 damage
                        {'damage': 6}    # Level 5: +6 damage
                    ]
                },
                UpgradeType.RANGE: {
                    'name': 'Scope',
                    'description': 'Increases range',
                    'max_level': 5,
                    'base_cost': 8,
                    'effects': [
                        {'range': 15},   # Level 1: +15 range
                        {'range': 20},   # Level 2: +20 range
                        {'range': 25},   # Level 3: +25 range
                        {'range': 30},   # Level 4: +30 range
                        {'range': 40}    # Level 5: +40 range
                    ]
                },
                UpgradeType.UTILITY: {
                    'name': 'Speed',
                    'description': 'Increases fire rate',
                    'max_level': 5,
                    'base_cost': 12,
                    'effects': [
                        {'fire_rate': -3},  # Level 1: 3 frames faster
                        {'fire_rate': -5},  # Level 2: 5 frames faster
                        {'fire_rate': -7},  # Level 3: 7 frames faster
                        {'fire_rate': -10}, # Level 4: 10 frames faster
                        {'fire_rate': -15}  # Level 5: 15 frames faster
                    ]
                }
            },
            'sniper': {
                UpgradeType.DAMAGE: {
                    'name': 'Precision',
                    'description': 'Increases damage',
                    'max_level': 5,
                    'base_cost': 15,
                    'effects': [
                        {'damage': 3}, {'damage': 5}, {'damage': 8}, {'damage': 12}, {'damage': 18}
                    ]
                },
                UpgradeType.RANGE: {
                    'name': 'Optics',
                    'description': 'Increases range',
                    'max_level': 5,
                    'base_cost': 12,
                    'effects': [
                        {'range': 30}, {'range': 40}, {'range': 50}, {'range': 60}, {'range': 80}
                    ]
                },
                UpgradeType.UTILITY: {
                    'name': 'Targeting',
                    'description': 'Can target invisible enemies',
                    'max_level': 3,
                    'base_cost': 20,
                    'effects': [
                        {'can_target_invisible': True},
                        {'crit_chance': 0.15},  # 15% crit chance
                        {'crit_multiplier': 2.5}  # 2.5x crit damage
                    ]
                }
            }
        }
        
        # Initialize upgrade definitions for all tower types
        self._initialize_all_upgrades()
    
    def _initialize_all_upgrades(self):
        """Initialize upgrade definitions for all tower types"""
        
        # Freezer Tower
        self.upgrade_definitions['freezer'] = {
            UpgradeType.DAMAGE: {
                'name': 'Frost',
                'description': 'Adds frost damage',
                'max_level': 5,
                'base_cost': 8,
                'effects': [
                    {'damage': 1}, {'damage': 2}, {'damage': 3}, {'damage': 5}, {'damage': 8}
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Reach',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 10,
                'effects': [
                    {'range': 12}, {'range': 18}, {'range': 25}, {'range': 32}, {'range': 40}
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Chill',
                'description': 'Improves freeze effect',
                'max_level': 5,
                'base_cost': 15,
                'effects': [
                    {'freeze_duration': 20}, {'freeze_duration': 30}, {'freeze_duration': 40}, 
                    {'freeze_duration': 60}, {'slow_factor': -0.2}
                ]
            }
        }
        
        # Detector Tower
        self.upgrade_definitions['detector'] = {
            UpgradeType.DAMAGE: {
                'name': 'Pulse',
                'description': 'Adds pulse damage',
                'max_level': 3,
                'base_cost': 12,
                'effects': [
                    {'damage': 1}, {'damage': 2}, {'damage': 4}
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Radar',
                'description': 'Increases detection range',
                'max_level': 5,
                'base_cost': 8,
                'effects': [
                    {'detection_range': 50}, {'detection_range': 75}, {'detection_range': 100}, 
                    {'detection_range': 125}, {'detection_range': 150}
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Scanner',
                'description': 'Detects more enemies',
                'max_level': 4,
                'base_cost': 18,
                'effects': [
                    {'max_detections': 1}, {'max_detections': 2}, {'max_detections': 3}, {'max_detections': 5}
                ]
            }
        }
        
        # Continue with remaining towers
        self._add_remaining_towers()
    
    def _add_remaining_towers(self):
        """Add upgrade definitions for remaining tower types"""
        
        # Anti-Air Tower
        self.upgrade_definitions['antiair'] = {
            UpgradeType.DAMAGE: {
                'name': 'Missiles',
                'description': 'Increases damage',
                'max_level': 5,
                'base_cost': 18,
                'effects': [
                    {'damage': 5}, {'damage': 8}, {'damage': 12}, {'damage': 18}, {'damage': 25}
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Radar',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 15,
                'effects': [
                    {'range': 25}, {'range': 35}, {'range': 45}, {'range': 55}, {'range': 70}
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Tracking',
                'description': 'Improves targeting',
                'max_level': 4,
                'base_cost': 20,
                'effects': [
                    {'can_target_invisible': True}, {'projectile_speed': 2}, 
                    {'fire_rate': -8}, {'splash_damage': 10}
                ]
            }
        }
        
        # Poison Tower
        self.upgrade_definitions['poison'] = {
            UpgradeType.DAMAGE: {
                'name': 'Toxin',
                'description': 'Increases poison damage',
                'max_level': 5,
                'base_cost': 12,
                'effects': [
                    {'poison_damage': 2}, {'poison_damage': 3}, {'poison_damage': 5}, 
                    {'poison_damage': 7}, {'poison_damage': 10}
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Spread',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 10,
                'effects': [
                    {'range': 20}, {'range': 25}, {'range': 30}, {'range': 40}, {'range': 50}
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Virulence',
                'description': 'Improves poison effects',
                'max_level': 5,
                'base_cost': 15,
                'effects': [
                    {'poison_duration': 60}, {'poison_duration': 120}, {'poison_spread': True}, 
                    {'poison_slow': 0.8}, {'poison_armor_reduction': 2}
                ]
            }
        }
        
        # Continue with more towers
        self._add_final_towers()
    
    def _add_final_towers(self):
        """Add upgrade definitions for final tower types"""
        
        # Laser Tower
        self.upgrade_definitions['laser'] = {
            UpgradeType.DAMAGE: {
                'name': 'Intensity',
                'description': 'Increases laser damage',
                'max_level': 5,
                'base_cost': 15,
                'effects': [
                    {'damage': 4}, {'damage': 6}, {'damage': 9}, {'damage': 13}, {'damage': 18}
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Focus',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 12,
                'effects': [
                    {'range': 20}, {'range': 30}, {'range': 40}, {'range': 50}, {'range': 65}
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Piercing',
                'description': 'Improves piercing',
                'max_level': 5,
                'base_cost': 18,
                'effects': [
                    {'max_pierce': 1}, {'max_pierce': 2}, {'max_pierce': 3}, 
                    {'max_pierce': 5}, {'burn_damage': 3}
                ]
            }
        }
        
        # Add all remaining tower types with similar structure
        for tower_type in ['cannon', 'lightning', 'flame', 'ice', 'explosive', 'missile', 'splash']:
            if tower_type not in self.upgrade_definitions:
                self.upgrade_definitions[tower_type] = self._generate_generic_upgrades(tower_type)
    
    def _generate_generic_upgrades(self, tower_type: str) -> Dict:
        """Generate generic upgrade paths for towers not explicitly defined"""
        return {
            UpgradeType.DAMAGE: {
                'name': 'Power',
                'description': 'Increases damage',
                'max_level': 5,
                'base_cost': 12,
                'effects': [
                    {'damage': 2}, {'damage': 4}, {'damage': 6}, {'damage': 9}, {'damage': 13}
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Range',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 10,
                'effects': [
                    {'range': 15}, {'range': 22}, {'range': 30}, {'range': 38}, {'range': 50}
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Efficiency',
                'description': 'Improves effectiveness',
                'max_level': 5,
                'base_cost': 15,
                'effects': [
                    {'fire_rate': -5}, {'fire_rate': -8}, {'fire_rate': -12}, 
                    {'fire_rate': -16}, {'fire_rate': -20}
                ]
            }
        }
    
    def get_tower_currency(self, tower_id: str, tower_type: str) -> int:
        """Get the current currency for a specific tower"""
        if tower_id not in self.tower_currencies:
            self.tower_currencies[tower_id] = 0
        return self.tower_currencies[tower_id]
    
    def add_tower_currency(self, tower_id: str, tower_type: str, amount: int):
        """Add currency to a specific tower based on damage dealt"""
        if tower_id not in self.tower_currencies:
            self.tower_currencies[tower_id] = 0
        self.tower_currencies[tower_id] += amount
    
    def get_upgrade_cost(self, tower_type: str, upgrade_type: UpgradeType, current_level: int) -> int:
        """Calculate the cost for the next upgrade level"""
        if tower_type not in self.upgrade_definitions:
            return 0
        
        upgrade_def = self.upgrade_definitions[tower_type][upgrade_type]
        if current_level >= upgrade_def['max_level']:
            return 0  # Max level reached
        
        # Cost increases with level: base_cost * (level + 1)
        return upgrade_def['base_cost'] * (current_level + 1)
    
    def can_upgrade(self, tower_id: str, tower_type: str, upgrade_type: UpgradeType, current_level: int) -> bool:
        """Check if a tower can be upgraded"""
        cost = self.get_upgrade_cost(tower_type, upgrade_type, current_level)
        currency = self.get_tower_currency(tower_id, tower_type)
        
        return cost > 0 and currency >= cost
    
    def upgrade_tower(self, tower_id: str, tower_type: str, upgrade_type: UpgradeType, current_level: int) -> bool:
        """Upgrade a tower if possible"""
        if not self.can_upgrade(tower_id, tower_type, upgrade_type, current_level):
            return False
        
        cost = self.get_upgrade_cost(tower_type, upgrade_type, current_level)
        self.tower_currencies[tower_id] -= cost
        return True
    
    def get_upgrade_info(self, tower_type: str, upgrade_type: UpgradeType) -> Dict:
        """Get upgrade information for UI display"""
        if tower_type not in self.upgrade_definitions:
            return {}
        
        return self.upgrade_definitions[tower_type][upgrade_type]
    
    def apply_upgrades_to_tower(self, tower, tower_id: str):
        """Apply all upgrades to a tower instance"""
        if not hasattr(tower, 'upgrades'):
            return
        
        tower_type = tower.tower_type
        if tower_type not in self.upgrade_definitions:
            return
        
        # Apply each upgrade type
        for upgrade_type in UpgradeType:
            level = tower.upgrades.get(upgrade_type, 0)
            if level > 0:
                self._apply_upgrade_effects(tower, tower_type, upgrade_type, level)
    
    def _apply_upgrade_effects(self, tower, tower_type: str, upgrade_type: UpgradeType, level: int):
        """Apply specific upgrade effects to a tower"""
        upgrade_def = self.upgrade_definitions[tower_type][upgrade_type]
        
        # Apply cumulative effects up to the current level
        for i in range(level):
            if i < len(upgrade_def['effects']):
                effects = upgrade_def['effects'][i]
                for stat, value in effects.items():
                    if hasattr(tower, stat):
                        if stat in ['fire_rate', 'slow_factor']:
                            # Additive for negative values
                            setattr(tower, stat, getattr(tower, stat) + value)
                        elif stat in ['crit_chance', 'lightning_multiplier']:
                            # Additive for multipliers
                            current = getattr(tower, stat, 0)
                            setattr(tower, stat, current + value)
                        elif stat in ['can_target_invisible', 'poison_spread', 'freeze_spread']:
                            # Boolean flags
                            setattr(tower, stat, value)
                        else:
                            # Additive for most stats
                            current = getattr(tower, stat, 0)
                            setattr(tower, stat, current + value) 