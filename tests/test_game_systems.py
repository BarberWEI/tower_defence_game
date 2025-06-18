import unittest
import sys
import os

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_systems.tower_upgrade_system import TowerUpgradeSystem, UpgradeType
from towers import BasicTower
from enemies import BasicEnemy


class TestGameSystems(unittest.TestCase):
    """Test cases for game systems"""
    
    def setUp(self):
        """Set up test environment"""
        self.upgrade_system = TowerUpgradeSystem()
        self.test_path = [(100, 100), (200, 100), (300, 100)]
        
    def test_tower_upgrade_system_creation(self):
        """Test TowerUpgradeSystem creation"""
        system = TowerUpgradeSystem()
        
        self.assertIsNotNone(system)
        self.assertTrue(hasattr(system, 'tower_currencies'))
        self.assertTrue(hasattr(system, 'tower_upgrades'))

    def test_add_tower_currency(self):
        """Test adding currency to a tower"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        amount = 50
        
        self.upgrade_system.add_tower_currency(tower_id, tower_type, amount)
        
        # Should have currency for this tower
        self.assertIn(tower_id, self.upgrade_system.tower_currencies)
        self.assertEqual(self.upgrade_system.tower_currencies[tower_id], amount)

    def test_get_tower_currency(self):
        """Test getting tower currency"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        amount = 75
        
        self.upgrade_system.add_tower_currency(tower_id, tower_type, amount)
        currency = self.upgrade_system.get_tower_currency(tower_id)
        
        self.assertEqual(currency, amount)

    def test_get_tower_currency_nonexistent(self):
        """Test getting currency for non-existent tower"""
        currency = self.upgrade_system.get_tower_currency("nonexistent_tower")
        
        self.assertEqual(currency, 0)

    def test_get_available_upgrades(self):
        """Test getting available upgrades for a tower"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add some currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 100)
        
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        
        self.assertIsInstance(upgrades, dict)
        self.assertIn(UpgradeType.DAMAGE, upgrades)
        self.assertIn(UpgradeType.RANGE, upgrades)
        self.assertIn(UpgradeType.UTILITY, upgrades)

    def test_purchase_upgrade_success(self):
        """Test successful upgrade purchase"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add sufficient currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 100)
        
        # Get available upgrades
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        
        if upgrades[UpgradeType.DAMAGE]:
            upgrade = upgrades[UpgradeType.DAMAGE][0]  # First damage upgrade
            initial_currency = self.upgrade_system.get_tower_currency(tower_id)
            
            success = self.upgrade_system.purchase_upgrade(tower_id, tower_type, upgrade)
            
            self.assertTrue(success)
            # Currency should be reduced
            new_currency = self.upgrade_system.get_tower_currency(tower_id)
            self.assertLess(new_currency, initial_currency)

    def test_purchase_upgrade_insufficient_currency(self):
        """Test upgrade purchase with insufficient currency"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add minimal currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 1)
        
        # Try to buy expensive upgrade
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        
        if upgrades[UpgradeType.DAMAGE]:
            # Find most expensive upgrade
            expensive_upgrade = max(upgrades[UpgradeType.DAMAGE], key=lambda x: x.cost)
            
            success = self.upgrade_system.purchase_upgrade(tower_id, tower_type, expensive_upgrade)
            
            self.assertFalse(success)

    def test_upgrade_level_tracking(self):
        """Test upgrade level tracking"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add currency and buy upgrade
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 100)
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        
        if upgrades[UpgradeType.DAMAGE]:
            upgrade = upgrades[UpgradeType.DAMAGE][0]
            self.upgrade_system.purchase_upgrade(tower_id, tower_type, upgrade)
            
            # Check upgrade level increased
            level = self.upgrade_system.get_upgrade_level(tower_id, upgrade.upgrade_type)
            self.assertGreater(level, 0)

    def test_upgrade_cost_scaling(self):
        """Test that upgrade costs scale properly"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add lots of currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 1000)
        
        # Buy multiple damage upgrades
        for _ in range(3):
            upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
            if upgrades[UpgradeType.DAMAGE]:
                upgrade = upgrades[UpgradeType.DAMAGE][0]
                self.upgrade_system.purchase_upgrade(tower_id, tower_type, upgrade)
        
        # Next upgrade should be more expensive
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        if upgrades[UpgradeType.DAMAGE]:
            next_upgrade = upgrades[UpgradeType.DAMAGE][0]
            # Cost should have scaled up
            self.assertGreater(next_upgrade.cost, 10)  # Base cost

    def test_apply_upgrades_to_tower(self):
        """Test applying upgrades to actual tower"""
        tower = BasicTower(100, 100)
        tower_id = tower.tower_id
        
        # Add currency and buy damage upgrade
        self.upgrade_system.add_tower_currency(tower_id, "basic", 100)
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, "basic")
        
        if upgrades[UpgradeType.DAMAGE]:
            initial_damage = tower.damage
            upgrade = upgrades[UpgradeType.DAMAGE][0]
            self.upgrade_system.purchase_upgrade(tower_id, "basic", upgrade)
            
            # Apply upgrades to tower
            self.upgrade_system.apply_upgrades_to_tower(tower)
            
            # Tower damage should increase
            self.assertGreater(tower.damage, initial_damage)

    def test_multiple_upgrade_types(self):
        """Test purchasing different types of upgrades"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add lots of currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 500)
        
        upgrade_types_purchased = set()
        
        # Try to buy one upgrade of each type
        for upgrade_type in [UpgradeType.DAMAGE, UpgradeType.RANGE, UpgradeType.UTILITY]:
            upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
            if upgrades[upgrade_type]:
                upgrade = upgrades[upgrade_type][0]
                success = self.upgrade_system.purchase_upgrade(tower_id, tower_type, upgrade)
                if success:
                    upgrade_types_purchased.add(upgrade_type)
        
        # Should have purchased multiple types
        self.assertGreater(len(upgrade_types_purchased), 1)

    def test_tower_specialization_upgrades(self):
        """Test tower-specific specialization upgrades"""
        tower_types = ["basic", "sniper", "freezer", "cannon"]
        
        for tower_type in tower_types:
            with self.subTest(tower_type=tower_type):
                tower_id = f"test_{tower_type}_tower"
                
                # Add currency
                self.upgrade_system.add_tower_currency(tower_id, tower_type, 200)
                
                # Get upgrades
                upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
                
                # Should have utility upgrades (specializations)
                self.assertIn(UpgradeType.UTILITY, upgrades)
                self.assertIsInstance(upgrades[UpgradeType.UTILITY], list)

    def test_currency_accumulation(self):
        """Test currency accumulation from multiple sources"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add currency multiple times
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 25)
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 30)
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 45)
        
        total_currency = self.upgrade_system.get_tower_currency(tower_id)
        
        self.assertEqual(total_currency, 100)

    def test_upgrade_system_reset(self):
        """Test resetting upgrade system state"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add currency and upgrades
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 100)
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        
        if upgrades[UpgradeType.DAMAGE]:
            upgrade = upgrades[UpgradeType.DAMAGE][0]
            self.upgrade_system.purchase_upgrade(tower_id, tower_type, upgrade)
        
        # Reset system
        self.upgrade_system.reset()
        
        # Should be clean state
        self.assertEqual(len(self.upgrade_system.tower_currencies), 0)
        self.assertEqual(len(self.upgrade_system.tower_upgrades), 0)

    def test_upgrade_prerequisites(self):
        """Test upgrade prerequisites and dependencies"""
        tower_id = "test_tower_1"
        tower_type = "basic"
        
        # Add lots of currency
        self.upgrade_system.add_tower_currency(tower_id, tower_type, 1000)
        
        # Some upgrades may have prerequisites
        upgrades = self.upgrade_system.get_available_upgrades(tower_id, tower_type)
        
        # Should only show upgrades we can actually purchase
        for upgrade_list in upgrades.values():
            for upgrade in upgrade_list:
                self.assertTrue(hasattr(upgrade, 'cost'))
                self.assertTrue(hasattr(upgrade, 'name'))
                self.assertTrue(hasattr(upgrade, 'description'))


if __name__ == '__main__':
    unittest.main() 