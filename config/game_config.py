"""
Game Configuration Loader

This module loads game configuration from a JSON file and provides 
access to various game settings including waves, maps, towers, and balance.
"""

import json
import os
from typing import Dict, Any, List, Tuple

# Cache for loaded configuration
_config_cache = None

def _load_config() -> Dict[str, Any]:
    """Load configuration from JSON file with caching"""
    global _config_cache
    
    if _config_cache is None:
        config_path = os.path.join(os.path.dirname(__file__), 'tower_defense_game.json')
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Process wave configurations
            if 'wave_config' in config:
                wave_config = config['wave_config']
                
                # Process round progression wave ranges
                if 'round_progression' in wave_config:
                    for section_name, section_data in wave_config['round_progression'].items():
                        if isinstance(section_data, dict) and 'wave_ranges' in section_data:
                            processed_ranges = {}
                            for wave_range, value in section_data['wave_ranges'].items():
                                if '-' in wave_range:
                                    start, end = map(int, wave_range.split('-'))
                                    processed_ranges[(start, end)] = value
                                else:
                                    processed_ranges[int(wave_range)] = value
                            section_data['wave_ranges'] = processed_ranges
                
                # Convert string keys to integers for special rounds and boss waves
                if 'round_progression' in wave_config and 'special_rounds' in wave_config['round_progression']:
                    special_rounds = {}
                    for wave_str, data in wave_config['round_progression']['special_rounds'].items():
                        special_rounds[int(wave_str)] = data
                    wave_config['round_progression']['special_rounds'] = special_rounds
                
                if 'boss_waves' in wave_config:
                    wave_config['boss_waves'] = {
                        int(k): v for k, v in wave_config['boss_waves'].items()
                    }
                
                # Process wave compositions
                if 'wave_compositions' in wave_config:
                    processed_compositions = {}
                    for wave_range, composition in wave_config['wave_compositions'].items():
                        if '-' in wave_range:
                            start, end = map(int, wave_range.split('-'))
                            processed_compositions[(start, end)] = composition
                        else:
                            processed_compositions[int(wave_range)] = composition
                    wave_config['wave_compositions'] = processed_compositions
            
            # Process map configurations
            if 'map_config' in config:
                for map_name, map_data in config['map_config'].items():
                    if 'path' in map_data:
                        # Convert path coordinates to tuples for compatibility
                        map_data['path'] = [tuple(coord) for coord in map_data['path']]
            
            _config_cache = config
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    return _config_cache

def get_wave_config() -> Dict[str, Any]:
    """Get wave configuration settings"""
    config = _load_config()
    return config.get('wave_config', {})

def get_map_config() -> Dict[str, Any]:
    """Get map configuration settings"""
    config = _load_config()
    return config.get('map_config', {})

def get_tower_config() -> Dict[str, Any]:
    """Get tower configuration settings"""
    config = _load_config()
    return config.get('tower_config', {})

def get_balance_config() -> Dict[str, Any]:
    """Get balance configuration settings"""
    config = _load_config()
    return config.get('balance_config', {})

def get_game_config() -> Dict[str, Any]:
    """Get game configuration settings"""
    config = _load_config()
    return config.get('game_config', {})

def get_available_maps() -> List[str]:
    """Get list of available map names"""
    map_config = get_map_config()
    return list(map_config.keys())

# For backward compatibility and easy access
def reload_config():
    """Force reload of configuration from file"""
    global _config_cache
    _config_cache = None
    _load_config() 