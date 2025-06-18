from .tower import Tower
import pygame
import math

class PoisonTower(Tower):
    """Tower that applies poison damage over time, counters regenerating enemies"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage = 8  # Lower direct damage
        self.range = 120
        self.fire_rate = 40
        self.projectile_speed = 5
        self.size = 12
        self.color = (50, 205, 50)  # Lime green
        
        # Poison properties
        self.poison_damage = 3  # Damage per second
        self.poison_duration = 300  # 5 seconds
        self.splash_radius = 40
        
    def shoot(self, projectiles):
        """Shoot poison projectile"""
        if self.target:
            # Create poison splash projectile
            projectile = PoisonProjectile(
                self.x, self.y, self.target.x, self.target.y,
                self.projectile_speed, self.damage
            )
            projectile.splash_radius = self.splash_radius
            projectile.poison_damage = self.poison_damage
            projectile.poison_duration = self.poison_duration
            projectiles.append(projectile)
    
    def draw(self, screen):
        """Draw poison tower"""
        # Draw range circle
        pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw base
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw poison tanks
        tank_positions = [
            (self.x - 6, self.y - 6),
            (self.x + 6, self.y - 6),
            (self.x, self.y + 6)
        ]
        
        for tank_x, tank_y in tank_positions:
            pygame.draw.circle(screen, (0, 100, 0), (int(tank_x), int(tank_y)), 4)
            pygame.draw.circle(screen, (255, 255, 255), (int(tank_x), int(tank_y)), 4, 1)
        
        # Draw poison cloud effect
        cloud_radius = int(15 + math.sin(pygame.time.get_ticks() * 0.01) * 3)
        pygame.draw.circle(screen, (50, 205, 50), (int(self.x), int(self.y)), cloud_radius, 1)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 3)

class PoisonProjectile:
    """Poison projectile that applies poison effect"""
    
    def __init__(self, x, y, target_x, target_y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.color = (50, 205, 50)  # Green
        self.poison_damage = 3
        self.poison_duration = 300
        self.splash_radius = 40
        
        # Calculate direction
        import math
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx = self.dy = 0
        
        self.active = True
        self.should_remove = False
        
    def update(self):
        """Update projectile position"""
        if self.active:
            self.x += self.dx
            self.y += self.dy
            
            # Remove if off screen
            if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
                self.active = False
                self.should_remove = True
    
    def draw(self, screen):
        """Draw poison projectile"""
        if self.active:
            import pygame
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
            
    def check_collision(self, enemies):
        """Check collision with enemies and apply poison"""
        if not self.active:
            return
            
        import math
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.splash_radius:
                # Apply direct damage
                enemy.take_damage(self.damage)
                
                # Apply poison effect
                if not hasattr(enemy, 'poison_timer'):
                    enemy.poison_timer = 0
                    enemy.poison_damage_timer = 0
                    
                enemy.poison_timer = self.poison_duration
                enemy.poison_damage = self.poison_damage
                
                # Stop regeneration for regenerating enemies
                if hasattr(enemy, 'last_damage_time'):
                    enemy.last_damage_time = 0
                    
        self.active = False
        self.should_remove = True 