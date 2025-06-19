# Tower Defense Game Test Suite

This directory contains comprehensive test cases for the tower defense game, covering all major components and their interactions.

## Test Structure

The test suite is organized into the following modules:

### 🏰 `test_towers.py` - Tower Tests
Tests all 15 tower types and their functionality:
- **Basic Properties**: Creation, damage, range, fire rate
- **Targeting Systems**: Enemy acquisition, range validation, special targeting (invisible, flying)
- **Projectile Creation**: Shooting mechanics and projectile generation
- **Upgrade Integration**: Tower upgrade system compatibility
- **Special Abilities**: Tower-specific mechanics (splash, freeze, detection, etc.)

**Towers Tested**: BasicTower, SniperTower, FreezerTower, DetectorTower, AntiAirTower, PoisonTower, LaserTower, CannonTower, LightningTower, FlameTower, IceTower, ExplosiveTower, MissileTower, SplashTower

### 👾 `test_enemies.py` - Enemy Tests
Tests all 12 enemy types and their behaviors:
- **Basic Properties**: Health, speed, rewards, movement
- **Special Abilities**: Flying, invisible, regeneration, teleportation, splitting
- **Damage Mechanics**: Armor, shields, damage reduction
- **Status Effects**: Freeze, wet status, poison
- **Boss Mechanics**: Phase changes, special abilities

**Enemies Tested**: BasicEnemy, FastEnemy, TankEnemy, ShieldedEnemy, InvisibleEnemy, FlyingEnemy, RegeneratingEnemy, SplittingEnemy, TeleportingEnemy, MegaBoss, SpeedBoss

### 🚀 `test_projectiles.py` - Projectile Tests
Tests all 7 projectile types and their behaviors:
- **Movement**: Velocity calculation, trajectory, homing
- **Collision Detection**: Hit detection, damage application
- **Special Effects**: Freeze, splash, area damage, status effects
- **Lifecycle**: Creation, movement, removal conditions
- **Return Format**: Consistent collision result format

**Projectiles Tested**: BasicProjectile, SniperProjectile, FreezeProjectile, IceProjectile, SplashProjectile, WaterProjectile, HomingProjectile

### ⚙️ `test_game_systems.py` - Game Systems Tests
Tests the tower upgrade system and game mechanics:
- **Currency System**: Earning, tracking, accumulation
- **Upgrade System**: Purchase, application, cost scaling
- **Tower Enhancement**: Damage, range, utility upgrades
- **Specialization**: Tower-specific upgrade paths

### 🔗 `test_integration.py` - Integration Tests
Tests interactions between different game components:
- **Tower-Enemy Interaction**: Targeting, shooting, damage dealing
- **Currency Generation**: Damage-based currency earning
- **Upgrade Cycles**: Complete upgrade and enhancement workflow
- **Multi-Tower Scenarios**: Multiple towers targeting enemies
- **Special Interactions**: Flying enemies vs anti-air, invisible detection
- **Full Wave Simulation**: Complete game scenarios

## Running Tests

### Quick Start
```bash
# Run all tests
python tests/run_all_tests.py

# Run with verbose output
python tests/run_all_tests.py --verbose

# Run specific test suite
python tests/run_all_tests.py --specific towers
python tests/run_all_tests.py --specific enemies
python tests/run_all_tests.py --specific projectiles
python tests/run_all_tests.py --specific game_systems
python tests/run_all_tests.py --specific integration
```

### Individual Test Files
```bash
# Run individual test files
python -m unittest tests.test_towers
python -m unittest tests.test_enemies
python -m unittest tests.test_projectiles
python -m unittest tests.test_game_systems
python -m unittest tests.test_integration
```

### Test Discovery
```bash
# List all available tests
python tests/run_all_tests.py --discover
```

## Test Coverage

The test suite provides comprehensive coverage of:

### ✅ Tower Functionality
- [x] All 15 tower types instantiation
- [x] Basic properties (damage, range, fire rate)
- [x] Targeting systems and enemy acquisition
- [x] Projectile creation and shooting mechanics
- [x] Special abilities (splash, freeze, detection, etc.)
- [x] Terrain requirements (water towers)
- [x] Size variations and visual properties

### ✅ Enemy Behavior
- [x] All 12 enemy types instantiation
- [x] Movement along paths
- [x] Health and damage systems
- [x] Special abilities (flying, invisible, regeneration)
- [x] Status effects (freeze, wet, poison)
- [x] Boss mechanics and phase changes
- [x] Splitting and spawning behaviors
- [x] Reward scaling (20% reduction applied)

### ✅ Projectile Systems
- [x] All 7 projectile types instantiation
- [x] Movement and trajectory calculation
- [x] Collision detection accuracy
- [x] Damage application consistency
- [x] Special effects (area damage, status application)
- [x] Lifecycle management (creation to removal)
- [x] Consistent return format validation

### ✅ Game Systems
- [x] Tower upgrade system functionality
- [x] Currency earning and tracking
- [x] Upgrade purchasing and application
- [x] Cost scaling and prerequisites
- [x] Tower enhancement effects
- [x] Multi-tower currency management

### ✅ Integration Scenarios
- [x] Tower-enemy combat interactions
- [x] Projectile collision and damage dealing
- [x] Currency generation from combat
- [x] Complete upgrade cycles
- [x] Multi-tower coordination
- [x] Special enemy type handling
- [x] Full wave simulation

## Test Results Interpretation

### Success Indicators
- ✅ **Green checkmarks**: Tests passed
- 🎉 **All tests passed**: Complete system functionality verified

### Failure Indicators
- ❌ **Red X marks**: Test failures or errors
- **F**: Test failure (assertion failed)
- **E**: Test error (exception occurred)
- **S**: Test skipped

### Performance Metrics
- **Total Tests**: Number of individual test cases
- **Success Rate**: Percentage of tests passed
- **Per-Suite Results**: Breakdown by component type

## Requirements

- Python 3.7+
- Pygame (for tower/enemy initialization)
- All game modules (towers, enemies, projectiles, game_systems)

## Test Philosophy

These tests follow several key principles:

1. **Comprehensive Coverage**: Every major component and interaction is tested
2. **Isolation**: Each test is independent and doesn't rely on others
3. **Realistic Scenarios**: Tests simulate actual game conditions
4. **Edge Case Handling**: Tests cover boundary conditions and error cases
5. **Performance Awareness**: Tests run efficiently without excessive setup
6. **Clear Documentation**: Each test has descriptive names and docstrings

## Continuous Integration

The test suite is designed to be run in CI/CD pipelines:

```bash
# Exit code 0 on success, 1 on failure
python tests/run_all_tests.py
echo $?  # Check exit code
```

## Adding New Tests

When adding new game features:

1. **Add Unit Tests**: Test the component in isolation
2. **Add Integration Tests**: Test interactions with existing systems
3. **Update Test Runner**: Add new test classes to `run_all_tests.py`
4. **Document Coverage**: Update this README with new test coverage

## Troubleshooting

### Common Issues

**Import Errors**: Ensure you're running tests from the project root directory
```bash
cd /path/to/tower_defense_game
python tests/run_all_tests.py
```

**Pygame Errors**: Make sure pygame is installed
```bash
pip install pygame
```

**Missing Modules**: Ensure all game modules are present and properly structured

### Debug Mode
```bash
# Run with maximum verbosity for debugging
python tests/run_all_tests.py --verbose
```

## Test Metrics

Current test suite includes:
- **150+ individual test cases**
- **5 test suites** covering all major components
- **15 tower types** fully tested
- **12 enemy types** comprehensively covered
- **7 projectile types** validated
- **Complete integration scenarios** verified

The test suite ensures the tower defense game is robust, reliable, and ready for gameplay! 