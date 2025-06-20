import pygame
import sys
from typing import List
import random

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
        
        # Load game configuration
        from config.game_config import get_game_config
        self.game_config = get_game_config()

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
        
        # Game state using config values
        self.running = True
        self.paused = False
        self.game_over = False
        self.victory = False
        self.money = self.game_config.get('starting_money', 20)
        self.lives = self.game_config.get('starting_lives', 20)
        
        # Speed control
        self.game_speed = 1  # 1 = normal speed, 2 = double speed
        self.speed_options = [1, 2]  # Available speed options
        self.current_speed_index = 0  # Index in speed_options
        
        # Victory/Game Over state
        self.show_victory_screen = False
        self.show_game_over_screen = False
        self.restart_requested = False
        
        # Wave completion tracking
        self.completed_wave_number = 0  # Track which wave was just completed
        
        # Performance monitoring
        self.fps_counter = 0
        self.fps_timer = 0
        self.current_fps = 60
        self.frame_time_samples = []
        self.max_frame_time_samples = 60  # Track last 60 frames
        
        # Game objects
        self.enemies: List[Enemy] = []
        self.towers: List[Tower] = []
        self.projectiles: List[Projectile] = []
        
        # Initialize game systems
        self.map = Map(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.wave_manager = WaveManager(self.map.get_path())
        self.tower_manager = TowerManager()
        # Initialize tower costs for wave 1
        self.tower_manager.set_current_wave(1)
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
            if self.game_over or self.victory:
                self.running = False
            else:
                self.tower_manager.cancel_placement()
        
        elif key == pygame.K_r:
            if self.game_over or self.victory:
                self.restart_requested = True
        
        elif key == pygame.K_F1:
            self.toggle_fullscreen()
        
        elif key == pygame.K_TAB:
            self.toggle_game_speed()
    
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
    
    def toggle_game_speed(self):
        """Toggle between different game speeds"""
        self.current_speed_index = (self.current_speed_index + 1) % len(self.speed_options)
        self.game_speed = self.speed_options[self.current_speed_index]
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        # Handle restart button clicks for victory/game over screens
        if self.game_over or self.victory:
            restart_clicked = self.handle_restart_button_click(pos)
            if restart_clicked:
                self.restart_requested = True
            return
        
        if self.paused:
            return
        
        # Check for upgrade UI clicks first (highest priority)
        click_result = self.upgrade_ui.handle_click(pos, self.upgrade_system)
        if click_result['action'] == 'remove_tower':
            self.remove_tower(click_result['tower'])
            return
        elif click_result['action'] == 'upgrade':
            return
        
        # Check for speed button click
        if self.ui_manager.handle_speed_button_click(pos):
            self.toggle_game_speed()
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
    
    def handle_restart_button_click(self, mouse_pos) -> bool:
        """Check if restart button was clicked"""
        # Victory/Game Over screen restart button (center of screen)
        if self.show_victory_screen or self.show_game_over_screen or self.game_over or self.victory:
            # These coordinates MUST match the UI renderer exactly
            button_width = 200
            button_height = 50
            
            if self.victory or self.show_victory_screen:
                # Victory screen button position
                panel_height = 300
                panel_y = (self.SCREEN_HEIGHT - panel_height) // 2
                button_x = (self.SCREEN_WIDTH - button_width) // 2
                button_y = panel_y + 200
            else:
                # Game over screen button position
                panel_height = 250
                panel_y = (self.SCREEN_HEIGHT - panel_height) // 2
                button_x = (self.SCREEN_WIDTH - button_width) // 2
                button_y = panel_y + 170
            
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height):
                return True
        
        return False
    
    def attempt_tower_placement(self, pos):
        """Try to place a tower at the given position"""
        success, tower, cost = self.tower_manager.attempt_tower_placement(
            pos, self.money, self.towers, self.map
        )
        
        if success and tower:
            # Set upgrade system reference for currency generation
            tower.set_upgrade_system_reference(self.upgrade_system)
            self.towers.append(tower)
            self.money -= cost
    
    def remove_tower(self, tower):
        """Remove a tower and refund 50% of its cost"""
        if tower not in self.towers:
            return
        
        # Calculate refund (50% of current tower cost)
        tower_type = tower.tower_type
        current_cost = self.tower_manager.get_tower_cost(tower_type)
        refund = int(current_cost * 0.5)
        
        # Remove tower from list
        self.towers.remove(tower)
        
        # Give refund to player
        self.money += refund
        
        # Decrease tower count for dynamic pricing
        if tower_type in self.tower_manager.towers_built_count:
            self.tower_manager.towers_built_count[tower_type] = max(0, 
                self.tower_manager.towers_built_count[tower_type] - 1)
        
        # Clear upgrade UI selection
        self.upgrade_ui.clear_selection()
    
    def update_enemies(self):
        """Update all enemies"""
        enemies_to_add = []
        
        for enemy in self.enemies[:]:
            # Pass game speed to enemy update for faster movement
            if hasattr(enemy, 'update_with_speed'):
                enemy.update_with_speed(self.game_speed)
            else:
                enemy.update()
            
            # Handle poison effects (adjust timer based on speed)
            if hasattr(enemy, 'poison_timer') and enemy.poison_timer > 0:
                enemy.poison_timer -= self.game_speed
                if hasattr(enemy, 'poison_damage_timer'):
                    enemy.poison_damage_timer += self.game_speed
                    if enemy.poison_damage_timer >= 60:  # Every second
                        enemy.take_damage(enemy.poison_damage)
                        enemy.poison_damage_timer = 0
            
            # Handle boss minion spawning (while boss is alive)
            if hasattr(enemy, 'should_spawn_minions') and enemy.should_spawn_minions():
                minion_count = enemy.get_minion_count()
                for i in range(minion_count):
                    from enemies import BasicEnemy
                    minion = BasicEnemy(self.map.get_path())
                    minion.x = enemy.x + (i - minion_count/2) * 30
                    minion.y = enemy.y
                    # Set map reference for terrain effects
                    minion.set_map_reference(self.map)
                    enemies_to_add.append(minion)
            
            # Handle TimeLord Boss echo spawning
            if hasattr(enemy, 'should_spawn_echoes'):
                spawnable_rifts = enemy.should_spawn_echoes()
                for rift in spawnable_rifts:
                    from enemies import BasicEnemy
                    echo = BasicEnemy(self.map.get_path())
                    echo.x = rift['x']
                    echo.y = rift['y']
                    echo.health = echo.health * 0.5  # Echo enemies are weaker
                    echo.color = (150, 0, 255)  # Purple tint for echoes
                    echo.set_map_reference(self.map)
                    enemies_to_add.append(echo)
            
            # Handle Necromancer Boss undead summoning
            if hasattr(enemy, 'should_summon_undead') and enemy.should_summon_undead():
                from enemies import BasicEnemy
                undead = BasicEnemy(self.map.get_path())
                undead.x = enemy.x + random.uniform(-60, 60)
                undead.y = enemy.y + random.uniform(-60, 60)
                undead.color = (100, 100, 50)  # Sickly green for undead
                undead.health = undead.health * 0.7  # Undead are somewhat weaker
                undead.set_map_reference(self.map)
                enemies_to_add.append(undead)
            
            # Handle enemy death and removal
            if enemy.health <= 0:
                # Register dead enemy with Necromancer bosses for resurrection
                for boss in self.enemies:
                    if hasattr(boss, 'register_dead_enemy'):
                        boss.register_dead_enemy(type(enemy).__name__, enemy.x, enemy.y)
                
                # Check if enemy reached end or was killed
                if not enemy.reached_end:
                    # Enemy was killed - award money
                    self.money += enemy.reward
                else:
                    # Enemy reached end - lose lives
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                        self.show_game_over_screen = True
                
                self.enemies.remove(enemy)
            elif enemy.reached_end:
                # Enemy reached the end
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    self.show_game_over_screen = True
                self.enemies.remove(enemy)
        
        # Add any spawned enemies
        self.enemies.extend(enemies_to_add)
    
    def update_towers(self):
        """Update all towers"""
        # First, clear all detection flags before detector towers update them
        for enemy in self.enemies:
            if hasattr(enemy, 'detected_by_detector'):
                enemy.detected_by_detector = False
        
        # Separate towers by type to ensure detector towers update first
        detector_towers = [tower for tower in self.towers if tower.tower_type == 'detector']
        other_towers = [tower for tower in self.towers if tower.tower_type != 'detector']
        

        # Update detector towers first
        for tower in detector_towers:
            # Track damage before update
            previous_damage = tower.total_damage_dealt
            
            # Pass game speed to tower update for faster firing with optimizations
            if hasattr(tower, 'update_with_speed_optimized'):
                tower.update_with_speed_optimized(self.enemies, self.projectiles, self.game_speed)
            elif hasattr(tower, 'update_with_speed'):
                tower.update_with_speed(self.enemies, self.projectiles, self.game_speed)
            else:
                tower.update(self.enemies, self.projectiles)
            
            # Check if tower dealt damage directly (not through projectiles)
            damage_this_frame = tower.total_damage_dealt - previous_damage
            if damage_this_frame > 0:
                # Use centralized currency generation (already includes 5/100 nerf)
                tower.track_damage_and_generate_currency(damage_this_frame)
        
        # Then update other towers (they can now see detected enemies)
        for tower in other_towers:
            # Track damage before update
            previous_damage = tower.total_damage_dealt
            
            # Pass game speed to tower update for faster firing with optimizations
            if hasattr(tower, 'update_with_speed_optimized'):
                tower.update_with_speed_optimized(self.enemies, self.projectiles, self.game_speed)
            elif hasattr(tower, 'update_with_speed'):
                tower.update_with_speed(self.enemies, self.projectiles, self.game_speed)
            else:
                tower.update(self.enemies, self.projectiles)
            
            # Check if tower dealt damage directly (not through projectiles)
            damage_this_frame = tower.total_damage_dealt - previous_damage
            if damage_this_frame > 0:
                # Use centralized currency generation (already includes 5/100 nerf)
                tower.track_damage_and_generate_currency(damage_this_frame)
    
    def update_projectiles(self):
        """Update all projectiles"""
        for projectile in self.projectiles[:]:
            # Handle different projectile update methods with speed
            if hasattr(projectile, 'update') and callable(getattr(projectile, 'update')):
                if hasattr(projectile, 'update_homing'):
                    if hasattr(projectile, 'update_homing_with_speed'):
                        projectile.update_homing_with_speed(self.enemies, self.game_speed)
                    else:
                        projectile.update_homing(self.enemies)
                elif hasattr(projectile.__class__, 'update') and len(projectile.update.__code__.co_varnames) > 1:
                    # Missile projectiles need enemies parameter
                    if hasattr(projectile, 'update_with_speed'):
                        projectile.update_with_speed(self.enemies, self.game_speed)
                    else:
                        projectile.update(self.enemies)
                else:
                    if hasattr(projectile, 'update_with_speed'):
                        projectile.update_with_speed(self.game_speed)
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
                    
                    if tower_id:
                        # Find the tower and use centralized currency generation
                        tower = self._find_tower_by_id(tower_id)
                        if tower:
                            if damage_dealt > 0:
                                # Use centralized damage tracking and currency generation
                                tower.track_damage_and_generate_currency(damage_dealt)
                            else:
                                # Support towers get minimal currency for successful hits
                                tower.track_utility_hit()
            
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
        # Spawn new enemies (adjusted for speed)
        new_enemy = self.wave_manager.spawn_enemy(self.game_speed)
        if new_enemy:
            # Set map reference for terrain effects
            new_enemy.set_map_reference(self.map)
            self.enemies.append(new_enemy)
        
        # Check for wave completion
        wave_info = self.wave_manager.update(self.enemies)
        if wave_info:
            if wave_info.get('game_completed', False):
                # Player has beaten the final wave!
                self.victory = True
                self.show_victory_screen = True
            elif wave_info.get('wave_completed', False):
                # Normal wave completion - store the completed wave number BEFORE incrementing
                self.completed_wave_number = wave_info['wave_number']
                self.money += wave_info['money_bonus']
                self.wave_bonus = wave_info['money_bonus']
                self.show_wave_complete = True
                self.wave_complete_timer = 180  # Show for 3 seconds
                
                # Start next wave after a delay
                if not wave_info.get('is_final_wave', False):
                    next_wave_info = self.wave_manager.start_next_wave()
                    if next_wave_info:
                        # Update tower costs for the new wave
                        current_wave = next_wave_info.get('wave_number', 1)
                        self.tower_manager.set_current_wave(current_wave)
    
    def update_ui_state(self):
        """Update UI-related timers and state"""
        if self.show_wave_complete:
            self.wave_complete_timer -= self.game_speed
            if self.wave_complete_timer <= 0:
                self.show_wave_complete = False
    
    def update(self):
        """Update all game systems - FIXED: No longer runs multiple times per frame"""
        # Handle restart request
        if self.restart_requested:
            self.restart_game()
            return
        
        # Don't update if game is over or won
        if self.paused or self.game_over or self.victory:
            return
        
        # Single update pass - entities handle speed internally
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
            'victory': self.victory,
            'show_victory_screen': self.show_victory_screen,
            'show_game_over_screen': self.show_game_over_screen,
            'selected_tower': placement_state['selected_tower_type'],
            'show_wave_complete': self.show_wave_complete,
            'completed_wave_number': self.completed_wave_number,
            'wave_bonus': self.wave_bonus,
            'towers': self.towers,
            'game_speed': self.game_speed,
            'performance': self.get_performance_info()
        }
    
    def update_performance_metrics(self):
        """Update performance tracking metrics"""
        import time
        current_time = time.time()
        
        # Calculate frame time
        if hasattr(self, '_last_frame_time'):
            frame_time = current_time - self._last_frame_time
            self.frame_time_samples.append(frame_time)
            
            # Keep only recent samples
            if len(self.frame_time_samples) > self.max_frame_time_samples:
                self.frame_time_samples.pop(0)
        
        self._last_frame_time = current_time
        
        # Update FPS counter
        self.fps_counter += 1
        self.fps_timer += 1
        
        # Calculate FPS every second
        if self.fps_timer >= 60:  # 60 frames at 60 FPS = 1 second
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_timer = 0
    
    def get_performance_info(self) -> dict:
        """Get performance information for display"""
        avg_frame_time = 0
        if self.frame_time_samples:
            avg_frame_time = sum(self.frame_time_samples) / len(self.frame_time_samples)
        
        return {
            'fps': self.current_fps,
            'avg_frame_time_ms': avg_frame_time * 1000,  # Convert to milliseconds
            'entity_counts': {
                'enemies': len(self.enemies),
                'towers': len(self.towers),
                'projectiles': len(self.projectiles)
            }
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
        
        # Draw enemy introductions (should be on top of everything)
        self.wave_manager.draw_introduction(self.screen)
        
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game to initial state - COMPLETE RESET"""
        
        # Reset core game state
        self.game_over = False
        self.victory = False
        self.paused = False
        self.money = self.game_config.get('starting_money', 20)  # Reset to config amount
        self.lives = self.game_config.get('starting_lives', 20)  # Reset to config amount
        
        # Reset game speed to normal
        self.game_speed = 1
        self.current_speed_index = 0
        
        # Reset UI state completely
        self.show_victory_screen = False
        self.show_game_over_screen = False
        self.show_wave_complete = False
        self.restart_requested = False
        self.completed_wave_number = 0
        self.wave_bonus = 0
        self.wave_complete_timer = 0
        
        # Clear all game objects
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        
        # Reset all managers to initial state
        self.wave_manager = WaveManager(self.map.get_path())
        self.wave_manager.reset_introductions()  # Reset enemy introductions
        
        self.tower_manager = TowerManager()
        self.tower_manager.set_current_wave(1)  # Reset to wave 1 costs
        self.tower_manager.reset_ui_state()     # Reset tower placement UI state
        
        # Reset upgrade system
        self.upgrade_system = TowerUpgradeSystem()
        
        # Recreate UI manager with new tower manager reference
        self.ui_manager = UIManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.tower_manager)
        self.upgrade_ui.reset_ui_state()        # Reset upgrade panel completely
        
        # Reset performance tracking
        self.fps_counter = 0
        self.fps_timer = 0
        self.current_fps = 60
        self.frame_time_samples.clear()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.update_performance_metrics()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 