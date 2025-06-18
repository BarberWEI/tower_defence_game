from .enemy import Enemy
from .basic_enemy import BasicEnemy
import pygame

class SplittingEnemy(Enemy):
    """Enemy that splits into smaller enemies when killed"""
    
    def __init__(self, path, split_count=2, generation=1):
        super().__init__(path, wave_number)
        self.generation = generation
        self.split_count = split_count
        
        # Scale stats based on generation
        base_health = 100
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
        """Return list of enemies to spawn when this enemy dies"""
        if self.generation < 3:  # Don't split beyond 3rd generation
            spawned_enemies = []
            for i in range(self.split_count):
                # Create smaller version at current position
                new_enemy = SplittingEnemy(self.path, self.split_count, self.generation + 1)
                new_enemy.path_index = self.path_index
                new_enemy.distance_traveled = self.distance_traveled
                
                # Position them slightly offset from the current position
                offset_x = (i - self.split_count/2) * 15  # Small offset
                offset_y = (i - self.split_count/2) * 10  # Small vertical offset
                new_enemy.x = self.x + offset_x
                new_enemy.y = self.y + offset_y
                spawned_enemies.append(new_enemy)
            return spawned_enemies
        return [] 