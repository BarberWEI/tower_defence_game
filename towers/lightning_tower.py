from .tower import Tower
import pygame
import math
import random

class LightningTower(Tower):
    """Tower that chains lightning between enemies"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'lightning')
        self.damage = 7   # Reduced damage for balance
        self.range = 120  # Medium range
        self.fire_rate = 40  # Slightly slower firing
        self.projectile_speed = 8  # Instant hit
        self.size = 12
        self.color = (255, 255, 0)  # Yellow
        
        # Lightning properties
        self.chain_count = 3  # Number of enemies to chain to
        self.chain_range = 60  # Range for chaining
        self.lightning_timer = 0
        self.lightning_duration = 8
        self.hit_enemies = []  # For visual effects
        
        # Can target flying enemies but not invisible
        self.can_target_flying = True
        self.can_target_invisible = False
    
    def can_target_enemy(self, enemy):
        """Check if this tower can target a specific enemy"""
        # Can target invisible enemies if they've been detected by a detector tower
        if hasattr(enemy, 'invisible') and enemy.invisible and not self.can_target_invisible:
            if not hasattr(enemy, 'detected_by_detector') or not enemy.detected_by_detector:
                return False
            
        return True
    
    def acquire_target(self, enemies):
        """Find target - prioritize enemies with many nearby targets for chaining"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                # Count nearby enemies for chain potential
                nearby_count = 0
                for other_enemy in enemies:
                    if self.can_target_enemy(other_enemy) and other_enemy != enemy:
                        chain_distance = math.sqrt((enemy.x - other_enemy.x)**2 + (enemy.y - other_enemy.y)**2)
                        if chain_distance <= self.chain_range:
                            nearby_count += 1
                
                valid_targets.append((enemy, distance, nearby_count))
        
        if valid_targets:
            # Target enemy with most chain potential
            valid_targets.sort(key=lambda x: x[2], reverse=True)
            self.target = valid_targets[0][0]
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
    
    def shoot(self, projectiles):
        """Fire lightning that chains between enemies"""
        # Note: This tower doesn't use projectiles, it directly damages enemies
        # The actual lightning will be fired through the update method
        pass
    
    def fire_lightning_chain(self, enemies, hit_enemies):
        """Create lightning chain effect"""
        if not enemies:
            return
            
        current_enemy = enemies[0]
        current_enemy.take_damage(self.damage)
        hit_enemies.append(current_enemy)
        
        # Visual effect
        self.lightning_timer = self.lightning_duration
        self.hit_enemies = hit_enemies.copy()
        
        # Find next enemy to chain to
        if len(hit_enemies) < self.chain_count:
            next_targets = []
            for enemy in enemies:
                if enemy not in hit_enemies and self.can_target_enemy(enemy):
                    distance = math.sqrt((current_enemy.x - enemy.x)**2 + (current_enemy.y - enemy.y)**2)
                    if distance <= self.chain_range:
                        next_targets.append((enemy, distance))
            
            if next_targets:
                # Chain to closest enemy
                next_targets.sort(key=lambda x: x[1])
                next_enemy = next_targets[0][0]
                # Recursive chain
                self.fire_lightning_chain([next_enemy], hit_enemies)
    
    def update(self, enemies, projectiles):
        """Update lightning tower"""
        # Update fire timer
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Fire lightning if ready and have target
        if self.target and self.fire_timer <= 0:
            self.fire_lightning_chain([self.target], [])
            self.fire_timer = self.fire_rate
        
        # Update lightning timer
        if self.lightning_timer > 0:
            self.lightning_timer -= 1
    
    def draw(self, screen, selected: bool = False):
        """Draw lightning tower"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw lightning effects
        if self.lightning_timer > 0 and len(self.hit_enemies) > 1:
            for i in range(len(self.hit_enemies) - 1):
                start_pos = (int(self.hit_enemies[i].x), int(self.hit_enemies[i].y))
                end_pos = (int(self.hit_enemies[i + 1].x), int(self.hit_enemies[i + 1].y))
                
                # Draw jagged lightning bolt
                self.draw_lightning_bolt(screen, start_pos, end_pos)
        
        # Draw main tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw tesla coil
        coil_height = 8
        for i in range(3):
            y_offset = -coil_height + i * 3
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y + y_offset)), 2)
        
        # Draw electrical sparks
        if random.random() < 0.3:  # Random sparks
            spark_x = self.x + random.randint(-8, 8)
            spark_y = self.y + random.randint(-8, 8)
            pygame.draw.circle(screen, (255, 255, 255), (int(spark_x), int(spark_y)), 1)
    
    def draw_lightning_bolt(self, screen, start_pos, end_pos):
        """Draw a jagged lightning bolt between two points"""
        segments = 5
        points = [start_pos]
        
        dx = (end_pos[0] - start_pos[0]) / segments
        dy = (end_pos[1] - start_pos[1]) / segments
        
        for i in range(1, segments):
            x = start_pos[0] + dx * i + random.randint(-10, 10)
            y = start_pos[1] + dy * i + random.randint(-10, 10)
            points.append((int(x), int(y)))
        
        points.append(end_pos)
        
        # Draw lightning segments
        for i in range(len(points) - 1):
            pygame.draw.line(screen, (255, 255, 255), points[i], points[i + 1], 3)
            pygame.draw.line(screen, (255, 255, 0), points[i], points[i + 1], 1)
