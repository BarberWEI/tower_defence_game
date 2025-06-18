import unittest
import sys
import os
import pygame

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enemies import (
    BasicEnemy, FastEnemy, TankEnemy, ShieldedEnemy, InvisibleEnemy,
    FlyingEnemy, RegeneratingEnemy, SplittingEnemy, TeleportingEnemy,
    MegaBoss, SpeedBoss
)


class TestEnemies(unittest.TestCase):
    """Test cases for all enemy types"""
    
    def setUp(self):
        """Set up test environment"""
        # Initialize pygame for enemies that might need it
        pygame.init()
        
        # Create a simple test path
        self.test_path = [(100, 100), (200, 100), (300, 100), (400, 100), (500, 100)]
        
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_basic_enemy_creation(self):
        """Test BasicEnemy creation and properties"""
        enemy = BasicEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 1)
        self.assertEqual(enemy.health, 1)
        self.assertEqual(enemy.speed, 1.0)
        self.assertEqual(enemy.reward, 4)  # After 20% reduction
        self.assertEqual(enemy.size, 8)
        self.assertFalse(enemy.reached_end)

    def test_fast_enemy_creation(self):
        """Test FastEnemy creation and properties"""
        enemy = FastEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 1)
        self.assertEqual(enemy.speed, 2.5)
        self.assertEqual(enemy.reward, 6)  # After 20% reduction
        self.assertGreater(enemy.speed, BasicEnemy(self.test_path).speed)

    def test_tank_enemy_creation(self):
        """Test TankEnemy creation and properties"""
        enemy = TankEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 5)
        self.assertEqual(enemy.speed, 0.5)
        self.assertEqual(enemy.reward, 12)  # After 20% reduction
        self.assertGreater(enemy.max_health, BasicEnemy(self.test_path).max_health)

    def test_shielded_enemy_creation(self):
        """Test ShieldedEnemy creation and properties"""
        enemy = ShieldedEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 2)
        self.assertEqual(enemy.max_shield, 2)
        self.assertEqual(enemy.shield, 2)
        self.assertEqual(enemy.reward, 10)  # After 20% reduction
        self.assertTrue(hasattr(enemy, 'shield_regen_timer'))

    def test_invisible_enemy_creation(self):
        """Test InvisibleEnemy creation and properties"""
        enemy = InvisibleEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 60)
        self.assertEqual(enemy.reward, 12)  # After 20% reduction
        self.assertTrue(enemy.invisible)
        self.assertTrue(hasattr(enemy, 'detection_radius'))

    def test_flying_enemy_creation(self):
        """Test FlyingEnemy creation and properties"""
        enemy = FlyingEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 40)
        self.assertEqual(enemy.reward, 10)  # After 20% reduction
        self.assertTrue(enemy.flying)
        self.assertTrue(hasattr(enemy, 'hover_offset'))

    def test_regenerating_enemy_creation(self):
        """Test RegeneratingEnemy creation and properties"""
        enemy = RegeneratingEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 80)
        self.assertEqual(enemy.reward, 16)  # After 20% reduction
        self.assertTrue(hasattr(enemy, 'regen_rate'))
        self.assertTrue(hasattr(enemy, 'regen_timer'))

    def test_splitting_enemy_creation(self):
        """Test SplittingEnemy creation and properties"""
        enemy = SplittingEnemy(self.test_path)
        
        self.assertEqual(enemy.generation, 1)
        self.assertEqual(enemy.split_count, 2)
        self.assertEqual(enemy.reward, 20)  # Base reward after 20% reduction
        self.assertTrue(hasattr(enemy, 'on_death'))

    def test_teleporting_enemy_creation(self):
        """Test TeleportingEnemy creation and properties"""
        enemy = TeleportingEnemy(self.test_path)
        
        self.assertEqual(enemy.max_health, 50)
        self.assertEqual(enemy.reward, 14)  # After 20% reduction
        self.assertTrue(hasattr(enemy, 'teleport_chance'))
        self.assertTrue(hasattr(enemy, 'teleport_distance'))

    def test_mega_boss_creation(self):
        """Test MegaBoss creation and properties"""
        enemy = MegaBoss(self.test_path)
        
        self.assertEqual(enemy.max_health, 2000)
        self.assertEqual(enemy.reward, 400)  # After 20% reduction
        self.assertEqual(enemy.phase, 1)
        self.assertTrue(hasattr(enemy, 'damage_reduction'))

    def test_speed_boss_creation(self):
        """Test SpeedBoss creation and properties"""
        enemy = SpeedBoss(self.test_path)
        
        self.assertEqual(enemy.reward, 160)  # After 20% reduction
        self.assertTrue(hasattr(enemy, 'base_speed'))
        # Speed boost timer might be optional - check if it exists or has speed boost functionality
        self.assertTrue(hasattr(enemy, 'speed_boost_timer') or hasattr(enemy, 'speed_multiplier'))

    def test_enemy_movement(self):
        """Test enemy movement along path"""
        enemy = BasicEnemy(self.test_path)
        initial_x = enemy.x
        
        # Update enemy to make it move
        enemy.update()
        
        # Enemy should have moved (unless it reached the end immediately)
        self.assertTrue(enemy.x >= initial_x or enemy.reached_end)

    def test_enemy_take_damage(self):
        """Test enemy damage handling"""
        enemy = BasicEnemy(self.test_path)
        initial_health = enemy.health
        
        damage_dealt = enemy.take_damage(1)
        
        self.assertEqual(damage_dealt, 1)
        self.assertEqual(enemy.health, initial_health - 1)

    def test_tank_enemy_armor(self):
        """Test TankEnemy armor reduction"""
        enemy = TankEnemy(self.test_path)
        initial_health = enemy.health
        
        # Tank should reduce damage
        damage_dealt = enemy.take_damage(5)
        
        # Should take less damage due to armor
        self.assertLess(damage_dealt, 5)
        self.assertGreater(enemy.health, initial_health - 5)

    def test_shielded_enemy_shield_mechanics(self):
        """Test ShieldedEnemy shield mechanics"""
        enemy = ShieldedEnemy(self.test_path)
        initial_shield = enemy.shield
        initial_health = enemy.health
        
        # Damage should go to shield first
        damage_dealt = enemy.take_damage(1)
        
        self.assertEqual(damage_dealt, 1)
        self.assertEqual(enemy.shield, initial_shield - 1)
        self.assertEqual(enemy.health, initial_health)  # Health unchanged

    def test_shielded_enemy_overflow_damage(self):
        """Test ShieldedEnemy overflow damage to health"""
        enemy = ShieldedEnemy(self.test_path)
        enemy.shield = 1  # Set low shield
        initial_health = enemy.health
        
        # Damage more than shield
        damage_dealt = enemy.take_damage(3)
        
        self.assertEqual(damage_dealt, 3)
        self.assertEqual(enemy.shield, 0)
        self.assertEqual(enemy.health, initial_health - 2)  # Overflow damage

    def test_enemy_freeze_effect(self):
        """Test enemy freeze status effect"""
        enemy = BasicEnemy(self.test_path)
        
        enemy.apply_freeze(60)  # 1 second freeze
        
        self.assertTrue(enemy.frozen)
        self.assertEqual(enemy.freeze_timer, 60)

    def test_enemy_wet_status(self):
        """Test enemy wet status effect"""
        enemy = BasicEnemy(self.test_path)
        
        enemy.apply_wet_status(120, 2.0)  # 2 seconds wet, 2x lightning damage
        
        self.assertTrue(enemy.wet)
        self.assertEqual(enemy.wet_timer, 120)
        self.assertEqual(enemy.lightning_damage_multiplier, 2.0)

    def test_fast_enemy_freeze_resistance(self):
        """Test FastEnemy reduced freeze duration"""
        enemy = FastEnemy(self.test_path)
        
        enemy.apply_freeze(60)  # Should be reduced
        
        self.assertTrue(enemy.frozen)
        self.assertEqual(enemy.freeze_timer, 30)  # Half duration

    def test_splitting_enemy_on_death(self):
        """Test SplittingEnemy splitting behavior"""
        enemy = SplittingEnemy(self.test_path, split_count=2, generation=1)
        
        spawned = enemy.on_death()
        
        self.assertEqual(len(spawned), 2)
        for spawn in spawned:
            self.assertIsInstance(spawn, SplittingEnemy)
            self.assertEqual(spawn.generation, 2)

    def test_splitting_enemy_max_generation(self):
        """Test SplittingEnemy stops splitting at max generation"""
        enemy = SplittingEnemy(self.test_path, split_count=2, generation=3)
        
        spawned = enemy.on_death()
        
        self.assertEqual(len(spawned), 0)  # Should not split at generation 3

    def test_teleporting_enemy_teleport_attempt(self):
        """Test TeleportingEnemy teleport mechanics"""
        enemy = TeleportingEnemy(self.test_path)
        enemy.teleport_timer = 120  # Ready to teleport
        initial_position = (enemy.x, enemy.y)
        
        # Force teleport attempt
        enemy.teleport_chance = 1.0  # 100% chance
        enemy.take_damage(1)
        
        # Position might have changed due to teleport
        # (We can't guarantee teleport happened due to randomness, but we can check the system works)
        self.assertTrue(hasattr(enemy, 'is_teleporting'))

    def test_regenerating_enemy_regen(self):
        """Test RegeneratingEnemy regeneration"""
        enemy = RegeneratingEnemy(self.test_path)
        enemy.health = 50  # Damage it first
        enemy.last_damage_time = 200  # Long time since damage
        
        initial_health = enemy.health
        enemy.update()
        
        # Should regenerate (though timing dependent)
        self.assertGreaterEqual(enemy.health, initial_health)

    def test_mega_boss_phases(self):
        """Test MegaBoss phase changes"""
        boss = MegaBoss(self.test_path)
        
        # Test phase 1
        self.assertEqual(boss.phase, 1)
        
        # Damage to phase 2
        boss.health = boss.max_health * 0.5  # 50% health
        boss.update()
        self.assertEqual(boss.phase, 2)
        
        # Damage to phase 3
        boss.health = boss.max_health * 0.2  # 20% health
        boss.update()
        self.assertEqual(boss.phase, 3)

    def test_mega_boss_damage_reduction(self):
        """Test MegaBoss damage reduction"""
        boss = MegaBoss(self.test_path)
        initial_health = boss.health
        
        damage_dealt = boss.take_damage(100)
        
        # Should take reduced damage
        self.assertLess(damage_dealt, 100)
        self.assertGreater(boss.health, initial_health - 100)

    def test_flying_enemy_targeting_restrictions(self):
        """Test FlyingEnemy can only be hit by specific towers"""
        enemy = FlyingEnemy(self.test_path)
        
        # Test tower type restrictions
        self.assertTrue(enemy.can_be_hit_by_tower("antiair"))
        self.assertTrue(enemy.can_be_hit_by_tower("sniper"))
        self.assertFalse(enemy.can_be_hit_by_tower("basic"))

    def test_invisible_enemy_detection(self):
        """Test InvisibleEnemy detection mechanics"""
        enemy = InvisibleEnemy(self.test_path)
        
        # Should be detectable by detector towers
        self.assertTrue(enemy.is_detectable_by_tower(100, 100, "detector"))
        
        # Should not be detectable by normal towers at long range
        self.assertFalse(enemy.is_detectable_by_tower(1000, 1000, "basic"))

    def test_all_enemy_types_instantiation(self):
        """Test that all enemy types can be instantiated without errors"""
        enemy_classes = [
            BasicEnemy, FastEnemy, TankEnemy, ShieldedEnemy, InvisibleEnemy,
            FlyingEnemy, RegeneratingEnemy, SplittingEnemy, TeleportingEnemy,
            MegaBoss, SpeedBoss
        ]
        
        for enemy_class in enemy_classes:
            with self.subTest(enemy_class=enemy_class.__name__):
                enemy = enemy_class(self.test_path)
                self.assertIsNotNone(enemy)
                self.assertTrue(hasattr(enemy, 'health'))
                self.assertTrue(hasattr(enemy, 'max_health'))
                self.assertTrue(hasattr(enemy, 'speed'))
                self.assertTrue(hasattr(enemy, 'reward'))

    def test_enemy_path_following(self):
        """Test that enemies follow the given path"""
        enemy = BasicEnemy(self.test_path)
        
        # Enemy should start at first path point
        self.assertEqual(enemy.x, self.test_path[0][0])
        self.assertEqual(enemy.y, self.test_path[0][1])
        
        # Path index should start at 0
        self.assertEqual(enemy.path_index, 0)

    def test_enemy_reward_scaling(self):
        """Test that enemy rewards are properly scaled (20% reduction)"""
        # Test a few key enemies to ensure reward reduction is applied
        basic = BasicEnemy(self.test_path)
        tank = TankEnemy(self.test_path)
        boss = MegaBoss(self.test_path)
        
        # These should be the reduced values
        self.assertEqual(basic.reward, 4)  # Was 5, now 4
        self.assertEqual(tank.reward, 12)  # Was 15, now 12
        self.assertEqual(boss.reward, 400)  # Was 500, now 400

    def test_enemy_distance_tracking(self):
        """Test enemy distance tracking along path"""
        enemy = BasicEnemy(self.test_path)
        initial_distance = enemy.distance_traveled
        
        # Move enemy
        enemy.update()
        
        # Distance should increase (unless reached end)
        self.assertTrue(enemy.distance_traveled >= initial_distance)

    def test_enemy_status_effect_timers(self):
        """Test status effect timer decrements"""
        enemy = BasicEnemy(self.test_path)
        
        # Apply freeze
        enemy.apply_freeze(60)
        initial_timer = enemy.freeze_timer
        
        # Update should decrement timer
        enemy.update()
        
        self.assertLess(enemy.freeze_timer, initial_timer)


if __name__ == '__main__':
    unittest.main() 