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
        self.base_speed = 1.0  # Store original speed for terrain effects
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
        
        # Map reference for terrain effects
        self.map_reference = None
    
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
    
    def has_resistance_to(self, effect_type: str) -> bool:
        """Check if enemy has resistance to a specific effect (same as immunity for now)"""
        return self.immunities.get(f"{effect_type}_immune", False)
    
    def set_map_reference(self, map_obj):
        """Set reference to map for terrain effects"""
        self.map_reference = map_obj
    
    def set_base_speed(self, speed: float):
        """Set base speed and current speed (for use by subclasses)"""
        self.base_speed = speed
        self.speed = speed
    
    def __setattr__(self, name, value):
        """Override to automatically update base_speed when speed is set during initialization"""
        super().__setattr__(name, value)
        # If setting speed and we don't have terrain effects applied yet, also set base_speed
        if name == 'speed' and hasattr(self, 'base_speed') and not hasattr(self, '_speed_initialized'):
            self.base_speed = value
            self._speed_initialized = True
    
    def apply_terrain_speed_effects(self):
        """Apply terrain-based speed modifications"""
        if not self.map_reference:
            return
        
        from game_systems.terrain_types import get_terrain_property, SAND
        
        # Get terrain at current position
        terrain_type = self.map_reference.get_terrain_at_pixel(int(self.x), int(self.y))
        
        # Reset speed to base (accounting for other effects like freeze)
        if not self.frozen:
            self.speed = self.base_speed
        
        # Apply terrain effects
        if terrain_type == SAND:
            # Sand increases enemy speed by 50%
            speed_multiplier = 1.5
            if self.frozen:
                # If frozen, apply both freeze and sand effects
                config = get_balance_config()
                if self.has_resistance_to('freeze'):
                    # Resistant enemies get less slow effect
                    freeze_factor = config['freeze']['resistance_slow_factor']
                else:
                    # Normal enemies get full slow effect
                    freeze_factor = config['freeze']['slow_factor']
                self.speed = self.base_speed * speed_multiplier * freeze_factor
            else:
                self.speed = self.base_speed * speed_multiplier
        else:
            # Handle freeze on non-sand terrain
            if self.frozen:
                config = get_balance_config()
                if self.has_resistance_to('freeze'):
                    # Resistant enemies get less slow effect
                    freeze_factor = config['freeze']['resistance_slow_factor']
                else:
                    # Normal enemies get full slow effect
                    freeze_factor = config['freeze']['slow_factor']
                self.speed = self.base_speed * freeze_factor
    
    def update(self):
        """Update enemy position and state"""
        # Handle freeze effect - now with resistance instead of immunity
        if self.frozen:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.frozen = False
        
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
        
        # Update counter effects
        if hasattr(self, 'counter_effects'):
            for effect in self.counter_effects[:]:
                effect['timer'] -= 1
                if effect['timer'] <= 0:
                    self.counter_effects.remove(effect)
        
        # Apply terrain-based speed effects (handles freeze interactions)
        self.apply_terrain_speed_effects()
        
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
        
        # Check if we've reached or passed the next waypoint (adaptive threshold based on speed)
        # Use larger threshold for fast enemies to prevent overshooting
        detection_threshold = max(5, self.speed * 1.5)
        distance_to_waypoint = math.sqrt((self.x - next_point[0])**2 + (self.y - next_point[1])**2)
        
        if distance_to_waypoint < detection_threshold:
            # Snap to waypoint to ensure exact path following
            self.x = float(next_point[0])
            self.y = float(next_point[1])
            self.path_index += 1
    
    def take_damage(self, damage: int, tower_type: str = 'basic'):
        """Apply damage to the enemy with counter system multipliers"""
        # Get counter system configuration
        config = get_balance_config()
        counter_config = config.get('counter_system', {})
        multipliers = counter_config.get('tower_enemy_multipliers', {})
        default_multiplier = counter_config.get('default_multiplier', 1.0)
        max_multiplier = counter_config.get('max_multiplier', 3.0)
        min_multiplier = counter_config.get('min_multiplier', 0.1)
        
        # Calculate damage multiplier
        damage_multiplier = default_multiplier
        
        # Get enemy class name
        enemy_class = self.__class__.__name__
        
        # Check for tower-specific multipliers
        if tower_type in multipliers:
            tower_multipliers = multipliers[tower_type]
            
            # Direct enemy type match
            if enemy_class in tower_multipliers:
                damage_multiplier = tower_multipliers[enemy_class]
            
            # Special case: Lightning towers do extra damage to wet enemies
            elif tower_type == 'lightning' and self.wet and 'wet_enemies' in tower_multipliers:
                damage_multiplier = tower_multipliers['wet_enemies']
        
        # Clamp multiplier to acceptable range
        damage_multiplier = max(min_multiplier, min(max_multiplier, damage_multiplier))
        
        # Apply multiplier to damage
        modified_damage = int(damage * damage_multiplier)
        
        # Calculate actual damage (can't deal more than remaining health)
        actual_damage = min(modified_damage, self.health)
        self.health -= modified_damage
        
        # Visual feedback for counter attacks (different colors)
        if damage_multiplier > 1.5:
            self._show_counter_effect('super_effective')
        elif damage_multiplier > 1.0:
            self._show_counter_effect('effective')
        elif damage_multiplier < 0.8:
            self._show_counter_effect('not_very_effective')
        
        return actual_damage
    
    def _show_counter_effect(self, effectiveness_type: str):
        """Show visual feedback for counter effectiveness"""
        # This creates a temporary visual effect that can be displayed
        # The actual visual implementation would be handled by the game's effect system
        import time
        
        if not hasattr(self, 'counter_effects'):
            self.counter_effects = []
        
        effect = {
            'type': effectiveness_type,
            'timer': 30,  # 0.5 seconds at 60 FPS
            'created_at': time.time()
        }
        
        self.counter_effects.append(effect)
    
    def apply_freeze(self, duration: int):
        """Apply freeze effect to the enemy with resistance reducing duration and effectiveness"""
        config = get_balance_config()
        
        if self.has_resistance_to('freeze'):
            # Resistant enemies get reduced duration
            reduced_duration = int(duration * config['freeze']['resistance_duration_multiplier'])
            self.frozen = True
            self.freeze_timer = max(self.freeze_timer, reduced_duration)
        else:
            # Normal enemies get full duration
            self.frozen = True
            self.freeze_timer = max(self.freeze_timer, duration)
        # Speed will be updated by apply_terrain_speed_effects() which handles freeze
    
    def apply_wet_status(self, duration: int, lightning_multiplier: float):
        """Apply wet status to the enemy (if not immune)"""
        if not self.is_immune_to('wet'):
            self.wet = True
            self.wet_timer = max(self.wet_timer, duration)
            self.lightning_damage_multiplier = lightning_multiplier
    
    def get_distance_from_start(self) -> float:
        """Get the total distance traveled along the path"""
        return self.distance_traveled
    
    def draw_health_bar(self, screen: pygame.Surface, x_offset: int = 0, y_offset: int = 0):
        """Draw health bar above the enemy - can be called by subclasses with custom positioning"""
        if self.health < self.max_health:
            bar_width = self.size * 2
            bar_height = 4
            bar_x = int(self.x - bar_width // 2) + x_offset
            bar_y = int(self.y - self.size - 8) + y_offset
            
            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Health (green)
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
    
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
        
        # Draw counter effectiveness indicators
        self._draw_counter_effects(screen)
        
        # Draw health bar using the new method
        self.draw_health_bar(screen)
    
    def _draw_immunity_indicators(self, screen: pygame.Surface):
        """Draw small indicators for resistances (formerly immunities)"""
        resistant_effects = [k.replace('_immune', '') for k, v in self.immunities.items() if v]
        
        if not resistant_effects:
            return
        
        # Draw resistance shield symbol (different color to indicate partial protection)
        shield_color = (255, 165, 0)  # Orange (instead of gold for immunity)
        shield_x = int(self.x + self.size - 3)
        shield_y = int(self.y - self.size + 3)
        
        # Draw small shield with slightly different design
        shield_points = [
            (shield_x, shield_y),
            (shield_x + 4, shield_y),
            (shield_x + 4, shield_y + 6),
            (shield_x + 2, shield_y + 8),
            (shield_x, shield_y + 6)
        ]
        pygame.draw.polygon(screen, shield_color, shield_points)
        pygame.draw.polygon(screen, (0, 0, 0), shield_points, 1)
        
        # Add small "R" inside shield to indicate resistance
        font = pygame.font.Font(None, 8)
        text = font.render("R", True, (0, 0, 0))
        text_rect = text.get_rect(center=(shield_x + 2, shield_y + 4))
        screen.blit(text, text_rect)
    
    def _draw_counter_effects(self, screen: pygame.Surface):
        """Draw visual feedback for counter effectiveness"""
        if not hasattr(self, 'counter_effects') or not self.counter_effects:
            return
        
        font = pygame.font.Font(None, 16)
        
        for i, effect in enumerate(self.counter_effects):
            # Calculate position (stack multiple effects)
            effect_x = int(self.x)
            effect_y = int(self.y - self.size - 20 - (i * 15))
            
            # Calculate alpha based on timer (fade out)
            alpha = min(255, effect['timer'] * 8)
            
            # Choose color and text based on effect type
            if effect['type'] == 'super_effective':
                color = (255, 100, 100)  # Bright red
                text = "SUPER!"
            elif effect['type'] == 'effective':
                color = (255, 255, 100)  # Yellow
                text = "HIT!"
            elif effect['type'] == 'not_very_effective':
                color = (150, 150, 150)  # Gray
                text = "WEAK"
            else:
                continue
            
            # Create text surface with alpha
            text_surface = font.render(text, True, color)
            
            # Apply alpha (create a new surface for proper alpha blending)
            if alpha < 255:
                alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, alpha))
                text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Center the text
            text_rect = text_surface.get_rect(center=(effect_x, effect_y))
            screen.blit(text_surface, text_rect) 