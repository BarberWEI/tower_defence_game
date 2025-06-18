from .tower import Tower
import pygame
import math

class DetectorTower(Tower):
    """Tower that can detect invisible enemies and has long range"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage = 15
        self.range = 200  # Very long range
        self.fire_rate = 45  # Moderate fire rate
        self.projectile_speed = 6
        self.size = 12
        self.color = (255, 255, 0)  # Yellow
        self.detection_range = 250  # Even longer detection range
        
        # Detection properties
        self.detected_enemies = set()  # Track detected invisible enemies
        self.detection_pulse_timer = 0
        
    def update(self, enemies, projectiles):
        """Update with detection capabilities"""
        super().update(enemies, projectiles)
        
        # Update detection pulse
        self.detection_pulse_timer += 0.1
        
        # Detect invisible enemies
        self.detected_enemies.clear()
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.detection_range:
                if hasattr(enemy, 'invisible') and enemy.invisible:
                    self.detected_enemies.add(enemy)
    
    def can_target_enemy(self, enemy):
        """Check if this tower can target an enemy"""
        # Can always target regular enemies
        if not hasattr(enemy, 'invisible') or not enemy.invisible:
            return True
            
        # Can target invisible enemies within detection range
        distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
        return distance <= self.detection_range
    
    def acquire_target(self, enemies):
        """Find target with detection capabilities"""
        targets_in_range = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                targets_in_range.append((enemy, distance))
        
        if targets_in_range:
            # Target closest enemy
            targets_in_range.sort(key=lambda x: x[1])
            self.target = targets_in_range[0][0]
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
    
    def shoot(self, projectiles):
        """Shoot at target"""
        if self.target:
            from projectiles import BasicProjectile
            projectile = BasicProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage
            )
            projectile.color = (255, 255, 0)  # Yellow projectile
            projectiles.append(projectile)
    
    def draw(self, screen):
        """Draw detector tower with detection effects"""
        # Draw range circle
        pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw detection pulse
        pulse_radius = int(30 + 10 * math.sin(self.detection_pulse_timer))
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), pulse_radius, 1)
        
        # Draw main tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw radar dish
        dish_points = []
        for i in range(8):
            angle = (i * 45) * math.pi / 180
            dish_x = self.x + math.cos(angle) * 8
            dish_y = self.y + math.sin(angle) * 8
            dish_points.append((dish_x, dish_y))
        
        if len(dish_points) >= 3:
            pygame.draw.polygon(screen, (200, 200, 200), dish_points)
        
        # Draw detection lines to invisible enemies
        for enemy in self.detected_enemies:
            pygame.draw.line(screen, (255, 255, 0), 
                           (int(self.x), int(self.y)), (int(enemy.x), int(enemy.y)), 1)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 3) 