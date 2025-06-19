import pygame
import math
from typing import List, Tuple, Optional
from config.game_config import get_map_config
from .terrain_types import *
from .tower_sizes import *

class Map:
    """Handles grid-based map layout, terrain types, and tower placement validation"""
    
    def __init__(self, screen_width: int, screen_height: int, map_name: str = 'default_map'):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_name = map_name
        
        # Load map data from centralized config
        all_maps = get_map_config()
        if map_name not in all_maps:
            map_name = 'default_map'  # Fallback to default
        
        map_data = all_maps[map_name]
        self.grid_layout = map_data['terrain']
        self.grid_width = map_data['width'] 
        self.grid_height = map_data['height']
        self.path_waypoints = map_data['path']
        
        # Calculate dynamic map positioning and cell size to fill available space
        self.top_ui_height = 140  # Space for top UI
        self.bottom_ui_height = 120  # Space for bottom UI
        
        # Available space for map
        available_width = screen_width
        available_height = screen_height - self.top_ui_height - self.bottom_ui_height
        
        # Calculate cell size to fit the grid perfectly in available space
        cell_width = available_width // self.grid_width
        cell_height = available_height // self.grid_height
        self.cell_size = min(cell_width, cell_height)  # Use smaller to maintain aspect ratio
        
        # Calculate actual map dimensions and center it
        actual_map_width = self.grid_width * self.cell_size
        actual_map_height = self.grid_height * self.cell_size
        
        self.map_offset_x = (available_width - actual_map_width) // 2
        self.map_offset_y = self.top_ui_height + (available_height - actual_map_height) // 2
        
        # Convert grid waypoints to pixel coordinates
        self.path = self._convert_waypoints_to_pixels()
        
        # Colors for placement preview
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        
        # Tower placement constraints (dynamic based on cell size)
        self.min_distance_between_towers = max(self.cell_size * 0.8, 25)  # Scale with cell size
    
    def _convert_waypoints_to_pixels(self) -> List[Tuple[int, int]]:
        """Convert grid-based waypoints to pixel coordinates"""
        pixel_path = []
        for grid_x, grid_y in self.path_waypoints:
            pixel_x = self.map_offset_x + grid_x * self.cell_size + self.cell_size // 2
            pixel_y = self.map_offset_y + grid_y * self.cell_size + self.cell_size // 2
            pixel_path.append((pixel_x, pixel_y))
        return pixel_path
    
    def get_path(self) -> List[Tuple[int, int]]:
        """Get the enemy path in pixel coordinates"""
        return self.path
    
    def pixel_to_grid(self, pixel_x: int, pixel_y: int) -> Tuple[int, int]:
        """Convert pixel coordinates to grid coordinates"""
        grid_x = (pixel_x - self.map_offset_x) // self.cell_size
        grid_y = (pixel_y - self.map_offset_y) // self.cell_size
        return (grid_x, grid_y)
    
    def grid_to_pixel(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """Convert grid coordinates to pixel coordinates (center of cell)"""
        pixel_x = self.map_offset_x + grid_x * self.cell_size + self.cell_size // 2
        pixel_y = self.map_offset_y + grid_y * self.cell_size + self.cell_size // 2
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
        
        # Check if tower can be placed at this position (multi-block support)
        if tower_type and not can_place_tower_at_position(grid_x, grid_y, tower_type, 
                                                         self.grid_width, self.grid_height, existing_towers):
            return False
        
        # Check if within map bounds (for single cell, multi-cell handled above)
        if not tower_type and not (0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height):
            return False
        
        # Get all cells that would be occupied by this tower
        if tower_type:
            occupied_cells = get_tower_occupied_cells(grid_x, grid_y, tower_type)
        else:
            occupied_cells = [(grid_x, grid_y)]
        
        # Check terrain for all occupied cells
        for cell_x, cell_y in occupied_cells:
            if not (0 <= cell_x < self.grid_width and 0 <= cell_y < self.grid_height):
                return False
                
            terrain_type = self.get_terrain_at_grid(cell_x, cell_y)
            
            # Check if terrain allows tower placement
            if not is_tower_placeable(terrain_type):
                return False
            
            # Check if specific tower type can be placed on this terrain
            if tower_type and not can_place_tower_type(terrain_type, tower_type):
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
                    self.map_offset_x + x * self.cell_size,
                    self.map_offset_y + y * self.cell_size,
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
        """Draw tower placement preview with terrain-aware feedback and multi-block support"""
        x, y = mouse_pos
        grid_x, grid_y = self.pixel_to_grid(x, y)
        
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
        
        # Draw multi-block placement preview
        if tower_type:
            occupied_cells = get_tower_occupied_cells(grid_x, grid_y, tower_type)
            
            # Draw all occupied cells
            for cell_x, cell_y in occupied_cells:
                if 0 <= cell_x < self.grid_width and 0 <= cell_y < self.grid_height:
                    cell_rect = pygame.Rect(
                        self.map_offset_x + cell_x * self.cell_size,
                        self.map_offset_y + cell_y * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(screen, color, cell_rect, 3)
            
            # Draw tower preview circle at center of multi-block area
            width, height = get_tower_size(tower_type)
            center_x = self.map_offset_x + (grid_x + width/2) * self.cell_size
            center_y = self.map_offset_y + (grid_y + height/2) * self.cell_size
            tower_radius = get_tower_visual_size(tower_type, self.cell_size)
            pygame.draw.circle(screen, color, (int(center_x), int(center_y)), tower_radius, 3)
        else:
            # Single cell preview
            center_x, center_y = self.grid_to_pixel(grid_x, grid_y)
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