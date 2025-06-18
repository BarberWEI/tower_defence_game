import pygame
import math
from typing import List, Tuple

class Map:
    """Handles map layout, path management, and tower placement validation"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Define the path that enemies will follow
        self.path = [
            (0, 400), (200, 400), (200, 200), (400, 200),
            (400, 600), (600, 600), (600, 100), (800, 100),
            (800, 500), (1000, 500), (1000, 300), (1200, 300)
        ]
        
        # Colors
        self.BROWN = (139, 69, 19)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        # Tower placement constraints
        self.min_distance_from_path = 50
        self.min_distance_between_towers = 40
    
    def get_path(self) -> List[Tuple[int, int]]:
        """Get the enemy path"""
        return self.path
    
    def is_valid_tower_position(self, x: int, y: int, existing_towers: List) -> bool:
        """Check if a position is valid for tower placement"""
        # Check if too close to path
        for path_x, path_y in self.path:
            if math.sqrt((x - path_x)**2 + (y - path_y)**2) < self.min_distance_from_path:
                return False
        
        # Check if too close to other towers
        for tower in existing_towers:
            if math.sqrt((x - tower.x)**2 + (y - tower.y)**2) < self.min_distance_between_towers:
                return False
        
        # Check if within screen bounds
        if x < 0 or x >= self.screen_width or y < 0 or y >= self.screen_height:
            return False
        
        return True
    
    def draw_background(self, screen: pygame.Surface):
        """Draw the map background"""
        screen.fill(self.WHITE)
    
    def draw_path(self, screen: pygame.Surface):
        """Draw the enemy path"""
        if len(self.path) > 1:
            pygame.draw.lines(screen, self.BROWN, False, self.path, 20)
    
    def draw_tower_placement_preview(self, screen: pygame.Surface, mouse_pos: Tuple[int, int], 
                                   existing_towers: List):
        """Draw a preview circle for tower placement"""
        x, y = mouse_pos
        color = self.GREEN if self.is_valid_tower_position(x, y, existing_towers) else self.RED
        pygame.draw.circle(screen, color, mouse_pos, 15, 2)
    
    def draw(self, screen: pygame.Surface, placing_tower: bool = False, 
             mouse_pos: Tuple[int, int] = None, existing_towers: List = None):
        """Draw the complete map"""
        self.draw_background(screen)
        self.draw_path(screen)
        
        # Draw tower placement preview if placing tower
        if placing_tower and mouse_pos and existing_towers is not None:
            self.draw_tower_placement_preview(screen, mouse_pos, existing_towers) 