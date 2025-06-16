import pygame
import random
from enemies import BasicEnemy, FastEnemy, TankEnemy, BossEnemy

class WaveManager:
    def __init__(self):
        self.wave_in_progress = False
        self.wave = 0
        self.enemies_per_wave = 10  # Base number of enemies
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.spawn_delay = 20  # Frames between spawns (instead of milliseconds)
        self.path_points = None
        self.config = None
    
    def start_wave(self, path_points, config, wave_number):
        self.wave = wave_number
        self.wave_in_progress = True
        self.enemies_spawned = 0
        self.spawn_timer = 0  # Reset timer when wave starts
        self.path_points = path_points
        self.config = config
        
        # Calculate number of enemies for this wave
        self.total_enemies = self.enemies_per_wave * wave_number
    
    def get_enemy_class(self, wave_number):
        # Enemy type probabilities based on wave number
        if wave_number == 1:
            # First wave: 80% basic, 20% fast
            return random.choices(
                [BasicEnemy, FastEnemy],
                weights=[0.8, 0.2]
            )[0]
        elif wave_number == 2:
            # Second wave: 50% basic, 30% fast, 20% tank
            return random.choices(
                [BasicEnemy, FastEnemy, TankEnemy],
                weights=[0.5, 0.3, 0.2]
            )[0]
        else:
            # Third wave: 30% basic, 20% fast, 30% tank, 20% boss
            return random.choices(
                [BasicEnemy, FastEnemy, TankEnemy, BossEnemy],
                weights=[0.3, 0.2, 0.3, 0.2]
            )[0]
    
    def update(self):
        if not self.wave_in_progress:
            return []
        
        new_enemies = []
        
        # Use frame-based timing instead of pygame timing
        if self.enemies_spawned < self.total_enemies:
            if self.spawn_timer <= 0:
                # Spawn enemy
                enemy_class = self.get_enemy_class(self.wave)
                new_enemies.append(enemy_class(self.path_points, self.config))
                self.enemies_spawned += 1
                self.spawn_timer = self.spawn_delay  # Reset timer
            else:
                self.spawn_timer -= 1  # Countdown each frame
        
        if self.enemies_spawned >= self.total_enemies:
            self.wave_in_progress = False
        
        return new_enemies 