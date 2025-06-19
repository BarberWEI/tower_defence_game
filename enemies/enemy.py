import pygame
import math
from typing import List, Tuple
from config.game_config import get_balance_config

class Enemy:
    """Base class for all enemies"""
    def __init__(self, path: List[Tuple[int, int]], wave_number: int = 1):
        self.path = path
        self.path_index = 0
        self.x = float(path[0][0])
        self.y = float(path[0][1])
        self.wave_number = wave_number
        
        # Base stats - to be overridden by subclasses
        self.max_health = 1
        self.health = self.max_health
        self.speed = 1.0
        self.reward = 4
        self.size = 10
        self.color = (255, 0, 0)  # Red by default
        
        # Status effects
        self.frozen = False
        self.freeze_timer = 0
        self.wet = False
        self.wet_timer = 0
        self.lightning_damage_multiplier = 1.0
        
        # Progressive immunity system
        self.immunities = self._generate_random_immunities()
        
        # State
        self.reached_end = False
        self.distance_traveled = 0
    
    def _generate_random_immunities(self) -> dict:
        """Generate random immunities based on wave progression using config values"""
        import random
        
        immunities = {
            'freeze_immune': False,
            'slow_immune': False,
            'poison_immune': False,
            'burn_immune': False,
            'wet_immune': False,
            'stun_immune': False
        }
        
        # Get immunity configuration
        config = get_balance_config()
        immunity_config = config['immunity']
        
        # Calculate immunity chances based on wave number using config
        base_chance = min(immunity_config['max_immunity_chance'], 
                         self.wave_number * immunity_config['base_chance_per_wave'])
        
        # Special waves have higher immunity chances using config multipliers
        if self.wave_number % 10 == 0:  # Boss waves
            base_chance *= immunity_config['boss_wave_multiplier']
        elif self.wave_number % 5 == 0:  # Mini-boss waves
            base_chance *= immunity_config['mini_boss_multiplier']
        
        # Randomly assign immunities
        for immunity_type in immunities:
            if random.random() < base_chance:
                immunities[immunity_type] = True
        
        # Ensure at least some enemies remain vulnerable early game using config
        if self.wave_number <= immunity_config['early_game_waves']:
            # Force at most max_immunities for early waves
            immune_count = sum(immunities.values())
            max_immunities = immunity_config['early_game_max_immunities']
            if immune_count > max_immunities:
                # Keep only max_immunities random immunities
                immune_types = [k for k, v in immunities.items() if v]
                keep_immunities = random.sample(immune_types, max_immunities)
                immunities = {k: (k in keep_immunities) for k in immunities}
        
        return immunities
    
    def is_immune_to(self, effect_type: str) -> bool:
        """Check if enemy is immune to a specific effect"""
        return self.immunities.get(f"{effect_type}_immune", False)
    
    def update(self):
        """Update enemy position and state"""
        # Handle freeze effect (if not immune) - NOW SLOWS INSTEAD OF STOPPING
        if self.frozen and not self.is_immune_to('freeze'):
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.frozen = False
                # Restore original speed when freeze ends
                if hasattr(self, 'original_speed'):
                    self.speed = self.original_speed
        elif self.is_immune_to('freeze'):
            # Immune enemies can't be frozen
            self.frozen = False
            self.freeze_timer = 0
            if hasattr(self, 'original_speed'):
                self.speed = self.original_speed
        
        # Handle wet effect (if not immune)
        if self.wet and not self.is_immune_to('wet'):
            self.wet_timer -= 1
            if self.wet_timer <= 0:
                self.wet = False
                self.lightning_damage_multiplier = 1.0
        elif self.is_immune_to('wet'):
            # Immune enemies can't be wet
            self.wet = False
            self.wet_timer = 0
            self.lightning_damage_multiplier = 1.0
        
        # Always move (even when "frozen" - just slower)
        self.move_along_path()
    
    def move_along_path(self):
        """Move the enemy along the predefined path"""
        if self.path_index >= len(self.path) - 1:
            self.reached_end = True
            return
        
        # Get current and next waypoints
        current_point = self.path[self.path_index]
        next_point = self.path[self.path_index + 1]
        
        # Calculate direction to next waypoint
        dx = next_point[0] - current_point[0]
        dy = next_point[1] - current_point[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            self.path_index += 1
            return
        
        # Normalize direction and apply speed
        dx = (dx / distance) * self.speed
        dy = (dy / distance) * self.speed
        
        # Move towards next waypoint
        self.x += dx
        self.y += dy
        self.distance_traveled += self.speed
        
        # Check if we've reached the next waypoint
        if math.sqrt((self.x - next_point[0])**2 + (self.y - next_point[1])**2) < 5:
            self.path_index += 1
    
    def take_damage(self, damage: int):
        """Apply damage to the enemy"""
        actual_damage = min(damage, self.health)  # Can't deal more damage than remaining health
        self.health -= damage
        return actual_damage
    
    def apply_freeze(self, duration: int):
        """Apply freeze effect to the enemy (if not immune) - NOW SLOWS USING CONFIG VALUE"""
        if not self.is_immune_to('freeze'):
            # Store original speed if not already stored
            if not hasattr(self, 'original_speed'):
                self.original_speed = self.speed
            
            # Apply freeze (heavy slow instead of complete stop)
            self.frozen = True
            self.freeze_timer = max(self.freeze_timer, duration)
            # Reduce speed using config value
            config = get_balance_config()
            self.speed = self.original_speed * config['freeze']['slow_factor']
    
    def apply_wet_status(self, duration: int, lightning_multiplier: float):
        """Apply wet status to the enemy (if not immune)"""
        if not self.is_immune_to('wet'):
            self.wet = True
            self.wet_timer = max(self.wet_timer, duration)
            self.lightning_damage_multiplier = lightning_multiplier
    
    def get_distance_from_start(self) -> float:
        """Get the total distance traveled along the path"""
        return self.distance_traveled
    
    def draw(self, screen: pygame.Surface):
        """Draw the enemy on the screen"""
        # Draw main enemy circle with status effects
        color = self.color
        if self.frozen:
            color = (100, 100, 255)  # Blue when frozen
        elif self.wet:
            # Slightly darker and more saturated when wet
            color = tuple(max(0, min(255, int(c * 0.8))) for c in self.color)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw immunity indicators
        self._draw_immunity_indicators(screen)
        
        # Draw wet effect overlay
        if self.wet:
            # Draw water droplets around enemy
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                drop_x = self.x + math.cos(rad) * (self.size + 3)
                drop_y = self.y + math.sin(rad) * (self.size + 3)
                pygame.draw.circle(screen, (30, 144, 255), (int(drop_x), int(drop_y)), 2)
        
        # Draw health bar
        if self.health < self.max_health:
            bar_width = self.size * 2
            bar_height = 4
            bar_x = int(self.x - bar_width // 2)
            bar_y = int(self.y - self.size - 8)
            
            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Health (green)
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
    
    def _draw_immunity_indicators(self, screen: pygame.Surface):
        """Draw small indicators for immunities"""
        immune_effects = [k.replace('_immune', '') for k, v in self.immunities.items() if v]
        
        if not immune_effects:
            return
        
        # Draw immunity shield symbol
        shield_color = (255, 215, 0)  # Gold
        shield_x = int(self.x + self.size - 3)
        shield_y = int(self.y - self.size + 3)
        
        # Draw small shield
        shield_points = [
            (shield_x, shield_y),
            (shield_x + 4, shield_y),
            (shield_x + 4, shield_y + 6),
            (shield_x + 2, shield_y + 8),
            (shield_x, shield_y + 6)
        ]
        pygame.draw.polygon(screen, shield_color, shield_points)
        pygame.draw.polygon(screen, (0, 0, 0), shield_points, 1) 