import pygame
from tower import Tower
from enemy import Enemy
from path import Path
from wave_manager import WaveManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tower Defense")
        
        # Game state
        self.money = 100
        self.lives = 20
        self.game_over = False
        
        # Game objects
        self.towers = []
        self.enemies = []
        self.path = Path()
        self.wave_manager = WaveManager()
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_tower_placement(event.pos)
    
    def handle_tower_placement(self, pos):
        if self.money >= 50:  # Tower cost
            self.towers.append(Tower(pos))
            self.money -= 50
    
    def update(self):
        if self.game_over:
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
        
        # Check game over
        if self.lives <= 0:
            self.game_over = True
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
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
    
    def draw_ui(self):
        # Draw money
        money_text = self.font.render(f"Money: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))
        
        # Draw game over
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(400, 300))
            self.screen.blit(game_over_text, text_rect) 