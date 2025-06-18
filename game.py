import pygame
import sys
import math
from typing import List, Tuple
from enemies import Enemy, BasicEnemy, FastEnemy, TankEnemy
from towers import Tower, BasicTower, SniperTower, FreezerTower
from projectiles import Projectile

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.running = True
        self.paused = False
        self.money = 100
        self.lives = 20
        self.wave_number = 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 10
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between enemy spawns
        
        # Game objects
        self.enemies: List[Enemy] = []
        self.towers: List[Tower] = []
        self.projectiles: List[Projectile] = []
        
        # Path for enemies to follow
        self.path = [
            (0, 400), (200, 400), (200, 200), (400, 200),
            (400, 600), (600, 600), (600, 100), (800, 100),
            (800, 500), (1000, 500), (1000, 300), (1200, 300)
        ]
        
        # Selected tower type for placing
        self.selected_tower_type = None
        self.placing_tower = False
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.BROWN = (139, 69, 19)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_1:
                    self.selected_tower_type = "basic"
                    self.placing_tower = True
                elif event.key == pygame.K_2:
                    self.selected_tower_type = "sniper"
                    self.placing_tower = True
                elif event.key == pygame.K_3:
                    self.selected_tower_type = "freezer"
                    self.placing_tower = True
                elif event.key == pygame.K_ESCAPE:
                    self.placing_tower = False
                    self.selected_tower_type = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.placing_tower:  # Left click
                    self.place_tower(event.pos)
    
    def place_tower(self, pos: Tuple[int, int]):
        x, y = pos
        
        # Check if position is valid (not on path, not too close to other towers)
        if self.is_valid_tower_position(x, y):
            tower_cost = self.get_tower_cost(self.selected_tower_type)
            if self.money >= tower_cost:
                if self.selected_tower_type == "basic":
                    tower = BasicTower(x, y)
                elif self.selected_tower_type == "sniper":
                    tower = SniperTower(x, y)
                elif self.selected_tower_type == "freezer":
                    tower = FreezerTower(x, y)
                
                self.towers.append(tower)
                self.money -= tower_cost
                self.placing_tower = False
                self.selected_tower_type = None
    
    def is_valid_tower_position(self, x: int, y: int) -> bool:
        # Check if too close to path
        for path_x, path_y in self.path:
            if math.sqrt((x - path_x)**2 + (y - path_y)**2) < 50:
                return False
        
        # Check if too close to other towers
        for tower in self.towers:
            if math.sqrt((x - tower.x)**2 + (y - tower.y)**2) < 40:
                return False
        
        return True
    
    def get_tower_cost(self, tower_type: str) -> int:
        costs = {"basic": 20, "sniper": 50, "freezer": 30}
        return costs.get(tower_type, 0)
    
    def spawn_enemies(self):
        if self.enemies_spawned < self.enemies_per_wave:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                # Spawn different enemy types based on wave
                if self.wave_number <= 3:
                    enemy = BasicEnemy(self.path)
                elif self.wave_number <= 6:
                    if self.enemies_spawned % 3 == 0:
                        enemy = FastEnemy(self.path)
                    else:
                        enemy = BasicEnemy(self.path)
                else:
                    enemy_type = self.enemies_spawned % 3
                    if enemy_type == 0:
                        enemy = TankEnemy(self.path)
                    elif enemy_type == 1:
                        enemy = FastEnemy(self.path)
                    else:
                        enemy = BasicEnemy(self.path)
                
                self.enemies.append(enemy)
                self.enemies_spawned += 1
                self.spawn_timer = 0
        elif len(self.enemies) == 0:
            # Start next wave
            self.wave_number += 1
            self.enemies_spawned = 0
            self.enemies_per_wave += 2
            self.money += 50  # Bonus money for completing wave
    
    def update(self):
        if self.paused:
            return
        
        # Spawn enemies
        self.spawn_enemies()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
            elif enemy.health <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)
        
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies, self.projectiles)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Check projectile collisions with enemies
            if hasattr(projectile, 'check_collision'):
                projectile.check_collision(self.enemies)
            
            # Handle homing projectiles
            if hasattr(projectile, 'update_homing'):
                projectile.update_homing(self.enemies)
            
            if projectile.should_remove:
                self.projectiles.remove(projectile)
        
        # Check game over
        if self.lives <= 0:
            print(f"Game Over! You reached wave {self.wave_number}")
            self.running = False
    
    def draw_path(self):
        if len(self.path) > 1:
            pygame.draw.lines(self.screen, self.BROWN, False, self.path, 20)
    
    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        
        # Game stats
        money_text = font.render(f"Money: ${self.money}", True, self.BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, self.BLACK)
        wave_text = font.render(f"Wave: {self.wave_number}", True, self.BLACK)
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(wave_text, (10, 90))
        
        # Tower selection
        tower_info = [
            ("1 - Basic Tower ($20)", self.GREEN),
            ("2 - Sniper Tower ($50)", self.BLUE),
            ("3 - Freezer Tower ($30)", self.BLUE)
        ]
        
        for i, (text, color) in enumerate(tower_info):
            tower_text = font.render(text, True, color)
            self.screen.blit(tower_text, (10, 140 + i * 30))
        
        # Instructions
        instructions = [
            "SPACE - Pause/Resume",
            "ESC - Cancel tower placement",
            "Click to place selected tower"
        ]
        
        small_font = pygame.font.Font(None, 24)
        for i, instruction in enumerate(instructions):
            inst_text = small_font.render(instruction, True, self.GRAY)
            self.screen.blit(inst_text, (10, 250 + i * 25))
    
    def draw(self):
        self.screen.fill(self.WHITE)
        
        # Draw path
        self.draw_path()
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw tower placement preview
        if self.placing_tower:
            mouse_pos = pygame.mouse.get_pos()
            color = self.GREEN if self.is_valid_tower_position(*mouse_pos) else self.RED
            pygame.draw.circle(self.screen, color, mouse_pos, 15, 2)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 