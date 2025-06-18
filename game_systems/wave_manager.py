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
        self.enemies_per_wave = 8
        self.spawn_timer = 0
        self.spawn_delay = 90
        self.wave_complete = False
        
        # Spawning configuration - easily adjustable difficulty settings
        self.spawn_config = {
            'base_spawn_delay': 90,          # Starting spawn delay in frames
            'min_spawn_delay': 15,           # Minimum spawn delay (maximum speed)
            'base_enemy_count': 8,           # Starting number of enemies per wave
            'boss_enemy_count': 1,           # Number of enemies in boss waves
        }
        
        # Per-round adjustment configuration - INCREASED DIFFICULTY!
        self.round_progression = {
            # How many enemies to add each round - INCREASED
            'enemy_increase_per_round': {
                'default': 3,                    # Default increase per round (+1 from 2)
                'wave_ranges': {
                    (1, 5): 2,                   # Waves 1-5: +2 enemy per round (+1 from 1)
                    (6, 10): 3,                  # Waves 6-10: +3 enemies per round (+1 from 2)
                    (11, 15): 4,                 # Waves 11-15: +4 enemies per round (+1 from 3)
                    (16, 20): 6,                 # Waves 16-20: +6 enemies per round (+2 from 4)
                    (21, 30): 8,                 # Waves 21-30: +8 enemies per round (+3 from 5)
                    (31, 99): 10,                # Waves 31+: +10 enemies per round (+4 from 6)
                }
            },
            
            # How much to reduce spawn delay each round (making spawning faster) - INCREASED
            'spawn_delay_reduction_per_round': {
                'default': 4,                    # Default reduction per round (+1 from 3)
                'wave_ranges': {
                    (1, 3): 3,                   # Waves 1-3: -3 frames per round (+1 from 2)
                    (4, 8): 4,                   # Waves 4-8: -4 frames per round (+1 from 3)
                    (9, 15): 5,                  # Waves 9-15: -5 frames per round (+1 from 4)
                    (16, 25): 7,                 # Waves 16-25: -7 frames per round (+2 from 5)
                    (26, 99): 9,                 # Waves 26+: -9 frames per round (+3 from 6)
                }
            },
            
            # Special round multipliers (for extra difficulty spikes)
            'special_rounds': {
                5: {'enemy_multiplier': 1.5, 'spawn_delay_multiplier': 0.8},    # Wave 5: 50% more enemies, 20% faster
                10: {'enemy_multiplier': 2.0, 'spawn_delay_multiplier': 0.7},   # Wave 10: Double enemies, 30% faster
                15: {'enemy_multiplier': 1.8, 'spawn_delay_multiplier': 0.6},   # Wave 15: 80% more enemies, 40% faster
                20: {'enemy_multiplier': 2.5, 'spawn_delay_multiplier': 0.5},   # Wave 20: 2.5x enemies, 50% faster
                25: {'enemy_multiplier': 3.0, 'spawn_delay_multiplier': 0.4},   # Wave 25: Triple enemies, 60% faster
                30: {'enemy_multiplier': 4.0, 'spawn_delay_multiplier': 0.3},   # Wave 30: Quadruple enemies, 70% faster
            }
        }
        
        # Money bonus configuration
        self.money_config = {
            'normal_wave_bonus': 50,
            'boss_wave_bonus': 100,
        }
        
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
            (20, 99): [(BasicEnemy, 0.1), (FastEnemy, 0.1), (TankEnemy, 0.1), (InvisibleEnemy, 0.15), (FlyingEnemy, 0.15), (ShieldedEnemy, 0.1), (RegeneratingEnemy, 0.1), (TeleportingEnemy, 0.1), (SplittingEnemy, 0.1)]  # All enemies
        }
        
        # Special boss waves
        self.boss_waves = {
            10: SpeedBoss,
            20: MegaBoss,
            30: MegaBoss,  # Mega boss returns
            40: SpeedBoss,  # Speed boss returns stronger
            50: MegaBoss   # Final mega boss
        }
    
    def get_value_for_wave(self, config_section: dict, wave_number: int) -> int:
        """Get a configuration value for a specific wave from wave ranges"""
        # Check wave ranges first
        for (min_wave, max_wave), value in config_section['wave_ranges'].items():
            if min_wave <= wave_number <= max_wave:
                return value
        
        # Fallback to default
        return config_section['default']
    
    def calculate_spawn_delay(self) -> int:
        """Calculate spawn delay based on current wave using per-round configuration"""
        base_delay = self.spawn_config['base_spawn_delay']
        min_delay = self.spawn_config['min_spawn_delay']
        
        # Calculate total reduction based on rounds completed
        total_reduction = 0
        for wave in range(2, self.wave_number + 1):  # Start from wave 2 (wave 1 uses base)
            reduction_per_round = self.get_value_for_wave(
                self.round_progression['spawn_delay_reduction_per_round'], wave
            )
            total_reduction += reduction_per_round
        
        # Calculate base delay after reductions
        current_delay = base_delay - total_reduction
        
        # Apply special round multipliers if applicable
        if self.wave_number in self.round_progression['special_rounds']:
            multiplier = self.round_progression['special_rounds'][self.wave_number]['spawn_delay_multiplier']
            current_delay = int(current_delay * multiplier)
        
        # Ensure we don't go below minimum
        return max(min_delay, current_delay)
    
    def calculate_enemies_per_wave(self) -> int:
        """Calculate number of enemies per wave using per-round configuration"""
        if self.wave_number in self.boss_waves:
            return self.spawn_config['boss_enemy_count']
        
        base_count = self.spawn_config['base_enemy_count']
        
        # Calculate total increase based on rounds completed
        total_increase = 0
        for wave in range(2, self.wave_number + 1):  # Start from wave 2 (wave 1 uses base)
            increase_per_round = self.get_value_for_wave(
                self.round_progression['enemy_increase_per_round'], wave
            )
            total_increase += increase_per_round
        
        # Calculate base enemy count after increases
        current_count = base_count + total_increase
        
        # Apply special round multipliers if applicable
        if self.wave_number in self.round_progression['special_rounds']:
            multiplier = self.round_progression['special_rounds'][self.wave_number]['enemy_multiplier']
            current_count = int(current_count * multiplier)
        
        return current_count

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
        
        # Apply progressive scaling based on wave number
        self.apply_enemy_scaling(enemy)
        
        self.enemies_spawned += 1
        
        return enemy
    
    def apply_enemy_scaling(self, enemy):
        """Apply progressive scaling to enemies based on wave number - INCREASED DIFFICULTY"""
        if self.wave_number <= 1:
            return  # No scaling for wave 1
        
        # Calculate scaling factors - MORE AGGRESSIVE
        wave_factor = (self.wave_number - 1)
        
        # Health scaling: +12% per wave (increased from 8%)
        health_multiplier = 1.0 + (wave_factor * 0.12)
        
        # Speed scaling: +4% per wave (increased from 2%)
        speed_multiplier = 1.0 + (wave_factor * 0.04)
        
        # Reward scaling: +3% per wave (reduced from 5% to compensate for base reward reduction)
        reward_multiplier = 1.0 + (wave_factor * 0.03)
        
        # Apply scaling with higher caps for more extreme late-game difficulty
        enemy.max_health = int(enemy.max_health * min(health_multiplier, 5.0))  # Cap at 5x health (increased from 3x)
        enemy.health = enemy.max_health
        enemy.speed = enemy.speed * min(speed_multiplier, 3.0)  # Cap at 3x speed (increased from 2x)
        enemy.reward = int(enemy.reward * min(reward_multiplier, 2.0))  # Cap at 2x reward (reduced from 2.5x)
    
    def is_wave_complete(self, active_enemies: List) -> bool:
        """Check if the current wave is complete"""
        return (self.enemies_spawned >= self.enemies_per_wave and 
                len(active_enemies) == 0)
    
    def start_next_wave(self) -> dict:
        """Start the next wave and return wave info"""
        if self.is_wave_complete([]):  # Empty list since we're just starting
            self.wave_number += 1
            self.enemies_spawned = 0
            
            # Calculate new wave parameters using configuration
            self.enemies_per_wave = self.calculate_enemies_per_wave()
            self.spawn_delay = self.calculate_spawn_delay()
            
            # Money bonus based on configuration
            money_bonus = (self.money_config['boss_wave_bonus'] if self.wave_number in self.boss_waves 
                          else self.money_config['normal_wave_bonus'])
            
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