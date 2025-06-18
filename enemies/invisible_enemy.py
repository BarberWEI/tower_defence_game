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
        # Create a surface with per-pixel alpha
        enemy_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Draw semi-transparent circle
        pygame.draw.circle(enemy_surface, self.color, (8, 8), 8)
        
        # Draw health bar if damaged (also semi-transparent)
        if self.health < self.max_health:
            health_percentage = self.health / self.max_health
            bar_width = 16
            bar_height = 4
            
            # Background (semi-transparent red)
            pygame.draw.rect(enemy_surface, (255, 0, 0, 100), 
                           (0, -8, bar_width, bar_height))
            # Health (semi-transparent green)
            pygame.draw.rect(enemy_surface, (0, 255, 0, 150), 
                           (0, -8, int(bar_width * health_percentage), bar_height))
        
        # Blit to screen
        screen.blit(enemy_surface, (self.x - 8, self.y - 8))
    
    def is_detectable_by_tower(self, tower_x, tower_y, tower_type=None):
        """Check if this enemy can be detected by a tower at given position"""
        if tower_type == "detector":
            return True  # Detector towers can always see invisible enemies
        
        # Other towers can only detect if enemy is very close
        distance = ((self.x - tower_x) ** 2 + (self.y - tower_y) ** 2) ** 0.5
        return distance <= self.detection_radius 