from .enemy import Enemy
import pygame
import math
import random

class CrystalOverlord(Enemy):
    """Ultra powerful crystalline boss that reflects attacks and creates crystal structures"""
    
    def __init__(self, path, wave_number=1):
        super().__init__(path, wave_number)
        self.health = 5500
        self.max_health = 5500
        self.speed = 0.3
        self.reward = 950
        self.color = (100, 255, 255)  # Cyan crystal
        self.size = 38
        
        # Crystal abilities
        self.reflection_chance = 0.4  # 40% chance to reflect
        self.barrier_timer = 0
        self.barrier_cooldown = 540  # 9 seconds
        self.active_barriers = []
        
        # Crystal shards
        self.shard_timer = 0
        self.shard_cooldown = 360  # 6 seconds
        self.active_shards = []
        
        # Boss resistances
        self.damage_reduction = 0.7  # Takes 30% damage
        
        # Phase system
        self.phase = 1
        self.max_phases = 3
        
        # Visual effects
        self.crystal_particles = []
        self.rotation = 0
        
    def update(self):
        """Update with crystal abilities"""
        # Update phase
        health_percentage = self.health / self.max_health
        if health_percentage > 0.66:
            self.phase = 1
        elif health_percentage > 0.33:
            self.phase = 2
        else:
            self.phase = 3
            
        super().update()
        
        # Update timers
        self.barrier_timer += 1
        self.shard_timer += 1
        self.rotation += 2
        
        # Update abilities
        if self.barrier_timer >= self.barrier_cooldown:
            self.create_barrier()
        
        if self.shard_timer >= self.shard_cooldown:
            self.create_shard()
    
    def create_barrier(self):
        """Create a crystal barrier"""
        self.barrier_timer = 0
        
    def create_shard(self):
        """Create a crystal shard"""
        self.shard_timer = 0
    
    def take_damage(self, damage, tower_type: str = 'basic'):
        """Take damage with crystal resistances"""
        # Laser immunity 
        if tower_type == 'laser':
            return 0
        
        # Reflection chance
        if random.random() < self.reflection_chance:
            return -damage * 1.5  # Reflect with bonus damage
        
        # Apply damage reduction
        reduced_damage = damage * (1 - self.damage_reduction)
        actual_damage = min(reduced_damage, self.health)
        
        self.health -= reduced_damage
        return actual_damage
    
    def draw(self, screen):
        """Draw the Crystal Overlord"""
        # Draw main crystal body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 4)
        
        # Draw health bar
        bar_width = self.size * 5
        bar_height = 15
        
        pygame.draw.rect(screen, (30, 30, 30), 
                       (self.x - bar_width//2, self.y - self.size - 40, bar_width, bar_height))
        
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, self.color, 
                       (self.x - bar_width//2, self.y - self.size - 40, 
                        int(bar_width * health_percentage), bar_height))
        
        # Draw boss title
        font = pygame.font.Font(None, 32)
        title_text = font.render("CRYSTAL OVERLORD", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x, self.y - self.size - 65))
        screen.blit(title_text, title_rect) 