from .enemy import Enemy
import pygame

class InvisibleEnemy(Enemy):
    """Enemy that is invisible to most towers"""
    
    def __init__(self, path):
        super().__init__(path)
        self.health = 60
        self.max_health = 60
        self.speed = 1.5
        self.reward = 15
        self.color = (128, 128, 128, 100)  # Semi-transparent gray
        self.invisible = True
        self.detection_radius = 80  # Radius where it becomes visible
        
    def draw(self, screen):
        """Draw the invisible enemy (semi-transparent)"""
        # Create a surface with per-pixel alpha for the enemy body
        enemy_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Draw semi-transparent circle
        pygame.draw.circle(enemy_surface, self.color, (8, 8), 8)
        
        # Blit enemy body to screen
        screen.blit(enemy_surface, (self.x - 8, self.y - 8))
        
        # Draw health bar directly on screen (like other enemies) if damaged
        if self.health < self.max_health:
            health_percentage = self.health / self.max_health
            bar_width = 16
            bar_height = 4
            bar_x = int(self.x - bar_width // 2)
            bar_y = int(self.y - 8 - 8)  # Above the enemy
            
            # Calculate health bar width, ensuring it's at least 1 pixel
            health_bar_width = max(1, int(bar_width * health_percentage))
            
            # Create semi-transparent surfaces for health bar
            health_bg_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
            health_fg_surface = pygame.Surface((health_bar_width, bar_height), pygame.SRCALPHA)
            
            # Background (semi-transparent red)
            pygame.draw.rect(health_bg_surface, (255, 0, 0, 150), (0, 0, bar_width, bar_height))
            # Health (semi-transparent green)
            pygame.draw.rect(health_fg_surface, (0, 255, 0, 200), 
                           (0, 0, health_bar_width, bar_height))
            
            # Blit health bar to screen
            screen.blit(health_bg_surface, (bar_x, bar_y))
            screen.blit(health_fg_surface, (bar_x, bar_y))
    
    def is_detectable_by_tower(self, tower_x, tower_y, tower_type=None):
        """Check if this enemy can be detected by a tower at given position"""
        if tower_type == "detector":
            return True  # Detector towers can always see invisible enemies
        
        # Other towers can only detect if enemy is very close
        distance = ((self.x - tower_x) ** 2 + (self.y - tower_y) ** 2) ** 0.5
        return distance <= self.detection_radius 