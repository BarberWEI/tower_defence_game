# Tower size configuration
# Defines how many grid blocks each tower type occupies

# Tower size format: (width_in_blocks, height_in_blocks)
TOWER_SIZES = {
    'basic': (1, 1),
    'sniper': (1, 1),
    'freezer': (1, 1),
    'detector': (2, 2),      # Larger detection tower
    'antiair': (1, 1),
    'poison': (1, 1),
    'laser': (1, 1),
    'cannon': (2, 2),        # Large cannon tower
    'lightning': (1, 1),
    'flame': (1, 1),
    'ice': (1, 1),
    'explosive': (3, 3),     # Massive explosive tower
    'missile': (2, 2),       # 2x2 size for missile tower
    'splash': (1, 1)         # Regular size splash tower
}

def get_tower_size(tower_type: str) -> tuple:
    """Get the size of a tower type in grid blocks"""
    return TOWER_SIZES.get(tower_type, (1, 1))

def get_tower_visual_size(tower_type: str, cell_size: int) -> int:
    """Get the visual size (radius) of a tower based on its grid size"""
    width, height = get_tower_size(tower_type)
    # Calculate radius based on the largest dimension
    max_dimension = max(width, height)
    
    # Base size calculation
    if max_dimension == 1:
        return int(cell_size * 0.3)  # Small towers
    elif max_dimension == 2:
        return int(cell_size * 0.5)  # Medium towers
    else:
        return int(cell_size * 0.7)  # Large towers

def get_tower_occupied_cells(grid_x: int, grid_y: int, tower_type: str) -> list:
    """Get all grid cells occupied by a tower"""
    width, height = get_tower_size(tower_type)
    occupied_cells = []
    
    for dx in range(width):
        for dy in range(height):
            occupied_cells.append((grid_x + dx, grid_y + dy))
    
    return occupied_cells

def can_place_tower_at_position(grid_x: int, grid_y: int, tower_type: str, 
                               grid_width: int, grid_height: int, existing_towers: list) -> bool:
    """Check if a multi-block tower can be placed at the given position"""
    width, height = get_tower_size(tower_type)
    
    # Check if tower fits within map bounds
    if grid_x + width > grid_width or grid_y + height > grid_height:
        return False
    
    # Get all cells this tower would occupy
    occupied_cells = get_tower_occupied_cells(grid_x, grid_y, tower_type)
    
    # Check if any existing tower occupies these cells
    for tower in existing_towers:
        tower_type_existing = getattr(tower, 'tower_type', 'basic')
        tower_grid_x, tower_grid_y = getattr(tower, 'grid_x', 0), getattr(tower, 'grid_y', 0)
        existing_occupied = get_tower_occupied_cells(tower_grid_x, tower_grid_y, tower_type_existing)
        
        # Check for overlap
        for cell in occupied_cells:
            if cell in existing_occupied:
                return False
    
    return True 