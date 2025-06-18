"""
Terrain Types and Properties for the Tower Defense Game
"""

# Terrain type constants
GRASS = 0      # Default placeable terrain
PATH = 1       # Enemy path - no towers allowed
ROCK = 2       # Unplaceable terrain (mountains, rocks)
WATER = 3      # Special terrain - only certain towers allowed
FOREST = 4     # Reduced tower range terrain
SAND = 5       # Faster enemy movement

# Terrain properties
TERRAIN_PROPERTIES = {
    GRASS: {
        'name': 'Grass',
        'color': (34, 139, 34),  # Forest green
        'tower_placeable': True,
        'enemy_walkable': False,
        'special_rules': None,
        'allowed_towers': 'all'
    },
    PATH: {
        'name': 'Path',
        'color': (139, 69, 19),  # Brown
        'tower_placeable': False,
        'enemy_walkable': True,
        'special_rules': None,
        'allowed_towers': None
    },
    ROCK: {
        'name': 'Rock',
        'color': (105, 105, 105),  # Dim gray
        'tower_placeable': False,
        'enemy_walkable': False,
        'special_rules': None,
        'allowed_towers': None
    },
    WATER: {
        'name': 'Water',
        'color': (30, 144, 255),  # Dodger blue
        'tower_placeable': True,
        'enemy_walkable': False,
        'special_rules': 'water_only',
        'allowed_towers': ['freezer', 'splash']  # Only freezer and splash towers can be placed on water
    },
    FOREST: {
        'name': 'Forest',
        'color': (0, 100, 0),  # Dark green
        'tower_placeable': True,
        'enemy_walkable': False,
        'special_rules': 'reduced_range',
        'allowed_towers': 'all'
    },
    SAND: {
        'name': 'Sand',
        'color': (238, 203, 173),  # Peach puff
        'tower_placeable': True,
        'enemy_walkable': False,
        'special_rules': None,
        'allowed_towers': 'all'
    }
}

def get_terrain_property(terrain_type: int, property_name: str):
    """Get a specific property of a terrain type"""
    return TERRAIN_PROPERTIES.get(terrain_type, {}).get(property_name)

def is_tower_placeable(terrain_type: int) -> bool:
    """Check if towers can be placed on this terrain type"""
    return get_terrain_property(terrain_type, 'tower_placeable') or False

def is_enemy_walkable(terrain_type: int) -> bool:
    """Check if enemies can walk on this terrain type"""
    return get_terrain_property(terrain_type, 'enemy_walkable') or False

def requires_water_terrain(tower_type: str) -> bool:
    """Check if a tower type requires water terrain"""
    water_only_towers = ['splash']
    return tower_type in water_only_towers

def can_place_tower_type(terrain_type: int, tower_type: str) -> bool:
    """Check if a specific tower type can be placed on this terrain"""
    if not is_tower_placeable(terrain_type):
        return False
    
    # Check if tower requires water terrain
    if requires_water_terrain(tower_type):
        return terrain_type == WATER
    
    allowed_towers = get_terrain_property(terrain_type, 'allowed_towers')
    if allowed_towers == 'all':
        return True
    elif isinstance(allowed_towers, list):
        return tower_type in allowed_towers
    else:
        return False

def get_terrain_color(terrain_type: int) -> tuple:
    """Get the color for rendering this terrain type"""
    return get_terrain_property(terrain_type, 'color') or (255, 255, 255)

def get_terrain_name(terrain_type: int) -> str:
    """Get the name of a terrain type"""
    return get_terrain_property(terrain_type, 'name') or 'Unknown' 