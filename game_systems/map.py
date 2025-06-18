import pygame
import math
from typing import List, Tuple, Optional
from .terrain_types import *
from maps.default_map import get_map_data

class Map:
    """Handles grid-based map layout, terrain types, and tower placement validation"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load map data
        map_data = get_map_data()
        self.grid_layout = map_data['layout']
        self.grid_width = map_data['width'] 
        self.grid_height = map_data['height']
        self.cell_size = map_data['cell_size']
        self.path_waypoints = map_data['path_waypoints']
        
        # Convert grid waypoints to pixel coordinates
        self.path = self._convert_waypoints_to_pixels()
        
        # Colors for placement preview
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        
        # Tower placement constraints
        self.min_distance_between_towers = 35  # Reduced since we use grid
    
    def _convert_waypoints_to_pixels(self) -> List[Tuple[int, int]]:
        """Convert grid-based waypoints to pixel coordinates"""
        pixel_path = []
        for grid_x, grid_y in self.path_waypoints:
            pixel_x = grid_x * self.cell_size + self.cell_size // 2
            pixel_y = grid_y * self.cell_size + self.cell_size // 2
            pixel_path.append((pixel_x, pixel_y))
        return pixel_path
    
    def get_path(self) -> List[Tuple[int, int]]:
        """Get the enemy path in pixel coordinates"""
        return self.path
    
    def pixel_to_grid(self, pixel_x: int, pixel_y: int) -> Tuple[int, int]:
        """Convert pixel coordinates to grid coordinates"""
        grid_x = pixel_x // self.cell_size
        grid_y = pixel_y // self.cell_size
        return (grid_x, grid_y)
    
    def grid_to_pixel(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """Convert grid coordinates to pixel coordinates (center of cell)"""
        pixel_x = grid_x * self.cell_size + self.cell_size // 2
        pixel_y = grid_y * self.cell_size + self.cell_size // 2
        return (pixel_x, pixel_y)
    
    def get_terrain_at_pixel(self, pixel_x: int, pixel_y: int) -> int:
        """Get terrain type at pixel coordinates"""
        grid_x, grid_y = self.pixel_to_grid(pixel_x, pixel_y)
        return self.get_terrain_at_grid(grid_x, grid_y)
    
    def get_terrain_at_grid(self, grid_x: int, grid_y: int) -> int:
        """Get terrain type at grid coordinates"""
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            return self.grid_layout[grid_y][grid_x]
        return GRASS  # Default to grass if out of bounds
    
    def is_valid_tower_position(self, pixel_x: int, pixel_y: int, existing_towers: List, 
                              tower_type: str = None) -> bool:
        """Check if a position is valid for tower placement"""
        grid_x, grid_y = self.pixel_to_grid(pixel_x, pixel_y)
        
        # Check if within map bounds
        if not (0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height):
            return False
        
        terrain_type = self.get_terrain_at_grid(grid_x, grid_y)
        
        # Check if terrain allows tower placement
        if not is_tower_placeable(terrain_type):
            return False
        
        # Check if specific tower type can be placed on this terrain
        if tower_type and not can_place_tower_type(terrain_type, tower_type):
            return False
        
        # Check if too close to other towers
        for tower in existing_towers:
            distance = math.sqrt((pixel_x - tower.x)**2 + (pixel_y - tower.y)**2)
            if distance < self.min_distance_between_towers:
                return False
        
        return True
    
    def get_placement_info(self, pixel_x: int, pixel_y: int, tower_type: str = None) -> dict:
        """Get detailed placement information for UI feedback"""
        grid_x, grid_y = self.pixel_to_grid(pixel_x, pixel_y)
        terrain_type = self.get_terrain_at_grid(grid_x, grid_y)
        
        info = {
            'terrain_name': get_terrain_name(terrain_type),
            'can_place': is_tower_placeable(terrain_type),
            'tower_allowed': True if not tower_type else can_place_tower_type(terrain_type, tower_type),
            'special_rules': get_terrain_property(terrain_type, 'special_rules')
        }
        
        return info
    
    def apply_terrain_effects_to_tower(self, tower, grid_x: int, grid_y: int):
        """Apply terrain-specific effects to a tower"""
        terrain_type = self.get_terrain_at_grid(grid_x, grid_y)
        special_rules = get_terrain_property(terrain_type, 'special_rules')
        
        if special_rules == 'reduced_range':
            # Forest reduces tower range by 20%
            tower.range = int(tower.range * 0.8)
        elif special_rules == 'water_only':
            # Water terrain might give special bonuses to freezer towers
            if hasattr(tower, 'freeze_duration'):
                tower.freeze_duration = int(tower.freeze_duration * 1.5)
    
    def draw_terrain(self, screen: pygame.Surface):
        """Draw the terrain grid"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                terrain_type = self.grid_layout[y][x]
                color = get_terrain_color(terrain_type)
                
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, color, rect)
                
                # Draw subtle grid lines
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)
    
    def draw_path_overlay(self, screen: pygame.Surface):
        """Draw path overlay on top of terrain"""
        if len(self.path) > 1:
            # Draw thick path line
            pygame.draw.lines(screen, (139, 69, 19), False, self.path, 8)
            # Draw path border
            pygame.draw.lines(screen, (100, 50, 15), False, self.path, 12)
    
    def draw_tower_placement_preview(self, screen: pygame.Surface, mouse_pos: Tuple[int, int], 
                                   existing_towers: List, tower_type: str = None):
        """Draw tower placement preview with terrain-aware feedback"""
        x, y = mouse_pos
        grid_x, grid_y = self.pixel_to_grid(x, y)
        
        # Snap to grid center
        center_x, center_y = self.grid_to_pixel(grid_x, grid_y)
        
        # Get placement info
        placement_info = self.get_placement_info(x, y, tower_type)
        valid_position = self.is_valid_tower_position(x, y, existing_towers, tower_type)
        
        # Choose color based on validity
        if valid_position:
            color = self.GREEN
        elif not placement_info['can_place']:
            color = self.RED
        elif not placement_info['tower_allowed']:
            color = self.YELLOW  # Tower type not allowed on this terrain
        else:
            color = self.RED
        
        # Draw placement preview
        pygame.draw.circle(screen, color, (center_x, center_y), 18, 3)
        
        # Draw terrain info tooltip
        if not valid_position:
            self._draw_terrain_tooltip(screen, mouse_pos, placement_info)
    
    def _draw_terrain_tooltip(self, screen: pygame.Surface, mouse_pos: Tuple[int, int], 
                            placement_info: dict):
        """Draw tooltip showing why tower can't be placed"""
        font = pygame.font.Font(None, 24)
        x, y = mouse_pos
        
        # Create tooltip text
        if not placement_info['can_place']:
            text = f"{placement_info['terrain_name']} - Cannot place towers"
        elif not placement_info['tower_allowed']:
            text = f"{placement_info['terrain_name']} - Tower type not allowed"
        else:
            text = f"{placement_info['terrain_name']} - Too close to other towers"
        
        # Render text
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        
        # Position tooltip
        tooltip_x = min(x + 20, self.screen_width - text_rect.width - 10)
        tooltip_y = max(y - 30, 10)
        
        # Draw background
        bg_rect = pygame.Rect(tooltip_x - 5, tooltip_y - 5, 
                             text_rect.width + 10, text_rect.height + 10)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)
        
        # Draw text
        screen.blit(text_surface, (tooltip_x, tooltip_y))
    
    def draw(self, screen: pygame.Surface, placing_tower: bool = False, 
             mouse_pos: Tuple[int, int] = None, existing_towers: List = None,
             tower_type: str = None):
        """Draw the complete map"""
        # Draw terrain
        self.draw_terrain(screen)
        
        # Draw path overlay
        self.draw_path_overlay(screen)
        
        # Draw tower placement preview if placing tower
        if placing_tower and mouse_pos and existing_towers is not None:
            self.draw_tower_placement_preview(screen, mouse_pos, existing_towers, tower_type) 