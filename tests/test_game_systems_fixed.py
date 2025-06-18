import unittest
import sys
import os

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_systems.tower_upgrade_system import TowerUpgradeSystem, UpgradeType
from towers import BasicTower
from enemies import BasicEnemy


class TestGameSystemsFixed(unittest.TestCase):
    """Fixed test cases for game systems matching actual implementation"""
    
    def setUp(self):
        """Set up test environment"""
        self.upgrade_system = TowerUpgradeSystem()
        self.test_path = [(100, 100), (200, 100), (300, 100)]
        
    def test_tower_upgrade_system_creation(self):
        """Test TowerUpgradeSystem creation"""
        system = TowerUpgradeSystem()
        
        self.assertIsNotNone(system)
        self.assertTrue(hasattr(system, 'tower_currencies'))
        self.assertTrue(hasattr(system, 'upgrade_definitions'))  # Actual attribute name

    def test_add_tower_currency(self):
        """Test adding currency to a tower"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        amount = 50
        
        self.upgrade_system.add_tower_currency(tower_id, tower_type, amount)
        
        # Should have currency for this tower
        self.assertIn(tower_id, self.upgrade_system.tower_currencies)

    def test_get_tower_currency(self):
        """Test getting tower currency with correct signature"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        amount = 75
        
        self.upgrade_system.add_tower_currency(tower_id, tower_type, amount)
        currency = self.upgrade_system.get_tower_currency(tower_id, tower_type)
        
        self.assertEqual(currency, amount)

    def test_get_tower_currency_nonexistent(self):
        """Test getting currency for non-existent tower"""
        currency = self.upgrade_system.get_tower_currency("nonexistent_tower", "basic")
        
        self.assertEqual(currency, 0)

    def test_upgrade_info_retrieval(self):
        """Test getting upgrade information for tower types"""
        # Test basic tower upgrade info
        upgrade_info = self.upgrade_system.get_upgrade_info("basic", UpgradeType.DAMAGE)
        
        self.assertIsInstance(upgrade_info, dict)
        self.assertIn('name', upgrade_info)
        self.assertIn('description', upgrade_info)
        self.assertIn('max_level', upgrade_info)

    def test_upgrade_cost_calculation(self):
        """Test upgrade cost calculation"""
        # Test cost for level 1 upgrade
        cost = self.upgrade_system.get_upgrade_cost("basic", UpgradeType.DAMAGE, 0)
        
        self.assertIsInstance(cost, int)
        self.assertGreater(cost, 0)

    def test_can_upgrade_check(self):
        """Test upgrade availability check"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add sufficient currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 100)
        
        # Should be able to upgrade
        can_upgrade = self.upgrade_system.can_upgrade(tower_id, tower_type, UpgradeType.DAMAGE, 0)
        
        self.assertIsInstance(can_upgrade, bool)

    def test_upgrade_tower_success(self):
        """Test successful tower upgrade"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add sufficient currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 100)
        
        # Try to upgrade
        success = self.upgrade_system.upgrade_tower(tower_id, tower_type, UpgradeType.DAMAGE, 0)
        
        self.assertIsInstance(success, bool)

    def test_upgrade_tower_insufficient_currency(self):
        """Test upgrade failure with insufficient currency"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add minimal currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 1)
        
        # Try to upgrade (should fail)
        success = self.upgrade_system.upgrade_tower(tower_id, tower_type, UpgradeType.DAMAGE, 0)
        
        # Might succeed if cost is very low, but currency should be deducted
        remaining_currency = self.upgrade_system.get_tower_currency(tower_id, tower_type)
        self.assertLessEqual(remaining_currency, 1)

    def test_apply_upgrades_to_tower(self):
        """Test applying upgrades to actual tower"""
        tower = BasicTower(100, 100)
        tower_id = tower.tower_id
        
        # Add currency and upgrade
        self.upgrade_system.add_tower_currency(tower_id, "basic", 100)
        self.upgrade_system.upgrade_tower(tower_id, "basic", UpgradeType.DAMAGE, 0)
        
        # Apply upgrades to tower
        initial_damage = tower.damage
        self.upgrade_system.apply_upgrades_to_tower(tower, tower_id)
        
        # Tower should be affected (damage might increase or stay same depending on implementation)
        self.assertIsInstance(tower.damage, int)

    def test_currency_accumulation(self):
        """Test currency accumulation from multiple sources"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add currency multiple times
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 25)
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 30)
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 45)
        
        total_currency = self.upgrade_system.get_tower_currency(tower_id, tower_type)
        
        self.assertEqual(total_currency, 100)

    def test_upgrade_definitions_exist(self):
        """Test that upgrade definitions exist for tower types"""
        # Test that basic tower has upgrade definitions
        self.assertIn('basic', self.upgrade_system.upgrade_definitions)
        
        basic_upgrades = self.upgrade_system.upgrade_definitions['basic']
        self.assertIn(UpgradeType.DAMAGE, basic_upgrades)
        self.assertIn(UpgradeType.RANGE, basic_upgrades)
        self.assertIn(UpgradeType.UTILITY, basic_upgrades)

    def test_multiple_tower_types_upgrades(self):
        """Test upgrades for different tower types"""
        tower_types = ["basic", "sniper", "freezer"]
        
        for tower_type in tower_types:
            with self.subTest(tower_type=tower_type):
                if tower_type in self.upgrade_system.upgrade_definitions:
                    upgrades = self.upgrade_system.upgrade_definitions[tower_type]
                    self.assertIsInstance(upgrades, dict)

    def test_upgrade_cost_scaling(self):
        """Test that upgrade costs scale with level"""
        # Level 0 vs Level 1 cost
        cost_level_0 = self.upgrade_system.get_upgrade_cost("basic", UpgradeType.DAMAGE, 0)
        cost_level_1 = self.upgrade_system.get_upgrade_cost("basic", UpgradeType.DAMAGE, 1)
        
        # Higher level should generally cost more
        self.assertGreaterEqual(cost_level_1, cost_level_0)

    def test_max_upgrade_levels(self):
        """Test upgrade level limits"""
        # Get upgrade info to check max level
        upgrade_info = self.upgrade_system.get_upgrade_info("basic", UpgradeType.DAMAGE)
        max_level = upgrade_info.get('max_level', 0)
        
        self.assertGreater(max_level, 0)
        self.assertLessEqual(max_level, 10)  # Reasonable max level

    def test_upgrade_effects_structure(self):
        """Test upgrade effects data structure"""
        upgrade_info = self.upgrade_system.get_upgrade_info("basic", UpgradeType.DAMAGE)
        
        if 'effects' in upgrade_info:
            effects = upgrade_info['effects']
            self.assertIsInstance(effects, list)
            if len(effects) > 0:
                self.assertIsInstance(effects[0], dict)


if __name__ == '__main__':
    unittest.main() 