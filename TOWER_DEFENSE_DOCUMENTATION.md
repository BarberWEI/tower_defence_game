# Tower Defense Game - Complete Documentation

## Table of Contents
1. [Game Overview](#game-overview)
2. [Core Game Mechanics](#core-game-mechanics)
3. [User Interface & Controls](#user-interface--controls)
4. [Towers](#towers)
5. [Enemies](#enemies)
6. [Boss Enemies](#boss-enemies)
7. [Counter System](#counter-system)
8. [Upgrade System](#upgrade-system)
9. [Wave System & Campaign](#wave-system--campaign)
10. [Terrain System](#terrain-system)
11. [Status Effects](#status-effects)
12. [Performance & Optimization](#performance--optimization)
13. [Configuration System](#configuration-system)
14. [Strategic Guide](#strategic-guide)

---

## Game Overview

This is a comprehensive tower defense game featuring 80 waves of progressively challenging enemies, 15 different tower types, over 25 enemy types including 4 ultimate bosses, and sophisticated counter-based combat mechanics.

### Key Features
- **80-Wave Campaign**: Complete campaign from basic enemies to ultimate bosses
- **15 Tower Types**: Each with unique mechanics and upgrade paths
- **25+ Enemy Types**: Including special abilities like teleportation, splitting, and adaptation
- **4 Ultimate Bosses**: Time manipulation, necromancy, shadow phasing, and crystal powers
- **Advanced Counter System**: Rock-paper-scissors style effectiveness multipliers
- **Detection Mechanics**: Invisible enemies require detector towers to target
- **Progressive Difficulty**: Dynamic scaling, random immunities, and adaptive challenges
- **Performance Optimization**: Smooth gameplay even at high speeds with many entities
- **Configurable Gameplay**: Customizable starting resources, difficulty, and wave composition

---

## Core Game Mechanics

### Speed System
- **Game Speed Control**: Use UP/DOWN arrow keys to adjust game speed (1x to 8x)
- **Optimized Updates**: Entities handle speed internally for smooth high-speed gameplay
- **Frame Rate Independence**: Consistent gameplay regardless of frame rate
- **Performance Monitoring**: Real-time FPS counter and entity tracking

### Currency System
- **Starting Money**: Configurable starting cash (default: 20)
- **Enemy Rewards**: Money gained from defeating enemies (scales with wave)
- **Upgrade Currency**: Generated from damage dealt (1 currency per 40 damage)
- **Dynamic Pricing**: Tower costs increase based on wave number and towers built

### Lives System
- **Starting Lives**: Configurable starting lives (default: 10)  
- **Life Loss**: Lose 1 life when enemy reaches the end
- **Game Over**: Game ends when lives reach 0

### Victory & Defeat
- **Victory Condition**: Complete all 80 waves
- **Victory Screen**: Golden celebration screen with restart option
- **Defeat Screen**: Game over screen with restart functionality
- **Restart System**: Press 'R' key or click restart button to begin again

---

## User Interface & Controls

### Mouse Controls
- **Tower Placement**: Click on valid terrain to build selected tower
- **Tower Selection**: Click on built tower to view stats and upgrades
- **Tower Upgrades**: Click upgrade buttons in tower info panel
- **UI Navigation**: Click buttons to select towers, toggle panels

### Keyboard Controls
- **Speed Control**: UP/DOWN arrows to increase/decrease game speed
- **Restart**: 'R' key to restart the game at any time
- **ESC**: Close dialogs and panels

### Visual Indicators
- **Upgrade Available**: Gold coin with "↑" symbol appears on towers with affordable upgrades
- **Range Circles**: Displayed when selecting towers
- **Health Bars**: Show enemy damage status
- **Status Effects**: Visual overlays for freeze, poison, wet, etc.
- **Counter Effects**: "SUPER!", "HIT!", "WEAK" damage indicators
- **Detection Radius**: Visual indication of detector tower coverage

### Performance Display
- **FPS Counter**: Real-time frame rate monitoring
- **Entity Count**: Live count of enemies, towers, and projectiles
- **Wave Progress**: Current wave number and completion status

---

## Towers

### 🟢 Basic Category

#### BasicTower
- **Cost**: $20 (base, increases with wave/count)
- **Damage**: 2
- **Range**: 80
- **Fire Rate**: 25 frames (0.42s at 60 FPS)
- **Projectile Speed**: 6
- **Targeting**: Ground enemies only
- **Description**: Reliable starter tower with decent DPS for the cost
- **Strong Against**: BasicEnemy (1.3x), general purpose
- **Upgrade Path**: Damage, range, and fire rate improvements

#### SniperTower  
- **Cost**: $40 (base)
- **Damage**: 35 (high single-target)
- **Range**: 200 (longest range)
- **Fire Rate**: 90 frames (1.5s)
- **Projectile Speed**: 12
- **Targeting**: Ground only, prioritizes highest HP enemies
- **Description**: High-damage precision tower for eliminating priority targets
- **Strong Against**: FastEnemy (2.0x), InvisibleEnemy (1.8x), TeleportingEnemy (1.5x), AdaptiveEnemy (2.0x)
- **Special**: Always damages AdaptiveEnemy regardless of current adaptation
- **Upgrade Path**: Damage scaling, range extension, faster targeting

### 🔥 Damage Specialists

#### CannonTower
- **Cost**: $60 (base)
- **Damage**: 25 (kinetic)
- **Range**: 120
- **Fire Rate**: 75 frames (1.25s)
- **Description**: Anti-armor specialist using heavy kinetic projectiles
- **Strong Against**: ArmoredEnemy (2.0x), TankEnemy (1.8x), ShieldedEnemy (1.5x)
- **Upgrade Path**: Armor penetration, explosive shells, rapid fire

#### LaserTower
- **Cost**: $80 (base)
- **Damage**: 15 (continuous beam)
- **Range**: 150
- **Fire Rate**: Continuous (charges then fires)
- **Targeting**: Must charge before firing, can retarget during charge
- **Description**: Energy-based continuous beam weapon
- **Strong Against**: CrystallineEnemy (3.0x), ArmoredEnemy (1.8x), BlastProofEnemy (2.0x)
- **Weak Against**: EnergyShieldEnemy (0.5x)
- **Special**: Continuous damage output, armor-piercing energy
- **Upgrade Path**: Beam intensity, charge speed, multi-target

#### FlameTower
- **Cost**: $45 (base)
- **Damage**: 12 + burn DoT
- **Range**: 100
- **Fire Rate**: 45 frames (0.75s)
- **Description**: Applies burning damage over time
- **Strong Against**: ArmoredEnemy (1.5x), ToxicMutantEnemy (2.0x), PhaseShiftEnemy (1.8x)
- **Special**: Fire damage heals FireElementalEnemy by 50% of damage dealt
- **Upgrade Path**: Burn duration, damage over time, area ignition

### ⚡ Energy/Electric

#### LightningTower
- **Cost**: $50 (base)
- **Damage**: 18 (chain lightning)
- **Range**: 130
- **Fire Rate**: 120 frames (2.0s, charges for 0.5s)
- **Description**: Electric damage that chains between nearby enemies
- **Strong Against**: SpectralEnemy (3.0x), EnergyShieldEnemy (2.0x), Wet enemies (2.0x)
- **Weak Against**: GroundedEnemy (0.3x)
- **Special**: Chains to nearby enemies, extra damage to wet enemies
- **Upgrade Path**: Chain count, chain range, electrical intensity

### 🧊 Crowd Control

#### FreezerTower
- **Cost**: $30 (base)
- **Damage**: 8
- **Range**: 110
- **Fire Rate**: 40 frames (0.67s)
- **Description**: Applies freeze status to slow enemy movement
- **Strong Against**: FastEnemy (2.5x), FireElementalEnemy (2.0x), TeleportingEnemy (1.8x)
- **Special**: Freeze reduces enemy speed by 75% (50% for resistant enemies)
- **Upgrade Path**: Freeze duration, freeze penetration, ice damage

#### IceTower
- **Cost**: $55 (base)
- **Damage**: 20
- **Range**: 125
- **Fire Rate**: 70 frames (1.17s)
- **Description**: Heavy ice damage with wet status application
- **Strong Against**: FastEnemy (2.0x), FireElementalEnemy (3.0x), AdaptiveEnemy (2.0x), FlyingEnemy (1.5x)
- **Special**: Always damages AdaptiveEnemy, applies wet status for lightning synergy
- **Upgrade Path**: Ice shards, area freeze, absolute zero

### 💣 Explosive/AOE

#### MissileTower
- **Cost**: $100 (base)
- **Damage**: 40 direct + 25 splash
- **Range**: 250
- **Fire Rate**: 150 frames (2.5s) + 2s charge time
- **AOE Radius**: 60
- **Description**: Long-range homing missiles with area damage
- **Strong Against**: VoidEnemy (2.5x), FlyingEnemy (2.0x), SplittingEnemy (1.8x)
- **Weak Against**: BlastProofEnemy (0.5x)
- **Special**: Homing missiles, essential for VoidEnemy
- **Upgrade Path**: Missile count, homing accuracy, warhead power

#### ExplosiveTower
- **Cost**: $90 (base)
- **Damage**: 30 + AOE splash
- **Range**: 140
- **Fire Rate**: 80 frames (1.33s)
- **AOE Radius**: 50
- **Description**: Area denial with explosive projectiles
- **Strong Against**: VoidEnemy (2.5x), SplittingEnemy (2.0x), TeleportingEnemy (1.5x)
- **Weak Against**: BlastProofEnemy (0.3x)
- **Special**: Area damage, essential for VoidEnemy
- **Upgrade Path**: Blast radius, explosive yield, cluster bombs

#### SplashTower
- **Cost**: $120 (base)
- **Damage**: 22 + splash damage
- **Range**: 160
- **Fire Rate**: 55 frames (0.92s)
- **Description**: Multi-target engagement with splash damage
- **Strong Against**: SplittingEnemy (2.2x), TeleportingEnemy (1.8x), RegeneratingEnemy (1.5x)
- **Upgrade Path**: Splash radius, penetration, multi-shot

### 🧪 Status Effects

#### PoisonTower
- **Cost**: $35 (base)
- **Damage**: 10 + poison DoT
- **Range**: 115
- **Fire Rate**: 50 frames (0.83s)
- **Description**: Applies poison damage over time, counters regeneration
- **Strong Against**: RegeneratingEnemy (2.5x), ToxicMutantEnemy (2.0x), BasicEnemy (1.3x)
- **Special**: Poison bypasses some defenses, prevents regeneration
- **Upgrade Path**: Poison potency, duration, toxic clouds

### 🎯 Support/Detection

#### DetectorTower
- **Cost**: $25 (base)
- **Damage**: 0 (support only)
- **Detection Range**: 300
- **Description**: **ESSENTIAL** - Reveals invisible enemies for targeting
- **Special Features**:
  - Makes invisible enemies targetable (max 3 simultaneously)
  - Generates 2 upgrade currency per detected enemy per second
  - No direct combat capability
- **Critical For**: InvisibleEnemy, SpectralEnemy
- **Strategy**: Place strategically to cover key choke points
- **Upgrade Path**: Detection range, detection count, currency generation

#### AntiAirTower
- **Cost**: $70 (base)
- **Damage**: 28
- **Range**: 180
- **Fire Rate**: 45 frames (0.75s)
- **Targeting**: Prioritizes flying enemies, can target ground
- **Description**: Specialized anti-aircraft system
- **Strong Against**: FlyingEnemy (2.5x), InvisibleEnemy (1.8x)
- **Upgrade Path**: AA missiles, tracking systems, dual-targeting

---

## Enemies

### 🟢 Basic Tier (Waves 1-10)

#### BasicEnemy
- **Health**: 1 + wave scaling
- **Speed**: 1.0
- **Reward**: 4 + wave scaling
- **Size**: 8
- **Color**: Red
- **Description**: Standard enemy with no special abilities
- **Countered By**: Most towers, especially BasicTower with poison support

#### FastEnemy
- **Health**: 1 + wave scaling
- **Speed**: 2.0 (double speed)
- **Reward**: 5 + wave scaling
- **Size**: 7
- **Color**: Orange
- **Description**: High-speed enemy that's hard to hit
- **Countered By**: FreezerTower (2.5x), IceTower (2.0x), SniperTower (2.0x)
- **Strategy**: Slow or high-precision weapons required

#### TankEnemy
- **Health**: 5 + wave scaling (5x basic health)
- **Speed**: 0.6
- **Reward**: 8 + wave scaling
- **Size**: 12
- **Color**: Dark gray
- **Description**: Slow but heavily armored enemy
- **Countered By**: CannonTower (1.8x), sustained damage focus fire

### 🔵 Intermediate Tier (Waves 11-25)

#### FlyingEnemy
- **Health**: 2 + wave scaling
- **Speed**: 1.3
- **Reward**: 6 + wave scaling
- **Size**: 9
- **Color**: Light blue
- **Special**: **Cannot be targeted by ground-only towers**
- **Countered By**: AntiAirTower (2.5x), MissileTower (2.0x), IceTower (1.5x)
- **Strategy**: Anti-air coverage essential

#### ShieldedEnemy
- **Health**: 3 + wave scaling
- **Speed**: 1.0
- **Reward**: 7 + wave scaling
- **Size**: 10
- **Color**: Blue with shield effect
- **Special**: Energy shield provides damage reduction
- **Countered By**: CannonTower (1.5x), kinetic damage
- **Strategy**: Physical damage more effective than energy

#### InvisibleEnemy
- **Health**: 2 + wave scaling
- **Speed**: 1.2
- **Reward**: 8 + wave scaling
- **Size**: 8
- **Color**: Translucent/faded
- **Special**: **Cannot be targeted without DetectorTower**
- **Countered By**: AntiAirTower (1.8x), SniperTower (1.8x) - **requires detection**
- **Strategy**: DetectorTower is mandatory

#### ArmoredEnemy
- **Health**: 4 + wave scaling
- **Speed**: 0.8
- **Reward**: 9 + wave scaling
- **Size**: 11
- **Color**: Metallic gray
- **Special**: High physical resistance
- **Countered By**: CannonTower (2.0x), LaserTower (1.8x), FlameTower (1.5x)
- **Strategy**: Armor-piercing weapons required

### 🟠 Advanced Tier (Waves 26-40)

#### RegeneratingEnemy
- **Health**: 6 + wave scaling
- **Speed**: 0.9
- **Reward**: 12 + wave scaling
- **Size**: 10
- **Color**: Green with pulse effect
- **Special**: Continuously regenerates health over time
- **Countered By**: PoisonTower (2.5x), SplashTower (1.5x)
- **Strategy**: Damage over time or burst damage to overwhelm regeneration

#### TeleportingEnemy
- **Health**: 3 + wave scaling
- **Speed**: 1.4
- **Reward**: 15 + wave scaling
- **Size**: 9
- **Color**: Purple with particle effects
- **Special**: **Teleports forward when taking damage (50% chance, 1.5s cooldown)**
- **Teleport Mechanics**:
  - Jumps 1/3 of remaining path distance
  - Avoids damage from current attack
  - Creates particle effects during teleport
- **Countered By**: SniperTower (1.5x), ExplosiveTower (1.5x), SplashTower (1.8x), FreezerTower (1.8x)
- **Strategy**: Area damage or prediction-based targeting

#### SplittingEnemy
- **Health**: 4 + wave scaling
- **Speed**: 1.1
- **Reward**: 10 + wave scaling
- **Size**: 12
- **Color**: Magenta with generation indicators
- **Special**: **Splits into 2 random enemies when destroyed**
- **Split Mechanics**:
  - Spawns 2 enemies appropriate for current wave (no bosses)
  - Spawned enemies have 75% health of their normal values
  - Inherit path position and continue from death location
  - Enemy types based on wave progression
- **Countered By**: MissileTower (1.8x), ExplosiveTower (2.0x), SplashTower (2.2x)
- **Strategy**: AOE damage to handle splits efficiently

### 🔴 Elite Tier (Waves 41-60)

#### EnergyShieldEnemy
- **Health**: 8 + wave scaling
- **Speed**: 1.0
- **Reward**: 18 + wave scaling
- **Size**: 12
- **Color**: Cyan with energy barrier
- **Special**: Energy shield absorbs laser attacks
- **Countered By**: LightningTower (2.0x), kinetic weapons
- **Weak Against**: LaserTower (0.5x)
- **Strategy**: Physical or lightning damage bypass shield

#### GroundedEnemy
- **Health**: 7 + wave scaling
- **Speed**: 0.7
- **Reward**: 16 + wave scaling
- **Size**: 13
- **Color**: Brown/earth tones
- **Special**: Grounded connection makes it immune to electrical attacks
- **Weak Against**: LightningTower (0.3x)
- **Strategy**: Avoid electric damage completely

#### FireElementalEnemy
- **Health**: 6 + wave scaling
- **Speed**: 1.3
- **Reward**: 20 + wave scaling
- **Size**: 11
- **Color**: Red-orange with flame effects
- **Special**: **Heals 50% of fire damage received instead of taking damage**
- **Countered By**: IceTower (3.0x), FreezerTower (2.0x)
- **Immune To**: FlameTower (actually heals from it)
- **Strategy**: Ice damage is critical, avoid all fire damage

#### PhaseShiftEnemy
- **Health**: 5 + wave scaling
- **Speed**: 1.6
- **Reward**: 22 + wave scaling
- **Size**: 9
- **Color**: Shifting translucent
- **Special**: Phases through some physical attacks
- **Countered By**: FlameTower (1.8x)
- **Strategy**: Flame damage disrupts phasing mechanism

#### BlastProofEnemy
- **Health**: 12 + wave scaling
- **Speed**: 0.5
- **Reward**: 25 + wave scaling
- **Size**: 14
- **Color**: Armored with blast-resistant plating
- **Special**: Highly resistant to all explosive damage
- **Countered By**: LaserTower (2.0x), kinetic weapons
- **Weak Against**: MissileTower (0.5x), ExplosiveTower (0.3x)
- **Strategy**: Completely avoid explosive damage

### 🟣 Legendary Tier (Waves 61+)

#### SpectralEnemy
- **Health**: 15 + wave scaling
- **Speed**: 1.2
- **Reward**: 35 + wave scaling
- **Size**: 10
- **Color**: Ghostly white/transparent
- **Special**: Partially invisible, phases through most physical attacks
- **Countered By**: LightningTower (3.0x), energy-based damage
- **Strategy**: Energy damage bypasses spectral nature

#### CrystallineEnemy
- **Health**: 20 + wave scaling
- **Speed**: 0.8
- **Reward**: 40 + wave scaling
- **Size**: 15
- **Color**: Crystalline with light refraction
- **Special**: Crystal structure reflects some attacks
- **Countered By**: LaserTower (3.0x)
- **Strategy**: Laser resonance shatters crystal armor

#### ToxicMutantEnemy
- **Health**: 18 + wave scaling
- **Speed**: 1.1
- **Reward**: 38 + wave scaling
- **Size**: 13
- **Color**: Sickly green with toxic aura
- **Special**: Toxic resistance and poisonous aura
- **Countered By**: PoisonTower (2.0x), FlameTower (2.0x)
- **Strategy**: Stronger toxins or fire damage overcome resistance

#### VoidEnemy
- **Health**: 40 + wave scaling
- **Speed**: 0.8
- **Reward**: 50 + wave scaling
- **Size**: 15
- **Color**: Deep black/void appearance
- **Special**: **Absorbs most attack types - ONLY vulnerable to explosives/missiles**
- **Countered By**: MissileTower (2.5x), ExplosiveTower (2.5x)
- **Immune To**: ALL other damage types
- **Strategy**: **MANDATORY** explosive/missile towers or VoidEnemy is invincible

#### AdaptiveEnemy
- **Health**: 45 + wave scaling
- **Speed**: 1.1
- **Reward**: 60 + wave scaling
- **Size**: 16
- **Color**: Shifting through different colors based on adaptation
- **Special**: **Changes immunities every 3 seconds, cycles through 5 adaptations**
- **Adaptation Cycle**:
  - **FIRE**: Immune to basic, cannon, poison, lightning
  - **NATURE**: Immune to laser, missile, flame, explosive
  - **WATER**: Immune to freezer, splash, antiair, basic
  - **ENERGY**: Immune to lightning, laser, cannon, poison
  - **VOID**: Immune to missile, explosive, flame, antiair
- **Countered By**: SniperTower (2.0x), IceTower (2.0x) - **ALWAYS effective**
- **Strategy**: Only sniper and ice towers can consistently damage regardless of adaptation

---

## Boss Enemies

The game features 4 ultimate bosses that appear in specific wave patterns and represent the pinnacle of the challenge.

### TimeLordBoss (Waves 20, 40, 60, 80)
- **Health**: 4000 + extreme wave scaling
- **Speed**: 1.2
- **Reward**: 500+
- **Size**: 30
- **Color**: Cosmic blue with time distortion effects
- **Ultimate Abilities**:
  - **Time Slow**: Slows all projectiles and towers in large radius
  - **Damage Rewind**: Can reverse recent damage taken
  - **Temporal Rifts**: Creates space-time distortions that affect projectile paths
  - **Chronos Shield**: Periodic invincibility phases
- **Strategy**: Focus fire during vulnerability windows, spread towers to minimize time effects
- **Lore**: Master of time and space, manipulates temporal flow to avoid damage

### NecromancerBoss (Waves 30, 50, 70)
- **Health**: 3500 + extreme wave scaling
- **Speed**: 0.9
- **Reward**: 450+
- **Size**: 28
- **Color**: Dark purple with necromantic aura
- **Ultimate Abilities**:
  - **Life Drain**: Heals by draining health from nearby enemies/towers
  - **Undead Summoning**: Spawns skeleton minions that move toward towers
  - **Death Aura**: Damages nearby towers over time
  - **Soul Shield**: Absorbs damage based on nearby undead minions
- **Immunities**: Completely immune to poison damage
- **Strategy**: Eliminate summoned minions quickly, use non-poison damage sources
- **Lore**: Dark mage commanding armies of the undead

### ShadowKing (Waves 25, 45, 65)
- **Health**: 4500 + extreme wave scaling
- **Speed**: 1.5
- **Reward**: 550+
- **Size**: 32
- **Color**: Pure black with shadow tendrils
- **Ultimate Abilities**:
  - **Dimension Phase**: 70% chance to dodge any attack by phasing into shadow realm
  - **Shadow Duplicates**: Creates shadow copies that confuse targeting
  - **Darkness Manipulation**: Reduces visibility and tower accuracy
  - **Void Step**: Can teleport past tower clusters
- **Strategy**: High rate of fire to overcome dodge chance, spread defenses for teleportation
- **Lore**: Ruler of the shadow dimension with mastery over darkness itself

### CrystalOverlord (Waves 35, 55, 75)
- **Health**: 5500 + extreme wave scaling (highest HP boss)
- **Speed**: 0.7
- **Reward**: 600+
- **Size**: 35
- **Color**: Brilliant crystal with light refraction
- **Ultimate Abilities**:
  - **Projectile Reflection**: 40% chance to reflect projectiles back at towers
  - **Crystal Barriers**: Creates protective barriers that block projectiles
  - **Prismatic Shield**: High damage reduction against most attack types
  - **Crystal Shard Rain**: Damages towers in large area periodically
- **Immunities**: Completely immune to laser damage (too much crystal resonance)
- **Strategy**: Use non-laser high-damage weapons, position towers to avoid reflection damage
- **Lore**: Ancient crystal entity with power over light and matter

---

## Counter System

The counter system creates rock-paper-scissors style interactions where certain towers are extremely effective or ineffective against specific enemies.

### Damage Multiplier Categories
- **Hard Counter (3.0x)**: Devastating effectiveness
- **Strong Counter (2.0-2.5x)**: Very effective
- **Effective (1.5-1.9x)**: Above average damage
- **Normal (1.0x)**: Standard damage
- **Weak (0.5-0.9x)**: Reduced effectiveness
- **Resistant (0.3-0.4x)**: Highly resistant
- **Immune (0.1x)**: Nearly no damage

### Critical Counter Relationships

#### Hard Counters (3.0x) - Build These!
- **IceTower → FireElementalEnemy**: Ice extinguishes fire completely
- **LaserTower → CrystallineEnemy**: Laser resonance shatters crystals
- **LightningTower → SpectralEnemy**: Energy disrupts spectral form

#### Essential Counters (2.5x)
- **AntiAirTower → FlyingEnemy**: Specialized anti-aircraft
- **FreezerTower → FastEnemy**: Slowing fast enemies
- **MissileTower → VoidEnemy**: Only way to damage void
- **ExplosiveTower → VoidEnemy**: Only way to damage void
- **PoisonTower → RegeneratingEnemy**: Stops regeneration

#### Always Effective (ignores immunities)
- **SniperTower → AdaptiveEnemy**: Always damages regardless of adaptation
- **IceTower → AdaptiveEnemy**: Always damages regardless of adaptation

#### Critical Weaknesses (avoid these!)
- **LightningTower → GroundedEnemy (0.3x)**: Grounding negates electricity
- **LaserTower → EnergyShieldEnemy (0.5x)**: Energy shield blocks lasers
- **ExplosiveTower → BlastProofEnemy (0.3x)**: Blast-resistant armor
- **MissileTower → BlastProofEnemy (0.5x)**: Explosion resistance
- **FlameTower → FireElementalEnemy**: Actually heals the enemy!

### Wet Status Synergy
- **IceTower** applies wet status
- **LightningTower** does 2.0x damage to wet enemies
- **Combo Strategy**: Ice towers set up lightning towers for massive damage

---

## Upgrade System

### Tower Upgrades
- **Upgrade Currency**: Generated by dealing damage (1 currency per 40 damage dealt)
- **Upgrade Availability**: Gold coin with "↑" symbol appears on towers with affordable upgrades
- **Upgrade Categories**: Damage, range, fire rate, special abilities
- **Progressive Costs**: Upgrades become more expensive with each tier

### DetectorTower Currency Generation
- **Passive Income**: DetectorTowers generate 2 upgrade currency per detected enemy per second
- **Economic Strategy**: DetectorTowers provide both utility and economic benefits
- **Scaling Rewards**: More valuable in later waves with stronger enemies

---

## Wave System & Campaign

### 80-Wave Campaign Structure
- **Waves 1-15**: Introduction and basic enemies
- **Waves 16-30**: Intermediate enemies and first boss cycle
- **Waves 31-50**: Advanced enemies and mid-game bosses
- **Waves 51-70**: Elite enemies and late-game bosses
- **Waves 71-80**: Legendary enemies and final boss encounters

### Boss Wave Distribution
- **TimeLordBoss**: Waves 20, 40, 60, 80 (final boss)
- **NecromancerBoss**: Waves 30, 50, 70
- **ShadowKing**: Waves 25, 45, 65
- **CrystalOverlord**: Waves 35, 55, 75

### Enemy Introduction System
- **New Enemy Alerts**: Pop-up introductions when new enemies first appear
- **Enemy Information**: Description, abilities, immunities, and counter recommendations
- **Strategic Preparation**: Advance warning allows strategic tower planning

### Wave Scaling
- **Health Scaling**: Enemy health increases significantly with wave number
- **Speed Scaling**: Some enemies become faster in later waves
- **Reward Scaling**: Money rewards increase to match tower costs
- **Immunity Progression**: Higher chance of random immunities in later waves

---

## Terrain System

### Terrain Types and Effects

#### Grass (Green)
- **Effect**: Standard terrain, no modifiers
- **Tower Placement**: Allowed
- **Enemy Movement**: Normal speed

#### Path (Brown)
- **Effect**: Enemy pathway
- **Tower Placement**: **Not allowed**
- **Enemy Movement**: Normal speed

#### Rock (Gray)
- **Effect**: Impassable terrain
- **Tower Placement**: **Not allowed**
- **Strategic Use**: Natural barriers and choke points

#### Water (Blue)
- **Effect**: Special placement rules
- **Tower Placement**: Limited tower types only
- **Enemy Movement**: Normal (enemies don't enter water)
- **Special**: Enhances freeze effects from nearby towers

#### Forest (Dark Green)
- **Effect**: Dense vegetation
- **Tower Placement**: Allowed with modifications
- **Tower Modifiers**: -20% range, +30% damage
- **Strategy**: High-damage, short-range positioning

#### Sand (Tan)
- **Effect**: Loose terrain
- **Tower Placement**: Allowed
- **Enemy Movement**: +50% speed (enemies move faster)
- **Strategy**: Use slowing towers in sand areas

---

## Status Effects

### Freeze
- **Effect**: Reduces enemy speed by 75% (50% for resistant enemies)
- **Duration**: Variable based on tower and enemy resistance
- **Applied By**: FreezerTower, IceTower
- **Visual**: Blue tint on frozen enemies
- **Strategy**: Essential for fast enemies and crowd control

### Poison
- **Effect**: Damage over time, prevents regeneration
- **Duration**: Stacks and refreshes with repeated application
- **Applied By**: PoisonTower
- **Visual**: Green bubbles around poisoned enemies
- **Strategy**: Excellent against regenerating enemies

### Wet
- **Effect**: Increases lightning damage by 100%
- **Duration**: Temporary, can be refreshed
- **Applied By**: IceTower, water effects
- **Visual**: Water droplets around wet enemies
- **Strategy**: Combo with lightning towers for massive damage

### Burn
- **Effect**: Damage over time from fire
- **Duration**: Stacks with repeated fire exposure
- **Applied By**: FlameTower
- **Visual**: Flame effects on burning enemies
- **Special**: Heals FireElementalEnemy instead of damaging

---

## Performance & Optimization

### Speed System Optimization
- **Internal Speed Handling**: All entities handle speed multipliers internally
- **Smooth High-Speed Play**: Game remains smooth even at 8x speed
- **Frame Rate Independence**: Consistent behavior regardless of FPS
- **Memory Efficient**: Optimized update loops and rendering

### Performance Monitoring
- **Real-time FPS**: Live frame rate display
- **Entity Tracking**: Count of active enemies, towers, projectiles
- **Performance Scaling**: System automatically optimizes based on entity count

### Visual Optimizations
- **Efficient Rendering**: Optimized drawing routines for high entity counts
- **Effect Management**: Particle effects cleaned up automatically
- **UI Optimization**: Streamlined interface updates

---

## Configuration System

### Main Configuration File
- **Location**: `config/tower_defense_game.json`
- **Format**: JSON configuration file
- **Hot Reload**: Some changes take effect immediately

### Configurable Game Settings

#### Starting Resources
```json
{
  "game_config": {
    "starting_money": 20,
    "starting_lives": 10
  }
}
```

#### Wave Configuration
- **Enemy Composition**: Which enemies appear in which waves
- **Boss Scheduling**: When boss enemies appear
- **Scaling Factors**: Health and reward scaling per wave

#### Tower Balance
- **Base Costs**: Starting prices for all tower types
- **Damage Values**: Base damage for each tower
- **Range Settings**: Attack ranges and detection ranges

#### Counter System
- **Damage Multipliers**: Effectiveness values between towers and enemies
- **Special Interactions**: Unique mechanics like wet/lightning synergy

### Easy Customization
- **Single File Changes**: Most gameplay tweaks in one configuration file
- **Modular Design**: Easy to adjust specific aspects without affecting others
- **Balanced Defaults**: Thoroughly tested default values

---

## Strategic Guide

### Early Game Strategy (Waves 1-15)
1. **Start with BasicTowers**: Cost-effective early damage
2. **Add FreezerTower**: Essential crowd control for FastEnemy
3. **Build DetectorTower**: Mandatory before InvisibleEnemy appears
4. **Focus on Economy**: More towers = more damage = more upgrade currency

### Mid Game Strategy (Waves 16-35)
1. **AntiAir Coverage**: FlyingEnemy requires specialized targeting
2. **Diversify Damage Types**: Counter system becomes critical
3. **Upgrade Key Towers**: Focus upgrades on most effective counters
4. **Boss Preparation**: Ensure multiple damage sources for boss waves

### Late Game Strategy (Waves 36-60)
1. **Counter Specialization**: Build specific counters for enemy types
2. **AOE Damage**: SplittingEnemy and groups require area damage
3. **Status Synergy**: Ice + Lightning combos become very powerful
4. **High-Damage Focus**: Elite enemies have massive health pools

### End Game Strategy (Waves 61-80)
1. **VoidEnemy Preparation**: **MANDATORY** explosive/missile towers
2. **AdaptiveEnemy Counters**: Only SniperTower and IceTower work consistently
3. **Boss Specialists**: Different strategies for each ultimate boss
4. **Resource Management**: Upgrade currency becomes critical for final push

### Universal Strategic Principles

#### Detection is Mandatory
- **DetectorTower Placement**: Cover all choke points where invisible enemies pass
- **Detection Limits**: Only 3 enemies can be detected simultaneously
- **Strategic Positioning**: Place detectors where most towers can benefit

#### Counter Knowledge is Critical
- **Study Enemy Types**: Learn which towers are effective against which enemies
- **Avoid Bad Matchups**: Never use towers that are weak against common enemies
- **Build Versatile**: Some enemies are only vulnerable to specific damage types

#### Economy Management
- **Early Investment**: More towers early = more damage = more upgrade currency
- **DetectorTower Income**: Use detector towers for both utility and economy
- **Upgrade Priority**: Focus upgrades on your most effective counters

#### Positioning Strategy
- **Choke Points**: Maximize damage by placing towers where enemies bunch up
- **Range Overlap**: Multiple towers covering the same area for focus fire
- **Terrain Utilization**: Use forest for high damage, avoid sand for enemy speed boost

#### Boss Fight Preparation
- **Diverse Damage Sources**: Don't rely on single tower types for bosses
- **Spread Positioning**: Some bosses have area effects that damage multiple towers
- **Resource Stockpiling**: Save upgrade currency for critical boss wave improvements

### Advanced Techniques

#### Ice + Lightning Synergy
1. Place IceTowers to apply wet status
2. Follow up with LightningTowers for 2.0x damage to wet enemies
3. Devastating combination for high-health targets

#### Detection Economy
1. Place DetectorTowers strategically for both detection and currency generation
2. Higher-level enemies provide more currency when detected
3. Balance detection coverage with economic benefit

#### Counter Cycling
1. Adapt tower builds based on upcoming enemy types
2. Use enemy introduction system to prepare counters in advance
3. Sometimes it's better to build counters preemptively

#### Resource Optimization
1. Balance money spent on new towers vs upgrading existing towers
2. Upgrade towers that handle multiple enemy types first
3. Use temporary towers to handle specific threats, then sell if needed

---

## Conclusion

This tower defense game offers deep strategic gameplay through its sophisticated counter system, diverse enemy types, and progressive difficulty scaling. Success requires understanding enemy weaknesses, building appropriate counters, managing resources effectively, and adapting strategies as new threats emerge.

The 80-wave campaign provides a complete and challenging experience, culminating in battles against four ultimate bosses, each requiring different tactical approaches. Master the counter system, utilize terrain effectively, and plan your economy to achieve victory!

**Remember**: Detection is mandatory, counters are critical, and adaptability is key to surviving all 80 waves and achieving ultimate victory! 