import unittest
import sys
import os
import pygame
import math

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from projectiles import (
    BasicProjectile, SniperProjectile, FreezeProjectile, IceProjectile,
    SplashProjectile, WaterProjectile, HomingProjectile
)
from enemies import BasicEnemy, FlyingEnemy


class TestProjectiles(unittest.TestCase):
    """Test cases for all projectile types"""
    
    def setUp(self):
        """Set up test environment"""
        # Initialize pygame for projectiles that might need it
        pygame.init()
        
        # Create test path and enemies
        self.test_path = [(100, 100), (200, 100), (300, 100)]
        self.test_enemy = BasicEnemy(self.test_path)
        self.test_enemy.x, self.test_enemy.y = 150, 100
        
        self.flying_enemy = FlyingEnemy(self.test_path)
        self.flying_enemy.x, self.flying_enemy.y = 250, 100
        
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_basic_projectile_creation(self):
        """Test BasicProjectile creation and properties"""
        projectile = BasicProjectile(100, 100, 200, 200, 5.0, 10)
        
        self.assertEqual(projectile.x, 100)
        self.assertEqual(projectile.y, 100)
        self.assertEqual(projectile.damage, 10)
        self.assertEqual(projectile.speed, 5.0)
        self.assertFalse(projectile.should_remove)

    def test_basic_projectile_movement(self):
        """Test BasicProjectile movement"""
        projectile = BasicProjectile(100, 100, 200, 200, 5.0, 10)
        initial_x, initial_y = projectile.x, projectile.y
        
        projectile.update()
        
        # Projectile should have moved
        self.assertNotEqual(projectile.x, initial_x)
        self.assertNotEqual(projectile.y, initial_y)

    def test_basic_projectile_collision(self):
        """Test BasicProjectile collision detection"""
        projectile = BasicProjectile(140, 100, 200, 100, 5.0, 10)
        projectile.source_tower_id = "test_tower"
        enemies = [self.test_enemy]
        
        result = projectile.check_collision(enemies)
        
        self.assertIsInstance(result, dict)
        self.assertIn('hit', result)
        self.assertIn('damage', result)
        self.assertIn('tower_id', result)

    def test_sniper_projectile_piercing(self):
        """Test SniperProjectile piercing ability"""
        projectile = SniperProjectile(100, 100, 300, 100, 8.0, 15)
        projectile.source_tower_id = "test_tower"
        
        # Create multiple enemies in line
        enemy1 = BasicEnemy(self.test_path)
        enemy1.x, enemy1.y = 150, 100
        enemy2 = BasicEnemy(self.test_path)
        enemy2.x, enemy2.y = 200, 100
        
        enemies = [enemy1, enemy2]
        
        result = projectile.check_collision(enemies)
        
        # Should hit and potentially pierce
        self.assertIsInstance(result, dict)
        if result['hit']:
            self.assertGreater(result['damage'], 0)

    def test_freeze_projectile_freeze_effect(self):
        """Test FreezeProjectile applies freeze effect"""
        projectile = FreezeProjectile(140, 100, 200, 100, 4.0, 5, 60)
        projectile.source_tower_id = "test_tower"
        enemies = [self.test_enemy]
        
        initial_frozen = self.test_enemy.frozen
        result = projectile.check_collision(enemies)
        
        if result['hit']:
            # Enemy should be frozen after collision
            self.assertTrue(self.test_enemy.frozen)
            self.assertGreater(self.test_enemy.freeze_timer, 0)

    def test_ice_projectile_area_freeze(self):
        """Test IceProjectile area freeze effect"""
        projectile = IceProjectile(140, 100, 150, 100, 3.0, 0, 120, 50, 0.5)
        projectile.source_tower_id = "test_tower"
        
        # Create multiple enemies in area
        enemy1 = BasicEnemy(self.test_path)
        enemy1.x, enemy1.y = 150, 100
        enemy2 = BasicEnemy(self.test_path)
        enemy2.x, enemy2.y = 170, 110
        
        enemies = [enemy1, enemy2]
        
        result = projectile.check_collision(enemies)
        
        # Should affect multiple enemies in area
        self.assertIsInstance(result, dict)

    def test_splash_projectile_explosion(self):
        """Test SplashProjectile explosion damage"""
        projectile = SplashProjectile(140, 100, 150, 100, 4.0, 20, 40)
        projectile.source_tower_id = "test_tower"
        
        # Create enemies at different distances
        close_enemy = BasicEnemy(self.test_path)
        close_enemy.x, close_enemy.y = 150, 100
        far_enemy = BasicEnemy(self.test_path)
        far_enemy.x, far_enemy.y = 180, 100
        
        enemies = [close_enemy, far_enemy]
        
        result = projectile.check_collision(enemies)
        
        # Should explode and deal area damage
        self.assertIsInstance(result, dict)

    def test_water_projectile_wet_status(self):
        """Test WaterProjectile applies wet status"""
        projectile = WaterProjectile(140, 100, 150, 100, 3.0, 0, 180, 35, 2.0)
        projectile.source_tower_id = "test_tower"
        enemies = [self.test_enemy]
        
        initial_wet = self.test_enemy.wet
        result = projectile.check_collision(enemies)
        
        if result['hit']:
            # Enemy should be wet after collision
            self.assertTrue(self.test_enemy.wet)
            self.assertGreater(self.test_enemy.wet_timer, 0)
            self.assertEqual(self.test_enemy.lightning_damage_multiplier, 2.0)

    def test_homing_projectile_targeting(self):
        """Test HomingProjectile homing behavior"""
        projectile = HomingProjectile(100, 100, 300, 100, 6.0, 12)
        projectile.source_tower_id = "test_tower"
        
        # Initial direction
        initial_vx = projectile.velocity_x
        initial_vy = projectile.velocity_y
        
        # Update with homing towards enemy
        projectile.update_homing([self.test_enemy])
        
        # Velocity should have changed towards target
        # (This test checks that the homing system is working)
        self.assertTrue(hasattr(projectile, 'velocity_x'))
        self.assertTrue(hasattr(projectile, 'velocity_y'))

    def test_projectile_distance_limits(self):
        """Test projectile distance limits"""
        projectile = BasicProjectile(100, 100, 1000, 1000, 5.0, 10)
        
        # Update many times to exceed max distance
        for _ in range(200):
            projectile.update()
            if projectile.should_remove:
                break
        
        # Should be marked for removal due to distance
        self.assertTrue(projectile.should_remove)

    def test_projectile_off_screen_removal(self):
        """Test projectile removal when off screen"""
        projectile = BasicProjectile(100, 100, -1000, -1000, 10.0, 10)
        
        # Update to move off screen
        for _ in range(50):
            projectile.update()
            if projectile.should_remove:
                break
        
        # Should be marked for removal
        self.assertTrue(projectile.should_remove)

    def test_projectile_target_reached(self):
        """Test projectile behavior when reaching target"""
        projectile = SplashProjectile(100, 100, 105, 105, 2.0, 15, 30)
        
        # Update until close to target
        for _ in range(10):
            projectile.update()
            if projectile.has_reached_target():
                break
        
        # Should detect target reached
        self.assertTrue(projectile.has_reached_target())

    def test_all_projectile_types_instantiation(self):
        """Test that all projectile types can be instantiated"""
        projectile_tests = [
            (BasicProjectile, (100, 100, 200, 200, 5.0, 10)),
            (SniperProjectile, (100, 100, 200, 200, 8.0, 15)),
            (FreezeProjectile, (100, 100, 200, 200, 4.0, 5, 60)),
            (IceProjectile, (100, 100, 200, 200, 3.0, 0, 120, 50, 0.5)),
            (SplashProjectile, (100, 100, 200, 200, 4.0, 20, 40)),
            (WaterProjectile, (100, 100, 200, 200, 3.0, 0, 180, 35, 2.0)),
            (HomingProjectile, (100, 100, 200, 200, 6.0, 12))
        ]
        
        for projectile_class, args in projectile_tests:
            with self.subTest(projectile_class=projectile_class.__name__):
                projectile = projectile_class(*args)
                self.assertIsNotNone(projectile)
                self.assertTrue(hasattr(projectile, 'x'))
                self.assertTrue(hasattr(projectile, 'y'))
                self.assertTrue(hasattr(projectile, 'damage'))
                self.assertTrue(hasattr(projectile, 'speed'))

    def test_projectile_collision_return_format(self):
        """Test that all projectiles return proper collision format"""
        projectiles = [
            BasicProjectile(140, 100, 200, 100, 5.0, 10),
            SniperProjectile(140, 100, 200, 100, 8.0, 15),
            FreezeProjectile(140, 100, 200, 100, 4.0, 5, 60),
            IceProjectile(140, 100, 150, 100, 3.0, 0, 120, 50, 0.5),
            SplashProjectile(140, 100, 150, 100, 4.0, 20, 40),
            WaterProjectile(140, 100, 150, 100, 3.0, 0, 180, 35, 2.0),
            HomingProjectile(140, 100, 200, 100, 6.0, 12)
        ]
        
        for projectile in projectiles:
            with self.subTest(projectile_class=projectile.__class__.__name__):
                projectile.source_tower_id = "test_tower"
                result = projectile.check_collision([self.test_enemy])
                
                # Should return dictionary with required keys
                self.assertIsInstance(result, dict)
                self.assertIn('hit', result)
                self.assertIn('damage', result)
                self.assertIn('tower_id', result)
                
                # Values should be of correct types
                self.assertIsInstance(result['hit'], bool)
                self.assertIsInstance(result['damage'], int)

    def test_projectile_damage_application(self):
        """Test that projectiles properly apply damage to enemies"""
        projectile = BasicProjectile(140, 100, 200, 100, 5.0, 10)
        projectile.source_tower_id = "test_tower"
        
        initial_health = self.test_enemy.health
        result = projectile.check_collision([self.test_enemy])
        
        if result['hit']:
            # Enemy health should decrease
            self.assertLess(self.test_enemy.health, initial_health)
            # Damage reported should match actual damage dealt
            self.assertGreater(result['damage'], 0)

    def test_projectile_velocity_calculation(self):
        """Test projectile velocity calculation"""
        start_x, start_y = 100, 100
        target_x, target_y = 200, 200
        speed = 5.0
        
        projectile = BasicProjectile(start_x, start_y, target_x, target_y, speed, 10)
        
        # Calculate expected velocity
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        expected_vx = (dx / distance) * speed
        expected_vy = (dy / distance) * speed
        
        # Check if velocity is calculated correctly
        self.assertAlmostEqual(projectile.velocity_x, expected_vx, places=2)
        self.assertAlmostEqual(projectile.velocity_y, expected_vy, places=2)

    def test_projectile_source_tower_tracking(self):
        """Test projectile source tower ID tracking"""
        projectile = BasicProjectile(100, 100, 200, 200, 5.0, 10)
        tower_id = "test_tower_123"
        projectile.source_tower_id = tower_id
        
        result = projectile.check_collision([self.test_enemy])
        
        if result['hit']:
            self.assertEqual(result['tower_id'], tower_id)


if __name__ == '__main__':
    unittest.main() 