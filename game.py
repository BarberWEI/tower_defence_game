import pygame
import sys
from typing import List

from enemies import Enemy
from towers import Tower
from projectiles import Projectile
from game_systems import Map, WaveManager, UIManager, TowerManager
from game_systems.tower_upgrade_system import TowerUpgradeSystem
from game_systems.upgrade_ui import UpgradeUI

class Game:
    """Main game controller - coordinates between all game systems"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup with fullscreen support
        self.fullscreen = False
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        
        # Get display info for fullscreen
        info = pygame.display.Info()
        self.fullscreen_width = info.current_w
        self.fullscreen_height = info.current_h
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        self.money = 20
        self.lives = 20
        
        # Game objects
        self.enemies: List[Enemy] = []
        self.towers: List[Tower] = []
        self.projectiles: List[Projectile] = []
        
        # Initialize game systems
        self.map = Map(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.wave_manager = WaveManager(self.map.get_path())
        self.tower_manager = TowerManager()
        self.ui_manager = UIManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.tower_manager)
        self.upgrade_system = TowerUpgradeSystem()
        self.upgrade_ui = UpgradeUI(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
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
                elif event.button == 4:  # Mouse wheel up
                    self.ui_manager.handle_scroll(-1)
                elif event.button == 5:  # Mouse wheel down
                    self.ui_manager.handle_scroll(1)
            
            elif event.type == pygame.MOUSEWHEEL:
                # Handle newer pygame wheel events
                self.ui_manager.handle_scroll(event.y)
            
            elif event.type == pygame.MOUSEMOTION:
                # Update mouse position for UI hover effects
                self.ui_manager.update_mouse_pos(event.pos)
                self.upgrade_ui.update_mouse_pos(event.pos)
    
    def handle_key_press(self, key):
        """Handle keyboard input - only essential keys"""
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
        
        elif key == pygame.K_F1:
            self.toggle_fullscreen()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            # Switch to fullscreen
            self.screen = pygame.display.set_mode((self.fullscreen_width, self.fullscreen_height), pygame.FULLSCREEN)
            # Update screen dimensions for game systems
            old_width, old_height = self.SCREEN_WIDTH, self.SCREEN_HEIGHT
            self.SCREEN_WIDTH = self.fullscreen_width
            self.SCREEN_HEIGHT = self.fullscreen_height
        else:
            # Switch to windowed
            self.screen = pygame.display.set_mode((1200, 800))
            # Restore original dimensions
            self.SCREEN_WIDTH = 1200
            self.SCREEN_HEIGHT = 800
        
        # Reinitialize systems with new screen dimensions
        self.map = Map(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ui_manager = UIManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.tower_manager)
        self.upgrade_ui = UpgradeUI(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Update wave manager with new path
        self.wave_manager = WaveManager(self.map.get_path())
    

    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        if self.paused or self.game_over:
            return
        
        # Check for upgrade UI clicks first (highest priority)
        if self.upgrade_ui.handle_click(pos, self.upgrade_system):
            return
        
        # Check for tower bar clicks
        clicked_tower_index = self.ui_manager.handle_tower_bar_click(pos)
        if clicked_tower_index is not None:
            tower_type = self.ui_manager.get_selected_tower_type()
            if tower_type:
                self.tower_manager.select_tower_type(tower_type)
            return
        
        # Check for tower clicks (for upgrade panel)
        if self.ui_manager.handle_tower_click(pos, self.towers):
            # Set the selected tower for upgrades
            selected_tower = self.ui_manager.selected_placed_tower
            self.upgrade_ui.set_selected_tower(selected_tower)
            return
        else:
            # Clear upgrade selection if clicking elsewhere
            self.upgrade_ui.clear_selection()
        
        # Handle tower placement
        if self.tower_manager.placing_tower:
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
        enemies_to_add = []
        
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Handle poison effects
            if hasattr(enemy, 'poison_timer') and enemy.poison_timer > 0:
                enemy.poison_timer -= 1
                if hasattr(enemy, 'poison_damage_timer'):
                    enemy.poison_damage_timer += 1
                    if enemy.poison_damage_timer >= 60:  # Every second
                        enemy.take_damage(enemy.poison_damage)
                        enemy.poison_damage_timer = 0
            
            if enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
            
            elif enemy.health <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)
                
                # Handle splitting enemies
                if hasattr(enemy, 'on_death'):
                    spawned_enemies = enemy.on_death()
                    if spawned_enemies:
                        enemies_to_add.extend(spawned_enemies)
                        
                # Handle boss minion spawning
                if hasattr(enemy, 'should_spawn_minions') and enemy.should_spawn_minions():
                    minion_count = enemy.get_minion_count()
                    for i in range(minion_count):
                        from enemies import BasicEnemy
                        minion = BasicEnemy(self.map.get_path())
                        minion.x = enemy.x + (i - minion_count/2) * 30
                        minion.y = enemy.y
                        enemies_to_add.append(minion)
        
        # Add any new enemies from splitting or boss abilities
        self.enemies.extend(enemies_to_add)
    
    def update_towers(self):
        """Update all towers"""
        for tower in self.towers:
            tower.update(self.enemies, self.projectiles)
    
    def update_projectiles(self):
        """Update all projectiles"""
        for projectile in self.projectiles[:]:
            # Handle different projectile update methods
            if hasattr(projectile, 'update') and callable(getattr(projectile, 'update')):
                if hasattr(projectile, 'update_homing'):
                    projectile.update_homing(self.enemies)
                elif hasattr(projectile.__class__, 'update') and len(projectile.update.__code__.co_varnames) > 1:
                    # Missile projectiles need enemies parameter
                    projectile.update(self.enemies)
                else:
                    projectile.update()
            
            # Check projectile collisions with enemies
            if hasattr(projectile, 'check_collision'):
                collision_result = projectile.check_collision(self.enemies)
                
                # Handle damage tracking for currency generation
                if isinstance(collision_result, dict) and collision_result.get('hit'):
                    damage_dealt = collision_result.get('damage', 0)
                    tower_id = collision_result.get('tower_id')
                    
                    # Ensure damage_dealt is not None and is a number
                    if damage_dealt is None:
                        damage_dealt = 0
                    
                    if tower_id and damage_dealt > 0:
                        # Find the tower and add currency
                        tower = self._find_tower_by_id(tower_id)
                        if tower:
                            tower.add_damage_dealt(damage_dealt)
                            # Add currency based on damage dealt (higher damage towers get more)
                            currency_amount = max(1, damage_dealt // 2)
                            self.upgrade_system.add_tower_currency(tower_id, tower.tower_type, currency_amount)
            
            if hasattr(projectile, 'should_remove') and projectile.should_remove:
                self.projectiles.remove(projectile)
    
    def _find_tower_by_id(self, tower_id: str):
        """Find a tower by its unique ID"""
        for tower in self.towers:
            if hasattr(tower, 'tower_id') and tower.tower_id == tower_id:
                return tower
        return None
    
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
        
        # Draw towers with selection state
        selected_tower = self.ui_manager.selected_placed_tower
        for tower in self.towers:
            is_selected = (tower == selected_tower)
            tower.draw(self.screen, selected=is_selected)
        
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
            'wave_bonus': self.wave_bonus,
            'towers': self.towers
        }
    
    def draw(self):
        """Draw everything"""
        # Fill entire screen with black background layer
        self.screen.fill((0, 0, 0))
        
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
        
        # Draw upgrade UI
        self.upgrade_ui.draw_upgrade_panel(self.screen, self.upgrade_system)
        
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game"""
        self.game_over = False
        self.paused = False
        self.money = 20
        self.lives = 20
        
        # Clear game objects
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        
        # Reset systems
        self.wave_manager = WaveManager(self.map.get_path())
        self.tower_manager = TowerManager()
        self.upgrade_system = TowerUpgradeSystem()
        
        # Reset UI state
        self.show_wave_complete = False
        self.wave_complete_timer = 0
        self.wave_bonus = 0
        self.ui_manager.clear_tower_selection()
        self.ui_manager.selected_placed_tower = None
        self.upgrade_ui.clear_selection()
    
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