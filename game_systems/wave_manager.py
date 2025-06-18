from typing import List, Tuple
from enemies import (BasicEnemy, FastEnemy, TankEnemy, ShieldedEnemy,
                    InvisibleEnemy, FlyingEnemy, RegeneratingEnemy, 
                    SplittingEnemy, TeleportingEnemy, MegaBoss, SpeedBoss)

class WaveManager:
    """Manages enemy waves and spawning"""
    
    def __init__(self, path: List[Tuple[int, int]]):
        self.path = path
        self.wave_number = 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 10
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between enemy spawns
        self.wave_complete = False
        
        # Wave configuration with boss waves
        self.wave_configs = {
            # Wave ranges and their enemy compositions
            (1, 2): [(BasicEnemy, 1.0)],  # Waves 1-2: Only basic enemies
            (3, 4): [(BasicEnemy, 0.7), (FastEnemy, 0.3)],  # Waves 3-4: Basic + Fast
            (5, 6): [(BasicEnemy, 0.5), (FastEnemy, 0.3), (TankEnemy, 0.2)],  # Basic mix
            (7, 8): [(BasicEnemy, 0.4), (FastEnemy, 0.2), (TankEnemy, 0.2), (InvisibleEnemy, 0.2)],  # Add invisible
            (9, 10): [(BasicEnemy, 0.3), (FastEnemy, 0.2), (TankEnemy, 0.2), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15)],  # Add flying
            (11, 12): [(BasicEnemy, 0.25), (FastEnemy, 0.15), (TankEnemy, 0.2), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15), (ShieldedEnemy, 0.1)],  # Add shielded
            (13, 14): [(BasicEnemy, 0.2), (FastEnemy, 0.15), (TankEnemy, 0.15), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15), (ShieldedEnemy, 0.1), (RegeneratingEnemy, 0.1)],  # Add regenerating
            (15, 16): [(BasicEnemy, 0.15), (FastEnemy, 0.15), (TankEnemy, 0.15), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15), (ShieldedEnemy, 0.1), (RegeneratingEnemy, 0.1), (TeleportingEnemy, 0.05)],  # Add teleporting
            (17, 19): [(BasicEnemy, 0.15), (FastEnemy, 0.15), (TankEnemy, 0.1), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15), (ShieldedEnemy, 0.1), (RegeneratingEnemy, 0.1), (TeleportingEnemy, 0.05), (SplittingEnemy, 0.05)],  # Add splitting
            (20, float('inf')): [(BasicEnemy, 0.1), (FastEnemy, 0.1), (TankEnemy, 0.1), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15), (ShieldedEnemy, 0.1), (RegeneratingEnemy, 0.1), (TeleportingEnemy, 0.1), (SplittingEnemy, 0.1)]  # All enemies
        }
        
        # Special boss waves
        self.boss_waves = {
            10: SpeedBoss,
            20: MegaBoss,
            30: MegaBoss,  # Mega boss returns
            40: SpeedBoss,  # Speed boss returns stronger
            50: MegaBoss   # Final mega boss
        }
    
    def get_enemy_type_for_wave(self) -> type:
        """Determine which enemy type to spawn based on current wave"""
        import random
        
        # Check for boss waves first
        if self.wave_number in self.boss_waves:
            return self.boss_waves[self.wave_number]
        
        # Find the appropriate wave configuration
        for (min_wave, max_wave), enemy_types in self.wave_configs.items():
            if min_wave <= self.wave_number <= max_wave:
                # Use weighted random selection
                rand = random.random()
                cumulative_weight = 0
                
                for enemy_class, weight in enemy_types:
                    cumulative_weight += weight
                    if rand <= cumulative_weight:
                        return enemy_class
        
        # Fallback to basic enemy
        return BasicEnemy
    
    def should_spawn_enemy(self) -> bool:
        """Check if it's time to spawn a new enemy"""
        if self.enemies_spawned >= self.enemies_per_wave:
            return False
        
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            return True
        
        return False
    
    def spawn_enemy(self) -> object:
        """Spawn and return a new enemy"""
        if not self.should_spawn_enemy():
            return None
        
        enemy_class = self.get_enemy_type_for_wave()
        enemy = enemy_class(self.path)
        self.enemies_spawned += 1
        
        return enemy
    
    def is_wave_complete(self, active_enemies: List) -> bool:
        """Check if the current wave is complete"""
        return (self.enemies_spawned >= self.enemies_per_wave and 
                len(active_enemies) == 0)
    
    def start_next_wave(self) -> dict:
        """Start the next wave and return wave info"""
        if self.is_wave_complete([]):  # Empty list since we're just starting
            self.wave_number += 1
            self.enemies_spawned = 0
            
            # Boss waves have different enemy counts
            if self.wave_number in self.boss_waves:
                self.enemies_per_wave = 1  # Only one boss
            else:
                self.enemies_per_wave += 2  # Increase difficulty for normal waves
            
            # Adjust spawn delay based on wave (faster spawning in later waves)
            if self.wave_number % 5 == 0:
                self.spawn_delay = max(30, self.spawn_delay - 5)
            
            # Boss waves give bigger money bonus
            money_bonus = 100 if self.wave_number in self.boss_waves else 50
            
            return {
                'wave_number': self.wave_number,
                'money_bonus': money_bonus,
                'enemies_per_wave': self.enemies_per_wave
            }
        
        return None
    
    def get_wave_info(self) -> dict:
        """Get current wave information"""
        return {
            'wave_number': self.wave_number,
            'enemies_spawned': self.enemies_spawned,
            'enemies_per_wave': self.enemies_per_wave,
            'progress': self.enemies_spawned / self.enemies_per_wave
        }
    
    def update(self, active_enemies: List) -> dict:
        """Update wave manager and return any wave completion info"""
        # Check if wave is complete
        if self.is_wave_complete(active_enemies):
            return self.start_next_wave()
        
        return None 