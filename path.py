import pygame

class Path:
    def __init__(self):
        # Define a simple path for enemies to follow
        self.points = [
            (0, 300),      # Start
            (200, 300),    # First turn
            (200, 100),    # Second turn
            (400, 100),    # Third turn
            (400, 500),    # Fourth turn
            (600, 500),    # Fifth turn
            (600, 300),    # Sixth turn
            (800, 300)     # End
        ]
    
    def draw(self, screen):
        # Draw the path
        for i in range(len(self.points) - 1):
            pygame.draw.line(screen, (100, 100, 100),
                           self.points[i], self.points[i + 1], 40)
        
        # Draw start and end points
        pygame.draw.circle(screen, (0, 255, 0), self.points[0], 10)  # Start
        pygame.draw.circle(screen, (255, 0, 0), self.points[-1], 10)  # End 