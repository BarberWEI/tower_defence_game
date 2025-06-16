import pygame

class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.pos = list(path[0])  # Start at first path point
        self.speed = 2
        self.health = 100
        self.max_health = 100
        self.reward = 10
    
    def update(self):
        if self.path_index >= len(self.path) - 1:
            return
        
        target = self.path[self.path_index + 1]
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance < self.speed:
            self.pos = list(target)
            self.path_index += 1
        else:
            self.pos[0] += (dx/distance) * self.speed
            self.pos[1] += (dy/distance) * self.speed
    
    def reached_end(self):
        return self.path_index >= len(self.path) - 1
    
    def draw(self, screen):
        # Draw enemy body
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 15)
        
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