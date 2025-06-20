from .enemy import Enemy
import pygame
import random
import math

class TeleportingEnemy(Enemy):
    """Enemy that can teleport to avoid damage"""
    
    def __init__(self, path, wave_number=1):
        super().__init__(path, wave_number)
        self.health = 50
        self.max_health = 50
        self.speed = 1.2
        self.reward = 14
        self.color = (138, 43, 226)  # Blue violet
        
        # Teleport mechanics
        self.teleport_chance = 0.5  # 50% chance to teleport when taking damage
        self.teleport_distance = 60
        self.teleport_cooldown = 90  # 1.5 seconds (reduced from 2 seconds)
        self.teleport_timer = 0
        self.is_teleporting = False
        self.teleport_animation_timer = 0
        self.teleport_animation_duration = 20
        
        # Visual effects
        self.particles = []
        
    def update(self):
        """Update with teleport mechanics"""
        super().update()
        
        # Update timers
        self.teleport_timer += 1
        
        # Handle teleport animation
        if self.is_teleporting:
            self.teleport_animation_timer += 1
            if self.teleport_animation_timer >= self.teleport_animation_duration:
                self.is_teleporting = False
                self.teleport_animation_timer = 0
        
        # Update particles
        for particle in self.particles[:]:
            particle['life'] -= 1
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def take_damage(self, damage, tower_type: str = 'basic'):
        """Take damage with chance to teleport"""
        # Check if can teleport
        if (self.teleport_timer >= self.teleport_cooldown and 
            random.random() < self.teleport_chance):
            self.attempt_teleport()
            # Show "TELEPORT!" message briefly
            print(f"Teleporting Enemy avoided {damage} damage by teleporting!")  # Debug message
            return 0  # Avoid damage by teleporting
        
        return super().take_damage(damage, tower_type)
        
    def attempt_teleport(self):
        """Attempt to teleport along the path"""
        if len(self.path) <= 1:
            return
            
        # Calculate teleport position - jump forward along path
        current_index = self.path_index
        max_jump = min(len(self.path) - 1, current_index + 5)  # Jump up to 5 path segments
        
        # Ensure we actually move forward
        new_index = min(max_jump, len(self.path) - 1)
        
        if new_index > current_index:
            # Create teleport particles at old position
            self.create_teleport_particles(self.x, self.y)
            
            # Update position and path progress
            self.path_index = new_index
            self.x, self.y = self.path[self.path_index]
            
            # Update distance traveled appropriately
            if hasattr(self, 'distance_traveled'):
                # Approximate distance jump
                segments_jumped = new_index - current_index
                self.distance_traveled += segments_jumped * 20  # Rough estimate
            
            # Create teleport particles at new position
            self.create_teleport_particles(self.x, self.y)
            
            # Reset teleport timer
            self.teleport_timer = 0
            self.is_teleporting = True
            self.teleport_animation_timer = 0
            
    def create_teleport_particles(self, x, y):
        """Create particle effects for teleportation"""
        for _ in range(12):  # More particles for better visibility
            particle = {
                'x': x + random.randint(-15, 15),
                'y': y + random.randint(-15, 15),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 40,  # Longer lasting
                'color': (138, 43, 226)
            }
            self.particles.append(particle)
        
        # Add some bright flash particles
        for _ in range(6):
            particle = {
                'x': x + random.randint(-8, 8),
                'y': y + random.randint(-8, 8),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'life': 20,
                'color': (255, 255, 255)  # Bright white flash
            }
            self.particles.append(particle)
            
    def draw(self, screen):
        """Draw teleporting enemy with effects"""
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 30))
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            particle_color = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, particle_color, (2, 2), 2)
            screen.blit(particle_surface, (particle['x'] - 2, particle['y'] - 2))
        
        # Draw main enemy with teleport effect
        if self.is_teleporting:
            # Flickering effect during teleport
            if self.teleport_animation_timer % 4 < 2:
                alpha = 128
            else:
                alpha = 255
                
            enemy_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            enemy_color = (*self.color, alpha)
            pygame.draw.circle(enemy_surface, enemy_color, (10, 10), 8)
            screen.blit(enemy_surface, (self.x - 10, self.y - 10))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 8)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 8, 2)
        
        # Draw teleport indicator
        if self.teleport_timer >= self.teleport_cooldown:
            # Draw pulsing glow when teleport is ready
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.3 + 0.7
            glow_radius = int(12 * pulse)
            
            # Bright pulsing outline
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), glow_radius, 2)
            pygame.draw.circle(screen, (138, 43, 226), (int(self.x), int(self.y)), glow_radius + 2, 1)
            
            # Draw "T" indicator above enemy
            font = pygame.font.Font(None, 16)
            teleport_text = font.render("T", True, (255, 255, 255))
            text_rect = teleport_text.get_rect(center=(int(self.x), int(self.y - 20)))
            screen.blit(teleport_text, text_rect)
        
        # Draw health bar
        if self.health < self.max_health:
            health_percentage = self.health / self.max_health
            bar_width = 16
            bar_height = 4
            
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.x - 8, self.y - 16, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), 
                           (self.x - 8, self.y - 16, int(bar_width * health_percentage), bar_height)) 