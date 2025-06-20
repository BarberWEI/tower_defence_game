import pygame
import math
from typing import Dict, List, Tuple, Optional
from .tower_data import TowerDataManager
from .ui_renderer import UIRenderer

class UIManager:
    """Manages UI state and coordinates with renderer and data manager"""
    
    def __init__(self, screen_width: int, screen_height: int, tower_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize sub-systems
        self.tower_data_manager = TowerDataManager(tower_manager)
        self.renderer = UIRenderer(screen_width, screen_height)
        
        # UI State
        self.selected_tower_index = None
        self.hovered_tower_index = None
        self.selected_placed_tower = None
        self.mouse_pos = (0, 0)
        
        # Scrolling state
        self.scroll_offset = 0
        self.max_scroll = self._calculate_max_scroll()
    
    def _calculate_max_scroll(self) -> int:
        """Calculate maximum scroll offset"""
        total_width = self.tower_data_manager.get_tower_count() * (
            self.renderer.tower_slot_width + self.renderer.tower_slot_margin
        )
        visible_width = self.screen_width - 40  # margins
        return max(0, total_width - visible_width)
    
    def update_mouse_pos(self, pos: Tuple[int, int]):
        """Update mouse position for hover effects"""
        self.mouse_pos = pos
        self._update_hover_state()
    
    def _update_hover_state(self):
        """Update which tower slot is being hovered"""
        mouse_x, mouse_y = self.mouse_pos
        
        # Check if mouse is in tower bar area
        if self.renderer.bottom_bar_y <= mouse_y <= self.screen_height:
            # Calculate which tower slot is hovered
            relative_x = mouse_x - 20 + self.scroll_offset  # 20 is left margin
            slot_index = int(relative_x // (self.renderer.tower_slot_width + self.renderer.tower_slot_margin))
            
            if 0 <= slot_index < self.tower_data_manager.get_tower_count():
                # Check if mouse is actually over the slot (not in margin)
                slot_x = slot_index * (self.renderer.tower_slot_width + self.renderer.tower_slot_margin) - self.scroll_offset + 20
                if slot_x <= mouse_x <= slot_x + self.renderer.tower_slot_width:
                    self.hovered_tower_index = slot_index
                else:
                    self.hovered_tower_index = None
            else:
                self.hovered_tower_index = None
        else:
            self.hovered_tower_index = None
    
    def handle_tower_bar_click(self, pos: Tuple[int, int]) -> Optional[int]:
        """Handle clicks on the tower bar, return selected tower index"""
        mouse_x, mouse_y = pos
        
        if self.renderer.bottom_bar_y <= mouse_y <= self.screen_height:
            relative_x = mouse_x - 20 + self.scroll_offset
            slot_index = int(relative_x // (self.renderer.tower_slot_width + self.renderer.tower_slot_margin))
            
            if 0 <= slot_index < self.tower_data_manager.get_tower_count():
                slot_x = slot_index * (self.renderer.tower_slot_width + self.renderer.tower_slot_margin) - self.scroll_offset + 20
                if slot_x <= mouse_x <= slot_x + self.renderer.tower_slot_width:
                    self.selected_tower_index = slot_index
                    return slot_index
        
        return None
    
    def handle_scroll(self, direction: int):
        """Handle scrolling in the tower bar"""
        # Only scroll if mouse is over the tower bar
        mouse_x, mouse_y = self.mouse_pos
        if not (self.renderer.bottom_bar_y <= mouse_y <= self.screen_height):
            return
            
        scroll_speed = 50
        
        if direction > 0:  # Scroll right
            self.scroll_offset = min(self.max_scroll, self.scroll_offset + scroll_speed)
        elif direction < 0:  # Scroll left  
            self.scroll_offset = max(0, self.scroll_offset - scroll_speed)
    
    def handle_tower_click(self, pos: Tuple[int, int], towers: List) -> bool:
        """Handle clicks on placed towers to show range"""
        mouse_x, mouse_y = pos
        
        # Don't handle if clicking in UI areas
        if mouse_y >= self.renderer.bottom_bar_y or mouse_y <= 130:
            return False
        
        # Check if click is within screen bounds
        if mouse_x < 0 or mouse_x > self.screen_width or mouse_y < 140 or mouse_y >= self.renderer.bottom_bar_y:
            return False
        
        for tower in towers:
            # Check if click is within tower's area
            distance = math.sqrt((mouse_x - tower.x)**2 + (mouse_y - tower.y)**2)
            if distance <= tower.size + 5:  # Small buffer for easier clicking
                self.selected_placed_tower = tower
                return True
        
        # Click elsewhere deselects tower
        self.selected_placed_tower = None
        return False
    
    def handle_speed_button_click(self, pos: Tuple[int, int]) -> bool:
        """Handle clicks on the speed button, return True if clicked"""
        return self.renderer.is_speed_button_clicked(pos)
    
    def get_selected_tower_type(self) -> Optional[str]:
        """Get the currently selected tower type"""
        if self.selected_tower_index is not None:
            return self.tower_data_manager.get_tower_type_by_index(self.selected_tower_index)
        return None
    
    def clear_tower_selection(self):
        """Clear tower selection"""
        self.selected_tower_index = None
    
    def draw_complete_ui(self, screen: pygame.Surface, game_state: Dict):
        """Draw the complete user interface"""
        # Main game stats (top area) with speed button
        self.renderer.draw_game_stats(screen, game_state['money'], game_state['lives'], 
                                    game_state['wave_info'], game_state.get('game_speed', 1))
        
        # Performance info (top right)
        if 'performance' in game_state:
            self.renderer.draw_performance_info(screen, game_state['performance'])
        
        # Bottom tower bar
        tower_data = self.tower_data_manager.get_all_tower_data()
        self.renderer.draw_tower_bar(screen, tower_data, game_state['money'], 
                                   self.scroll_offset, self.max_scroll, 
                                   self.selected_tower_index, self.hovered_tower_index)
        
        # Tower tooltip
        if self.hovered_tower_index is not None:
            tower_data = self.tower_data_manager.get_tower_data(
                self.tower_data_manager.get_tower_type_by_index(self.hovered_tower_index)
            )
            if tower_data:
                self.renderer.draw_tower_tooltip(screen, tower_data, self.mouse_pos)
        
        # Overlays
        if game_state.get('paused'):
            self.renderer.draw_pause_overlay(screen)
        elif game_state.get('game_over'):
            self.renderer.draw_game_over_overlay(screen, game_state['wave_info']['wave_number'])
