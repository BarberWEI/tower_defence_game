from .tower import Tower
import pygame
import math

class MissileTower(Tower):
    """Long-range tower that fires slow homing missiles with AOE damage"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'missile')
        self.damage = 40  # High damage
        self.range = 400  # Extremely long range - increased from 250
        self.fire_rate = 150  # Extremely slow firing (2.5 seconds at 60 FPS)
        self.projectile_speed = 3.0  # Slow missile speed
        self.size = 14
        self.color = (128, 128, 128)  # Gray
        
        # Missile properties
        self.explosion_radius = 60  # Large AOE
        self.explosion_damage = 25  # Splash damage
        self.missile_count = 2  # Fires 2 missiles at once
        
        # Can target both ground and flying enemies
        self.can_target_flying = True
        self.can_target_invisible = False
        
        # Visual effects
        self.charging = False
        self.charge_timer = 0
        self.charge_duration = 120  # 2 second charge time
        
    def can_target_enemy(self, enemy):
        """Check if this tower can target a specific enemy"""
        # Can target invisible enemies if they've been detected by a detector tower
        if hasattr(enemy, 'invisible') and enemy.invisible and not self.can_target_invisible:
            if not hasattr(enemy, 'detected_by_detector') or not enemy.detected_by_detector:
                return False
        return True
    
    def acquire_target(self, enemies):
        """Find target - prioritize enemies with most health"""
        valid_targets = []
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and self.can_target_enemy(enemy):
                valid_targets.append((enemy, distance))
        
        if valid_targets:
            # Target enemy with most health for maximum impact
            valid_targets.sort(key=lambda x: x[0].health, reverse=True)
            self.target = valid_targets[0][0]
            
            # Calculate angle to target
            if self.target:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                self.angle = math.atan2(dy, dx)
        else:
            self.target = None
    
    def update(self, enemies, projectiles):
        """Update missile tower with charging mechanism"""
        # Update fire timer
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        # Update charging
        if self.charging:
            self.charge_timer += 1
            if self.charge_timer >= self.charge_duration:
                # Fire missiles
                self.fire_missiles(projectiles)
                self.charging = False
                self.charge_timer = 0
                self.fire_timer = self.fire_rate
        
        # Find and acquire target
        self.acquire_target(enemies)
        
        # Start charging if ready and have target
        if self.target and self.fire_timer <= 0 and not self.charging:
            self.charging = True
            self.charge_timer = 0
    
    def shoot(self, projectiles):
        """This is called by the base class but we handle firing in update()"""
        pass
    
    def fire_missiles(self, projectiles):
        """Fire homing missiles"""
        if not self.target:
            return
            
        for i in range(self.missile_count):
            # Slight offset for multiple missiles
            offset_angle = (i - 0.5) * 0.3  # Spread missiles slightly
            launch_x = self.x + math.cos(self.angle + offset_angle) * 10
            launch_y = self.y + math.sin(self.angle + offset_angle) * 10
            
            missile = HomingMissile(
                launch_x, launch_y, self.target.x, self.target.y,
                self.projectile_speed, self.damage, self.explosion_radius, self.explosion_damage
            )
            missile.source_tower_id = self.tower_id
            projectiles.append(missile)
        
        # Generate currency immediately when firing
        self.generate_firing_currency()
    
    def draw(self, screen, selected: bool = False):
        """Draw missile tower"""
        # Draw range circle only when selected
        if selected:
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw charging effect
        if self.charging:
            charge_progress = self.charge_timer / self.charge_duration
            charge_radius = int(20 + 10 * charge_progress)
            charge_color = (255, int(100 + 155 * charge_progress), 0)
            
            pygame.draw.circle(screen, charge_color, (int(self.x), int(self.y)), charge_radius, 2)
            
            # Draw charge sparks
            for i in range(int(charge_progress * 8)):
                spark_angle = (i * 45) * math.pi / 180
                spark_x = self.x + math.cos(spark_angle) * charge_radius
                spark_y = self.y + math.sin(spark_angle) * charge_radius
                pygame.draw.circle(screen, (255, 255, 0), (int(spark_x), int(spark_y)), 2)
        
        # Draw main tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.size, 2)
        
        # Draw missile launchers
        launcher_positions = [
            (self.x - 8, self.y - 8),
            (self.x + 8, self.y - 8),
            (self.x - 8, self.y + 8),
            (self.x + 8, self.y + 8)
        ]
        
        for launcher_x, launcher_y in launcher_positions:
            pygame.draw.rect(screen, (100, 100, 100), 
                           (int(launcher_x - 3), int(launcher_y - 3), 6, 6))
            # Draw missile in launcher
            pygame.draw.circle(screen, (255, 0, 0), (int(launcher_x), int(launcher_y)), 2)
        
        # Draw targeting system
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y - 18)), 3)
        
        # Draw barrel pointing at target
        if self.target:
            barrel_length = self.size + 5
            end_x = self.x + math.cos(self.angle) * barrel_length
            end_y = self.y + math.sin(self.angle) * barrel_length
            pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 3)


class HomingMissile:
    """Homing missile projectile with AOE damage"""
    
    def __init__(self, x, y, target_x, target_y, speed, damage, explosion_radius, explosion_damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.explosion_radius = explosion_radius
        self.explosion_damage = explosion_damage
        self.color = (255, 100, 0)  # Orange missile
        
        # Homing properties
        self.homing_strength = 0.08  # How strongly it homes
        self.target_x = target_x
        self.target_y = target_y
        
        # Calculate initial direction
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
        self.trail_positions = []  # For visual trail
        
        # Explosion animation
        self.exploding = False
        self.explosion_timer = 0
        self.explosion_duration = 15
        self.explosion_particles = []
        
    def update(self, enemies):
        """Update missile position with homing"""
        if self.exploding:
            # Update explosion animation
            self.explosion_timer += 1
            if self.explosion_timer >= self.explosion_duration:
                self.should_remove = True
            return
            
        if not self.active:
            return
            
        # Find closest enemy to home towards
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
        
        # Update target if we found a closer enemy
        if closest_enemy:
            self.target_x = closest_enemy.x
            self.target_y = closest_enemy.y
        
        # Calculate direction to target
        target_dx = self.target_x - self.x
        target_dy = self.target_y - self.y
        target_distance = math.sqrt(target_dx**2 + target_dy**2)
        
        if target_distance > 0:
            # Normalize target direction
            target_dx /= target_distance
            target_dy /= target_distance
            
            # Apply homing
            self.dx += target_dx * self.homing_strength
            self.dy += target_dy * self.homing_strength
            
            # Normalize velocity to maintain speed
            current_speed = math.sqrt(self.dx**2 + self.dy**2)
            if current_speed > 0:
                self.dx = (self.dx / current_speed) * self.speed
                self.dy = (self.dy / current_speed) * self.speed
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Add to trail
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > 8:
            self.trail_positions.pop(0)
        
        # Check if reached target or off screen
        if target_distance < 10 or self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
            self.explode(enemies)
    
    def explode(self, enemies):
        """Create explosion and damage nearby enemies"""
        # Damage all enemies in explosion radius
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.explosion_radius:
                # Direct hit gets full damage, splash gets reduced damage
                if distance < 15:  # Direct hit
                    enemy.take_damage(self.damage, 'missile')
                else:  # Splash damage
                    enemy.take_damage(self.explosion_damage, 'missile')
        
        # Start explosion animation
        self.active = False
        self.exploding = True
        self.explosion_timer = 0
        self.create_explosion_particles()
    
    def draw(self, screen):
        """Draw missile with trail or explosion"""
        if self.exploding:
            # Draw explosion animation
            self.draw_explosion(screen)
            return
            
        if not self.active:
            return
            
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail_positions):
            alpha = (i + 1) / len(self.trail_positions)
            trail_color = (int(255 * alpha), int(100 * alpha), 0)
            pygame.draw.circle(screen, trail_color, (int(trail_x), int(trail_y)), max(1, int(3 * alpha)))
        
        # Draw missile body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 2)
        
        # Draw flame trail
        if len(self.trail_positions) > 1:
            prev_x, prev_y = self.trail_positions[-1]
            flame_x = prev_x - self.dx * 0.5
            flame_y = prev_y - self.dy * 0.5
            pygame.draw.circle(screen, (255, 0, 0), (int(flame_x), int(flame_y)), 2)
    
    def draw_explosion(self, screen):
        """Draw explosion animation with particles"""
        # Update and draw explosion particles
        for particle in self.explosion_particles[:]:
            # Update particle position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
            # Apply gravity and friction
            particle['dy'] += 0.2
            particle['dx'] *= 0.98
            
            if particle['life'] <= 0:
                self.explosion_particles.remove(particle)
                continue
            
            # Calculate alpha based on life remaining
            alpha = particle['life'] / particle['max_life']
            size = int(particle['size'] * alpha)
            
            if size > 0:
                # Draw particle with fading effect
                color = particle['color']
                faded_color = (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))
                pygame.draw.circle(screen, faded_color, (int(particle['x']), int(particle['y'])), size)
        
        # Draw explosion shockwave
        progress = self.explosion_timer / self.explosion_duration
        shockwave_radius = int(self.explosion_radius * progress)
        shockwave_alpha = int(255 * (1 - progress))
        
        if shockwave_alpha > 0 and shockwave_radius > 0:
            shockwave_color = (255, 100, 0, shockwave_alpha)
            pygame.draw.circle(screen, shockwave_color[:3], (int(self.x), int(self.y)), shockwave_radius, 3)
    
    def check_collision(self, enemies):
        """Check collision with enemies"""
        if not self.active:
            return {'hit': False, 'damage': 0, 'tower_id': None}
            
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= 8:  # Close enough for collision
                # Calculate total damage dealt in explosion
                total_damage = 0
                for enemy_in_range in enemies:
                    explosion_distance = math.sqrt((enemy_in_range.x - self.x)**2 + (enemy_in_range.y - self.y)**2)
                    if explosion_distance <= self.explosion_radius:
                        if explosion_distance < 15:  # Direct hit
                            damage_dealt = enemy_in_range.take_damage(self.damage, 'missile')
                        else:  # Splash damage
                            damage_dealt = enemy_in_range.take_damage(self.explosion_damage, 'missile')
                        total_damage += damage_dealt
                
                # Start explosion animation instead of immediate removal
                self.active = False
                self.exploding = True
                self.explosion_timer = 0
                self.create_explosion_particles()
                
                return {'hit': True, 'damage': total_damage, 'tower_id': getattr(self, 'source_tower_id', None)}
        
        return {'hit': False, 'damage': 0, 'tower_id': None}

    def create_explosion_particles(self):
        """Create explosion particle effects"""
        import random
        for _ in range(20):  # Create 20 explosion particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(8, 15),
                'max_life': 15,
                'size': random.randint(2, 6),
                'color': random.choice([(255, 100, 0), (255, 150, 0), (255, 200, 0), (255, 255, 0)])
            }
            self.explosion_particles.append(particle) 