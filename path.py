import pygame
import random
import math

class Path:
    def __init__(self, difficulty=0.5):
        self.difficulty = max(0, min(1, difficulty))  # Clamp between 0 and 1
        self.points = self.generate_path()
        self.path_width = 40  # Width of the path for collision detection
    
    def generate_path(self):
        # Base path points
        base_points = [
            (0, 300),      # Start
            (800, 300)     # End
        ]
        
        if self.difficulty < 0.2:
            # Simple straight path
            return base_points
        
        # Calculate number of turns based on difficulty
        num_turns = int(self.difficulty * 5) + 1  # 1 to 6 turns
        
        # Generate intermediate points
        points = [base_points[0]]  # Start with the first point
        
        # Define possible path segments
        segments = [
            # Horizontal segments
            lambda x, y: [(x + 200, y)],
            # Vertical segments
            lambda x, y: [(x, y - 200)],
            lambda x, y: [(x, y + 200)],
            # Diagonal segments (for higher difficulty)
            lambda x, y: [(x + 150, y - 150)],
            lambda x, y: [(x + 150, y + 150)]
        ]
        
        current_x, current_y = base_points[0]
        target_x, target_y = base_points[1]
        
        # Generate path segments
        for i in range(num_turns):
            # Choose segment type based on difficulty
            if self.difficulty > 0.7 and random.random() < self.difficulty:
                # Use diagonal segments for higher difficulty
                segment = random.choice(segments[3:])
            else:
                # Use basic segments
                segment = random.choice(segments[:3])
            
            # Add new points
            new_points = segment(current_x, current_y)
            points.extend(new_points)
            current_x, current_y = new_points[-1]
        
        # Add final point
        points.append(base_points[1])
        
        # Ensure path stays within screen bounds
        points = self.adjust_points_to_bounds(points)
        
        return points
    
    def adjust_points_to_bounds(self, points):
        # Screen bounds
        min_x, max_x = 0, 800
        min_y, max_y = 0, 600
        
        adjusted_points = []
        for x, y in points:
            # Clamp coordinates to screen bounds
            x = max(min_x, min(max_x, x))
            y = max(min_y, min(max_y, y))
            adjusted_points.append((x, y))
        
        return adjusted_points
    
    def is_point_on_path(self, point, tolerance=20):
        """
        Check if a point is on or near the path.
        Args:
            point: (x, y) tuple of the point to check
            tolerance: How close to the path the point needs to be
        Returns:
            bool: True if the point is on/near the path, False otherwise
        """
        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i + 1]
            
            # Calculate distance from point to line segment
            distance = self.point_to_line_distance(point, start, end)
            if distance <= tolerance:
                return True
        return False
    
    def point_to_line_distance(self, point, line_start, line_end):
        """
        Calculate the distance from a point to a line segment.
        """
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Calculate the length of the line segment
        line_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if line_length == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        
        # Calculate the distance
        t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (line_length ** 2)))
        projection_x = x1 + t * (x2 - x1)
        projection_y = y1 + t * (y2 - y1)
        
        return math.sqrt((x - projection_x) ** 2 + (y - projection_y) ** 2)
    
    def draw(self, screen):
        # Draw the path
        for i in range(len(self.points) - 1):
            pygame.draw.line(screen, (100, 100, 100),
                           self.points[i], self.points[i + 1], self.path_width)
        
        # Draw start and end points
        pygame.draw.circle(screen, (0, 255, 0), self.points[0], 10)  # Start
        pygame.draw.circle(screen, (255, 0, 0), self.points[-1], 10)  # End 