from .enemy import Enemy
from .basic_enemy import BasicEnemy
import pygame

class SplittingEnemy(Enemy):
    """Enemy that splits into smaller enemies when destroyed"""
    
    def __init__(self, path, split_count=2, generation=1, wave_number=1):
        super().__init__(path, wave_number)
        self.generation = generation
        self.split_count = split_count
        
        # Scale stats based on generation
        base_health = 30
        base_speed = 0.8
        base_reward = 20
        
        self.health = int(base_health / generation)
        self.max_health = self.health
        self.speed = base_speed + (generation - 1) * 0.3
        self.reward = int(base_reward / generation)
        
        # Visual properties
        self.color = (255, 0, 255)  # Magenta
        self.size = max(12 - generation * 2, 6)  # Smaller each generation
        
    def draw(self, screen):
        """Draw splitting enemy with generation indicators"""
        # Draw main body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw generation indicators (small dots)
        for i in range(self.generation):
            dot_x = self.x - self.size + 3 + i * 4
            dot_y = self.y - self.size + 3
            pygame.draw.circle(screen, (255, 255, 255), (int(dot_x), int(dot_y)), 2)
        
        # Draw health bar
        if self.health < self.max_health:
            health_percentage = self.health / self.max_health
            bar_width = self.size * 2
            bar_height = 3
            
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.x - self.size, self.y - self.size - 8, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), 
                           (self.x - self.size, self.y - self.size - 8, 
                            int(bar_width * health_percentage), bar_height))
    
    def on_death(self):
        """Return list of random enemies to spawn when this enemy dies"""
        # Always spawn 2 random enemies (regardless of generation)
        spawned_enemies = []
        
        # Import available enemy types
        from . import BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy, FlyingEnemy
        from . import ArmoredEnemy, EnergyShieldEnemy, GroundedEnemy, FireElementalEnemy, ToxicEnemy
        
        # Define enemies available at different wave ranges (no bosses!)
        wave_based_enemies = {
            1: [BasicEnemy, FastEnemy],
            5: [BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy],
            10: [BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy, FlyingEnemy],
            15: [BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy, FlyingEnemy, ArmoredEnemy],
            20: [BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy, FlyingEnemy, ArmoredEnemy, EnergyShieldEnemy],
            25: [BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy, FlyingEnemy, ArmoredEnemy, EnergyShieldEnemy, GroundedEnemy],
            30: [BasicEnemy, FastEnemy, TankEnemy, InvisibleEnemy, FlyingEnemy, ArmoredEnemy, EnergyShieldEnemy, GroundedEnemy, FireElementalEnemy, ToxicEnemy]
        }
        
        # Find appropriate enemy pool based on current wave
        available_enemies = [BasicEnemy, FastEnemy]  # Default
        for wave_threshold in sorted(wave_based_enemies.keys(), reverse=True):
            if self.wave_number >= wave_threshold:
                available_enemies = wave_based_enemies[wave_threshold]
                break
        
        # Spawn 2 random enemies from the available pool
        import random
        for i in range(2):
            enemy_class = random.choice(available_enemies)
            new_enemy = enemy_class(self.path, self.wave_number)
            
            # CRITICAL: Properly inherit path position and state
            new_enemy.path_index = self.path_index
            new_enemy.distance_traveled = self.distance_traveled
            
            # Position them at the actual death location with very small offsets
            # This ensures they continue from where the splitting enemy died
            offset_x = random.uniform(-8, 8)   # Very small random horizontal offset
            offset_y = random.uniform(-8, 8)   # Very small random vertical offset
            new_enemy.x = self.x + offset_x
            new_enemy.y = self.y + offset_y
            
            # Make spawned enemies slightly weaker (75% health)
            new_enemy.health = int(new_enemy.health * 0.75)
            new_enemy.max_health = new_enemy.health
            
            # Ensure they inherit any status effects appropriately
            new_enemy.reached_end = False
            
            # Debug info
            print(f"Split enemy spawned: {enemy_class.__name__} at path_index {new_enemy.path_index}, pos ({new_enemy.x:.1f}, {new_enemy.y:.1f})")
            
            spawned_enemies.append(new_enemy)
        
        return spawned_enemies 