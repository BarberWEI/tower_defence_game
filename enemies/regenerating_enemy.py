from .enemy import Enemy
import pygame

class RegeneratingEnemy(Enemy):
    """Enemy that regenerates health over time"""
    
    def __init__(self, path):
        super().__init__(path)
        self.health = 80
        self.max_health = 80
        self.speed = 1.0
        self.reward = 16
        self.color = (0, 255, 100)  # Light green
        self.regen_rate = 0.5  # Health per second
        self.regen_timer = 0
        self.last_damage_time = 0
        self.regen_delay = 180  # 3 seconds before regen starts (60 FPS)
        
    def update(self):
        """Update with regeneration logic"""
        super().update()
        
        # Increment timers
        self.regen_timer += 1
        self.last_damage_time += 1
        
        # Regenerate health if not damaged recently
        if (self.last_damage_time > self.regen_delay and 
            self.health < self.max_health and 
            self.regen_timer >= 60):  # Regen every second
            
            self.health = min(self.max_health, self.health + self.regen_rate)
            self.regen_timer = 0
    
    def take_damage(self, damage):
        """Take damage and reset regeneration timer"""
        actual_damage = super().take_damage(damage)
        self.last_damage_time = 0  # Reset damage timer
        return actual_damage
        
    def draw(self, screen):
        """Draw regenerating enemy with special effects"""
        # Draw main enemy
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 10, 2)
        
        # Draw regeneration aura if regenerating
        if (self.last_damage_time > self.regen_delay and 
            self.health < self.max_health):
            aura_color = (0, 255, 0, 50)
            pygame.draw.circle(screen, aura_color, (int(self.x), int(self.y)), 15, 3)
        
        # Draw health bar
        if self.health < self.max_health:
            health_percentage = self.health / self.max_health
            bar_width = 20
            bar_height = 4
            
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.x - 10, self.y - 18, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), 
                           (self.x - 10, self.y - 18, int(bar_width * health_percentage), bar_height)) 