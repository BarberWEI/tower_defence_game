import unittest
import sys
import os
import pygame

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from towers import (
    BasicTower, SniperTower, FreezerTower, DetectorTower, AntiAirTower,
    PoisonTower, LaserTower, CannonTower, LightningTower, FlameTower,
    IceTower, ExplosiveTower, MissileTower, SplashTower
)
from enemies import BasicEnemy, FlyingEnemy, InvisibleEnemy, FastEnemy
from game_systems.tower_upgrade_system import TowerUpgradeSystem, UpgradeType


class TestTowers(unittest.TestCase):
    """Test cases for all tower types"""
    
    def setUp(self):
        """Set up test environment"""
        # Initialize pygame for towers that might need it
        pygame.init()
        
        # Create a simple test path for enemies
        self.test_path = [(100, 100), (200, 100), (300, 100), (400, 100)]
        
        # Create test enemies
        self.basic_enemy = BasicEnemy(self.test_path)
        self.flying_enemy = FlyingEnemy(self.test_path)
        self.invisible_enemy = InvisibleEnemy(self.test_path)
        self.fast_enemy = FastEnemy(self.test_path)
        
        # Position enemies for testing
        self.basic_enemy.x, self.basic_enemy.y = 150, 100
        self.flying_enemy.x, self.flying_enemy.y = 250, 100
        self.invisible_enemy.x, self.invisible_enemy.y = 350, 100
        self.fast_enemy.x, self.fast_enemy.y = 450, 100
        
        # Create upgrade system for testing
        self.upgrade_system = TowerUpgradeSystem()
        
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_basic_tower_creation(self):
        """Test BasicTower creation and basic properties"""
        tower = BasicTower(100, 200)
        
        self.assertEqual(tower.x, 100)
        self.assertEqual(tower.y, 200)
        self.assertEqual(tower.tower_type, 'basic')
        self.assertGreater(tower.damage, 0)
        self.assertGreater(tower.range, 0)
        self.assertGreater(tower.fire_rate, 0)
        self.assertTrue(hasattr(tower, 'tower_id'))

    def test_sniper_tower_creation(self):
        """Test SniperTower creation and properties"""
        tower = SniperTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'sniper')
        self.assertGreater(tower.damage, 0)
        self.assertGreater(tower.range, 100)  # Sniper should have long range
        self.assertTrue(tower.can_target_invisible)  # Sniper can target invisible

    def test_freezer_tower_creation(self):
        """Test FreezerTower creation and properties"""
        tower = FreezerTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'freezer')
        self.assertGreater(tower.damage, 0)
        self.assertTrue(hasattr(tower, 'freeze_duration'))

    def test_detector_tower_creation(self):
        """Test DetectorTower creation and properties"""
        tower = DetectorTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'detector')
        self.assertTrue(tower.can_target_invisible)
        self.assertTrue(hasattr(tower, 'detection_range'))

    def test_antiair_tower_creation(self):
        """Test AntiAirTower creation and properties"""
        tower = AntiAirTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'antiair')
        self.assertTrue(tower.can_target_flying)
        self.assertFalse(tower.can_target_ground)  # Should only target flying

    def test_poison_tower_creation(self):
        """Test PoisonTower creation and properties"""
        tower = PoisonTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'poison')
        self.assertTrue(hasattr(tower, 'poison_damage'))
        self.assertTrue(hasattr(tower, 'poison_duration'))

    def test_laser_tower_creation(self):
        """Test LaserTower creation and properties"""
        tower = LaserTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'laser')
        self.assertGreater(tower.damage, 0)

    def test_cannon_tower_creation(self):
        """Test CannonTower creation and properties"""
        tower = CannonTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'cannon')
        self.assertTrue(hasattr(tower, 'splash_radius'))
        self.assertTrue(hasattr(tower, 'splash_damage'))

    def test_lightning_tower_creation(self):
        """Test LightningTower creation and properties"""
        tower = LightningTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'lightning')
        self.assertTrue(hasattr(tower, 'chain_count'))

    def test_flame_tower_creation(self):
        """Test FlameTower creation and properties"""
        tower = FlameTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'flame')
        self.assertTrue(hasattr(tower, 'cone_angle'))

    def test_ice_tower_creation(self):
        """Test IceTower creation and properties"""
        tower = IceTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'ice')
        self.assertEqual(tower.damage, 0)  # Ice tower does no damage
        self.assertTrue(hasattr(tower, 'freeze_duration'))

    def test_explosive_tower_creation(self):
        """Test ExplosiveTower creation and properties"""
        tower = ExplosiveTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'explosive')
        self.assertGreater(tower.damage, 20)  # Should have high damage
        self.assertTrue(hasattr(tower, 'splash_radius'))

    def test_missile_tower_creation(self):
        """Test MissileTower creation and properties"""
        tower = MissileTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'missile')
        self.assertTrue(hasattr(tower, 'missile_count'))
        self.assertTrue(hasattr(tower, 'explosion_radius'))

    def test_splash_tower_creation(self):
        """Test SplashTower creation and properties"""
        tower = SplashTower(100, 200)
        
        self.assertEqual(tower.tower_type, 'splash')
        self.assertTrue(hasattr(tower, 'wet_duration'))

    def test_tower_targeting_basic_enemy(self):
        """Test that towers can target basic enemies"""
        tower = BasicTower(100, 100)
        enemies = [self.basic_enemy]
        
        tower.acquire_target(enemies)
        self.assertIsNotNone(tower.target)

    def test_antiair_tower_targeting(self):
        """Test AntiAirTower only targets flying enemies"""
        tower = AntiAirTower(200, 100)
        
        # Should not target ground enemies
        ground_enemies = [self.basic_enemy]
        tower.acquire_target(ground_enemies)
        self.assertIsNone(tower.target)
        
        # Should target flying enemies
        flying_enemies = [self.flying_enemy]
        tower.acquire_target(flying_enemies)
        self.assertIsNotNone(tower.target)

    def test_detector_tower_invisible_targeting(self):
        """Test DetectorTower can target invisible enemies"""
        tower = DetectorTower(300, 100)
        enemies = [self.invisible_enemy]
        
        tower.acquire_target(enemies)
        self.assertIsNotNone(tower.target)

    def test_tower_projectile_creation(self):
        """Test that towers create projectiles when shooting"""
        tower = BasicTower(100, 100)
        tower.target = self.basic_enemy
        projectiles = []
        
        # Force tower to be ready to shoot
        tower.shoot_timer = tower.fire_rate
        
        tower.update([self.basic_enemy], projectiles)
        
        # Should have created a projectile
        self.assertGreater(len(projectiles), 0)

    def test_tower_upgrade_system_integration(self):
        """Test tower integration with upgrade system"""
        tower = BasicTower(100, 100)
        tower_id = tower.tower_id
        
        # Add some currency
        self.upgrade_system.add_tower_currency(tower_id, 'basic', 100)
        
        # Test upgrade availability
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, 'basic')
        self.assertIsInstance(upgrades, dict)
        self.assertIn(UpgradeType.DAMAGE, upgrades)
        self.assertIn(UpgradeType.RANGE, upgrades)
        self.assertIn(UpgradeType.UTILITY, upgrades)

    def test_tower_damage_tracking(self):
        """Test tower damage tracking for currency generation"""
        tower = BasicTower(100, 100)
        
        initial_damage = tower.total_damage_dealt
        tower.add_damage_dealt(50)
        
        self.assertEqual(tower.total_damage_dealt, initial_damage + 50)

    def test_tower_range_validation(self):
        """Test tower range calculations"""
        tower = BasicTower(100, 100)
        
        # Enemy within range
        close_enemy = BasicEnemy(self.test_path)
        close_enemy.x, close_enemy.y = 120, 120
        
        # Enemy outside range
        far_enemy = BasicEnemy(self.test_path)
        far_enemy.x, far_enemy.y = 1000, 1000
        
        tower.acquire_target([close_enemy, far_enemy])
        
        # Should target the close enemy, not the far one
        self.assertEqual(tower.target, close_enemy)

    def test_all_tower_types_instantiation(self):
        """Test that all tower types can be instantiated without errors"""
        tower_classes = [
            BasicTower, SniperTower, FreezerTower, DetectorTower, AntiAirTower,
            PoisonTower, LaserTower, CannonTower, LightningTower, FlameTower,
            IceTower, ExplosiveTower, MissileTower, SplashTower
        ]
        
        for tower_class in tower_classes:
            with self.subTest(tower_class=tower_class.__name__):
                tower = tower_class(100, 100)
                self.assertIsNotNone(tower)
                self.assertTrue(hasattr(tower, 'tower_type'))
                self.assertTrue(hasattr(tower, 'damage'))
                self.assertTrue(hasattr(tower, 'range'))
                self.assertTrue(hasattr(tower, 'fire_rate'))

    def test_tower_terrain_requirements(self):
        """Test tower terrain requirements"""
        # Splash tower should require water terrain
        splash_tower = SplashTower(100, 100)
        self.assertTrue(hasattr(splash_tower, 'requires_water_terrain'))
        if hasattr(splash_tower, 'requires_water_terrain'):
            self.assertTrue(splash_tower.requires_water_terrain())

    def test_tower_size_variations(self):
        """Test that different towers have appropriate sizes"""
        basic = BasicTower(100, 100)
        cannon = CannonTower(100, 100)
        explosive = ExplosiveTower(100, 100)
        
        # Cannon and explosive should be larger than basic
        self.assertGreaterEqual(cannon.size, basic.size)
        self.assertGreaterEqual(explosive.size, basic.size)


if __name__ == '__main__':
    unittest.main() 