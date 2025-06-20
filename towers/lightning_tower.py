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
        self.fire_rate = 120  # Much slower firing (2 seconds at 60 FPS)
        self.projectile_speed = 8  # Instant hit
        self.size = 12
        self.color = (255, 255, 0)  # Yellow
        
        # Lightning properties
        self.chain_count = 3  # Number of enemies to chain to
        self.chain_range = 60  # Range for chaining
        self.lightning_timer = 0
        self.lightning_duration = 15  # Longer duration for better visibility
        self.chain_sequence = []  # Store the full chain sequence for visuals
        self.charging_timer = 0  # Pre-fire charging effect
        self.charging_duration = 30  # Longer charge time for more dramatic effect
        
        # Visual effects
        self.spark_effects = []
        self.screen_flash_timer = 0
        self.potential_chain = []  # Store potential chain for targeting preview
        
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
            
            # Build potential chain for preview
            self.potential_chain = self.build_chain_sequence(enemies, self.target)
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
            self.potential_chain = []
    
    def shoot(self, projectiles):
        """Fire lightning that chains between enemies"""
        # Note: This tower doesn't use projectiles, it directly damages enemies
        # The actual lightning will be fired through the update method
        pass
    
    def build_chain_sequence(self, enemies, start_enemy):
        """Build the complete chain sequence for visual effects"""
        chain_sequence = [start_enemy]
        hit_enemies = {start_enemy}
        current_enemy = start_enemy
        
        # Build the chain
        for _ in range(self.chain_count - 1):
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
                chain_sequence.append(next_enemy)
                hit_enemies.add(next_enemy)
                current_enemy = next_enemy
            else:
                break
        
        return chain_sequence
    
    def fire_lightning_chain(self, enemies):
        """Fire lightning and build chain sequence"""
        if not enemies or not self.target:
            return 0
        
        # Build the complete chain sequence
        self.chain_sequence = self.build_chain_sequence(enemies, self.target)
        
        total_damage = 0
        
        # Apply damage to all enemies in chain
        for i, enemy in enumerate(self.chain_sequence):
            # Calculate damage based on wet status and chain position
            damage = self.damage
            if hasattr(enemy, 'wet') and enemy.wet:
                damage = int(damage * enemy.lightning_damage_multiplier)
            
            # Reduce damage for each chain hop
            chain_multiplier = 0.8 ** i  # 80% damage for each hop
            final_damage = int(damage * chain_multiplier)
            
            actual_damage = enemy.take_damage(final_damage, 'lightning')
            total_damage += actual_damage
        
        # Visual effects
        self.lightning_timer = self.lightning_duration
        self.screen_flash_timer = 3  # Brief screen flash
        self.create_spark_effects()
        
        return total_damage
    
    def create_spark_effects(self):
        """Create spark particle effects"""
        self.spark_effects = []
        
        # Add sparks around tower
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 20)
            spark_x = self.x + math.cos(angle) * distance
            spark_y = self.y + math.sin(angle) * distance
            velocity_x = random.uniform(-2, 2)
            velocity_y = random.uniform(-2, 2)
            
            spark = {
                'x': spark_x,
                'y': spark_y,
                'vx': velocity_x,
                'vy': velocity_y,
                'life': 15,
                'max_life': 15
            }
            self.spark_effects.append(spark)
        
        # Add sparks around each enemy in chain
        for enemy in self.chain_sequence:
            for _ in range(6):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(5, 15)
                spark_x = enemy.x + math.cos(angle) * distance
                spark_y = enemy.y + math.sin(angle) * distance
                velocity_x = random.uniform(-1.5, 1.5)
                velocity_y = random.uniform(-1.5, 1.5)
                
                spark = {
                    'x': spark_x,
                    'y': spark_y,
                    'vx': velocity_x,
                    'vy': velocity_y,
                    'life': 12,
                    'max_life': 12
                }
                self.spark_effects.append(spark)
    
    def update_spark_effects(self):
        """Update spark particle effects"""
        for spark in self.spark_effects[:]:
            spark['x'] += spark['vx']
            spark['y'] += spark['vy']
            spark['life'] -= 1
            
            # Fade and slow down over time
            spark['vx'] *= 0.95
            spark['vy'] *= 0.95
            
            if spark['life'] <= 0:
                self.spark_effects.remove(spark)
    
    def update(self, enemies, projectiles):
        """Update lightning tower"""
        # Update fire timer
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        # Update charging timer
        if self.charging_timer > 0:
            self.charging_timer -= 1
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Start charging if ready and have target
        if self.target and self.fire_timer <= 0 and self.charging_timer <= 0:
            self.charging_timer = self.charging_duration
        
        # Fire lightning when charging is complete
        if self.charging_timer == 1 and self.target:  # Fire on last frame of charging
            damage_dealt = self.fire_lightning_chain(enemies)
            if damage_dealt > 0:
                self.add_damage_dealt(damage_dealt)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
            
            self.fire_timer = self.fire_rate
        
        # Update visual effect timers
        if self.lightning_timer > 0:
            self.lightning_timer -= 1
        
        if self.screen_flash_timer > 0:
            self.screen_flash_timer -= 1
        
        # Update spark effects
        self.update_spark_effects()
    
    def update_with_speed(self, enemies, projectiles, speed_multiplier: float):
        """Update lightning tower with speed multiplier for performance optimization"""
        # Update fire timer with speed multiplier
        if self.fire_timer > 0:
            self.fire_timer -= speed_multiplier
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Start charging if ready and have target
        if self.target and self.fire_timer <= 0 and self.charging_timer <= 0:
            self.charging_timer = self.charging_duration
        
        # Fire lightning when charging is complete
        if self.charging_timer > 0 and self.charging_timer <= speed_multiplier and self.target:  # Fire when charging completes this frame
            damage_dealt = self.fire_lightning_chain(enemies)
            if damage_dealt > 0:
                self.add_damage_dealt(damage_dealt)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
            
            self.fire_timer = self.fire_rate
            self.charging_timer = 0  # Reset charging
        
        # Update charging timer with speed multiplier (after firing check)
        if self.charging_timer > 0:
            self.charging_timer -= speed_multiplier
        
        # Update visual effect timers with speed multiplier
        if self.lightning_timer > 0:
            self.lightning_timer -= speed_multiplier
        
        if self.screen_flash_timer > 0:
            self.screen_flash_timer -= speed_multiplier
        
        # Update spark effects (faster at higher speeds)
        for _ in range(int(speed_multiplier)):
            self.update_spark_effects()
    
    def update_with_speed_optimized(self, enemies, projectiles, speed_multiplier: float):
        """Update lightning tower with speed multiplier and optimizations"""
        # Update fire timer with speed multiplier
        if self.fire_timer > 0:
            self.fire_timer -= speed_multiplier
        
        # Find and acquire target with optimizations
        self.acquire_target_optimized(enemies)
        
        # Start charging if ready and have target
        if self.target and self.fire_timer <= 0 and self.charging_timer <= 0:
            self.charging_timer = self.charging_duration
        
        # Fire lightning when charging is complete
        if self.charging_timer > 0 and self.charging_timer <= speed_multiplier and self.target:  # Fire when charging completes this frame
            damage_dealt = self.fire_lightning_chain(enemies)
            if damage_dealt > 0:
                self.add_damage_dealt(damage_dealt)
            
            # Generate currency immediately when firing
            self.generate_firing_currency()
            
            self.fire_timer = self.fire_rate
            self.charging_timer = 0  # Reset charging
        
        # Update charging timer with speed multiplier (after firing check)
        if self.charging_timer > 0:
            self.charging_timer -= speed_multiplier
        
        # Update visual effect timers with speed multiplier
        if self.lightning_timer > 0:
            self.lightning_timer -= speed_multiplier
        
        if self.screen_flash_timer > 0:
            self.screen_flash_timer -= speed_multiplier
        
        # Update spark effects (faster at higher speeds)
        for _ in range(int(speed_multiplier)):
            self.update_spark_effects()
    
    def acquire_target_optimized(self, enemies):
        """Optimized targeting for lightning tower using squared distance"""
        if not enemies:
            self.target = None
            self.potential_chain = []
            return
        
        range_squared = self.range * self.range
        valid_targets = []
        
        # Use squared distance for initial filtering (avoids sqrt)
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance_squared = dx * dx + dy * dy
            
            if distance_squared <= range_squared and self.can_target_enemy(enemy):
                # Only calculate actual distance for valid targets
                actual_distance = math.sqrt(distance_squared)
                
                # Count nearby enemies for chain potential (using squared distance)
                nearby_count = 0
                chain_range_squared = self.chain_range * self.chain_range
                for other_enemy in enemies:
                    if self.can_target_enemy(other_enemy) and other_enemy != enemy:
                        other_dx = enemy.x - other_enemy.x
                        other_dy = enemy.y - other_enemy.y
                        other_distance_squared = other_dx * other_dx + other_dy * other_dy
                        if other_distance_squared <= chain_range_squared:
                            nearby_count += 1
                
                valid_targets.append((enemy, actual_distance, nearby_count))
                
                # Early termination for performance
                if len(valid_targets) >= 10:
                    break
        
        if valid_targets:
            # Target enemy with most chain potential
            valid_targets.sort(key=lambda x: x[2], reverse=True)
            self.target = valid_targets[0][0]
            
            # Build potential chain for preview
            self.potential_chain = self.build_chain_sequence(enemies, self.target)
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
            self.potential_chain = []
    
    def draw(self, screen, selected: bool = False):
        """Draw lightning tower with enhanced effects"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
            # Also show chain range around current target
            if self.target:
                pygame.draw.circle(screen, (255, 255, 100), (int(self.target.x), int(self.target.y)), int(self.chain_range), 1)
        
        # Draw charging effect
        if self.charging_timer > 0:
            charge_intensity = 1.0 - (self.charging_timer / self.charging_duration)
            self.draw_charging_effect(screen, charge_intensity)
        
        # Draw lightning chain effects
        if self.lightning_timer > 0 and self.chain_sequence:
            self.draw_lightning_chain(screen)
        
        # Draw target indicators
        if self.target and self.lightning_timer <= 0:
            self.draw_target_indicators(screen)
        
        # Draw main tower
        tower_color = self.color
        if self.charging_timer > 0:
            # Pulse white while charging
            intensity = 1.0 - (self.charging_timer / self.charging_duration)
            white_amount = int(255 * intensity * 0.5)
            tower_color = tuple(min(255, c + white_amount) for c in self.color)
        
        pygame.draw.circle(screen, tower_color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw tesla coil
        coil_height = 8
        for i in range(3):
            y_offset = -coil_height + i * 3
            coil_color = (200, 200, 200)
            if self.charging_timer > 0:
                # Brighten coil while charging
                coil_color = (255, 255, 255)
            pygame.draw.circle(screen, coil_color, (int(self.x), int(self.y + y_offset)), 2)
        
        # Draw spark effects
        self.draw_spark_effects(screen)
        
        # Draw electrical sparks around tower
        if random.random() < 0.2 or self.charging_timer > 0:  # More frequent when charging
            for _ in range(2 if self.charging_timer > 0 else 1):
                spark_x = self.x + random.randint(-10, 10)
                spark_y = self.y + random.randint(-10, 10)
                pygame.draw.circle(screen, (255, 255, 255), (int(spark_x), int(spark_y)), 1)
        
        # Draw upgrade indicator if available
        self.draw_upgrade_indicator(screen)
    
    def draw_charging_effect(self, screen, intensity):
        """Draw charging up effect before firing"""
        if self.target:
            # Draw energy gathering lines from around tower to center
            for i in range(8):
                angle = (i / 8) * 2 * math.pi + (pygame.time.get_ticks() * 0.02)
                start_radius = 20
                end_radius = 5
                
                start_x = self.x + math.cos(angle) * start_radius
                start_y = self.y + math.sin(angle) * start_radius
                end_x = self.x + math.cos(angle) * end_radius
                end_y = self.y + math.sin(angle) * end_radius
                
                alpha = int(255 * intensity)
                color = (255, 255, 255, alpha)
                
                # Create gradient effect
                for j in range(3):
                    mid_x = start_x + (end_x - start_x) * (j / 3)
                    mid_y = start_y + (end_y - start_y) * (j / 3)
                    thickness = 3 - j
                    if thickness > 0:
                        pygame.draw.line(screen, (255, 255, 200), 
                                       (int(start_x), int(start_y)), 
                                       (int(mid_x), int(mid_y)), thickness)
    
    def draw_target_indicators(self, screen):
        """Draw indicators showing chain targets"""
        if not self.target or not self.potential_chain:
            return
        
        # Draw targeting indicators for all enemies in potential chain
        for i, enemy in enumerate(self.potential_chain):
            if hasattr(enemy, 'x'):  # Make sure enemy still exists
                # Draw pulsing target indicator
                pulse = math.sin(pygame.time.get_ticks() * 0.01 + i * 0.5) * 0.3 + 0.7
                radius = int((enemy.size + 8) * pulse)
                
                # Different colors for chain order
                if i == 0:
                    color = (255, 255, 100)  # Yellow for primary target
                elif i == 1:
                    color = (255, 200, 100)  # Orange for secondary
                else:
                    color = (255, 150, 100)  # Red for tertiary+
                
                pygame.draw.circle(screen, color, (int(enemy.x), int(enemy.y)), radius, 2)
                
                # Draw chain order number
                font = pygame.font.Font(None, 16)
                text = font.render(str(i + 1), True, color)
                text_rect = text.get_rect(center=(int(enemy.x), int(enemy.y - enemy.size - 15)))
                screen.blit(text, text_rect)
        
        # Draw targeting line from tower to first target
        if len(self.potential_chain) > 0:
            pygame.draw.line(screen, (255, 255, 150), 
                            (int(self.x), int(self.y)), 
                            (int(self.potential_chain[0].x), int(self.potential_chain[0].y)), 1)
        
        # Draw chain preview lines between targets
        for i in range(len(self.potential_chain) - 1):
            start_enemy = self.potential_chain[i]
            end_enemy = self.potential_chain[i + 1]
            if hasattr(start_enemy, 'x') and hasattr(end_enemy, 'x'):
                # Draw faint chain preview line
                chain_color = (200, 200, 100, 128)  # Semi-transparent yellow
                pygame.draw.line(screen, (200, 200, 100), 
                               (int(start_enemy.x), int(start_enemy.y)), 
                               (int(end_enemy.x), int(end_enemy.y)), 1)
    
    def draw_lightning_chain(self, screen):
        """Draw the full lightning chain effect"""
        if not self.chain_sequence:
            return
        
        # Draw lightning from tower to first enemy
        if len(self.chain_sequence) > 0:
            start_pos = (int(self.x), int(self.y))
            end_pos = (int(self.chain_sequence[0].x), int(self.chain_sequence[0].y))
            self.draw_lightning_bolt(screen, start_pos, end_pos, thickness=4)
        
        # Draw lightning between chained enemies
        for i in range(len(self.chain_sequence) - 1):
            if hasattr(self.chain_sequence[i], 'x') and hasattr(self.chain_sequence[i + 1], 'x'):
                start_pos = (int(self.chain_sequence[i].x), int(self.chain_sequence[i].y))
                end_pos = (int(self.chain_sequence[i + 1].x), int(self.chain_sequence[i + 1].y))
                
                # Make subsequent chains slightly thinner
                thickness = 4 - i
                self.draw_lightning_bolt(screen, start_pos, end_pos, max(1, thickness))
    
    def draw_lightning_bolt(self, screen, start_pos, end_pos, thickness=3):
        """Draw a jagged lightning bolt between two points"""
        distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        segments = max(3, int(distance / 20))  # More segments for longer bolts
        points = [start_pos]
        
        dx = (end_pos[0] - start_pos[0]) / segments
        dy = (end_pos[1] - start_pos[1]) / segments
        
        # Create jagged path
        for i in range(1, segments):
            # Random deviation based on distance from endpoints
            max_deviation = min(20, distance / 10)
            deviation = random.randint(-int(max_deviation), int(max_deviation))
            
            # Perpendicular offset
            perpendicular_angle = math.atan2(dy, dx) + math.pi / 2
            offset_x = math.cos(perpendicular_angle) * deviation
            offset_y = math.sin(perpendicular_angle) * deviation
            
            x = start_pos[0] + dx * i + offset_x
            y = start_pos[1] + dy * i + offset_y
            points.append((int(x), int(y)))
        
        points.append(end_pos)
        
        # Draw lightning with multiple layers for glow effect
        colors_and_thickness = [
            ((100, 100, 255), thickness + 3),  # Blue outer glow
            ((200, 200, 255), thickness + 1),  # Light blue
            ((255, 255, 255), thickness),      # White core
        ]
        
        for color, thick in colors_and_thickness:
            for i in range(len(points) - 1):
                pygame.draw.line(screen, color, points[i], points[i + 1], thick)
        
        # Add some random branches
        if len(points) > 3:
            branch_point = points[len(points) // 2]
            branch_length = 15
            for _ in range(2):
                branch_angle = random.uniform(0, 2 * math.pi)
                branch_end = (
                    int(branch_point[0] + math.cos(branch_angle) * branch_length),
                    int(branch_point[1] + math.sin(branch_angle) * branch_length)
                )
                pygame.draw.line(screen, (255, 255, 255), branch_point, branch_end, 1)
    
    def draw_spark_effects(self, screen):
        """Draw spark particle effects"""
        for spark in self.spark_effects:
            if spark['life'] > 0:
                # Calculate alpha based on remaining life
                alpha = spark['life'] / spark['max_life']
                size = max(1, int(3 * alpha))
                
                # Color transitions from white to yellow to red
                if alpha > 0.7:
                    color = (255, 255, 255)  # White
                elif alpha > 0.3:
                    color = (255, 255, 100)  # Yellow
                else:
                    color = (255, 100, 100)  # Red
                
                pygame.draw.circle(screen, color, (int(spark['x']), int(spark['y'])), size)
