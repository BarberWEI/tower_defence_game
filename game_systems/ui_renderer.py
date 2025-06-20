"""
UI Rendering - Handles all drawing operations for the game UI
"""
import pygame
import math
from typing import Dict, List, Tuple, Optional

class UIRenderer:
    """Handles all UI drawing operations"""
    
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
        
        # Layout constants
        self.bottom_bar_height = 120
        self.bottom_bar_y = screen_height - self.bottom_bar_height
        self.tower_slot_width = 80
        self.tower_slot_height = 80
        self.tower_slot_margin = 10
        
        # Speed button constants
        self.speed_button_width = 80
        self.speed_button_height = 40
        self.speed_button_x = screen_width - 120
        self.speed_button_y = 80
    
    def draw_game_stats(self, screen: pygame.Surface, money: int, lives: int, wave_info: Dict, game_speed: int = 1):
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
        
        # Speed button
        self.draw_speed_button(screen, game_speed)
        
        # Terrain legend (moved to top right)
        self.draw_terrain_legend(screen)
    
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
    
    def draw_performance_info(self, screen: pygame.Surface, performance_data: Dict):
        """Draw performance information in top right corner"""
        perf_x = self.screen_width - 200
        perf_y = 140  # Below terrain legend
        
        # Background
        perf_rect = pygame.Rect(perf_x - 10, perf_y - 10, 190, 90)
        pygame.draw.rect(screen, (20, 20, 20), perf_rect)
        pygame.draw.rect(screen, self.UI_BORDER, perf_rect, 1)
        
        # Title
        perf_title = self.small_font.render("Performance:", True, self.WHITE)
        screen.blit(perf_title, (perf_x, perf_y))
        
        # FPS
        fps = performance_data.get('fps', 0)
        fps_color = self.GREEN if fps >= 50 else self.YELLOW if fps >= 30 else self.RED
        fps_text = self.tiny_font.render(f"FPS: {fps}", True, fps_color)
        screen.blit(fps_text, (perf_x, perf_y + 20))
        
        # Frame time
        frame_time = performance_data.get('avg_frame_time_ms', 0)
        frame_color = self.GREEN if frame_time <= 20 else self.YELLOW if frame_time <= 33 else self.RED
        frame_text = self.tiny_font.render(f"Frame: {frame_time:.1f}ms", True, frame_color)
        screen.blit(frame_text, (perf_x, perf_y + 35))
        
        # Entity counts
        entities = performance_data.get('entity_counts', {})
        enemies_text = self.tiny_font.render(f"Enemies: {entities.get('enemies', 0)}", True, self.WHITE)
        screen.blit(enemies_text, (perf_x, perf_y + 50))
        
        projectiles_text = self.tiny_font.render(f"Projectiles: {entities.get('projectiles', 0)}", True, self.WHITE)
        screen.blit(projectiles_text, (perf_x, perf_y + 65))
    
    def draw_speed_button(self, screen: pygame.Surface, game_speed: int):
        """Draw the game speed control button"""
        button_rect = pygame.Rect(self.speed_button_x, self.speed_button_y, 
                                self.speed_button_width, self.speed_button_height)
        
        # Button background - different color based on speed
        if game_speed == 1:
            button_color = (60, 60, 100)  # Blue for normal speed
            text_color = self.WHITE
        else:
            button_color = (100, 60, 60)  # Red for fast speed
            text_color = self.YELLOW
        
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, self.WHITE, button_rect, 2)
        
        # Button text
        speed_text = self.small_font.render(f"Speed: {game_speed}x", True, text_color)
        text_rect = speed_text.get_rect(center=button_rect.center)
        screen.blit(speed_text, text_rect)
        
        # Add visual indicator for different speeds
        if game_speed == 2:
            # Add arrows for fast speed
            arrow_y = self.speed_button_y - 8
            for i in range(2):
                arrow_x = self.speed_button_x + 20 + i * 20
                pygame.draw.polygon(screen, self.YELLOW, [
                    (arrow_x, arrow_y),
                    (arrow_x + 8, arrow_y + 4),
                    (arrow_x, arrow_y + 8)
                ])
    
    def is_speed_button_clicked(self, pos: Tuple[int, int]) -> bool:
        """Check if the speed button was clicked"""
        mouse_x, mouse_y = pos
        return (self.speed_button_x <= mouse_x <= self.speed_button_x + self.speed_button_width and
                self.speed_button_y <= mouse_y <= self.speed_button_y + self.speed_button_height)
    
    def draw_tower_bar(self, screen: pygame.Surface, tower_data: List[dict], money: int, 
                      scroll_offset: int, max_scroll: int, selected_index: Optional[int], 
                      hovered_index: Optional[int]):
        """Draw the scrollable tower bar at the bottom"""
        # Background
        tower_bar_rect = pygame.Rect(0, self.bottom_bar_y, self.screen_width, self.bottom_bar_height)
        pygame.draw.rect(screen, self.UI_BG, tower_bar_rect)
        pygame.draw.rect(screen, self.UI_BORDER, tower_bar_rect, 2)
        
        # Title
        title_text = self.medium_font.render("Towers", True, self.WHITE)
        screen.blit(title_text, (20, self.bottom_bar_y + 5))
        
        # Tower slots
        start_x = 20
        start_y = self.bottom_bar_y + 30
        
        for i, tower in enumerate(tower_data):
            slot_x = start_x + i * (self.tower_slot_width + self.tower_slot_margin) - scroll_offset
            
            # Skip if completely off screen
            if slot_x + self.tower_slot_width < 0 or slot_x > self.screen_width:
                continue
            
            self._draw_tower_slot(screen, tower, slot_x, start_y, money, 
                                i == selected_index, i == hovered_index)
        
        # Scroll indicators
        if scroll_offset > 0:
            # Left scroll indicator
            pygame.draw.polygon(screen, self.WHITE, [
                (5, self.bottom_bar_y + 60),
                (15, self.bottom_bar_y + 50),
                (15, self.bottom_bar_y + 70)
            ])
        
        if scroll_offset < max_scroll:
            # Right scroll indicator
            pygame.draw.polygon(screen, self.WHITE, [
                (self.screen_width - 5, self.bottom_bar_y + 60),
                (self.screen_width - 15, self.bottom_bar_y + 50),
                (self.screen_width - 15, self.bottom_bar_y + 70)
            ])
    
    def _draw_tower_slot(self, screen: pygame.Surface, tower_data: dict, x: int, y: int, 
                        money: int, is_selected: bool, is_hovered: bool):
        """Draw a single tower slot"""
        slot_rect = pygame.Rect(x, y, self.tower_slot_width, self.tower_slot_height)
        
        # Determine slot state
        can_afford = money >= tower_data['cost']
        
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
        icon_center = (x + self.tower_slot_width // 2, y + 25)
        tower_color = tower_data['color'] if can_afford else self.GRAY
        
        # Draw tower icon
        pygame.draw.circle(screen, tower_color, icon_center, 12)
        pygame.draw.circle(screen, border_color, icon_center, 12, 2)
        
        # Draw tower "barrel" for visual appeal
        barrel_end = (icon_center[0] + 8, icon_center[1] - 8)
        pygame.draw.line(screen, border_color, icon_center, barrel_end, 3)
        
        # Cost text
        cost_color = self.WHITE if can_afford else self.RED
        cost_text = self.tiny_font.render(f"${tower_data['cost']}", True, cost_color)
        cost_rect = cost_text.get_rect(centerx=x + self.tower_slot_width // 2, y=y + 50)
        screen.blit(cost_text, cost_rect)
    
    def draw_tower_tooltip(self, screen: pygame.Surface, tower_data: dict, mouse_pos: Tuple[int, int]):
        """Draw tooltip for hovered tower"""
        # Tooltip background
        tooltip_width = 200
        tooltip_height = 80
        tooltip_x = min(mouse_pos[0] + 10, self.screen_width - tooltip_width)
        tooltip_y = max(10, mouse_pos[1] - tooltip_height - 10)
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        pygame.draw.rect(screen, self.UI_BG, tooltip_rect)
        pygame.draw.rect(screen, self.UI_BORDER, tooltip_rect, 2)
        
        # Tower name
        name_text = self.small_font.render(tower_data['name'], True, self.WHITE)
        screen.blit(name_text, (tooltip_x + 5, tooltip_y + 5))
        
        # Description
        desc_text = self.tiny_font.render(tower_data['description'], True, self.LIGHT_GRAY)
        screen.blit(desc_text, (tooltip_x + 5, tooltip_y + 25))
        
        # Stats
        y_offset = 45
        for stat, value in tower_data['stats'].items():
            stat_text = self.tiny_font.render(f"{stat}: {value}", True, self.WHITE)
            screen.blit(stat_text, (tooltip_x + 5, tooltip_y + y_offset))
            y_offset += 15
    
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
        
        speed_text = self.small_font.render("Press TAB to change speed", True, self.LIGHT_GRAY)
        speed_rect = speed_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
        screen.blit(speed_text, speed_rect)
    
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