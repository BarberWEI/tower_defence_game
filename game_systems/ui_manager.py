import pygame
from typing import Dict, List, Tuple

class UIManager:
    """Handles all user interface rendering and display"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        
        # Fonts
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        
        # Tower information
        self.tower_info = [
            ("1 - Basic Tower ($20)", self.GREEN, "Fast firing, good all-around"),
            ("2 - Sniper Tower ($50)", self.BLUE, "Long range, high damage"),
            ("3 - Freezer Tower ($30)", self.BLUE, "Slows enemies, no damage")
        ]
        
        # UI layout
        self.stats_area = pygame.Rect(10, 10, 300, 120)
        self.tower_selection_area = pygame.Rect(10, 140, 400, 100)
        self.instructions_area = pygame.Rect(10, 250, 400, 100)
    
    def draw_game_stats(self, screen: pygame.Surface, money: int, lives: int, wave_info: Dict):
        """Draw the main game statistics"""
        # Money
        money_text = self.large_font.render(f"Money: ${money}", True, self.BLACK)
        screen.blit(money_text, (10, 10))
        
        # Lives
        lives_text = self.large_font.render(f"Lives: {lives}", True, self.BLACK)
        screen.blit(lives_text, (10, 50))
        
        # Wave information
        wave_text = self.large_font.render(f"Wave: {wave_info['wave_number']}", True, self.BLACK)
        screen.blit(wave_text, (10, 90))
        
        # Wave progress
        progress_text = self.medium_font.render(
            f"Enemies: {wave_info['enemies_spawned']}/{wave_info['enemies_per_wave']}", 
            True, self.GRAY
        )
        screen.blit(progress_text, (150, 95))
    
    def draw_tower_selection(self, screen: pygame.Surface, selected_tower: str = None):
        """Draw tower selection menu"""
        y_offset = 140
        
        for i, (text, color, description) in enumerate(self.tower_info):
            # Highlight selected tower
            if selected_tower and str(i + 1) in selected_tower:
                pygame.draw.rect(screen, (200, 200, 200), 
                               (5, y_offset + i * 35 - 5, 450, 30))
            
            # Tower name and cost
            tower_text = self.large_font.render(text, True, color)
            screen.blit(tower_text, (10, y_offset + i * 35))
            
            # Description
            desc_text = self.small_font.render(description, True, self.GRAY)
            screen.blit(desc_text, (320, y_offset + i * 35 + 5))
    
    def draw_instructions(self, screen: pygame.Surface):
        """Draw game instructions"""
        instructions = [
            "SPACE - Pause/Resume",
            "ESC - Cancel tower placement",
            "Click to place selected tower",
            "R - Restart game"
        ]
        
        y_offset = 250
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, self.GRAY)
            screen.blit(inst_text, (10, y_offset + i * 25))
    
    def draw_wave_progress_bar(self, screen: pygame.Surface, wave_info: Dict):
        """Draw a progress bar for the current wave"""
        bar_x = self.screen_width - 220
        bar_y = 20
        bar_width = 200
        bar_height = 20
        
        # Background
        pygame.draw.rect(screen, self.GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Progress
        progress = wave_info['progress']
        progress_width = int(bar_width * progress)
        pygame.draw.rect(screen, self.GREEN, (bar_x, bar_y, progress_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, self.BLACK, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Text
        progress_text = self.small_font.render("Wave Progress", True, self.BLACK)
        screen.blit(progress_text, (bar_x, bar_y - 20))
    
    def draw_pause_overlay(self, screen: pygame.Surface):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("PAUSED", True, self.WHITE)
        text_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(pause_text, text_rect)
        
        # Resume instruction
        resume_text = self.medium_font.render("Press SPACE to resume", True, self.WHITE)
        resume_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(resume_text, resume_rect)
    
    def draw_game_over_overlay(self, screen: pygame.Surface, final_wave: int):
        """Draw game over overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(self.RED)
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.large_font.render("GAME OVER", True, self.WHITE)
        text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(game_over_text, text_rect)
        
        # Final wave text
        wave_text = self.medium_font.render(f"You reached wave {final_wave}!", True, self.WHITE)
        wave_rect = wave_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(wave_text, wave_rect)
        
        # Restart instruction
        restart_text = self.medium_font.render("Press R to restart or ESC to quit", True, self.WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)
    
    def draw_wave_complete_notification(self, screen: pygame.Surface, wave_number: int, money_bonus: int):
        """Draw wave completion notification"""
        notification_y = self.screen_height - 100
        
        # Background
        pygame.draw.rect(screen, (50, 150, 50), 
                        (self.screen_width // 2 - 150, notification_y - 10, 300, 60))
        pygame.draw.rect(screen, self.BLACK, 
                        (self.screen_width // 2 - 150, notification_y - 10, 300, 60), 3)
        
        # Text
        wave_text = self.medium_font.render(f"Wave {wave_number - 1} Complete!", True, self.WHITE)
        bonus_text = self.small_font.render(f"+${money_bonus} bonus", True, self.WHITE)
        
        wave_rect = wave_text.get_rect(center=(self.screen_width // 2, notification_y + 10))
        bonus_rect = bonus_text.get_rect(center=(self.screen_width // 2, notification_y + 35))
        
        screen.blit(wave_text, wave_rect)
        screen.blit(bonus_text, bonus_rect)
    
    def draw_complete_ui(self, screen: pygame.Surface, game_state: Dict):
        """Draw the complete user interface"""
        # Main game stats
        self.draw_game_stats(screen, game_state['money'], game_state['lives'], 
                           game_state['wave_info'])
        
        # Tower selection
        self.draw_tower_selection(screen, game_state.get('selected_tower'))
        
        # Instructions
        self.draw_instructions(screen)
        
        # Wave progress bar
        self.draw_wave_progress_bar(screen, game_state['wave_info'])
        
        # Overlays based on game state
        if game_state.get('paused'):
            self.draw_pause_overlay(screen)
        elif game_state.get('game_over'):
            self.draw_game_over_overlay(screen, game_state['wave_info']['wave_number'])
        
        # Notifications
        if game_state.get('show_wave_complete'):
            self.draw_wave_complete_notification(screen, 
                                               game_state['wave_info']['wave_number'],
                                               game_state.get('wave_bonus', 50)) 