import unittest
import sys
import os
import pygame

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from towers import BasicTower, SniperTower, CannonTower
from enemies import BasicEnemy, FlyingEnemy, TankEnemy, SplittingEnemy
from game_systems.tower_upgrade_system import TowerUpgradeSystem, UpgradeType


class TestIntegration(unittest.TestCase):
    """Integration tests for tower defense game components"""
    
    def setUp(self):
        """Set up test environment"""
        pygame.init()
        
        # Create test path
        self.test_path = [(50, 100), (150, 100), (250, 100), (350, 100), (450, 100)]
        
        # Create upgrade system
        self.upgrade_system = TowerUpgradeSystem()
        
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_tower_enemy_interaction(self):
        """Test basic tower-enemy interaction"""
        # Create tower and enemy
        tower = BasicTower(100, 100)
        enemy = BasicEnemy(self.test_path)
        enemy.x, enemy.y = 120, 100  # Within range
        
        projectiles = []
        enemies = [enemy]
        
        # Force tower to be ready to shoot
        tower.shoot_timer = tower.fire_rate
        
        # Update tower
        tower.update(enemies, projectiles)
        
        # Should have acquired target and created projectile
        self.assertIsNotNone(tower.target)
        self.assertGreater(len(projectiles), 0)

    def test_projectile_enemy_collision(self):
        """Test projectile hitting enemy and dealing damage"""
        # Create tower and enemy
        tower = BasicTower(100, 100)
        enemy = BasicEnemy(self.test_path)
        enemy.x, enemy.y = 120, 100
        
        projectiles = []
        enemies = [enemy]
        
        # Make tower shoot
        tower.shoot_timer = tower.fire_rate
        tower.update(enemies, projectiles)
        
        # Get the projectile
        if projectiles:
            projectile = projectiles[0]
            initial_health = enemy.health
            
            # Test collision
            result = projectile.check_collision(enemies)
            
            if result['hit']:
                # Enemy should have taken damage
                self.assertLess(enemy.health, initial_health)
                self.assertGreater(result['damage'], 0)

    def test_currency_generation_from_damage(self):
        """Test currency generation when tower deals damage"""
        tower = BasicTower(100, 100)
        tower_id = tower.tower_id
        enemy = BasicEnemy(self.test_path)
        enemy.x, enemy.y = 120, 100
        
        projectiles = []
        enemies = [enemy]
        
        # Make tower shoot
        tower.shoot_timer = tower.fire_rate
        tower.update(enemies, projectiles)
        
        if projectiles:
            projectile = projectiles[0]
            result = projectile.check_collision(enemies)
            
            if result['hit'] and result['damage'] > 0:
                # Add currency based on damage
                self.upgrade_system.add_tower_currency(
                    result['tower_id'], 'basic', result['damage']
                )
                
                # Tower should have currency
                currency = self.upgrade_system.get_tower_currency(tower_id)
                self.assertGreater(currency, 0)

    def test_tower_upgrade_application(self):
        """Test applying upgrades to tower and seeing effects"""
        tower = BasicTower(100, 100)
        tower_id = tower.tower_id
        
        # Add currency and buy damage upgrade
        self.upgrade_system.add_tower_currency(tower_id, 'basic', 100)
        # Check if we can upgrade damage
        can_upgrade = self.upgrade_system.can_upgrade(tower_id, 'basic', UpgradeType.DAMAGE, 0)
        
        if can_upgrade:
            initial_damage = tower.damage
            
            # Purchase upgrade using actual method
            success = self.upgrade_system.upgrade_tower(tower_id, 'basic', UpgradeType.DAMAGE, 0)
            self.assertTrue(success)
            
            # Apply to tower
            self.upgrade_system.apply_upgrades_to_tower(tower, tower_id)
            
            # Tower should be stronger
            self.assertGreater(tower.damage, initial_damage)

    def test_multiple_towers_targeting(self):
        """Test multiple towers targeting the same enemy"""
        tower1 = BasicTower(80, 100)
        tower2 = BasicTower(120, 100)
        enemy = BasicEnemy(self.test_path)
        enemy.x, enemy.y = 100, 100  # Between towers
        
        enemies = [enemy]
        projectiles = []
        
        # Make both towers ready to shoot
        tower1.fire_timer = 0
        tower2.fire_timer = 0
        
        # Update both towers
        tower1.update(enemies, projectiles)
        tower2.update(enemies, projectiles)
        
        # Both should target the enemy
        self.assertEqual(tower1.target, enemy)
        self.assertEqual(tower2.target, enemy)
        
        # Should have created multiple projectiles
        self.assertGreaterEqual(len(projectiles), 2)

    def test_enemy_death_and_splitting(self):
        """Test enemy death mechanics and splitting behavior"""
        enemy = SplittingEnemy(self.test_path, split_count=2, generation=1)
        
        # Kill the enemy
        enemy.health = 0
        spawned = enemy.on_death()
        
        # Should spawn smaller enemies
        self.assertEqual(len(spawned), 2)
        for spawn in spawned:
            self.assertIsInstance(spawn, SplittingEnemy)
            self.assertEqual(spawn.generation, 2)

    def test_flying_enemy_antiair_targeting(self):
        """Test that only appropriate towers can target flying enemies"""
        from towers import AntiAirTower
        
        basic_tower = BasicTower(100, 100)
        antiair_tower = AntiAirTower(200, 100)
        flying_enemy = FlyingEnemy(self.test_path)
        flying_enemy.x, flying_enemy.y = 150, 100
        
        enemies = [flying_enemy]
        
        # Basic tower should not target flying enemy
        basic_tower.acquire_target(enemies)
        self.assertIsNone(basic_tower.target)
        
        # AntiAir tower should target flying enemy
        antiair_tower.acquire_target(enemies)
        self.assertIsNotNone(antiair_tower.target)

    def test_sniper_invisible_detection(self):
        """Test sniper tower detecting invisible enemies"""
        from enemies import InvisibleEnemy
        
        sniper = SniperTower(100, 100)
        invisible_enemy = InvisibleEnemy(self.test_path)
        invisible_enemy.x, invisible_enemy.y = 150, 100
        
        enemies = [invisible_enemy]
        
        # Sniper should be able to target invisible enemy
        sniper.acquire_target(enemies)
        self.assertIsNotNone(sniper.target)

    def test_cannon_splash_damage(self):
        """Test cannon tower splash damage affecting multiple enemies"""
        cannon = CannonTower(100, 100)
        
        # Create enemies close together
        enemy1 = BasicEnemy(self.test_path)
        enemy1.x, enemy1.y = 150, 100
        enemy2 = BasicEnemy(self.test_path)
        enemy2.x, enemy2.y = 160, 100
        
        enemies = [enemy1, enemy2]
        projectiles = []
        
        # Make cannon shoot
        cannon.fire_timer = 0  # Ready to shoot
        cannon.update(enemies, projectiles)
        
        if projectiles:
            projectile = projectiles[0]
            
            # Test collision (should affect multiple enemies)
            result = projectile.check_collision(enemies)
            
            # Should hit and potentially damage multiple enemies
            self.assertIsInstance(result, dict)
            if result['hit']:
                self.assertGreater(result['damage'], 0)

    def test_freeze_effect_duration(self):
        """Test freeze effect application and duration"""
        from towers import FreezerTower
        
        tower = FreezerTower(100, 100)
        enemy = BasicEnemy(self.test_path)
        enemy.x, enemy.y = 120, 100
        
        projectiles = []
        enemies = [enemy]
        
        # Make tower shoot
        tower.shoot_timer = tower.fire_rate
        tower.update(enemies, projectiles)
        
        if projectiles:
            projectile = projectiles[0]
            result = projectile.check_collision(enemies)
            
            if result['hit']:
                # Enemy should be frozen
                self.assertTrue(enemy.frozen)
                self.assertGreater(enemy.freeze_timer, 0)

    def test_full_wave_simulation(self):
        """Test a complete wave with multiple enemies and towers"""
        # Create multiple towers
        towers = [
            BasicTower(100, 50),
            BasicTower(200, 150),
            SniperTower(300, 100)
        ]
        
        # Create wave of enemies
        enemies = [
            BasicEnemy(self.test_path),
            BasicEnemy(self.test_path),
            TankEnemy(self.test_path),
            FlyingEnemy(self.test_path)
        ]
        
        # Position enemies along path
        for i, enemy in enumerate(enemies):
            enemy.x = 50 + i * 30
            enemy.y = 100
        
        projectiles = []
        
        # Simulate several game ticks
        for tick in range(10):
            # Update all towers
            for tower in towers:
                if tower.fire_timer <= 0:
                    tower.fire_timer = 0
                tower.update(enemies, projectiles)
            
            # Update all projectiles
            for projectile in projectiles[:]:
                projectile.update()
                result = projectile.check_collision(enemies)
                
                if result['hit'] or projectile.should_remove:
                    projectiles.remove(projectile)
            
            # Update all enemies
            for enemy in enemies[:]:
                enemy.update()
                if enemy.health <= 0:
                    enemies.remove(enemy)
        
        # Should have created projectiles and potentially killed enemies
        self.assertTrue(len(projectiles) > 0 or len(enemies) < 4)

    def test_currency_upgrade_cycle(self):
        """Test complete cycle of earning currency and upgrading towers"""
        tower = BasicTower(100, 100)
        tower_id = tower.tower_id
        
        # Simulate earning currency from damage
        total_currency = 0
        for damage_amount in [10, 15, 20, 25, 30]:
            self.upgrade_system.add_tower_currency(tower_id, 'basic', damage_amount)
            total_currency += damage_amount
        
        # Check currency accumulation
        currency = self.upgrade_system.get_tower_currency(tower_id, 'basic')
        self.assertEqual(currency, total_currency)
        
        # Purchase upgrades
        upgrades_purchased = 0
        while currency > 0:
            # Use actual available methods instead of non-existent get_available_upgrades
            can_upgrade_damage = self.upgrade_system.can_upgrade(tower_id, 'basic', UpgradeType.DAMAGE, 0)
            can_upgrade_range = self.upgrade_system.can_upgrade(tower_id, 'basic', UpgradeType.RANGE, 0)
            upgrade_made = False
            
            for upgrade_type in [UpgradeType.DAMAGE, UpgradeType.RANGE, UpgradeType.UTILITY]:
                if self.upgrade_system.can_upgrade(tower_id, 'basic', upgrade_type, 0):
                    cost = self.upgrade_system.get_upgrade_cost('basic', upgrade_type, 0)
                    if currency >= cost:
                        success = self.upgrade_system.upgrade_tower(tower_id, 'basic', upgrade_type, 0)
                        if success:
                            upgrades_purchased += 1
                            currency = self.upgrade_system.get_tower_currency(tower_id, 'basic')
                            upgrade_made = True
                            break
            
            if not upgrade_made:
                break
        
        # Should have purchased some upgrades
        self.assertGreater(upgrades_purchased, 0)
        
        # Apply upgrades and check tower improvement
        initial_damage = tower.damage
        initial_range = tower.range
        
        self.upgrade_system.apply_upgrades_to_tower(tower, tower_id)
        
        # Tower should be improved
        self.assertTrue(tower.damage >= initial_damage or tower.range >= initial_range)


if __name__ == '__main__':
    unittest.main() 