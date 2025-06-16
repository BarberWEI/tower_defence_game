import pygame
import math

class Tower:
    def __init__(self, pos, tower_type='basic', config=None):
        self.pos = pos
        self.type = tower_type
        
        # Get tower properties from config
        if config and tower_type in config.available_towers:
            props = config.available_towers[tower_type]
            self.range = props['range']
            self.damage = props['damage']
            self.cooldown = props['cooldown']
            self.cost = props['cost']
            self.splash_radius = props.get('splash_radius', 0)
            self.continuous = props.get('continuous', False)
        else:
            # Default properties
            self.range = 150
            self.damage = 20
            self.cooldown = 30
            self.cost = 50
            self.splash_radius = 0
            self.continuous = False
        
        self.cooldown_timer = 0
        self.target = None
        self.color = self.get_tower_color()
    
    def get_tower_color(self):
        colors = {
            'basic': (100, 100, 100),   # Gray
            'sniper': (0, 0, 255),      # Blue
            'splash': (255, 255, 0),    # Yellow
            'laser': (0, 255, 255)      # Cyan
        }
        return colors.get(self.type, (100, 100, 100))
    
    def update(self, enemies):
        if self.cooldown_timer > 0 and not self.continuous:
            self.cooldown_timer -= 1
            return
        
        # Find closest enemy in range
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((enemy.pos[0] - self.pos[0])**2 + 
                               (enemy.pos[1] - self.pos[1])**2)
            if distance <= self.range and distance < min_distance:
                closest_enemy = enemy
                min_distance = distance
        
        # Attack if enemy found
        if closest_enemy:
            if self.splash_radius > 0:
                # Splash damage
                for enemy in enemies:
                    distance = math.sqrt((enemy.pos[0] - closest_enemy.pos[0])**2 + 
                                       (enemy.pos[1] - closest_enemy.pos[1])**2)
                    if distance <= self.splash_radius:
                        enemy.health -= self.damage
            else:
                # Single target damage
                closest_enemy.health -= self.damage
            
            if not self.continuous:
                self.cooldown_timer = self.cooldown
    
    def draw(self, screen):
        # Draw tower base
        pygame.draw.circle(screen, self.color, self.pos, 20)
        
        # Draw range circle (for debugging)
        pygame.draw.circle(screen, (*self.color, 50), self.pos, self.range, 1)
        
        # Draw tower top
        pygame.draw.circle(screen, (150, 150, 150), self.pos, 15)
        
        # Draw splash radius if applicable
        if self.splash_radius > 0:
            pygame.draw.circle(screen, (*self.color, 30), self.pos, self.splash_radius, 1)
        
        # Draw tower type indicator
        type_text = pygame.font.Font(None, 20).render(self.type[0].upper(), True, (255, 255, 255))
        text_rect = type_text.get_rect(center=self.pos)
        screen.blit(type_text, text_rect) 