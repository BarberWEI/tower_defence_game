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
        
        # Upgrade definitions for each tower type - SIGNIFICANTLY NERFED
        self.upgrade_definitions = {
            'basic': {
                UpgradeType.DAMAGE: {
                    'name': 'Power',
                    'description': 'Increases damage',
                    'max_level': 5,
                    'base_cost': 30,  # 3x increase from 10
                    'effects': [
                        {'damage': 1},   # Level 1: +1 damage (unchanged, already small)
                        {'damage': 1},   # Level 2: +1 damage (reduced from +2)
                        {'damage': 2},   # Level 3: +2 damage (reduced from +3)
                        {'damage': 2},   # Level 4: +2 damage (reduced from +4)
                        {'damage': 3}    # Level 5: +3 damage (reduced from +6)
                    ]
                },
                UpgradeType.RANGE: {
                    'name': 'Scope',
                    'description': 'Increases range',
                    'max_level': 5,
                    'base_cost': 25,  # 3x increase from 8
                    'effects': [
                        {'range': 8},    # Level 1: +8 range (reduced from +15)
                        {'range': 10},   # Level 2: +10 range (reduced from +20)
                        {'range': 12},   # Level 3: +12 range (reduced from +25)
                        {'range': 15},   # Level 4: +15 range (reduced from +30)
                        {'range': 20}    # Level 5: +20 range (reduced from +40)
                    ]
                },
                UpgradeType.UTILITY: {
                    'name': 'Speed',
                    'description': 'Increases fire rate',
                    'max_level': 5,
                    'base_cost': 35,  # 3x increase from 12
                    'effects': [
                        {'fire_rate': -2},  # Level 1: 2 frames faster (reduced from -3)
                        {'fire_rate': -3},  # Level 2: 3 frames faster (reduced from -5)
                        {'fire_rate': -4},  # Level 3: 4 frames faster (reduced from -7)
                        {'fire_rate': -5},  # Level 4: 5 frames faster (reduced from -10)
                        {'fire_rate': -8}   # Level 5: 8 frames faster (reduced from -15)
                    ]
                }
            },
            'sniper': {
                UpgradeType.DAMAGE: {
                    'name': 'Precision',
                    'description': 'Increases damage',
                    'max_level': 5,
                    'base_cost': 45,  # 3x increase from 15
                    'effects': [
                        {'damage': 2}, {'damage': 3}, {'damage': 4}, {'damage': 6}, {'damage': 8}  # ~50% reduction
                    ]
                },
                UpgradeType.RANGE: {
                    'name': 'Optics',
                    'description': 'Increases range',
                    'max_level': 5,
                    'base_cost': 36,  # 3x increase from 12
                    'effects': [
                        {'range': 15}, {'range': 20}, {'range': 25}, {'range': 30}, {'range': 40}  # ~50% reduction
                    ]
                },
                UpgradeType.UTILITY: {
                    'name': 'Targeting',
                    'description': 'Can target invisible enemies',
                    'max_level': 3,
                    'base_cost': 60,  # 3x increase from 20
                    'effects': [
                        {'can_target_invisible': True},
                        {'crit_chance': 0.10},  # 10% crit chance (reduced from 15%)
                        {'crit_multiplier': 2.0}  # 2.0x crit damage (reduced from 2.5x)
                    ]
                }
            }
        }
        
        # Initialize upgrade definitions for all tower types
        self._initialize_all_upgrades()
    
    def _initialize_all_upgrades(self):
        """Initialize upgrade definitions for all tower types"""
        
        # Freezer Tower - NERFED
        self.upgrade_definitions['freezer'] = {
            UpgradeType.DAMAGE: {
                'name': 'Frost',
                'description': 'Adds frost damage',
                'max_level': 5,
                'base_cost': 24,  # 3x increase from 8
                'effects': [
                    {'damage': 1}, {'damage': 1}, {'damage': 2}, {'damage': 2}, {'damage': 3}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Reach',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 30,  # 3x increase from 10
                'effects': [
                    {'range': 6}, {'range': 9}, {'range': 12}, {'range': 16}, {'range': 20}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Chill',
                'description': 'Improves freeze effect',
                'max_level': 5,
                'base_cost': 45,  # 3x increase from 15
                'effects': [
                    {'freeze_duration': 10}, {'freeze_duration': 15}, {'freeze_duration': 20}, 
                    {'freeze_duration': 30}, {'slow_factor': -0.1}  # ~50% reduction
                ]
            }
        }
        
        # Detector Tower - NERFED
        self.upgrade_definitions['detector'] = {
            UpgradeType.DAMAGE: {
                'name': 'Pulse',
                'description': 'Adds pulse damage',
                'max_level': 3,
                'base_cost': 36,  # 3x increase from 12
                'effects': [
                    {'damage': 1}, {'damage': 1}, {'damage': 2}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Radar',
                'description': 'Increases detection range',
                'max_level': 5,
                'base_cost': 24,  # 3x increase from 8
                'effects': [
                    {'detection_range': 25}, {'detection_range': 35}, {'detection_range': 50}, 
                    {'detection_range': 60}, {'detection_range': 75}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Scanner',
                'description': 'Detects more enemies',
                'max_level': 4,
                'base_cost': 54,  # 3x increase from 18
                'effects': [
                    {'max_detections': 1}, {'max_detections': 1}, {'max_detections': 2}, {'max_detections': 3}  # ~40% reduction
                ]
            }
        }
        
        # Continue with remaining towers
        self._add_remaining_towers()
    
    def _add_remaining_towers(self):
        """Add upgrade definitions for remaining tower types - ALL NERFED"""
        
        # Anti-Air Tower - NERFED
        self.upgrade_definitions['antiair'] = {
            UpgradeType.DAMAGE: {
                'name': 'Missiles',
                'description': 'Increases damage',
                'max_level': 5,
                'base_cost': 54,  # 3x increase from 18
                'effects': [
                    {'damage': 3}, {'damage': 4}, {'damage': 6}, {'damage': 9}, {'damage': 12}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Radar',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 45,  # 3x increase from 15
                'effects': [
                    {'range': 12}, {'range': 17}, {'range': 22}, {'range': 27}, {'range': 35}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Tracking',
                'description': 'Improves targeting',
                'max_level': 4,
                'base_cost': 60,  # 3x increase from 20
                'effects': [
                    {'can_target_invisible': True}, {'projectile_speed': 1}, 
                    {'fire_rate': -4}, {'splash_damage': 5}  # ~50% reduction
                ]
            }
        }
        
        # Continue with final towers
        self._add_final_towers()
    
    def _add_final_towers(self):
        """Add upgrade definitions for final tower types - ALL HEAVILY NERFED"""
        
        # Laser Tower - NERFED
        self.upgrade_definitions['laser'] = {
            UpgradeType.DAMAGE: {
                'name': 'Power',
                'description': 'Increases laser damage',
                'max_level': 5,
                'base_cost': 60,  # 3x increase from 20
                'effects': [
                    {'damage': 2}, {'damage': 3}, {'damage': 4}, {'damage': 6}, {'damage': 8}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Focus',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 45,  # 3x increase from 15
                'effects': [
                    {'range': 10}, {'range': 15}, {'range': 20}, {'range': 25}, {'range': 35}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Beam',
                'description': 'Improves laser properties',
                'max_level': 4,
                'base_cost': 75,  # 3x increase from 25
                'effects': [
                    {'fire_rate': -3}, {'laser_width': 1}, {'charge_time': -5}, {'penetration': 1}  # ~50% reduction
                ]
            }
        }
        
        # Lightning Tower - NERFED
        self.upgrade_definitions['lightning'] = {
            UpgradeType.DAMAGE: {
                'name': 'Voltage',
                'description': 'Increases damage',
                'max_level': 5,
                'base_cost': 54,  # 3x increase from 18
                'effects': [
                    {'damage': 1}, {'damage': 2}, {'damage': 3}, {'damage': 4}, {'damage': 6}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Conductor',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 42,  # 3x increase from 14
                'effects': [
                    {'range': 8}, {'range': 12}, {'range': 16}, {'range': 20}, {'range': 25}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Chain',
                'description': 'Improves chain lightning',
                'max_level': 4,
                'base_cost': 66,  # 3x increase from 22
                'effects': [
                    {'chain_count': 1}, {'chain_range': 10}, {'fire_rate': -3}, {'wet_bonus': 0.2}  # ~50% reduction
                ]
            }
        }
        
        # Flame Tower - NERFED
        self.upgrade_definitions['flame'] = {
            UpgradeType.DAMAGE: {
                'name': 'Heat',
                'description': 'Increases flame damage',
                'max_level': 5,
                'base_cost': 48,  # 3x increase from 16
                'effects': [
                    {'damage': 1}, {'damage': 2}, {'damage': 3}, {'damage': 4}, {'damage': 5}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Reach',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': 36,  # 3x increase from 12
                'effects': [
                    {'range': 6}, {'range': 9}, {'range': 12}, {'range': 15}, {'range': 20}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Burn',
                'description': 'Improves burn effect',
                'max_level': 4,
                'base_cost': 57,  # 3x increase from 19
                'effects': [
                    {'burn_damage': 1}, {'burn_duration': 30}, {'fire_rate': -2}, {'cone_angle': 5}  # ~50% reduction
                ]
            }
        }
        
        # Add generic upgrades for remaining towers
        for tower_type in ['cannon', 'ice', 'poison', 'explosive', 'missile', 'splash']:
            self.upgrade_definitions[tower_type] = self._generate_generic_upgrades(tower_type)
    
    def _generate_generic_upgrades(self, tower_type: str) -> Dict:
        """Generate generic upgrade definitions for towers - HEAVILY NERFED"""
        base_costs = {
            'cannon': 60,    # 3x increase
            'ice': 36,       # 3x increase  
            'poison': 48,    # 3x increase
            'explosive': 90, # 3x increase
            'missile': 75,   # 3x increase
            'splash': 42     # 3x increase
        }
        
        base_cost = base_costs.get(tower_type, 45)
        
        return {
            UpgradeType.DAMAGE: {
                'name': 'Power',
                'description': 'Increases damage',
                'max_level': 5,
                'base_cost': base_cost,
                'effects': [
                    {'damage': 1}, {'damage': 2}, {'damage': 3}, {'damage': 4}, {'damage': 6}  # ~50% reduction
                ]
            },
            UpgradeType.RANGE: {
                'name': 'Range',
                'description': 'Increases range',
                'max_level': 5,
                'base_cost': int(base_cost * 0.8),
                'effects': [
                    {'range': 8}, {'range': 12}, {'range': 16}, {'range': 20}, {'range': 25}  # ~50% reduction
                ]
            },
            UpgradeType.UTILITY: {
                'name': 'Utility',
                'description': 'Improves special abilities',
                'max_level': 4,
                'base_cost': int(base_cost * 1.2),
                'effects': [
                    {'fire_rate': -2}, {'special_effect': 0.1}, {'efficiency': 0.15}, {'bonus_effect': 0.2}  # ~50% reduction
                ]
            }
        }

    def get_tower_currency(self, tower_id: str, tower_type: str) -> int:
        """Get the current currency for a specific tower"""
        key = f"{tower_id}_{tower_type}"
        return self.tower_currencies.get(key, 0)
    
    def add_tower_currency(self, tower_id: str, tower_type: str, amount: int):
        """Add currency for a specific tower"""
        key = f"{tower_id}_{tower_type}"
        current = self.tower_currencies.get(key, 0)
        self.tower_currencies[key] = current + amount
    
    def get_upgrade_cost(self, tower_type: str, upgrade_type: UpgradeType, current_level: int) -> int:
        """Calculate the cost for the next upgrade level"""
        if tower_type not in self.upgrade_definitions:
            return 999999  # Invalid tower type
        
        upgrade_def = self.upgrade_definitions[tower_type][upgrade_type]
        if current_level >= upgrade_def['max_level']:
            return 999999  # Max level reached
        
        base_cost = upgrade_def['base_cost']
        # Exponential cost scaling: cost increases by 50% each level
        return int(base_cost * (1.5 ** current_level))
    
    def can_upgrade(self, tower_id: str, tower_type: str, upgrade_type: UpgradeType, current_level: int) -> bool:
        """Check if a tower can be upgraded"""
        cost = self.get_upgrade_cost(tower_type, upgrade_type, current_level)
        currency = self.get_tower_currency(tower_id, tower_type)
        return currency >= cost and cost < 999999
    
    def upgrade_tower(self, tower_id: str, tower_type: str, upgrade_type: UpgradeType, current_level: int) -> bool:
        """Attempt to upgrade a tower"""
        if self.can_upgrade(tower_id, tower_type, upgrade_type, current_level):
            cost = self.get_upgrade_cost(tower_type, upgrade_type, current_level)
            key = f"{tower_id}_{tower_type}"
            self.tower_currencies[key] = self.tower_currencies.get(key, 0) - cost
            return True
        return False
    
    def get_upgrade_info(self, tower_type: str, upgrade_type: UpgradeType) -> Dict:
        """Get information about an upgrade path"""
        if tower_type in self.upgrade_definitions:
            return self.upgrade_definitions[tower_type][upgrade_type]
        return {}
    
    def apply_upgrades_to_tower(self, tower, tower_id: str):
        """Apply all upgrades to a tower"""
        tower_type = tower.tower_type
        
        # Reset to base stats first
        tower.reset_stats_to_base()
        
        # Apply each upgrade type
        for upgrade_type in UpgradeType:
            level = tower.get_upgrade_level(upgrade_type)
            if level > 0:
                self._apply_upgrade_effects(tower, tower_type, upgrade_type, level)
    
    def _apply_upgrade_effects(self, tower, tower_type: str, upgrade_type: UpgradeType, level: int):
        """Apply specific upgrade effects to a tower"""
        if tower_type not in self.upgrade_definitions:
            return
        
        upgrade_def = self.upgrade_definitions[tower_type][upgrade_type]
        effects = upgrade_def.get('effects', [])
        
        # Apply effects for each level
        for i in range(min(level, len(effects))):
            effect = effects[i]
            for stat, value in effect.items():
                if hasattr(tower, stat):
                    current_value = getattr(tower, stat)
                    if isinstance(value, (int, float)):
                        setattr(tower, stat, current_value + value)
                    else:
                        setattr(tower, stat, value) 