import pygame
from enemy import Enemy

class WaveManager:
    def __init__(self):
        self.wave = 0
        self.enemies_per_wave = 5
        self.enemies_spawned = 0
        self.spawn_delay = 60  # frames between spawns
        self.spawn_timer = 0
        self.wave_in_progress = False
        self.path = None  # Will be set by Game class
    
    def start_wave(self, path):
        self.wave += 1
        self.enemies_spawned = 0
        self.wave_in_progress = True
        self.path = path
    
    def update(self):
        if not self.wave_in_progress:
            return []
        
        new_enemies = []
        
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        elif self.enemies_spawned < self.enemies_per_wave:
            new_enemies.append(Enemy(self.path))
            self.enemies_spawned += 1
            self.spawn_timer = self.spawn_delay
        
        if self.enemies_spawned >= self.enemies_per_wave:
            self.wave_in_progress = False
        
        return new_enemies 