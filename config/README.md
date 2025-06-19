# Tower Defense Game Configuration

This directory contains the configuration system for the Tower Defense Game.

## Configuration Files

### `tower_defence_game.json`
The main configuration file containing all game settings. This single file contains four main sections:

#### Wave Configuration (`wave_config`)
Controls enemy spawning, wave progression, and enemy scaling:

- **spawn_config**: Base spawning parameters
  - `base_enemy_count`: Starting number of enemies per wave
  - `base_spawn_delay`: Initial delay between enemy spawns (frames)
  - `min_spawn_delay`: Minimum spawn delay allowed
  - `boss_enemy_count`: Number of boss enemies per boss wave

- **round_progression**: Wave difficulty scaling
  - `enemy_increase_per_round`: How many more enemies spawn per wave range
  - `spawn_delay_reduction_per_round`: How much faster enemies spawn per wave range
  - `special_rounds`: Special wave multipliers (waves 10, 20, 30, etc.)

- **wave_compositions**: Enemy type distributions by wave ranges
- **boss_waves**: Which waves spawn boss enemies
- **enemy_scaling**: How enemy stats scale with wave number
- **money_config**: Currency rewards for completing waves

#### Map Configuration (`map_config`)
Defines the game map layout:

- **default_map**: The main game map
  - `width`/`height`: Grid dimensions
  - `terrain`: 2D array defining terrain types (0=GRASS, 1=PATH, 2=ROCK, etc.)
  - `path`: Array of coordinates defining the enemy path

#### Tower Configuration (`tower_config`)
Controls tower costs and progression:

- **base_costs**: Starting cost for each tower type
- **cost_progression**: How tower costs increase with wave number
  - `early_game_waves`: Wave threshold for early game pricing
  - `mid_game_waves`: Wave threshold for mid game pricing
  - Per-wave cost increase percentages for each game phase

#### Balance Configuration (`balance_config`)
Game balance settings:

- **currency**: Currency generation settings
- **immunity**: Enemy immunity system parameters
- **freeze**: Freeze effect mechanics

### `game_config.py`
Python loader that reads the JSON configuration and provides access functions:

- `get_wave_config()`: Returns wave configuration
- `get_map_config()`: Returns all map configurations
- `get_tower_config()`: Returns tower configuration
- `get_balance_config()`: Returns balance configuration
- `get_available_maps()`: Returns list of available map names

## Usage

The configuration system is used throughout the game:

```python
from config.game_config import get_wave_config, get_tower_config

# Get wave settings
wave_config = get_wave_config()
spawn_delay = wave_config['spawn_config']['base_spawn_delay']

# Get tower costs
tower_config = get_tower_config()
basic_tower_cost = tower_config['base_costs']['BasicTower']
```

## Benefits

- **Human Readable**: JSON format is easy to edit without programming knowledge
- **Centralized**: All game parameters in one file
- **Version Control Friendly**: Changes are easy to track in git
- **Easy Balancing**: Modify difficulty by editing JSON values
- **Maintainable**: Clear separation of configuration from code

## Modifying the Game

To adjust game difficulty or behavior:

1. Edit `tower_defence_game.json` with your desired values
2. Save the file
3. Restart the game to apply changes

The configuration is loaded once at game startup and cached for performance. 