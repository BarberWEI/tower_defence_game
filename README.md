# Tower Defense Game

A Bloons TD-style tower defense game built in Python using Pygame.

## Features

### Enemy Types
- **Basic Enemy**: Standard health and speed
- **Fast Enemy**: High speed, low health, less affected by freeze
- **Tank Enemy**: High health, slow speed, has armor that reduces damage
- **Shielded Enemy**: Has regenerating shields that must be destroyed first

### Tower Types
- **Basic Tower**: Standard damage and range, targets enemies closest to the end
- **Sniper Tower**: High damage and range, targets enemies with the most health
- **Freezer Tower**: Applies freeze effect, targets fastest enemies

### Projectile Types  
- **Basic Projectile**: Standard damage projectile
- **Sniper Projectile**: High-speed projectile that can pierce through enemies
- **Freeze Projectile**: Applies freeze effect to enemies
- **Splash Projectile**: Deals area damage on impact
- **Homing Projectile**: Homes in on the nearest enemy

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python game.py
   ```

2. **Controls:**
   - **1**: Select Basic Tower ($20)
   - **2**: Select Sniper Tower ($50) 
   - **3**: Select Freezer Tower ($30)
   - **Click**: Place selected tower
   - **ESC**: Cancel tower placement
   - **SPACE**: Pause/Resume game

3. **Objective:**
   - Defend your base by placing towers along the path
   - Enemies will spawn in waves and follow the brown path
   - Prevent enemies from reaching the end to avoid losing lives
   - Earn money by defeating enemies to buy more towers
   - Survive as many waves as possible!

## Game Mechanics

- **Money**: Earned by defeating enemies, used to buy towers
- **Lives**: Lost when enemies reach the end of the path
- **Waves**: Enemies spawn in increasingly difficult waves
- **Tower Placement**: Towers cannot be placed on the path or too close to other towers

## Object-Oriented Design

The game follows good OOP principles with:

- **Base Classes**: `Enemy`, `Tower`, and `Projectile` provide common functionality
- **Inheritance**: Specialized classes inherit from base classes and override specific behaviors
- **Encapsulation**: Each class contains only what it needs to function
- **Polymorphism**: Different enemy/tower/projectile types can be treated uniformly

## Project Structure

```
tower_defence_game/
├── enemies/
│   ├── __init__.py          # Package exports
│   ├── enemy.py             # Base Enemy class
│   ├── basic_enemy.py       # BasicEnemy class
│   ├── fast_enemy.py        # FastEnemy class
│   ├── tank_enemy.py        # TankEnemy class
│   └── shielded_enemy.py    # ShieldedEnemy class
├── towers/
│   ├── __init__.py          # Package exports
│   ├── tower.py             # Base Tower class
│   ├── basic_tower.py       # BasicTower class
│   ├── sniper_tower.py      # SniperTower class
│   └── freezer_tower.py     # FreezerTower class
├── projectiles/
│   ├── __init__.py          # Package exports
│   ├── projectile.py        # Base Projectile class
│   ├── basic_projectile.py  # BasicProjectile class
│   ├── sniper_projectile.py # SniperProjectile class
│   ├── freeze_projectile.py # FreezeProjectile class
│   ├── splash_projectile.py # SplashProjectile class
│   └── homing_projectile.py # HomingProjectile class
├── game.py                  # Main game loop and logic
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

Each class is properly separated with clean dependencies and modular design for easy maintenance and extension.

Enjoy defending your base! 