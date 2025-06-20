from typing import List, Tuple
from config.game_config import get_wave_config
from enemies import (BasicEnemy, FastEnemy, TankEnemy, ShieldedEnemy,
                    InvisibleEnemy, FlyingEnemy, RegeneratingEnemy, 
                    SplittingEnemy, TeleportingEnemy, MegaBoss, SpeedBoss,
                    TimeLordBoss, NecromancerBoss, ShadowKing, CrystalOverlord,
                    ArmoredEnemy, EnergyShieldEnemy, GroundedEnemy, 
                    FireElementalEnemy, ToxicEnemy, PhaseShiftEnemy, BlastProofEnemy,
                    SpectralEnemy, CrystallineEnemy, ToxicMutantEnemy, VoidEnemy, AdaptiveEnemy)
from .enemy_introduction import EnemyIntroduction

class WaveManager:
    """Manages enemy waves and spawning"""
    
    def __init__(self, path: List[Tuple[int, int]]):
        self.path = path
        self.wave_number = 1
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.wave_complete = False
        
        # Load configuration from centralized config
        self.config = get_wave_config()
        self.spawn_config = self.config['spawn_config']
        self.round_progression = self.config['round_progression']
        self.money_config = self.config['money_config']
        
        # Initialize with starting values
        self.enemies_per_wave = self.spawn_config['base_enemy_count']
        self.spawn_delay = self.spawn_config['base_spawn_delay']
        
        # Enemy introduction system
        self.enemy_introduction = EnemyIntroduction()
        
        # Create enemy class mapping from string names to classes
        self.enemy_classes = {
            'BasicEnemy': BasicEnemy,
            'FastEnemy': FastEnemy,
            'TankEnemy': TankEnemy,
            'InvisibleEnemy': InvisibleEnemy,
            'FlyingEnemy': FlyingEnemy,
            'ShieldedEnemy': ShieldedEnemy,
            'RegeneratingEnemy': RegeneratingEnemy,
            'TeleportingEnemy': TeleportingEnemy,
            'SplittingEnemy': SplittingEnemy,
            'SpeedBoss': SpeedBoss,
            'MegaBoss': MegaBoss,
            'TimeLordBoss': TimeLordBoss,
            'NecromancerBoss': NecromancerBoss,
            'ShadowKing': ShadowKing,
            'CrystalOverlord': CrystalOverlord,
            # Tower-immune enemies
            'ArmoredEnemy': ArmoredEnemy,
            'EnergyShieldEnemy': EnergyShieldEnemy,
            'GroundedEnemy': GroundedEnemy,
            'FireElementalEnemy': FireElementalEnemy,
            'ToxicEnemy': ToxicEnemy,
            'PhaseShiftEnemy': PhaseShiftEnemy,
            'BlastProofEnemy': BlastProofEnemy,
            'SpectralEnemy': SpectralEnemy,
            'CrystallineEnemy': CrystallineEnemy,
            'ToxicMutantEnemy': ToxicMutantEnemy,
            'VoidEnemy': VoidEnemy,
            'AdaptiveEnemy': AdaptiveEnemy
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
        # Check for boss waves first
        boss_waves = self.config['boss_waves']
        if self.wave_number in boss_waves:
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
        boss_waves = self.config['boss_waves']
        if self.wave_number in boss_waves:
            boss_class_name = boss_waves[self.wave_number]
            return self.enemy_classes[boss_class_name]
        
        # Find the appropriate wave configuration
        wave_compositions = self.config['wave_compositions']
        for (min_wave, max_wave), enemy_types in wave_compositions.items():
            if min_wave <= self.wave_number <= max_wave:
                # Use weighted random selection
                rand = random.random()
                cumulative_weight = 0
                
                for enemy_class_name, weight in enemy_types:
                    cumulative_weight += weight
                    if rand <= cumulative_weight:
                        return self.enemy_classes[enemy_class_name]
        
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
    
    def should_spawn_enemy_with_speed(self, speed_multiplier: float) -> bool:
        """Check if it's time to spawn a new enemy with speed multiplier"""
        if self.enemies_spawned >= self.enemies_per_wave:
            return False
        
        self.spawn_timer += speed_multiplier
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            return True
        
        return False
    
    def spawn_enemy(self, speed_multiplier: float = 1.0) -> object:
        """Spawn and return a new enemy with optional speed multiplier"""
        if speed_multiplier != 1.0:
            if not self.should_spawn_enemy_with_speed(speed_multiplier):
                return None
        else:
            if not self.should_spawn_enemy():
                return None
        
        enemy_class = self.get_enemy_type_for_wave()
        # Pass wave number to enemy for immunity system
        enemy = enemy_class(self.path, self.wave_number)
        
        # Check if this enemy type needs introduction
        enemy_type_name = enemy_class.__name__
        self.enemy_introduction.check_new_enemy(enemy_type_name)
        
        # Apply progressive scaling based on wave number
        self.apply_enemy_scaling(enemy)
        
        self.enemies_spawned += 1
        
        return enemy
    
    def apply_enemy_scaling(self, enemy):
        """Apply comprehensive progressive scaling to ALL aspects of enemies based on wave number"""
        if self.wave_number <= 1:
            return  # No scaling for wave 1
        
        # Get scaling configuration
        scaling_config = self.config['enemy_scaling']
        wave_factor = (self.wave_number - 1)
        
        # Calculate scaling factors from config for ALL aspects
        health_multiplier = 1.0 + (wave_factor * scaling_config['health_per_wave'])
        speed_multiplier = 1.0 + (wave_factor * scaling_config['speed_per_wave'])
        reward_multiplier = 1.0 + (wave_factor * scaling_config['reward_per_wave'])
        size_multiplier = 1.0 + (wave_factor * scaling_config['size_per_wave'])
        damage_multiplier = 1.0 + (wave_factor * scaling_config['damage_scaling_per_wave'])
        
        # Apply comprehensive scaling with caps from config
        enemy.max_health = int(enemy.max_health * min(health_multiplier, scaling_config['max_health_multiplier']))
        enemy.health = enemy.max_health
        enemy.speed = enemy.speed * min(speed_multiplier, scaling_config['max_speed_multiplier'])
        
        # Only update base_speed for regular enemies, not bosses that manage their own speed
        if not hasattr(enemy, 'speed_multiplier') and not hasattr(enemy, 'phase'):
            enemy.base_speed = enemy.speed  # Update base speed for terrain calculations
        else:
            # For bosses, scale their base_speed appropriately to maintain their speed mechanics
            if hasattr(enemy, 'base_speed'):
                enemy.base_speed = enemy.base_speed * min(speed_multiplier, scaling_config['max_speed_multiplier'])
        
        enemy.reward = int(enemy.reward * min(reward_multiplier, scaling_config['max_reward_multiplier']))
        enemy.size = int(enemy.size * min(size_multiplier, scaling_config['max_size_multiplier']))
        
        # Scale enemy damage (for enemies that deal damage when reaching the end or special abilities)
        if hasattr(enemy, 'damage'):
            enemy.damage = int(enemy.damage * min(damage_multiplier, scaling_config['max_damage_multiplier']))
        
        # Scale special abilities (regeneration rate, teleport frequency, etc.)
        if hasattr(enemy, 'regeneration_rate'):
            enemy.regeneration_rate = int(enemy.regeneration_rate * min(health_multiplier * 0.5, 2.0))
        
        if hasattr(enemy, 'teleport_cooldown') and enemy.teleport_cooldown > 0:
            # Reduce cooldown (make teleporting more frequent) but not below 30 frames
            enemy.teleport_cooldown = max(30, int(enemy.teleport_cooldown / min(speed_multiplier * 0.5, 1.5)))
        
        if hasattr(enemy, 'split_health_ratio'):
            # Splitting enemies create stronger children
            enemy.split_health_ratio = min(0.8, enemy.split_health_ratio + (wave_factor * 0.02))
        
        # Scale boss-specific abilities
        if hasattr(enemy, 'minion_health'):
            enemy.minion_health = int(enemy.minion_health * min(health_multiplier * 0.7, 3.0))
        
        if hasattr(enemy, 'minion_count_range'):
            # Bosses spawn more minions
            min_minions, max_minions = enemy.minion_count_range
            scaling_factor = min(1.5, 1.0 + (wave_factor * 0.05))
            enemy.minion_count_range = (int(min_minions * scaling_factor), int(max_minions * scaling_factor))
    
    def is_wave_complete(self, active_enemies: List) -> bool:
        """Check if the current wave is complete"""
        return (self.enemies_spawned >= self.enemies_per_wave and 
                len(active_enemies) == 0)
    
    def start_next_wave(self) -> dict:
        """Start the next wave and return wave info"""
        # Check if we've completed the final wave (don't start a new wave beyond max)
        max_wave = self.get_max_wave_number()
        if self.wave_number >= max_wave:
            # We've completed the final wave - game should end
            return {
                'wave_completed': True,
                'wave_number': self.wave_number,
                'money_bonus': self.money_config['boss_wave_bonus'] if self.wave_number in self.config['boss_waves'] else self.money_config['normal_wave_bonus'],
                'is_final_wave': True,
                'game_completed': True
            }
        
        # Increment wave and reset counters
        self.wave_number += 1
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.wave_complete = False
        
        # Update wave parameters using proper calculation methods
        self.enemies_per_wave = self.calculate_enemies_per_wave()
        self.spawn_delay = self.calculate_spawn_delay()
        
        return {
            'wave_started': True,
            'wave_number': self.wave_number,
            'money_bonus': 0
        }
    
    def get_wave_info(self) -> dict:
        """Get current wave information"""
        return {
            'wave_number': self.wave_number,
            'enemies_spawned': self.enemies_spawned,
            'enemies_per_wave': self.enemies_per_wave,
            'progress': self.enemies_spawned / self.enemies_per_wave
        }
    
    def update(self, active_enemies: List) -> dict:
        """Update wave state and return wave completion info"""
        # Update enemy introduction system
        self.enemy_introduction.update()
        
        if self.is_wave_complete(active_enemies):
            if not self.wave_complete:
                self.wave_complete = True
                
                # Check if this is the final wave
                max_wave = self.get_max_wave_number()
                is_final_wave = self.wave_number >= max_wave
                

                
                # Calculate wave completion bonus
                wave_bonus = self.money_config['normal_wave_bonus']
                
                # Check if this was a boss wave
                if self.wave_number in self.config['boss_waves']:
                    wave_bonus = self.money_config['boss_wave_bonus']
                
                # If not final wave, prepare for next wave
                if not is_final_wave:
                    # Start next wave after a brief delay
                    # This will be handled by the game loop
                    pass
                
                return {
                    'wave_completed': True,
                    'wave_number': self.wave_number,
                    'money_bonus': wave_bonus,
                    'is_final_wave': is_final_wave,
                    'game_completed': is_final_wave
                }
        
        return None
    
    def get_max_wave_number(self) -> int:
        """Get the maximum wave number from boss waves and wave compositions"""
        max_boss_wave = 0
        if self.config['boss_waves']:
            max_boss_wave = max(int(wave) for wave in self.config['boss_waves'].keys())
        
        max_composition_wave = 0
        if self.config['wave_compositions']:
            for wave_range in self.config['wave_compositions'].keys():
                # Parse range like "1-5" or handle tuple ranges
                if isinstance(wave_range, tuple):
                    end_wave = wave_range[1] 
                elif isinstance(wave_range, str) and '-' in wave_range:
                    end_wave = int(wave_range.split('-')[1])
                else:
                    end_wave = int(wave_range)
                max_composition_wave = max(max_composition_wave, end_wave)
        
        return max(max_boss_wave, max_composition_wave)
    
    def draw_introduction(self, screen):
        """Draw enemy introduction overlay if active"""
        self.enemy_introduction.draw(screen)
    
    def has_active_introduction(self) -> bool:
        """Check if an enemy introduction is currently being displayed"""
        return self.enemy_introduction.has_active_introduction()
    
    def reset_introductions(self):
        """Reset all enemy introductions (for new game)"""
        self.enemy_introduction.reset_introductions() 