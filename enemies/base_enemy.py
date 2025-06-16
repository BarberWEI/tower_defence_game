import pygame

class BaseEnemy:
    def __init__(self, path, config):
        self.path = path
        self.path_index = 0
        self.pos = list(path[0])
        self.config = config
        self.color = self.get_enemy_color()
        self.slow_factor = 1.0
        self.slow_end_time = 0
    
    def get_enemy_color(self):
        return (255, 0, 0)  # Default red color
    
    def apply_slow(self, slow_amount, duration):
        now = pygame.time.get_ticks()
        if self.slow_end_time < now:
            self.slow_factor = slow_amount
            self.slow_end_time = now + duration
        else:
            # If already slowed, extend the slow duration if needed
            self.slow_end_time = max(self.slow_end_time, now + duration)

    def update(self):
        # Handle slow effect
        now = pygame.time.get_ticks()
        if now > self.slow_end_time:
            self.slow_factor = 1.0
        effective_speed = self.speed * self.slow_factor
        remaining_speed = effective_speed
        while self.path_index < len(self.path) - 1 and remaining_speed > 0:
            target = self.path[self.path_index + 1]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist == 0:
                self.path_index += 1
                continue
            move_dist = min(remaining_speed, dist)
            move_x = dx / dist * move_dist
            move_y = dy / dist * move_dist
            self.pos = (self.pos[0] + move_x, self.pos[1] + move_y)
            remaining_speed -= move_dist
            if move_dist == dist:
                self.pos = target
                self.path_index += 1
    
    def reached_end(self):
        return self.path_index >= len(self.path) - 1
    
    def draw(self, screen):
        # Draw enemy body
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), 15)
        
        # Draw health bar
        health_width = 30
        health_height = 5
        health_x = self.pos[0] - health_width/2
        health_y = self.pos[1] - 25
        
        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (health_x, health_y, health_width, health_height))
        
        # Foreground (green)
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0),
                        (health_x, health_y, health_width * health_percentage, health_height))
        
        # Draw enemy type indicator
        if self.type != 'basic':
            type_text = pygame.font.Font(None, 20).render(self.type[0].upper(), True, (255, 255, 255))
            text_rect = type_text.get_rect(center=(self.pos[0], self.pos[1]))
            screen.blit(type_text, text_rect) 