# Tower Defense Game

A comprehensive tower defense game built with Python and Pygame, featuring multiple tower types, diverse enemies, strategic terrain effects, and a centralized JSON configuration system.

## Features

### Core Gameplay
- **Multiple Tower Types**: 14+ unique towers with different abilities and upgrade paths
- **Diverse Enemy Types**: Various enemies with unique behaviors, immunities, and boss encounters
- **Strategic Terrain**: Different terrain types affect tower placement and effectiveness
- **Wave-Based Progression**: Increasingly challenging waves with adaptive difficulty scaling
- **Currency System**: Earn money by dealing damage and completing waves

### Advanced Systems
- **Multi-Block Towers**: Large towers that occupy multiple grid cells
- **Enemy Immunity System**: Progressive immunity chances that scale with wave difficulty
- **Terrain Effects**: Towers perform differently on various terrain types
- **Status Effects**: Freeze, poison, burn, wet, and other tactical effects
- **Boss Battles**: Special boss enemies with unique mechanics and phases

### Configuration System
- **JSON-Based Configuration**: All game settings in a single, human-readable file
- **Easy Balancing**: Modify difficulty, costs, and mechanics without coding
- **Centralized Control**: Wave settings, tower costs, map layouts, and balance parameters
- **Version Control Friendly**: Track changes easily in git

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tower_defence_game
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python game.py
   ```

## Game Controls

- **Left Click**: Place selected tower or interact with UI
- **Right Click**: Cancel tower placement
- **ESC**: Pause/unpause game
- **Space**: Start next wave (when ready)

## Project Structure

```
tower_defence_game/
├── config/
│   ├── tower_defence_game.json    # Main configuration file
│   ├── game_config.py             # Configuration loader
│   └── README.md                  # Configuration documentation
├── enemies/                       # Enemy classes and behaviors
├── towers/                        # Tower classes and abilities
├── projectiles/                   # Projectile systems
├── game_systems/                  # Core game logic
├── tests/                         # Unit tests
├── game.py                        # Main game file
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Configuration

The game uses a centralized JSON configuration system in `config/tower_defence_game.json`. This file contains:

- **Wave Configuration**: Enemy spawning, wave progression, boss encounters
- **Map Configuration**: Terrain layouts and enemy paths  
- **Tower Configuration**: Costs, progression, and balance
- **Balance Configuration**: Currency system, immunity mechanics, status effects

To modify game balance or difficulty, simply edit the JSON file and restart the game.

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Content

**New Tower Types**:
1. Create tower class in `towers/` directory
2. Add tower configuration to JSON file
3. Update tower manager mappings

**New Enemy Types**:
1. Create enemy class in `enemies/` directory  
2. Add to wave compositions in JSON configuration
3. Test with various wave configurations

**New Maps**:
1. Add map configuration to JSON file with terrain layout and path
2. Maps are automatically available through the configuration system

## Technical Features

- **Modular Architecture**: Clean separation of concerns across game systems
- **Configuration-Driven**: JSON-based settings for easy modification
- **Extensible Design**: Easy to add new towers, enemies, and mechanics
- **Performance Optimized**: Efficient collision detection and rendering
- **Comprehensive Testing**: Unit tests for core game systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License. 