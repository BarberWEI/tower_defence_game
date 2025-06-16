import numpy as np
from path import Path
from wave_manager import WaveManager
from config import GameConfig
from towers import BasicTower, SniperTower, SplashTower, LaserTower, FrostTower
from enemies import BasicEnemy, FastEnemy, TankEnemy, BossEnemy, SaboteurEnemy
import pygame

class GameAI:
    def __init__(self, difficulty=0.5):
        # Initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
        
        self.difficulty = difficulty
        self.config = GameConfig(self.difficulty)
        self.money = self.config.starting_money
        self.lives = self.config.starting_lives
        self.game_over = False
        self.game_started = False  # Add the missing game_started flag
        self.selected_tower_type = BasicTower
        self.wave_number = 0
        self.max_waves = 3
        self.wave_completed = True  # Start with first wave completed to allow starting
        self.towers = []
        self.enemies = []
        self.path = Path(self.difficulty)
        self.wave_manager = WaveManager()
        self.state_dim = 10
        self.action_dim = 6
        self.prev_enemy_count = 0
        self.prev_wave_completed = False
        
        # AI-specific timing (since pygame.time.get_ticks() doesn't work in headless mode)
        self.ai_time = 0
        self.time_step = 50  # Simulate 50ms per step

    def reset(self):
        self.money = self.config.starting_money
        self.lives = self.config.starting_lives
        self.game_over = False
        self.game_started = True  # Start the game immediately for AI
        self.selected_tower_type = BasicTower
        self.wave_number = 0
        self.wave_completed = True  # Allow starting first wave
        self.towers = []
        self.enemies = []
        self.path = Path(self.difficulty)
        self.wave_manager = WaveManager()
        self.prev_enemy_count = 0
        self.prev_wave_completed = False
        self.ai_time = 0
        return self.get_state()

    def start_next_wave(self):
        """Properly start next wave like the real game"""
        if self.wave_completed and self.wave_number < self.max_waves:
            self.wave_number += 1
            self.wave_completed = False
            self.wave_manager.start_wave(self.path.points, self.config, self.wave_number)
            return True
        return False

    def step(self, action):
        # Action: 0-4: place tower, 5: start wave
        reward = 0
        done = False
        info = {}
        
        if self.game_over:
            return self.get_state(), 0, True, info
            
        prev_enemy_count = len(self.enemies)
        prev_money = self.money
        prev_lives = self.lives
        prev_wave_completed = self.wave_completed
        
        # Execute action
        if action in range(5):  # Place tower
            tower_type = [BasicTower, SniperTower, SplashTower, LaserTower, FrostTower][action]
            # Use a more strategic position (not completely random)
            pos = (np.random.randint(100, 700), np.random.randint(100, 500))
            
            # Check if position is valid (not on path and affordable)
            if not self.path.is_point_on_path(pos):
                tower = tower_type(pos, self.config)
                if self.money >= tower.cost:
                    # Check if position overlaps with existing towers
                    if not any(self.check_tower_overlap(tower, existing_tower) for existing_tower in self.towers):
                        self.towers.append(tower)
                        self.money -= tower.cost
                        reward += 0.01  # Small reward for successful tower placement
                    else:
                        reward -= 0.01  # Penalty for invalid placement
                else:
                    reward -= 0.01  # Penalty for trying to place tower without money
            else:
                reward -= 0.01  # Penalty for trying to place tower on path
                
        elif action == 5:  # Start wave
            if self.start_next_wave():
                reward += 0.05  # Reward for starting a wave
            else:
                reward -= 0.01  # Penalty for trying to start wave when not possible
        
        # Update game state
        self.update()
        
        # Calculate rewards based on game state changes
        money_gained = self.money - prev_money
        if money_gained > 0:
            reward += money_gained * 0.01  # Reward for money gained from killing enemies
        
        lives_lost = prev_lives - self.lives
        if lives_lost > 0:
            reward -= lives_lost * 0.2  # Penalty for losing lives
        
        # Reward for completing waves
        if not prev_wave_completed and self.wave_completed:
            reward += 1.0  # Big reward for completing a wave
        
        # Check game end conditions
        if self.lives <= 0:
            done = True
            reward -= 1.0  # Big penalty for losing
        elif self.wave_completed and self.wave_number >= self.max_waves:
            done = True
            reward += 2.0  # Big reward for winning
            
        return self.get_state(), reward, done, info

    def check_tower_overlap(self, new_tower, existing_tower):
        """Check if towers overlap (same as real game)"""
        min_distance = 40
        dx = new_tower.pos[0] - existing_tower.pos[0]
        dy = new_tower.pos[1] - existing_tower.pos[1]
        return (dx * dx + dy * dy) < (min_distance * min_distance)

    def update(self):
        """Update game state (modified from real game to work without pygame loop)"""
        if self.game_over or not self.game_started:
            return
            
        # Advance AI time
        self.ai_time += self.time_step
        
        # Patch pygame.time.get_ticks() for WaveManager
        original_get_ticks = pygame.time.get_ticks
        pygame.time.get_ticks = lambda: self.ai_time
        
        try:
            # Update wave manager
            new_enemies = self.wave_manager.update()
            self.enemies.extend(new_enemies)
        finally:
            # Restore original get_ticks
            pygame.time.get_ticks = original_get_ticks
        
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
        if not self.wave_manager.wave_in_progress and len(self.enemies) == 0 and self.wave_number > 0:
            self.wave_completed = True
            if self.wave_number >= self.max_waves:
                self.game_over = True
        
        # Check game over
        if self.lives <= 0:
            self.game_over = True

    def get_state(self):
        # 10-dimensional state vector (improved)
        avg_enemy_health = np.mean([e.health for e in self.enemies]) if self.enemies else 0
        avg_enemy_dist = 0
        num_different_enemy_types = 0
        enemy_types = set()
        
        for e in self.enemies:
            if hasattr(e, 'type'):
                enemy_types.add(e.type)
            # Distance to end (simplified)
            if hasattr(e, 'path_index') and hasattr(e, 'path'):
                if e.path_index < len(e.path) - 1:
                    avg_enemy_dist += len(e.path) - e.path_index
        
        avg_enemy_dist = avg_enemy_dist / len(self.enemies) if self.enemies else 0
        num_different_enemy_types = len(enemy_types)
        
        # Count tower types
        tower_counts = {}
        for tower in self.towers:
            tower_type = getattr(tower, 'type', 'basic')
            tower_counts[tower_type] = tower_counts.get(tower_type, 0) + 1
        
        state = [
            self.money / 100.0,  # Normalize money
            self.lives / 20.0,   # Normalize lives
            self.wave_number / self.max_waves,  # Normalize wave
            len(self.towers) / 20.0,  # Normalize tower count
            len(self.enemies) / 30.0,  # Normalize enemy count
            avg_enemy_health / 100.0,  # Normalize health
            avg_enemy_dist / 50.0,  # Normalize distance
            num_different_enemy_types / 4.0,  # Normalize enemy type diversity
            tower_counts.get('basic', 0) / 10.0,  # Basic tower count
            1.0 if self.wave_completed else 0.0  # Wave completion status
        ]
        return np.array(state, dtype=np.float32) 