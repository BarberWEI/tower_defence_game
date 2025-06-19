import pygame
from typing import Dict, Set, Optional

class EnemyIntroduction:
    """System for introducing new enemy types to players"""
    
    def __init__(self):
        # Track which enemies have been introduced
        self.introduced_enemies: Set[str] = set()
        
        # Current introduction being displayed
        self.current_introduction: Optional[Dict] = None
        self.introduction_timer = 0
        self.introduction_duration = 300  # 5 seconds at 60 FPS
        
        # Enemy information database
        self.enemy_info = {
            'ArmoredEnemy': {
                'name': 'Armored Enemy',
                'description': 'Heavy armor plating makes this enemy immune to Basic Tower damage!',
                'counters': 'Use Sniper, Laser, or Lightning Towers to penetrate armor',
                'color': (255, 255, 0),  # Yellow warning
                'icon': 'ARM'
            },
            'EnergyShieldEnemy': {
                'name': 'Energy Shield Enemy',
                'description': 'Energy shields deflect all Laser Tower attacks!',
                'counters': 'Use Basic, Sniper, or Lightning Towers to bypass shields',
                'color': (0, 255, 255),  # Cyan
                'icon': 'SHLD'
            },
            'GroundedEnemy': {
                'name': 'Grounded Enemy', 
                'description': 'Electrical grounding makes this enemy immune to Lightning damage!',
                'counters': 'Use Basic, Sniper, or Laser Towers for effective damage',
                'color': (255, 215, 0),  # Gold
                'icon': 'GND'
            },
            'FireElementalEnemy': {
                'name': 'Fire Elemental',
                'description': 'Made of pure fire - immune to Flame Towers and actually heals from fire!',
                'counters': 'Use Ice, Lightning, or Basic Towers to extinguish',
                'color': (255, 100, 0),  # Orange-red
                'icon': 'FIRE'
            },
            'ToxicEnemy': {
                'name': 'Toxic Enemy',
                'description': 'Already poisonous - completely immune to Poison Tower damage!',
                'counters': 'Use Basic, Laser, or Lightning Towers to neutralize',
                'color': (76, 175, 80),  # Toxic green
                'icon': 'TOX'
            },
            'PhaseShiftEnemy': {
                'name': 'Phase Shifter',
                'description': 'Phases through dimensions - Sniper Tower shots pass right through!',
                'counters': 'Use area-effect towers like Laser or Lightning',
                'color': (128, 0, 128),  # Purple
                'icon': 'PHASE'
            },
            'BlastProofEnemy': {
                'name': 'Blast-Proof Enemy',
                'description': 'Reinforced armor resists all explosive damage! Immune to Cannon, Missile, and Explosive Towers!',
                'counters': 'Use precision towers like Sniper or Laser',
                'color': (255, 255, 255),  # White
                'icon': 'BLAST'
            }
        }
    
    def check_new_enemy(self, enemy_type: str) -> bool:
        """Check if this enemy type needs to be introduced"""
        if enemy_type not in self.introduced_enemies and enemy_type in self.enemy_info:
            self.introduce_enemy(enemy_type)
            self.introduced_enemies.add(enemy_type)
            return True
        return False
    
    def introduce_enemy(self, enemy_type: str):
        """Start introducing a new enemy type"""
        if enemy_type in self.enemy_info:
            self.current_introduction = self.enemy_info[enemy_type].copy()
            self.current_introduction['enemy_type'] = enemy_type
            self.introduction_timer = 0
    
    def update(self):
        """Update introduction display timer"""
        if self.current_introduction:
            self.introduction_timer += 1
            if self.introduction_timer >= self.introduction_duration:
                self.current_introduction = None
                self.introduction_timer = 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the introduction overlay if active"""
        if not self.current_introduction:
            return
        
        screen_width, screen_height = screen.get_size()
        
        # Calculate fade alpha based on timer
        fade_in_time = 30
        fade_out_time = 60
        
        if self.introduction_timer < fade_in_time:
            alpha = int(255 * (self.introduction_timer / fade_in_time))
        elif self.introduction_timer > (self.introduction_duration - fade_out_time):
            remaining = self.introduction_duration - self.introduction_timer
            alpha = int(255 * (remaining / fade_out_time))
        else:
            alpha = 255
        
        # Draw semi-transparent background
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(128, alpha // 2)))
        screen.blit(overlay, (0, 0))
        
        # Introduction panel dimensions
        panel_width = 400
        panel_height = 150
        panel_x = (screen_width - panel_width) // 2
        panel_y = screen_height // 4
        
        # Draw panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_color = (40, 40, 40, min(240, alpha))
        pygame.draw.rect(panel_surface, panel_color, (0, 0, panel_width, panel_height))
        pygame.draw.rect(panel_surface, (255, 255, 255, min(255, alpha)), 
                        (0, 0, panel_width, panel_height), 3)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Enemy icon and accent color
        icon_color = (*self.current_introduction['color'], min(255, alpha))
        
        # Draw "NEW ENEMY!" header
        font_large = pygame.font.Font(None, 28)
        header_text = font_large.render("NEW ENEMY DETECTED!", True, (255, 255, 0))
        header_rect = header_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 25))
        screen.blit(header_text, header_rect)
        
        # Draw enemy name with icon
        font_medium = pygame.font.Font(None, 24)
        name_text = font_medium.render(self.current_introduction['name'], True, icon_color[:3])
        name_rect = name_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 50))
        screen.blit(name_text, name_rect)
        
        # Draw icon next to name
        icon_text = font_medium.render(f"[{self.current_introduction['icon']}]", True, icon_color[:3])
        icon_rect = icon_text.get_rect(left=name_rect.right + 10, centery=name_rect.centery)
        screen.blit(icon_text, icon_rect)
        
        # Draw description
        font_small = pygame.font.Font(None, 18)
        desc_lines = self.wrap_text(self.current_introduction['description'], font_small, panel_width - 20)
        
        y_offset = panel_y + 75
        for line in desc_lines:
            desc_text = font_small.render(line, True, (255, 255, 255))
            desc_rect = desc_text.get_rect(center=(panel_x + panel_width // 2, y_offset))
            screen.blit(desc_text, desc_rect)
            y_offset += 20
        
        # Draw counter strategy
        counter_text = font_small.render(f"Strategy: {self.current_introduction['counters']}", True, (0, 255, 0))
        counter_rect = counter_text.get_rect(center=(panel_x + panel_width // 2, panel_y + panel_height - 15))
        screen.blit(counter_text, counter_rect)
        
        # Draw progress bar
        progress = self.introduction_timer / self.introduction_duration
        bar_width = panel_width - 40
        bar_height = 4
        bar_x = panel_x + 20
        bar_y = panel_y + panel_height - 30
        
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list:
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def has_active_introduction(self) -> bool:
        """Check if an introduction is currently being displayed"""
        return self.current_introduction is not None
    
    def reset_introductions(self):
        """Reset all introductions (for new game)"""
        self.introduced_enemies.clear()
        self.current_introduction = None
        self.introduction_timer = 0 