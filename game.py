import pygame
import random
from towers import BasicTower, SniperTower, SplashTower, LaserTower
from path import Path
from wave_manager import WaveManager
from config import GameConfig

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tower Defense")
        
        # Game state
        self.difficulty = 0.5  # Default difficulty
        self.config = GameConfig(self.difficulty)
        self.money = self.config.starting_money
        self.lives = self.config.starting_lives
        self.game_over = False
        self.selected_tower_type = BasicTower
        self.game_started = False
        self.wave_number = 0
        self.max_waves = 3
        self.wave_completed = False
        
        # Game objects
        self.towers = []
        self.enemies = []
        self.path = Path(self.difficulty)
        self.wave_manager = WaveManager()
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def handle_event(self, event):
        if not self.game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start game
                    self.game_started = True
                    self.start_next_wave()
                elif event.key == pygame.K_UP:  # Increase difficulty
                    self.difficulty = min(1.0, self.difficulty + 0.1)
                    self.update_difficulty()
                elif event.key == pygame.K_DOWN:  # Decrease difficulty
                    self.difficulty = max(0.0, self.difficulty - 0.1)
                    self.update_difficulty()
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_tower_placement(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space bar to start next wave
                if self.wave_completed and self.wave_number < self.max_waves:
                    self.start_next_wave()
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:  # Tower selection
                self.handle_tower_selection(event.key)
    
    def handle_tower_selection(self, key):
        tower_types = {
            pygame.K_1: BasicTower,
            pygame.K_2: SniperTower,
            pygame.K_3: SplashTower,
            pygame.K_4: LaserTower
        }
        
        if key in tower_types:
            tower_class = tower_types[key]
            if self.difficulty >= self.get_tower_unlock_difficulty(tower_class):
                self.selected_tower_type = tower_class
    
    def get_tower_unlock_difficulty(self, tower_class):
        unlock_difficulties = {
            BasicTower: 0.0,
            SniperTower: 0.3,
            SplashTower: 0.5,
            LaserTower: 0.7
        }
        return unlock_difficulties.get(tower_class, 1.0)
    
    def update_difficulty(self):
        self.config = GameConfig(self.difficulty)
        self.money = self.config.starting_money
        self.lives = self.config.starting_lives
        self.path = Path(self.difficulty)
        self.selected_tower_type = BasicTower  # Reset to BasicTower class
    
    def handle_tower_placement(self, pos):
        if self.selected_tower_type:
            # Check if position is valid (not on path)
            if not self.path.is_point_on_path(pos):
                tower = self.selected_tower_type(pos, self.config)
                if self.money >= tower.cost:
                    # Check if position overlaps with existing towers
                    if not any(self.check_tower_overlap(tower, existing_tower) for existing_tower in self.towers):
                        self.towers.append(tower)
                        self.money -= tower.cost
    
    def check_tower_overlap(self, new_tower, existing_tower):
        # Towers should not be placed too close to each other
        min_distance = 40  # Minimum distance between towers
        dx = new_tower.pos[0] - existing_tower.pos[0]
        dy = new_tower.pos[1] - existing_tower.pos[1]
        return (dx * dx + dy * dy) < (min_distance * min_distance)
    
    def start_next_wave(self):
        self.wave_number += 1
        self.wave_completed = False
        self.wave_manager.start_wave(self.path.points, self.config, self.wave_number)
    
    def update(self):
        if self.game_over or not self.game_started:
            return
            
        # Update wave manager
        new_enemies = self.wave_manager.update()
        self.enemies.extend(new_enemies)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.reached_end():
                self.lives -= 1
                self.enemies.remove(enemy)
            elif enemy.health <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)
        
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies)
        
        # Check if wave is completed
        if not self.wave_manager.wave_in_progress and len(self.enemies) == 0:
            self.wave_completed = True
            if self.wave_number >= self.max_waves:
                self.game_over = True
        
        # Check game over
        if self.lives <= 0:
            self.game_over = True
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if not self.game_started:
            self.draw_start_screen()
            return
        
        # Draw path
        self.path.draw(self.screen)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over or wave completion
        if self.game_over:
            self.draw_game_over()
        elif self.wave_completed:
            self.draw_wave_completion()
    
    def draw_ui(self):
        # Draw money
        money_text = self.font.render(f"Money: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))
        
        # Draw wave info
        wave_text = self.font.render(f"Wave: {self.wave_number}/{self.max_waves}", True, (255, 255, 255))
        self.screen.blit(wave_text, (10, 90))
        
        # Draw tower selection
        self.draw_tower_selection()
    
    def draw_wave_completion(self):
        if self.wave_number < self.max_waves:
            text = self.font.render("Wave Completed! Press SPACE for next wave", True, (255, 255, 255))
        else:
            text = self.font.render("Game Completed! You Win!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)
    
    def draw_game_over(self):
        text = self.font.render("Game Over!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)
    
    def draw_start_screen(self):
        # Title
        title = self.font.render("Tower Defense", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)
        
        # Difficulty
        diff_text = self.font.render(f"Difficulty: {self.difficulty:.1f}", True, (255, 255, 255))
        diff_rect = diff_text.get_rect(center=(400, 100))
        self.screen.blit(diff_text, diff_rect)
        
        # Enemy Information
        y = 150
        enemy_info = [
            ("Basic Enemy", "Normal speed and health", (255, 0, 0)),
            ("Fast Enemy", "50% faster, 30% less health", (255, 165, 0)),
            ("Tank Enemy", "50% slower, 100% more health", (128, 0, 128)),
            ("Boss Enemy", "50% slower, 200% more health", (255, 0, 255))
        ]
        
        for name, desc, color in enemy_info:
            # Enemy name
            name_text = self.small_font.render(name, True, color)
            self.screen.blit(name_text, (200, y))
            
            # Enemy description
            desc_text = self.small_font.render(desc, True, (200, 200, 200))
            self.screen.blit(desc_text, (400, y))
            
            y += 30
        
        # Tower Information
        y = 300
        tower_info = [
            ("Basic Tower", "Balanced tower", (0, 255, 0)),
            ("Sniper Tower", "Long range, high damage", (0, 0, 255)),
            ("Splash Tower", "Area damage", (255, 255, 0)),
            ("Laser Tower", "Continuous damage", (0, 255, 255))
        ]
        
        for name, desc, color in tower_info:
            # Tower name
            name_text = self.small_font.render(name, True, color)
            self.screen.blit(name_text, (200, y))
            
            # Tower description
            desc_text = self.small_font.render(desc, True, (200, 200, 200))
            self.screen.blit(desc_text, (400, y))
            
            y += 30
        
        # Instructions
        instructions = [
            "Use UP/DOWN arrows to change difficulty",
            "Press SPACE to start the game",
            "During the game:",
            "1-4 keys to select towers",
            "Click to place towers",
            "Complete all 3 waves to win!"
        ]
        
        y = 450
        for instruction in instructions:
            text = self.small_font.render(instruction, True, (200, 200, 200))
            text_rect = text.get_rect(center=(400, y))
            self.screen.blit(text, text_rect)
            y += 25
    
    def draw_tower_selection(self):
        y = 170
        tower_classes = [BasicTower, SniperTower, SplashTower, LaserTower]
        
        for i, tower_class in enumerate(tower_classes):
            unlocked = self.difficulty >= self.get_tower_unlock_difficulty(tower_class)
            color = (255, 255, 255) if tower_class == self.selected_tower_type else (150, 150, 150)
            if not unlocked:
                color = (100, 100, 100)
            
            # Create a temporary tower instance to get its properties
            temp_tower = tower_class((0, 0), self.config)
            text = f"{i+1}: {temp_tower.type.capitalize()} (${temp_tower.cost})"
            if not unlocked:
                text += " [Locked]"
            
            tower_text = self.small_font.render(text, True, color)
            self.screen.blit(tower_text, (10, y))
            y += 25 