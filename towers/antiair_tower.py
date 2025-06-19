from .tower import Tower
import pygame
import math

class AntiAirTower(Tower):
    """Tower specialized for targeting flying enemies"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'antiair')
        self.damage = 20
        self.range = 180
        self.fire_rate = 50  # Medium fire rate
        self.projectile_speed = 5.0
        self.size = 12
        self.color = (0, 191, 255)  # Deep sky blue
        
        # Anti-air properties
        self.prioritize_flying = True
        self.can_target_flying = True
        self.can_target_invisible = False
        
        # Finalize initialization to update base stats
        self.finalize_initialization()
    
    def can_target_enemy(self, enemy):
        """Check if this tower can target a specific enemy"""
        # Can target invisible enemies if they've been detected by a detector tower
        if hasattr(enemy, 'invisible') and enemy.invisible and not self.can_target_invisible:
            if not hasattr(enemy, 'detected_by_detector') or not enemy.detected_by_detector:
                return False
        return True
    
    def acquire_target(self, enemies):
        """Find target, prioritizing flying enemies"""
        flying_targets = []
        ground_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                if hasattr(enemy, 'flying') and enemy.flying:
                    flying_targets.append((enemy, distance))
                else:
                    ground_targets.append((enemy, distance))
        
        # Prioritize flying enemies
        if flying_targets:
            flying_targets.sort(key=lambda x: x[1])
            self.target = flying_targets[0][0]
        elif ground_targets:
            # Can hit ground enemies too, but with lower priority
            ground_targets.sort(key=lambda x: x[1])
            self.target = ground_targets[0][0]
        else:
            self.target = None
        
        # Calculate angle to target
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.atan2(dy, dx)
    
    def shoot(self, projectiles):
        """Fire homing missile at targets"""
        if self.target:
            try:
                from projectiles import HomingProjectile
                
                missile = HomingProjectile(
                    self.x, self.y, self.target.x, self.target.y,
                    self.projectile_speed, self.damage, self.tower_type
                )
                missile.target_enemy = self.target
                
                # Link projectile to tower for damage tracking
                missile.source_tower_id = self.tower_id
                projectiles.append(missile)
                
                # Generate currency immediately when firing
                self.generate_firing_currency()
            except Exception:
                # Fallback to basic projectile
                from projectiles import BasicProjectile
                projectile = BasicProjectile(
                    self.x, self.y, self.target.x, self.target.y,
                    self.projectile_speed, self.damage, self.tower_type
                )
                projectile.source_tower_id = self.tower_id
                projectiles.append(projectile)
                self.generate_firing_currency()
    
    def draw(self, screen, selected: bool = False):
        """Draw anti-air tower"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw base
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw missile launcher
        launcher_points = [
            (self.x - 8, self.y - 8),
            (self.x + 8, self.y - 8),
            (self.x + 8, self.y - 4),
            (self.x - 8, self.y - 4)
        ]
        pygame.draw.polygon(screen, (100, 100, 100), launcher_points)
        
        # Draw missiles in launcher
        for i in range(3):
            missile_x = self.x - 6 + i * 4
            missile_y = self.y - 6
            pygame.draw.circle(screen, (255, 0, 0), (int(missile_x), int(missile_y)), 2)
        
        # Draw targeting radar
        radar_center = (self.x, self.y - 15)
        pygame.draw.circle(screen, (0, 255, 0), radar_center, 4)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 3) 