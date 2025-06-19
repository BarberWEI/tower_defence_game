from .tower import Tower
from config.game_config import get_balance_config
import pygame
import math

class DetectorTower(Tower):
    """Support tower that reveals invisible enemies to other towers and generates currency from detection - does not attack"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'detector')
        self.damage = 0  # No damage - pure support
        self.range = 0   # No attack range
        self.fire_rate = 0  # No firing
        self.projectile_speed = 0
        self.size = 12
        self.color = (255, 255, 0)  # Yellow
        self.detection_range = 300  # Large detection range
        
        # Detection properties
        self.detected_enemies = set()  # Track detected invisible enemies
        self.detection_pulse_timer = 0
        self.max_detections = 3  # Can only detect 3 invisible enemies at once
        
        # Currency generation
        self.currency_timer = 0
        self.last_detected_count = 0
        
        # No targeting - pure support
        self.can_target_flying = False
        self.can_target_invisible = False
        
    def update(self, enemies, projectiles):
        """Update with detection capabilities and currency generation"""
        # Update detection pulse
        self.detection_pulse_timer += 0.1
        
        # Detect invisible enemies and make them targetable by other towers (max 3)
        self.detected_enemies.clear()
        invisible_in_range = []
        
        # Find all invisible enemies in range
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.detection_range:
                if hasattr(enemy, 'invisible') and enemy.invisible:
                    invisible_in_range.append((enemy, distance))
        
        # Sort by distance and take only the closest 3
        invisible_in_range.sort(key=lambda x: x[1])
        detected_count = 0
        
        for enemy, distance in invisible_in_range:
            if detected_count < self.max_detections:
                self.detected_enemies.add(enemy)
                # Mark enemy as detected so other towers can target it
                enemy.detected_by_detector = True
                detected_count += 1
            else:
                # Clear detection flag for enemies beyond the limit
                if hasattr(enemy, 'detected_by_detector'):
                    enemy.detected_by_detector = False
        
        # Generate currency based on detection
        self.generate_detection_currency(detected_count)
    
    def generate_detection_currency(self, detected_count):
        """Generate currency based on detected enemies"""
        if detected_count == 0:
            return 0
        
        config = get_balance_config()
        currency_config = config['currency']
        
        # Generate currency based on detection interval
        self.currency_timer += 1
        if self.currency_timer >= currency_config['detector_reward_interval']:
            self.currency_timer = 0
            # Generate currency for each enemy being detected
            currency_gained = detected_count * currency_config['detector_reward_per_enemy']
            
            # Use the upgrade system to add currency
            if self.upgrade_system_reference:
                self.upgrade_system_reference.add_tower_currency(
                    self.tower_id, self.tower_type, currency_gained
                )
            
            return currency_gained
        
        return 0
    
    def acquire_target(self, enemies):
        """Detector tower doesn't target enemies - pure support"""
        self.target = None
    
    def shoot(self, projectiles):
        """Detector tower doesn't shoot - pure support"""
        pass
    
    def draw(self, screen, selected: bool = False):
        """Draw detector tower with detection effects"""
        # Draw detection range circle when selected
        if selected:
            pygame.draw.circle(screen, (255, 255, 100), (int(self.x), int(self.y)), int(self.detection_range), 1)
        
        # Draw detection pulse
        pulse_radius = int(25 + 8 * math.sin(self.detection_pulse_timer))
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
                           (int(self.x), int(self.y)), (int(enemy.x), int(enemy.y)), 2)
        
        # Draw rotating radar sweep
        sweep_angle = self.detection_pulse_timer * 2
        sweep_x = self.x + math.cos(sweep_angle) * 15
        sweep_y = self.y + math.sin(sweep_angle) * 15
        pygame.draw.line(screen, (255, 255, 255), (int(self.x), int(self.y)), (int(sweep_x), int(sweep_y)), 2)
        
        # Draw currency generation indicator when detecting enemies
        if len(self.detected_enemies) > 0:
            # Draw a small coin symbol
            coin_x = int(self.x - 15)
            coin_y = int(self.y - 15)
            pygame.draw.circle(screen, (255, 215, 0), (coin_x, coin_y), 6)  # Gold coin
            pygame.draw.circle(screen, (0, 0, 0), (coin_x, coin_y), 6, 1)
            
            # Draw "$" symbol in coin
            font = pygame.font.Font(None, 12)
            text = font.render("$", True, (0, 0, 0))
            text_rect = text.get_rect(center=(coin_x, coin_y))
            screen.blit(text, text_rect) 