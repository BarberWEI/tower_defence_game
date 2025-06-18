import pygame
import math
from typing import Dict, List, Tuple, Optional

class UIManager:
    """Handles all user interface rendering and display with modern scrollable UI"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_GRAY = (64, 64, 64)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        
        # UI Colors
        self.UI_BG = (40, 40, 40)
        self.UI_BORDER = (80, 80, 80)
        self.UI_HOVER = (60, 60, 60)
        self.UI_SELECTED = (100, 150, 100)
        
        # Fonts
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        
        # Bottom UI Bar
        self.bottom_bar_height = 120
        self.bottom_bar_y = screen_height - self.bottom_bar_height
        self.tower_bar_rect = pygame.Rect(0, self.bottom_bar_y, screen_width, self.bottom_bar_height)
        
        # Tower selection
        self.tower_slot_width = 80
        self.tower_slot_height = 80
        self.tower_slot_margin = 10
        self.scroll_offset = 0
        self.max_scroll = 0
        self.selected_tower_index = None
        self.hovered_tower_index = None
        
        # Tower information with visual data - rebalanced
        self.tower_data = [
            {
                'name': 'Basic Tower',
                'cost': 15,
                'color': (0, 200, 0),
                'description': 'Cheap starter tower',
                'stats': {'Damage': 2, 'Range': 80, 'Speed': 'Fast'},
                'key': '1'
            },
            {
                'name': 'Sniper Tower',
                'cost': 45,
                'color': (0, 0, 255),
                'description': 'Long range, high damage',
                'stats': {'Damage': 5, 'Range': 200, 'Speed': 'Slow'},
                'key': '2'
            },
            {
                'name': 'Freezer Tower',
                'cost': 25,
                'color': (0, 255, 255),
                'description': 'Slows enemies, no damage',
                'stats': {'Damage': 0, 'Range': 70, 'Speed': 'Medium'},
                'key': '3'
            },
            {
                'name': 'Detector Tower',
                'cost': 30,
                'color': (255, 255, 0),
                'description': 'Reveals invisible enemies',
                'stats': {'Damage': 0, 'Range': 300, 'Speed': 'Support'},
                'key': '4'
            },
            {
                'name': 'Anti-Air Tower',
                'cost': 55,
                'color': (0, 191, 255),
                'description': 'Targets flying enemies',
                'stats': {'Damage': 20, 'Range': 180, 'Speed': 'Medium'},
                'key': '5'
            },
            {
                'name': 'Poison Tower',
                'cost': 40,
                'color': (50, 205, 50),
                'description': 'Poison damage over time',
                'stats': {'Damage': 6, 'Range': 120, 'Speed': 'Medium'},
                'key': '6'
            },
            {
                'name': 'Laser Tower',
                'cost': 60,
                'color': (255, 0, 255),
                'description': 'Pierces through enemies',
                'stats': {'Damage': 12, 'Range': 140, 'Speed': 'Medium'},
                'key': '7'
            },
            {
                'name': 'Cannon Tower',
                'cost': 75,
                'color': (139, 69, 19),
                'description': 'Splash damage, 2x2 size',
                'stats': {'Damage': 25, 'Range': 160, 'Speed': 'Slow'},
                'key': '8'
            },
            {
                'name': 'Lightning Tower',
                'cost': 50,
                'color': (255, 255, 0),
                'description': 'Chains between enemies',
                'stats': {'Damage': 7, 'Range': 120, 'Speed': 'Medium'},
                'key': '9'
            },
            {
                'name': 'Flame Tower',
                'cost': 35,
                'color': (255, 69, 0),
                'description': 'Cone attack with burn',
                'stats': {'Damage': 6, 'Range': 90, 'Speed': 'Very Fast'},
                'key': '0'
            },
            {
                'name': 'Ice Tower',
                'cost': 30,
                'color': (173, 216, 230),
                'description': 'Area freeze and slow',
                'stats': {'Damage': 2, 'Range': 90, 'Speed': 'Slow'},
                'key': 'Q'
            },
            {
                'name': 'Explosive Tower',
                'cost': 100,
                'color': (255, 165, 0),
                'description': 'Massive splash, 3x3 size',
                'stats': {'Damage': 35, 'Range': 180, 'Speed': 'Very Slow'},
                'key': 'W'
            },
            {
                'name': 'Missile Tower',
                'cost': 120,
                'color': (128, 128, 128),
                'description': 'Homing missiles, AOE, 2x2 size',
                'stats': {'Damage': 40, 'Range': 250, 'Speed': 'Ultra Slow'},
                'key': 'E'
            }
        ]
        
        # Tower selection for range display
        self.selected_placed_tower = None
        
        # Mouse state
        self.mouse_pos = (0, 0)
        
        # Calculate max scroll
        total_width = len(self.tower_data) * (self.tower_slot_width + self.tower_slot_margin)
        visible_width = self.screen_width - 40  # margins
        self.max_scroll = max(0, total_width - visible_width)
    
    def update_mouse_pos(self, pos: Tuple[int, int]):
        """Update mouse position for hover effects"""
        self.mouse_pos = pos
        self.update_hover_state()
    
    def update_hover_state(self):
        """Update which tower slot is being hovered"""
        mouse_x, mouse_y = self.mouse_pos
        
        # Check if mouse is in tower bar area
        if self.bottom_bar_y <= mouse_y <= self.screen_height:
            # Calculate which tower slot is hovered
            relative_x = mouse_x - 20 + self.scroll_offset  # 20 is left margin
            slot_index = int(relative_x // (self.tower_slot_width + self.tower_slot_margin))
            
            if 0 <= slot_index < len(self.tower_data):
                # Check if mouse is actually over the slot (not in margin)
                slot_x = slot_index * (self.tower_slot_width + self.tower_slot_margin) - self.scroll_offset + 20
                if slot_x <= mouse_x <= slot_x + self.tower_slot_width:
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
        
        if self.bottom_bar_y <= mouse_y <= self.screen_height:
            relative_x = mouse_x - 20 + self.scroll_offset
            slot_index = int(relative_x // (self.tower_slot_width + self.tower_slot_margin))
            
            if 0 <= slot_index < len(self.tower_data):
                slot_x = slot_index * (self.tower_slot_width + self.tower_slot_margin) - self.scroll_offset + 20
                if slot_x <= mouse_x <= slot_x + self.tower_slot_width:
                    self.selected_tower_index = slot_index
                    return slot_index
        
        return None
    
    def handle_scroll(self, direction: int):
        """Handle scrolling in the tower bar"""
        scroll_speed = 30
        if direction > 0:  # Scroll right
            self.scroll_offset = min(self.max_scroll, self.scroll_offset + scroll_speed)
        else:  # Scroll left
            self.scroll_offset = max(0, self.scroll_offset - scroll_speed)
    
    def draw_bottom_tower_bar(self, screen: pygame.Surface, money: int):
        """Draw the modern scrollable tower bar at the bottom"""
        # Background
        pygame.draw.rect(screen, self.UI_BG, self.tower_bar_rect)
        pygame.draw.rect(screen, self.UI_BORDER, self.tower_bar_rect, 2)
        
        # Title
        title_text = self.medium_font.render("Towers", True, self.WHITE)
        screen.blit(title_text, (20, self.bottom_bar_y + 5))
        
        # Tower slots
        start_x = 20
        start_y = self.bottom_bar_y + 30
        
        for i, tower in enumerate(self.tower_data):
            slot_x = start_x + i * (self.tower_slot_width + self.tower_slot_margin) - self.scroll_offset
            
            # Skip if completely off screen
            if slot_x + self.tower_slot_width < 0 or slot_x > self.screen_width:
                continue
            
            slot_rect = pygame.Rect(slot_x, start_y, self.tower_slot_width, self.tower_slot_height)
            
            # Determine slot state
            can_afford = money >= tower['cost']
            is_selected = i == self.selected_tower_index
            is_hovered = i == self.hovered_tower_index
            
            # Slot background
            if is_selected:
                bg_color = self.UI_SELECTED
            elif is_hovered:
                bg_color = self.UI_HOVER
            else:
                bg_color = self.DARK_GRAY
            
            pygame.draw.rect(screen, bg_color, slot_rect)
            
            # Border color based on affordability
            border_color = self.WHITE if can_afford else self.RED
            pygame.draw.rect(screen, border_color, slot_rect, 2)
            
            # Tower icon (simplified tower representation)
            icon_center = (slot_x + self.tower_slot_width // 2, start_y + 25)
            tower_color = tower['color'] if can_afford else self.GRAY
            
            # Draw tower icon
            pygame.draw.circle(screen, tower_color, icon_center, 12)
            pygame.draw.circle(screen, border_color, icon_center, 12, 2)
            
            # Draw tower "barrel" for visual appeal
            barrel_end = (icon_center[0] + 8, icon_center[1] - 8)
            pygame.draw.line(screen, border_color, icon_center, barrel_end, 3)
            
            # Cost text
            cost_color = self.WHITE if can_afford else self.RED
            cost_text = self.tiny_font.render(f"${tower['cost']}", True, cost_color)
            cost_rect = cost_text.get_rect(centerx=slot_x + self.tower_slot_width // 2, 
                                         y=start_y + 50)
            screen.blit(cost_text, cost_rect)
            
            # Hotkey
            key_text = self.tiny_font.render(tower['key'], True, self.LIGHT_GRAY)
            screen.blit(key_text, (slot_x + 2, start_y + 2))
        
        # Scroll indicators
        if self.scroll_offset > 0:
            # Left scroll indicator
            pygame.draw.polygon(screen, self.WHITE, [
                (5, self.bottom_bar_y + 60),
                (15, self.bottom_bar_y + 50),
                (15, self.bottom_bar_y + 70)
            ])
        
        if self.scroll_offset < self.max_scroll:
            # Right scroll indicator
            pygame.draw.polygon(screen, self.WHITE, [
                (self.screen_width - 5, self.bottom_bar_y + 60),
                (self.screen_width - 15, self.bottom_bar_y + 50),
                (self.screen_width - 15, self.bottom_bar_y + 70)
            ])
    
    def draw_tower_tooltip(self, screen: pygame.Surface):
        """Draw tooltip for hovered tower"""
        if self.hovered_tower_index is not None:
            tower = self.tower_data[self.hovered_tower_index]
            
            # Tooltip background
            tooltip_width = 200
            tooltip_height = 80
            tooltip_x = min(self.mouse_pos[0] + 10, self.screen_width - tooltip_width)
            tooltip_y = max(10, self.mouse_pos[1] - tooltip_height - 10)
            
            tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
            pygame.draw.rect(screen, self.UI_BG, tooltip_rect)
            pygame.draw.rect(screen, self.UI_BORDER, tooltip_rect, 2)
            
            # Tower name
            name_text = self.small_font.render(tower['name'], True, self.WHITE)
            screen.blit(name_text, (tooltip_x + 5, tooltip_y + 5))
            
            # Description
            desc_text = self.tiny_font.render(tower['description'], True, self.LIGHT_GRAY)
            screen.blit(desc_text, (tooltip_x + 5, tooltip_y + 25))
            
            # Stats
            y_offset = 45
            for stat, value in tower['stats'].items():
                stat_text = self.tiny_font.render(f"{stat}: {value}", True, self.WHITE)
                screen.blit(stat_text, (tooltip_x + 5, tooltip_y + y_offset))
                y_offset += 15
    
    def draw_upgrade_panel(self, screen: pygame.Surface, tower, money: int):
        """Draw the tower upgrade panel - simplified to just show range"""
        # Note: The actual range circle is drawn in the game loop when tower is selected
        # This method is kept for compatibility but does nothing now
        pass
    
    def handle_tower_click(self, pos: Tuple[int, int], towers: List) -> bool:
        """Handle clicks on placed towers to show range"""
        mouse_x, mouse_y = pos
        
        # Don't handle if clicking in UI areas - map starts at y=140 and ends before bottom bar
        if mouse_y >= self.bottom_bar_y or mouse_y <= 130:  # Bottom bar or top stats area
            return False
        
        # Check if click is within screen bounds (dynamic for fullscreen)
        if mouse_x < 0 or mouse_x > self.screen_width or mouse_y < 140 or mouse_y >= self.bottom_bar_y:
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
    
    def draw_game_stats(self, screen: pygame.Surface, money: int, lives: int, wave_info: Dict):
        """Draw the main game statistics in top area"""
        # Background for stats area
        stats_rect = pygame.Rect(0, 0, self.screen_width, 130)
        pygame.draw.rect(screen, (20, 20, 20), stats_rect)
        pygame.draw.rect(screen, self.UI_BORDER, stats_rect, 2)
        
        # Money
        money_text = self.large_font.render(f"Money: ${money}", True, self.GREEN)
        screen.blit(money_text, (20, 20))
        
        # Lives
        lives_color = self.RED if lives <= 3 else self.WHITE
        lives_text = self.large_font.render(f"Lives: {lives}", True, lives_color)
        screen.blit(lives_text, (20, 60))
        
        # Wave information with scaling indicator
        wave_text = self.large_font.render(f"Wave: {wave_info['wave_number']}", True, self.WHITE)
        screen.blit(wave_text, (20, 100))
        
        # Enemy scaling indicator (subtle)
        if wave_info['wave_number'] > 1:
            scaling_factor = (wave_info['wave_number'] - 1) * 8  # 8% per wave
            scaling_text = self.tiny_font.render(f"Enemy Boost: +{scaling_factor}%", True, (255, 200, 100))
            screen.blit(scaling_text, (150, 105))
        
        # Wave progress bar
        self.draw_wave_progress_bar(screen, wave_info)
        
        # Terrain legend (moved to top right)
        self.draw_terrain_legend(screen)
        
        # Fullscreen indicator (bottom right of stats area)
        fullscreen_text = self.tiny_font.render("F1: Fullscreen", True, self.WHITE)
        screen.blit(fullscreen_text, (self.screen_width - 120, 110))
    
    def draw_wave_progress_bar(self, screen: pygame.Surface, wave_info: Dict):
        """Draw wave progress bar in stats area"""
        bar_x = 250
        bar_y = 50
        bar_width = 200
        bar_height = 20
        
        # Background
        pygame.draw.rect(screen, self.DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Progress
        progress = wave_info.get('progress', 0)
        progress_width = int(bar_width * progress)
        pygame.draw.rect(screen, self.GREEN, (bar_x, bar_y, progress_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, self.WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Text
        progress_text = self.small_font.render("Wave Progress", True, self.WHITE)
        screen.blit(progress_text, (bar_x, bar_y - 25))
        
        # Enemy count
        enemy_text = self.tiny_font.render(
            f"{wave_info.get('enemies_spawned', 0)}/{wave_info.get('enemies_per_wave', 0)}", 
            True, self.WHITE
        )
        enemy_rect = enemy_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(enemy_text, enemy_rect)
    
    def draw_terrain_legend(self, screen: pygame.Surface):
        """Draw terrain legend in top right"""
        legend_x = min(self.screen_width - 200, 980 - 190)  # Keep within game area
        legend_y = 20
        
        # Background
        legend_rect = pygame.Rect(legend_x - 10, legend_y - 10, 190, 110)
        pygame.draw.rect(screen, (20, 20, 20), legend_rect)
        pygame.draw.rect(screen, self.UI_BORDER, legend_rect, 1)
        
        legend_title = self.small_font.render("Terrain:", True, self.WHITE)
        screen.blit(legend_title, (legend_x, legend_y))
        
        terrain_legend = [
            ((34, 139, 34), "Grass"),
            ((139, 69, 19), "Path"),
            ((105, 105, 105), "Rock"),
            ((30, 144, 255), "Water"),
            ((0, 100, 0), "Forest")
        ]
        
        for i, (color, name) in enumerate(terrain_legend):
            y = legend_y + 20 + i * 15
            pygame.draw.rect(screen, color, (legend_x, y, 10, 10))
            pygame.draw.rect(screen, self.WHITE, (legend_x, y, 10, 10), 1)
            desc_text = self.tiny_font.render(name, True, self.WHITE)
            screen.blit(desc_text, (legend_x + 15, y - 1))
    
    def draw_pause_overlay(self, screen: pygame.Surface):
        """Draw pause overlay"""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        screen.blit(overlay, (0, 0))
        
        pause_text = self.large_font.render("PAUSED", True, self.WHITE)
        text_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(pause_text, text_rect)
        
        resume_text = self.medium_font.render("Press SPACE to resume", True, self.WHITE)
        resume_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(resume_text, resume_rect)
        
        fullscreen_text = self.small_font.render("Press F11 for fullscreen", True, self.WHITE)
        fullscreen_rect = fullscreen_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 90))
        screen.blit(fullscreen_text, fullscreen_rect)
    
    def draw_game_over_overlay(self, screen: pygame.Surface, final_wave: int):
        """Draw game over overlay"""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(self.RED)
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.large_font.render("GAME OVER", True, self.WHITE)
        text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(game_over_text, text_rect)
        
        wave_text = self.medium_font.render(f"You reached wave {final_wave}!", True, self.WHITE)
        wave_rect = wave_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(wave_text, wave_rect)
        
        restart_text = self.medium_font.render("Press R to restart or ESC to quit", True, self.WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)
    
    def draw_complete_ui(self, screen: pygame.Surface, game_state: Dict):
        """Draw the complete modern user interface"""
        # Main game stats (top area)
        self.draw_game_stats(screen, game_state['money'], game_state['lives'], 
                           game_state['wave_info'])
        
        # Bottom tower bar
        self.draw_bottom_tower_bar(screen, game_state['money'])
        
        # Tower tooltip
        self.draw_tower_tooltip(screen)
        
        # Tower range display is handled in game loop when tower is selected
        
        # Overlays
        if game_state.get('paused'):
            self.draw_pause_overlay(screen)
        elif game_state.get('game_over'):
            self.draw_game_over_overlay(screen, game_state['wave_info']['wave_number'])
    
    def get_selected_tower_type(self) -> Optional[str]:
        """Get the currently selected tower type"""
        if self.selected_tower_index is not None:
            tower_types = ['basic', 'sniper', 'freezer', 'detector', 'antiair', 'poison', 'laser', 
                          'cannon', 'lightning', 'flame', 'ice', 'explosive', 'missile']
            return tower_types[self.selected_tower_index]
        return None
    
    def clear_tower_selection(self):
        """Clear tower selection"""
        self.selected_tower_index = None
