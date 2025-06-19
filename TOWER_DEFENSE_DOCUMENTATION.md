# Tower Defense Game - Complete Documentation

## Table of Contents
1. [Game Mechanics](#game-mechanics)
2. [Towers](#towers)
3. [Enemies](#enemies)
4. [Counter System](#counter-system)
5. [Upgrade System](#upgrade-system)
6. [Strategic Recommendations](#strategic-recommendations)

---

## Game Mechanics

### Core Systems
- **Progressive Immunity**: Enemies gain random resistances based on wave number (1% chance per wave, max 15%)
- **Counter System**: Towers deal 0.1x to 3.0x damage based on enemy matchups
- **Currency Generation**: Towers generate upgrade currency based on damage dealt (1 per 40 damage)
- **Terrain Effects**: Different terrain types modify tower and enemy performance
- **Dynamic Pricing**: Tower costs increase per wave and per tower built

### Terrain Types
- **Grass** (Green): Standard terrain, no modifiers
- **Path** (Brown): Enemy pathway, no tower placement
- **Rock** (Gray): Impassable terrain
- **Water** (Blue): Special placement rules, boosts freeze effects
- **Forest** (Dark Green): -20% range, +30% damage for towers
- **Sand** (Tan): +50% enemy speed

---

## Towers

### 🟢 Basic Category

#### BasicTower
- **Cost**: $20 (base)
- **Damage**: 2
- **Range**: 80
- **Fire Rate**: 25 frames (0.42s)
- **Speed**: 6
- **Targeting**: Ground only
- **Use**: Early game staple, cost-effective DPS
- **Strong Against**: BasicEnemy (1.3x via poison synergy)
- **Weak Against**: Flying, Invisible enemies

#### SniperTower  
- **Cost**: $40 (base)
- **Damage**: 35
- **Range**: 200 (longest)
- **Fire Rate**: 90 frames (1.5s)
- **Speed**: 12
- **Targeting**: Ground only, prioritizes highest HP
- **Use**: High-value target elimination
- **Strong Against**: FastEnemy (2.0x), InvisibleEnemy (1.8x), TeleportingEnemy (1.5x), AdaptiveEnemy (2.0x)
- **Special**: Can always damage AdaptiveEnemy regardless of adaptation

### 🔥 Damage Specialists

#### CannonTower
- **Cost**: $60 (base)  
- **Damage**: 25
- **Range**: 120
- **Fire Rate**: 75 frames (1.25s)
- **Use**: Anti-armor specialist
- **Strong Against**: ArmoredEnemy (2.0x), TankEnemy (1.8x), ShieldedEnemy (1.5x)
- **Special**: Heavy kinetic damage pierces armor

#### LaserTower
- **Cost**: $80 (base)
- **Damage**: 15 (continuous beam)
- **Range**: 150
- **Fire Rate**: Continuous
- **Use**: Energy damage, armor piercing
- **Strong Against**: CrystallineEnemy (3.0x), ArmoredEnemy (1.8x), BlastProofEnemy (2.0x)
- **Weak Against**: EnergyShieldEnemy (0.5x)
- **Special**: Continuous damage over time

#### FlameTower
- **Cost**: $45 (base)
- **Damage**: 12 + burn DoT
- **Range**: 100  
- **Fire Rate**: 45 frames (0.75s)
- **Use**: Damage over time, area denial
- **Strong Against**: ArmoredEnemy (1.5x), ToxicMutantEnemy (2.0x), PhaseShiftEnemy (1.8x)
- **Special**: Applies burn status, stacks damage

### ⚡ Energy/Electric

#### LightningTower
- **Cost**: $50 (base)
- **Damage**: 18 (chain lightning)
- **Range**: 130
- **Fire Rate**: 60 frames (1s)
- **Use**: Multi-target electric damage
- **Strong Against**: SpectralEnemy (3.0x), EnergyShieldEnemy (2.0x), Wet enemies (2.0x)
- **Weak Against**: GroundedEnemy (0.3x)
- **Special**: Chains between nearby enemies, synergizes with wet status

### 🧊 Crowd Control

#### FreezerTower
- **Cost**: $30 (base)
- **Damage**: 8
- **Range**: 110
- **Fire Rate**: 40 frames (0.67s)
- **Use**: Crowd control and slowing
- **Strong Against**: FastEnemy (2.5x), FireElementalEnemy (2.0x), TeleportingEnemy (1.8x)
- **Special**: Applies freeze status (75% speed reduction)

#### IceTower
- **Cost**: $55 (base)
- **Damage**: 20
- **Range**: 125
- **Fire Rate**: 70 frames (1.17s)
- **Use**: Heavy freeze damage
- **Strong Against**: FastEnemy (2.0x), FireElementalEnemy (3.0x), AdaptiveEnemy (2.0x), FlyingEnemy (1.5x)
- **Special**: Can always damage AdaptiveEnemy, applies wet status

### 💣 Explosive/AOE

#### MissileTower
- **Cost**: $100 (base)
- **Damage**: 40 direct + 25 splash
- **Range**: 250
- **Fire Rate**: 150 frames (2.5s) + 2s charge
- **AOE**: 60 radius
- **Use**: Long-range area damage
- **Strong Against**: VoidEnemy (2.5x), FlyingEnemy (2.0x), SplittingEnemy (1.8x)
- **Weak Against**: BlastProofEnemy (0.5x)
- **Special**: Homing missiles, charges before firing

#### ExplosiveTower
- **Cost**: $90 (base)
- **Damage**: 30 + AOE splash
- **Range**: 140
- **Fire Rate**: 80 frames (1.33s)
- **AOE**: 50 radius
- **Use**: Area denial, group damage
- **Strong Against**: VoidEnemy (2.5x), SplittingEnemy (2.0x), TeleportingEnemy (1.5x)
- **Weak Against**: BlastProofEnemy (0.3x)

#### SplashTower
- **Cost**: $120 (base)
- **Damage**: 22 + splash damage
- **Range**: 160
- **Fire Rate**: 55 frames (0.92s)
- **Use**: Multi-enemy engagements
- **Strong Against**: SplittingEnemy (2.2x), TeleportingEnemy (1.8x), RegeneratingEnemy (1.5x)

### 🧪 Status Effects

#### PoisonTower
- **Cost**: $35 (base)
- **Damage**: 10 + poison DoT
- **Range**: 115
- **Fire Rate**: 50 frames (0.83s)
- **Use**: Damage over time, anti-regen
- **Strong Against**: RegeneratingEnemy (2.5x), ToxicMutantEnemy (2.0x), BasicEnemy (1.3x)
- **Special**: Applies poison status, bypasses some defenses

### 🎯 Support/Utility

#### DetectorTower
- **Cost**: $25 (base)
- **Damage**: 0
- **Range**: 0 (300 detection range)
- **Use**: Reveals invisible enemies, generates currency
- **Special**: Makes invisible enemies targetable by other towers (max 3), generates 2 currency per enemy per second
- **Essential For**: Dealing with InvisibleEnemy, SpectralEnemy

#### AntiAirTower
- **Cost**: $70 (base)
- **Damage**: 28
- **Range**: 180
- **Fire Rate**: 45 frames (0.75s)
- **Targeting**: Flying priority
- **Use**: Flying enemy specialist
- **Strong Against**: FlyingEnemy (2.5x), InvisibleEnemy (1.8x)
- **Special**: Can target both ground and air, prioritizes flying

---

## Enemies

### 🟢 Basic Tier (Waves 1-10)

#### BasicEnemy
- **Health**: 1 + wave scaling
- **Speed**: 1.0
- **Reward**: 4 + wave scaling  
- **Size**: 8
- **Immunities**: Random (wave-based)
- **Countered By**: Most towers, especially BasicTower with poison support

#### FastEnemy
- **Health**: 1 + wave scaling
- **Speed**: 2.0 (double speed)
- **Reward**: 5 + wave scaling
- **Size**: 7
- **Countered By**: FreezerTower (2.5x), IceTower (2.0x), SniperTower (2.0x)
- **Strategy**: Use slowing effects to manage speed advantage

#### TankEnemy
- **Health**: 5 + wave scaling (5x basic)
- **Speed**: 0.6
- **Reward**: 8 + wave scaling
- **Size**: 12
- **Countered By**: CannonTower (1.8x), high-damage focused fire
- **Strategy**: High HP requires sustained damage or armor-piercing

### 🔵 Intermediate Tier (Waves 11-25)

#### FlyingEnemy
- **Health**: 2 + wave scaling
- **Speed**: 1.3
- **Reward**: 6 + wave scaling
- **Size**: 9
- **Special**: Cannot be targeted by ground-only towers
- **Countered By**: AntiAirTower (2.5x), MissileTower (2.0x), IceTower (1.5x)
- **Strategy**: Requires specialized anti-air coverage

#### ShieldedEnemy
- **Health**: 3 + wave scaling  
- **Speed**: 1.0
- **Reward**: 7 + wave scaling
- **Size**: 10
- **Special**: Energy shield reduces some damage
- **Countered By**: CannonTower (1.5x), kinetic damage
- **Strategy**: Physical damage more effective than energy

#### InvisibleEnemy
- **Health**: 2 + wave scaling
- **Speed**: 1.2
- **Reward**: 8 + wave scaling
- **Size**: 8
- **Special**: Cannot be targeted without DetectorTower
- **Countered By**: AntiAirTower (1.8x), SniperTower (1.8x) (both require detection)
- **Strategy**: DetectorTower mandatory for engagement

#### ArmoredEnemy
- **Health**: 4 + wave scaling
- **Speed**: 0.8
- **Reward**: 9 + wave scaling
- **Size**: 11
- **Special**: High physical resistance
- **Countered By**: CannonTower (2.0x), LaserTower (1.8x), FlameTower (1.5x)
- **Strategy**: Armor-piercing or energy damage required

### 🟠 Advanced Tier (Waves 26-40)

#### RegeneratingEnemy
- **Health**: 6 + wave scaling
- **Speed**: 0.9
- **Reward**: 12 + wave scaling
- **Size**: 10
- **Special**: Regenerates health over time
- **Countered By**: PoisonTower (2.5x), SplashTower (1.5x)
- **Strategy**: Sustained DoT or burst damage to overwhelm regen

#### TeleportingEnemy
- **Health**: 3 + wave scaling
- **Speed**: 1.4
- **Reward**: 15 + wave scaling
- **Size**: 9
- **Special**: Teleports forward randomly
- **Countered By**: SniperTower (1.5x), ExplosiveTower (1.5x), SplashTower (1.8x), FreezerTower (1.8x)
- **Strategy**: Area damage or prediction-based targeting

#### SplittingEnemy
- **Health**: 4 + wave scaling
- **Speed**: 1.1
- **Reward**: 10 + wave scaling
- **Size**: 12
- **Special**: Splits into smaller enemies on death
- **Countered By**: MissileTower (1.8x), ExplosiveTower (2.0x), SplashTower (2.2x)
- **Strategy**: AOE damage to handle splits efficiently

### 🔴 Elite Tier (Waves 41-60)

#### EnergyShieldEnemy
- **Health**: 8 + wave scaling
- **Speed**: 1.0
- **Reward**: 18 + wave scaling
- **Size**: 12
- **Special**: Energy shield absorbs energy attacks
- **Countered By**: LightningTower (2.0x)
- **Weak Against**: LaserTower (0.5x)
- **Strategy**: Physical or lightning damage bypass shield

#### GroundedEnemy
- **Health**: 7 + wave scaling
- **Speed**: 0.7
- **Reward**: 16 + wave scaling
- **Size**: 13
- **Special**: Immune to electrical attacks
- **Weak Against**: LightningTower (0.3x)
- **Strategy**: Avoid electric damage, use physical/fire/ice

#### FireElementalEnemy
- **Health**: 6 + wave scaling
- **Speed**: 1.3
- **Reward**: 20 + wave scaling
- **Size**: 11
- **Special**: Fire-based, heat aura
- **Countered By**: IceTower (3.0x), FreezerTower (2.0x)
- **Strategy**: Ice damage extremely effective

#### PhaseShiftEnemy
- **Health**: 5 + wave scaling
- **Speed**: 1.6
- **Reward**: 22 + wave scaling
- **Size**: 9
- **Special**: Phases through some attacks
- **Countered By**: FlameTower (1.8x)
- **Strategy**: Flame damage disrupts phasing

#### BlastProofEnemy
- **Health**: 12 + wave scaling
- **Speed**: 0.5
- **Reward**: 25 + wave scaling
- **Size**: 14
- **Special**: Highly resistant to explosives
- **Countered By**: LaserTower (2.0x)
- **Weak Against**: MissileTower (0.5x), ExplosiveTower (0.3x)
- **Strategy**: Avoid explosive damage entirely

### 🟣 Legendary Tier (Waves 61+)

#### SpectralEnemy
- **Health**: 15 + wave scaling
- **Speed**: 1.2
- **Reward**: 35 + wave scaling
- **Size**: 10
- **Special**: Partially invisible, phases through physical attacks
- **Countered By**: LightningTower (3.0x)
- **Strategy**: Energy damage bypasses spectral nature

#### CrystallineEnemy
- **Health**: 20 + wave scaling
- **Speed**: 0.8
- **Reward**: 40 + wave scaling
- **Size**: 15
- **Special**: Crystal armor, reflects some attacks
- **Countered By**: LaserTower (3.0x)
- **Strategy**: Laser damage resonates with crystal structure

#### ToxicMutantEnemy
- **Health**: 18 + wave scaling
- **Speed**: 1.1
- **Reward**: 38 + wave scaling
- **Size**: 13
- **Special**: Toxic aura, poison immunity
- **Countered By**: PoisonTower (2.0x), FlameTower (2.0x)
- **Strategy**: Fire or stronger poisons overcome resistance

#### VoidEnemy
- **Health**: 40 + wave scaling
- **Speed**: 0.8
- **Reward**: 50 + wave scaling
- **Size**: 15
- **Special**: Absorbs most attack types, only vulnerable to explosives/missiles
- **Countered By**: MissileTower (2.5x), ExplosiveTower (2.5x)
- **Vulnerable To**: ONLY missile and explosive damage
- **Strategy**: Build explosive/missile towers or void enemies are invincible

#### AdaptiveEnemy
- **Health**: 45 + wave scaling
- **Speed**: 1.1
- **Reward**: 60 + wave scaling
- **Size**: 16
- **Special**: Changes immunities every 3 seconds, cycles through 5 adaptations
- **Countered By**: SniperTower (2.0x), IceTower (2.0x) - ALWAYS effective
- **Adaptations**: 
  - FIRE: Immune to basic, cannon, poison, lightning
  - NATURE: Immune to laser, missile, flame, explosive  
  - WATER: Immune to freezer, splash, antiair, basic
  - ENERGY: Immune to lightning, laser, cannon, poison
  - VOID: Immune to missile, explosive, flame, antiair
- **Strategy**: Only sniper and ice towers can consistently damage

### 👑 Boss Enemies

#### SpeedBoss (Waves 15, 25, 55, 65)
- **Health**: 100+ (massive scaling)
- **Speed**: 2.5 (very fast)
- **Reward**: 100+
- **Size**: 20
- **Special**: Spawns minions, high speed
- **Strategy**: Focus fire, crowd control essential

#### MegaBoss (Waves 35, 45, 50, 60, 70, 75, 80)  
- **Health**: 200+ (extreme scaling)
- **Speed**: 1.0
- **Reward**: 200+
- **Size**: 25
- **Special**: Spawns minions continuously, multiple phases
- **Strategy**: Sustained damage, anti-minion measures

---

## Counter System

### Damage Multipliers
- **Super Effective**: 2.5x - 3.0x damage
- **Effective**: 1.5x - 2.0x damage  
- **Normal**: 1.0x damage
- **Not Very Effective**: 0.5x - 0.8x damage
- **Immune/Absorbed**: 0.1x - 0.3x damage

### Key Counter Relationships

#### Hard Counters (3.0x)
- IceTower → FireElementalEnemy
- LaserTower → CrystallineEnemy  
- LightningTower → SpectralEnemy

#### Soft Counters (2.0-2.5x)
- AntiAirTower → FlyingEnemy (2.5x)
- FreezerTower → FastEnemy (2.5x)
- MissileTower → VoidEnemy (2.5x)
- PoisonTower → RegeneratingEnemy (2.5x)
- SniperTower → AdaptiveEnemy (2.0x)

#### Resistances (0.3-0.5x)
- LightningTower → GroundedEnemy (0.3x)
- LaserTower → EnergyShieldEnemy (0.5x)
- MissileTower → BlastProofEnemy (0.5x)
- ExplosiveTower → BlastProofEnemy (0.3x)

---

## Strategic Recommendations

### Early Game (Waves 1-10)
- **Core**: BasicTower spam for cost efficiency
- **Support**: 1-2 FreezerTowers for crowd control
- **Specialist**: SniperTower for FastEnemy waves

### Mid Game (Waves 11-25)
- **Add**: DetectorTower (mandatory for InvisibleEnemy)
- **Upgrade**: AntiAirTower for FlyingEnemy
- **Status**: PoisonTower for sustained damage

### Late Game (Waves 26-50)
- **AOE**: MissileTower/ExplosiveTower for groups
- **Specialists**: LaserTower for armored enemies
- **Control**: Multiple FreezerTower for TeleportingEnemy

### End Game (Waves 51+)
- **VoidEnemy**: ONLY MissileTower/ExplosiveTower work
- **AdaptiveEnemy**: ONLY SniperTower/IceTower work consistently
- **Mixed**: Diversified tower types for varied threats

### Universal Tips
1. **DetectorTower is mandatory** - invisible enemies cannot be damaged without it
2. **Terrain matters** - water boosts freeze, forest trades range for damage
3. **Counter knowledge is critical** - some enemies are nearly immune to wrong tower types
4. **Currency management** - damage dealing generates upgrade resources
5. **Positioning** - maximize range coverage and choke point utilization 