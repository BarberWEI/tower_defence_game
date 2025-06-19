"""
Upgrade UI - Handles the display and interaction for tower upgrades
"""
import pygame
import math
from typing import Dict, List, Tuple, Optional
from .tower_upgrade_system import UpgradeType, TowerUpgradeSystem

class UpgradeUI:
    """Handles upgrade panel display and interactions"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_GRAY = (64, 64, 64)
        self.GOLD = (255, 215, 0)
        
        # UI Colors
        self.UI_BG = (40, 40, 40)
        self.UI_BORDER = (80, 80, 80)
        self.UI_HOVER = (60, 60, 60)
        self.UI_BUTTON = (100, 100, 100)
        self.UI_BUTTON_HOVER = (120, 120, 120)
        self.UI_BUTTON_DISABLED = (60, 60, 60)
        
        # Fonts
        self.large_font = pygame.font.Font(None, 28)
        self.medium_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.tiny_font = pygame.font.Font(None, 16)
        
        # Panel dimensions
        self.panel_width = 300
        self.panel_height = 450  # Increased for remove button
        self.upgrade_slot_height = 80
        
        # State
        self.selected_tower = None
        self.mouse_pos = (0, 0)
        self.hovered_upgrade = None
        self.hovered_remove_button = False
    
    def update_mouse_pos(self, pos: Tuple[int, int]):
        """Update mouse position for hover effects"""
        self.mouse_pos = pos
        self._update_hover_state()
    
    def _update_hover_state(self):
        """Update which upgrade button is being hovered"""
        if not self.selected_tower:
            self.hovered_upgrade = None
            self.hovered_remove_button = False
            return
        
        panel_x, panel_y = self._get_panel_position()
        mouse_x, mouse_y = self.mouse_pos
        
        # Check if mouse is over the panel
        if not (panel_x <= mouse_x <= panel_x + self.panel_width and 
                panel_y <= mouse_y <= panel_y + self.panel_height):
            self.hovered_upgrade = None
            self.hovered_remove_button = False
            return
        
        # Check remove button first (at bottom of panel)
        remove_button_y = panel_y + self.panel_height - 50
        if (panel_x + 10 <= mouse_x <= panel_x + self.panel_width - 10 and
            remove_button_y <= mouse_y <= remove_button_y + 35):
            self.hovered_remove_button = True
            self.hovered_upgrade = None
            return
        
        self.hovered_remove_button = False
        
        # Check which upgrade button is hovered
        upgrade_y_start = panel_y + 80  # After header
        for i, upgrade_type in enumerate(UpgradeType):
            upgrade_y = upgrade_y_start + i * self.upgrade_slot_height
            if upgrade_y <= mouse_y <= upgrade_y + self.upgrade_slot_height:
                self.hovered_upgrade = upgrade_type
                return
        
        self.hovered_upgrade = None
    
    def _get_panel_position(self) -> Tuple[int, int]:
        """Get the position for the upgrade panel"""
        if not self.selected_tower:
            return (0, 0)
        
        # Position panel to the right of the tower, but keep on screen
        panel_x = min(self.selected_tower.x + 50, self.screen_width - self.panel_width - 10)
        panel_y = max(10, min(self.selected_tower.y - self.panel_height // 2, 
                             self.screen_height - self.panel_height - 140))  # 140 for bottom UI
        
        return (panel_x, panel_y)
    
    def handle_click(self, pos: Tuple[int, int], upgrade_system: TowerUpgradeSystem) -> dict:
        """Handle clicks on upgrade buttons and remove button"""
        if not self.selected_tower:
            return {'action': 'none'}
        
        # Handle remove button click
        if self.hovered_remove_button:
            return {'action': 'remove_tower', 'tower': self.selected_tower}
        
        # Handle upgrade button click
        if not self.hovered_upgrade:
            return {'action': 'none'}
        
        tower_type = self.selected_tower.tower_type
        tower_id = self.selected_tower.tower_id
        upgrade_type = self.hovered_upgrade
        current_level = self.selected_tower.get_upgrade_level(upgrade_type)
        
        # Check if upgrade is possible
        if upgrade_system.can_upgrade(tower_id, tower_type, upgrade_type, current_level):
            # Perform upgrade
            if upgrade_system.upgrade_tower(tower_id, tower_type, upgrade_type, current_level):
                # Update tower upgrade level
                self.selected_tower.set_upgrade_level(upgrade_type, current_level + 1)
                
                # Reset tower stats and reapply all upgrades
                self.selected_tower.reset_stats_to_base()
                upgrade_system.apply_upgrades_to_tower(self.selected_tower, tower_id)
                
                return {'action': 'upgrade', 'success': True}
        
        return {'action': 'upgrade', 'success': False}
    
    def set_selected_tower(self, tower):
        """Set the currently selected tower for upgrades"""
        self.selected_tower = tower
    
    def clear_selection(self):
        """Clear the selected tower"""
        self.selected_tower = None
        self.hovered_upgrade = None
    
    def draw_upgrade_panel(self, screen: pygame.Surface, upgrade_system: TowerUpgradeSystem):
        """Draw the upgrade panel for the selected tower"""
        if not self.selected_tower:
            return
        
        panel_x, panel_y = self._get_panel_position()
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, self.panel_width, self.panel_height)
        pygame.draw.rect(screen, self.UI_BG, panel_rect)
        pygame.draw.rect(screen, self.UI_BORDER, panel_rect, 2)
        
        # Draw header
        self._draw_panel_header(screen, panel_x, panel_y, upgrade_system)
        
        # Draw upgrade slots
        upgrade_y_start = panel_y + 80
        for i, upgrade_type in enumerate(UpgradeType):
            upgrade_y = upgrade_y_start + i * self.upgrade_slot_height
            self._draw_upgrade_slot(screen, panel_x, upgrade_y, upgrade_type, upgrade_system)
        
        # Draw remove tower button
        self._draw_remove_button(screen, panel_x, panel_y)
    
    def _draw_panel_header(self, screen: pygame.Surface, panel_x: int, panel_y: int, 
                          upgrade_system: TowerUpgradeSystem):
        """Draw the upgrade panel header"""
        # Tower name
        tower_name = self.selected_tower.tower_type.title() + " Tower"
        name_text = self.large_font.render(tower_name, True, self.WHITE)
        screen.blit(name_text, (panel_x + 10, panel_y + 10))
        
        # Tower currency
        currency = upgrade_system.get_tower_currency(self.selected_tower.tower_id, 
                                                   self.selected_tower.tower_type)
        currency_text = self.medium_font.render(f"Currency: {currency}", True, self.GOLD)
        screen.blit(currency_text, (panel_x + 10, panel_y + 35))
        
        # Total damage dealt
        damage_text = self.small_font.render(f"Damage Dealt: {self.selected_tower.total_damage_dealt}", 
                                           True, self.LIGHT_GRAY)
        screen.blit(damage_text, (panel_x + 10, panel_y + 55))
    
    def _draw_upgrade_slot(self, screen: pygame.Surface, panel_x: int, slot_y: int, 
                          upgrade_type: UpgradeType, upgrade_system: TowerUpgradeSystem):
        """Draw a single upgrade slot"""
        tower_type = self.selected_tower.tower_type
        tower_id = self.selected_tower.tower_id
        current_level = self.selected_tower.get_upgrade_level(upgrade_type)
        
        # Get upgrade info
        upgrade_info = upgrade_system.get_upgrade_info(tower_type, upgrade_type)
        if not upgrade_info:
            return
        
        max_level = upgrade_info['max_level']
        upgrade_name = upgrade_info['name']
        upgrade_desc = upgrade_info['description']
        
        # Calculate cost and affordability
        cost = upgrade_system.get_upgrade_cost(tower_type, upgrade_type, current_level)
        currency = upgrade_system.get_tower_currency(tower_id, tower_type)
        can_afford = currency >= cost if cost > 0 else False
        is_max_level = current_level >= max_level
        
        # Determine button state
        is_hovered = (upgrade_type == self.hovered_upgrade)
        
        # Draw slot background
        slot_rect = pygame.Rect(panel_x + 5, slot_y, self.panel_width - 10, self.upgrade_slot_height - 5)
        
        if is_max_level:
            bg_color = self.UI_BUTTON_DISABLED
        elif is_hovered and can_afford:
            bg_color = self.UI_BUTTON_HOVER
        elif can_afford:
            bg_color = self.UI_BUTTON
        else:
            bg_color = self.UI_BUTTON_DISABLED
        
        pygame.draw.rect(screen, bg_color, slot_rect)
        pygame.draw.rect(screen, self.UI_BORDER, slot_rect, 1)
        
        # Draw upgrade icon/type indicator
        icon_color = self._get_upgrade_type_color(upgrade_type)
        icon_rect = pygame.Rect(panel_x + 15, slot_y + 10, 20, 20)
        pygame.draw.rect(screen, icon_color, icon_rect)
        pygame.draw.rect(screen, self.WHITE, icon_rect, 1)
        
        # Draw upgrade name and level
        name_level_text = f"{upgrade_name} ({current_level}/{max_level})"
        name_text = self.medium_font.render(name_level_text, True, self.WHITE)
        screen.blit(name_text, (panel_x + 45, slot_y + 8))
        
        # Draw description
        desc_text = self.small_font.render(upgrade_desc, True, self.LIGHT_GRAY)
        screen.blit(desc_text, (panel_x + 45, slot_y + 28))
        
        # Draw cost or max level indicator
        if is_max_level:
            status_text = self.small_font.render("MAX LEVEL", True, self.GOLD)
        elif cost > 0:
            cost_color = self.GREEN if can_afford else self.RED
            status_text = self.small_font.render(f"Cost: {cost}", True, cost_color)
        else:
            status_text = self.small_font.render("Unavailable", True, self.GRAY)
        
        screen.blit(status_text, (panel_x + 45, slot_y + 48))
        
        # Draw level progress bar
        if max_level > 1:
            self._draw_level_progress(screen, panel_x + 10, slot_y + 65, 
                                    self.panel_width - 20, current_level, max_level)
    
    def _draw_level_progress(self, screen: pygame.Surface, x: int, y: int, width: int, 
                           current_level: int, max_level: int):
        """Draw a progress bar showing upgrade level"""
        bar_height = 6
        progress = current_level / max_level if max_level > 0 else 0
        
        # Background
        bg_rect = pygame.Rect(x, y, width, bar_height)
        pygame.draw.rect(screen, self.DARK_GRAY, bg_rect)
        
        # Progress
        if progress > 0:
            progress_width = int(width * progress)
            progress_rect = pygame.Rect(x, y, progress_width, bar_height)
            pygame.draw.rect(screen, self.GOLD, progress_rect)
        
        # Border
        pygame.draw.rect(screen, self.WHITE, bg_rect, 1)
    
    def _draw_remove_button(self, screen: pygame.Surface, panel_x: int, panel_y: int):
        """Draw the remove tower button"""
        button_y = panel_y + self.panel_height - 50
        button_rect = pygame.Rect(panel_x + 10, button_y, self.panel_width - 20, 35)
        
        # Button color based on hover state
        if self.hovered_remove_button:
            button_color = (180, 60, 60)  # Darker red when hovered
        else:
            button_color = (200, 80, 80)  # Light red
        
        # Draw button
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, self.WHITE, button_rect, 2)
        
        # Calculate refund amount (50% of current tower cost)
        if hasattr(self.selected_tower, 'tower_type'):
            # We'll calculate the refund in the game logic, but show estimate
            tower_type = self.selected_tower.tower_type
            button_text = "Remove Tower (50% Refund)"
        else:
            button_text = "Remove Tower"
        
        # Draw button text
        text_surface = self.medium_font.render(button_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _get_upgrade_type_color(self, upgrade_type: UpgradeType) -> Tuple[int, int, int]:
        """Get color for upgrade type icon"""
        color_map = {
            UpgradeType.DAMAGE: (255, 100, 100),  # Red
            UpgradeType.RANGE: (100, 255, 100),   # Green
            UpgradeType.UTILITY: (100, 100, 255)  # Blue
        }
        return color_map.get(upgrade_type, self.GRAY) 