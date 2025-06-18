import pygame
import sys
from typing import List

from enemies import Enemy
from towers import Tower
from projectiles import Projectile
from game_systems import Map, WaveManager, UIManager, TowerManager

class Game:
    """Main game controller - coordinates between all game systems"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        self.money = 100
        self.lives = 20
        
        # Game objects
        self.enemies: List[Enemy] = []
        self.towers: List[Tower] = []
        self.projectiles: List[Projectile] = []
        
        # Initialize game systems
        self.map = Map(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.wave_manager = WaveManager(self.map.get_path())
        self.ui_manager = UIManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.tower_manager = TowerManager()
        
        # UI state
        self.show_wave_complete = False
        self.wave_complete_timer = 0
        self.wave_bonus = 0
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
    
    def handle_key_press(self, key):
        """Handle keyboard input"""
        if key == pygame.K_SPACE:
            self.paused = not self.paused
        
        elif key == pygame.K_ESCAPE:
            if self.game_over:
                self.running = False
            else:
                self.tower_manager.cancel_placement()
        
        elif key == pygame.K_r:
            if self.game_over:
                self.restart_game()
        
        elif key == pygame.K_1:
            self.tower_manager.select_tower_type("basic")
        
        elif key == pygame.K_2:
            self.tower_manager.select_tower_type("sniper")
        
        elif key == pygame.K_3:
            self.tower_manager.select_tower_type("freezer")
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        if self.tower_manager.placing_tower and not self.paused and not self.game_over:
            self.attempt_tower_placement(pos)
    
    def attempt_tower_placement(self, pos):
        """Try to place a tower at the given position"""
        success, tower, cost = self.tower_manager.attempt_tower_placement(
            pos, self.money, self.towers, self.map
        )
        
        if success and tower:
            self.towers.append(tower)
            self.money -= cost
    
    def update_enemies(self):
        """Update all enemies"""
        for enemy in self.enemies[:]:
            enemy.update()
            
            if enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
            
            elif enemy.health <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)
    
    def update_towers(self):
        """Update all towers"""
        for tower in self.towers:
            tower.update(self.enemies, self.projectiles)
    
    def update_projectiles(self):
        """Update all projectiles"""
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Check projectile collisions with enemies
            if hasattr(projectile, 'check_collision'):
                projectile.check_collision(self.enemies)
            
            # Handle homing projectiles
            if hasattr(projectile, 'update_homing'):
                projectile.update_homing(self.enemies)
            
            if projectile.should_remove:
                self.projectiles.remove(projectile)
    
    def update_waves(self):
        """Update wave management"""
        # Spawn new enemies
        new_enemy = self.wave_manager.spawn_enemy()
        if new_enemy:
            self.enemies.append(new_enemy)
        
        # Check for wave completion
        wave_info = self.wave_manager.update(self.enemies)
        if wave_info:
            self.money += wave_info['money_bonus']
            self.wave_bonus = wave_info['money_bonus']
            self.show_wave_complete = True
            self.wave_complete_timer = 180  # Show for 3 seconds
    
    def update_ui_state(self):
        """Update UI-related timers and state"""
        if self.show_wave_complete:
            self.wave_complete_timer -= 1
            if self.wave_complete_timer <= 0:
                self.show_wave_complete = False
    
    def update(self):
        """Update all game systems"""
        if self.paused or self.game_over:
            return
        
        self.update_enemies()
        self.update_towers()
        self.update_projectiles()
        self.update_waves()
        self.update_ui_state()
    
    def draw_game_objects(self):
        """Draw all game objects"""
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
    
    def get_game_state(self) -> dict:
        """Get current game state for UI rendering"""
        wave_info = self.wave_manager.get_wave_info()
        placement_state = self.tower_manager.get_placement_state()
        
        return {
            'money': self.money,
            'lives': self.lives,
            'wave_info': wave_info,
            'paused': self.paused,
            'game_over': self.game_over,
            'selected_tower': placement_state['selected_tower_type'],
            'show_wave_complete': self.show_wave_complete,
            'wave_bonus': self.wave_bonus
        }
    
    def draw(self):
        """Draw everything"""
        # Draw map (includes background and path)
        mouse_pos = pygame.mouse.get_pos()
        self.map.draw(
            self.screen, 
            self.tower_manager.placing_tower, 
            mouse_pos, 
            self.towers,
            self.tower_manager.selected_tower_type
        )
        
        # Draw game objects
        self.draw_game_objects()
        
        # Draw UI
        game_state = self.get_game_state()
        self.ui_manager.draw_complete_ui(self.screen, game_state)
        
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game"""
        self.game_over = False
        self.paused = False
        self.money = 100
        self.lives = 20
        
        # Clear game objects
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        
        # Reset systems
        self.wave_manager = WaveManager(self.map.get_path())
        self.tower_manager = TowerManager()
        
        # Reset UI state
        self.show_wave_complete = False
        self.wave_complete_timer = 0
        self.wave_bonus = 0
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 