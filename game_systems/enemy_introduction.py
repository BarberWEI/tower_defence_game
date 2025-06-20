import pygame
from typing import Dict, Set, Optional

class EnemyIntroduction:
    """System for introducing new enemy types to players"""
    
    def __init__(self):
        # Track which enemies have been introduced
        self.introduced_enemies: Set[str] = set()
        
        # Current introduction being displayed
        self.current_introduction: Optional[Dict] = None
        self.introduction_timer = 0
        self.introduction_duration = 300  # 5 seconds at 60 FPS
        
        # Enemy information database
        self.enemy_info = {
            # Basic Tier (Waves 1-10)
            'BasicEnemy': {
                'name': 'Basic Enemy',
                'description': 'Standard enemy with no special abilities. Foundation of all enemy forces.',
                'counters': 'Any tower works well. BasicTower with poison support is cost-effective.',
                'color': (255, 100, 100),  # Light red
                'icon': 'BASIC'
            },
            'FastEnemy': {
                'name': 'Fast Enemy',
                'description': 'Double-speed enemy that moves at 2x normal rate. Hard to target with slow towers.',
                'counters': 'Use FreezerTower (2.5x damage), IceTower (2.0x), or SniperTower (2.0x) for effective hits.',
                'color': (255, 165, 0),  # Orange
                'icon': 'FAST'
            },
            'TankEnemy': {
                'name': 'Tank Enemy',
                'description': 'Heavily armored slow enemy with 5x normal health. Extremely durable.',
                'counters': 'Use CannonTower (1.8x damage) or focus fire with multiple towers.',
                'color': (128, 128, 128),  # Gray
                'icon': 'TANK'
            },
            
            # Intermediate Tier (Waves 11-25)
            'FlyingEnemy': {
                'name': 'Flying Enemy',
                'description': 'Airborne enemy that CANNOT be targeted by ground-only towers!',
                'counters': 'REQUIRES AntiAirTower (2.5x damage), MissileTower (2.0x), or IceTower (1.5x).',
                'color': (173, 216, 230),  # Light blue
                'icon': 'FLY'
            },
            'ShieldedEnemy': {
                'name': 'Shielded Enemy',
                'description': 'Energy shield provides damage reduction against energy-based attacks.',
                'counters': 'Use CannonTower (1.5x damage) for kinetic damage that bypasses shields.',
                'color': (100, 149, 237),  # Cornflower blue
                'icon': 'SHLD'
            },
            'InvisibleEnemy': {
                'name': 'Invisible Enemy',
                'description': 'CRITICAL: Cannot be targeted by ANY tower without DetectorTower!',
                'counters': 'MANDATORY DetectorTower first, then AntiAirTower (1.8x) or SniperTower (1.8x).',
                'color': (169, 169, 169),  # Dark gray (faded)
                'icon': 'INVIS'
            },
            'ArmoredEnemy': {
                'name': 'Armored Enemy',
                'description': 'Heavy physical armor provides high resistance to basic attacks.',
                'counters': 'Use CannonTower (2.0x), LaserTower (1.8x), or FlameTower (1.5x) for armor penetration.',
                'color': (255, 215, 0),  # Gold
                'icon': 'ARM'
            },
            
            # Advanced Tier (Waves 26-40)
            'RegeneratingEnemy': {
                'name': 'Regenerating Enemy',
                'description': 'Continuously heals over time. Must overwhelm regeneration rate.',
                'counters': 'Use PoisonTower (2.5x damage) to stop healing or burst damage with SplashTower (1.5x).',
                'color': (0, 255, 127),  # Spring green
                'icon': 'REGEN'
            },
            'TeleportingEnemy': {
                'name': 'Teleporting Enemy',
                'description': 'Teleports forward when hit (50% chance)! Jumps 1/3 of remaining path distance.',
                'counters': 'Use area damage: ExplosiveTower (1.5x), SplashTower (1.8x), or FreezerTower (1.8x).',
                'color': (138, 43, 226),  # Blue violet
                'icon': 'TELE'
            },
            'SplittingEnemy': {
                'name': 'Splitting Enemy',
                'description': 'Splits into 2 random enemies when destroyed! Spawned enemies have 75% health.',
                'counters': 'Use AOE damage: MissileTower (1.8x), ExplosiveTower (2.0x), or SplashTower (2.2x).',
                'color': (255, 20, 147),  # Deep pink
                'icon': 'SPLIT'
            },
            
            # Elite Tier (Waves 41-60)
            'EnergyShieldEnemy': {
                'name': 'Energy Shield Enemy',
                'description': 'Energy shield absorbs laser attacks but vulnerable to lightning!',
                'counters': 'Use LightningTower (2.0x damage) or kinetic weapons. AVOID LaserTower (0.5x damage).',
                'color': (0, 255, 255),  # Cyan
                'icon': 'ESHLD'
            },
            'GroundedEnemy': {
                'name': 'Grounded Enemy',
                'description': 'Electrical grounding provides immunity to lightning attacks!',
                'counters': 'Use any non-electric towers. AVOID LightningTower (0.3x damage only).',
                'color': (139, 69, 19),  # Saddle brown
                'icon': 'GND'
            },
            'FireElementalEnemy': {
                'name': 'Fire Elemental',
                'description': 'HEALS 50% of fire damage received! FlameTowers make it stronger!',
                'counters': 'Use IceTower (3.0x damage) or FreezerTower (2.0x). NEVER use FlameTower!',
                'color': (255, 69, 0),  # Red-orange
                'icon': 'FIRE'
            },
            'PhaseShiftEnemy': {
                'name': 'Phase Shifter',
                'description': 'Phases through dimensions, avoiding many physical attacks.',
                'counters': 'Use FlameTower (1.8x damage) to disrupt phasing mechanism.',
                'color': (128, 0, 128),  # Purple
                'icon': 'PHASE'
            },
            'BlastProofEnemy': {
                'name': 'Blast-Proof Enemy',
                'description': 'Reinforced armor highly resistant to ALL explosive damage!',
                'counters': 'Use LaserTower (2.0x damage). AVOID Missile/Explosive Towers (0.3-0.5x damage).',
                'color': (192, 192, 192),  # Silver
                'icon': 'BLAST'
            },
            
            # Legendary Tier (Waves 61+)
            'SpectralEnemy': {
                'name': 'Spectral Enemy',
                'description': 'Partially invisible, phases through physical attacks! Requires detection.',
                'counters': 'CRITICAL: DetectorTower required, then ONLY LightningTower (3.0x damage) works!',
                'color': (230, 230, 250),  # Lavender
                'icon': 'GHOST'
            },
            'CrystallineEnemy': {
                'name': 'Crystalline Enemy',
                'description': 'Living crystal structure reflects most attacks except focused light beams!',
                'counters': 'ONLY LaserTower (3.0x damage) can shatter crystal - all others ineffective!',
                'color': (224, 255, 255),  # Light cyan
                'icon': 'CRYST'
            },
            'ToxicEnemy': {
                'name': 'Toxic Enemy',
                'description': 'Poisonous creature completely immune to poison damage! Toxic aura damages nearby towers.',
                'counters': 'AVOID poison towers completely. Use basic, laser, or lightning towers instead.',
                'color': (76, 175, 80),  # Toxic green
                'icon': 'TOX'
            },
            'ToxicMutantEnemy': {
                'name': 'Toxic Mutant',
                'description': 'Evolved toxic creature immune to poison and most physical attacks! Only flame damage works.',
                'counters': 'ONLY FlameTower (2.0x damage) works - immune to poison and all other tower types!',
                'color': (127, 255, 0),  # Chartreuse
                'icon': 'TOXIC'
            },
            'VoidEnemy': {
                'name': 'Void Enemy',
                'description': 'CRITICAL: Absorbs ALL attack types except explosives! Most towers are useless!',
                'counters': 'ONLY MissileTower (2.5x) and ExplosiveTower (2.5x) work - everything else feeds it!',
                'color': (25, 25, 112),  # Midnight blue
                'icon': 'VOID'
            },
            'AdaptiveEnemy': {
                'name': 'Adaptive Enemy',
                'description': 'Changes immunities every 3 seconds through 5 adaptation cycles!',
                'counters': 'ONLY SniperTower (2.0x) and IceTower (2.0x) ALWAYS work regardless of adaptation!',
                'color': (255, 105, 180),  # Hot pink
                'icon': 'ADAPT'
            },
            
            # Ultimate Bosses
            'TimeLordBoss': {
                'name': 'TimeLord Boss',
                'description': 'Master of time manipulation! Slows projectiles, rewinds damage, creates temporal rifts.',
                'counters': 'Focus fire during vulnerability windows - spread towers to minimize time effects.',
                'color': (100, 149, 237),  # Cornflower blue
                'icon': 'TIME',
                'immunities': ['Periodic invincibility phases'],
                'special_abilities': ['Time slow field', 'Damage rewind', 'Temporal rifts', 'Chronos shield'],
                'threat_level': 'ULTIMATE'
            },
            'NecromancerBoss': {
                'name': 'Necromancer Boss',
                'description': 'Dark sorcerer of death! Life drain, undead summoning, death auras.',
                'counters': 'Eliminate minions quickly, use non-poison damage, maintain distance from auras.',
                'color': (148, 0, 211),  # Dark violet
                'icon': 'NECRO',
                'immunities': ['Poison damage (complete immunity)'],
                'special_abilities': ['Life drain aura', 'Undead summoning', 'Death aura', 'Soul shield'],
                'threat_level': 'ULTIMATE'
            },
            'ShadowKing': {
                'name': 'Shadow King',
                'description': 'Ruler of shadows! 70% dodge chance, shadow duplicates, darkness manipulation.',
                'counters': 'High rate of fire to overcome dodge - area effects for duplicates.',
                'color': (72, 61, 139),  # Dark slate blue
                'icon': 'KING',
                'immunities': ['70% dodge chance when phased'],
                'special_abilities': ['Dimension phasing', 'Shadow duplicates', 'Void step teleport'],
                'threat_level': 'ULTIMATE'
            },
            'CrystalOverlord': {
                'name': 'Crystal Overlord',
                'description': 'Crystalline titan! 40% projectile reflection, crystal barriers, immune to lasers.',
                'counters': 'Use non-laser high-damage weapons - beware of reflected projectiles!',
                'color': (0, 206, 209),  # Dark turquoise
                'icon': 'CRYST',
                'immunities': ['Laser damage (complete immunity)'],
                'special_abilities': ['40% projectile reflection', 'Crystal barriers', 'Shard rain attacks'],
                'threat_level': 'ULTIMATE'
            },
            
            # Legacy bosses (for compatibility)
            'MegaBoss': {
                'name': 'Mega Boss',
                'description': 'Massive boss with multiple phases and damage reduction. Spawns minions periodically.',
                'counters': 'Focus all available firepower - prepare for extended engagement.',
                'color': (255, 0, 0),  # Red
                'icon': 'MEGA',
                'immunities': ['50% damage reduction'],
                'special_abilities': ['Multi-phase system', 'Minion spawning', 'Damage reduction'],
                'threat_level': 'HIGH'
            },
            'SpeedBoss': {
                'name': 'Speed Boss',
                'description': 'Becomes faster as it takes damage. Lightning-fast dashes at low health.',
                'counters': 'High burst damage to eliminate quickly before speed becomes overwhelming.',
                'color': (255, 255, 0),  # Yellow
                'icon': 'SPEED',
                'immunities': ['None'],
                'special_abilities': ['Speed increases with damage', 'Dash ability', 'Speed trails'],
                'threat_level': 'HIGH'
            }
        }
    
    def check_new_enemy(self, enemy_type: str) -> bool:
        """Check if this enemy type needs to be introduced"""
        if enemy_type not in self.introduced_enemies and enemy_type in self.enemy_info:
            self.introduce_enemy(enemy_type)
            self.introduced_enemies.add(enemy_type)
            return True
        return False
    
    def introduce_enemy(self, enemy_type: str):
        """Start introducing a new enemy type"""
        if enemy_type in self.enemy_info:
            self.current_introduction = self.enemy_info[enemy_type].copy()
            self.current_introduction['enemy_type'] = enemy_type
            self.introduction_timer = 0
    
    def update(self):
        """Update introduction display timer"""
        if self.current_introduction:
            self.introduction_timer += 1
            if self.introduction_timer >= self.introduction_duration:
                self.current_introduction = None
                self.introduction_timer = 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the introduction overlay if active"""
        if not self.current_introduction:
            return
        
        screen_width, screen_height = screen.get_size()
        
        # Calculate fade alpha based on timer
        fade_in_time = 30
        fade_out_time = 60
        
        if self.introduction_timer < fade_in_time:
            alpha = int(255 * (self.introduction_timer / fade_in_time))
        elif self.introduction_timer > (self.introduction_duration - fade_out_time):
            remaining = self.introduction_duration - self.introduction_timer
            alpha = int(255 * (remaining / fade_out_time))
        else:
            alpha = 255
        
        # Draw semi-transparent background
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(128, alpha // 2)))
        screen.blit(overlay, (0, 0))
        
        # Introduction panel dimensions
        panel_width = 400
        panel_height = 150
        panel_x = (screen_width - panel_width) // 2
        panel_y = screen_height // 4
        
        # Draw panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_color = (40, 40, 40, min(240, alpha))
        pygame.draw.rect(panel_surface, panel_color, (0, 0, panel_width, panel_height))
        pygame.draw.rect(panel_surface, (255, 255, 255, min(255, alpha)), 
                        (0, 0, panel_width, panel_height), 3)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Enemy icon and accent color
        icon_color = (*self.current_introduction['color'], min(255, alpha))
        
        # Draw "NEW ENEMY!" header
        font_large = pygame.font.Font(None, 28)
        header_text = font_large.render("NEW ENEMY DETECTED!", True, (255, 255, 0))
        header_rect = header_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 25))
        screen.blit(header_text, header_rect)
        
        # Draw enemy name with icon
        font_medium = pygame.font.Font(None, 24)
        name_text = font_medium.render(self.current_introduction['name'], True, icon_color[:3])
        name_rect = name_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 50))
        screen.blit(name_text, name_rect)
        
        # Draw icon next to name
        icon_text = font_medium.render(f"[{self.current_introduction['icon']}]", True, icon_color[:3])
        icon_rect = icon_text.get_rect(left=name_rect.right + 10, centery=name_rect.centery)
        screen.blit(icon_text, icon_rect)
        
        # Draw description
        font_small = pygame.font.Font(None, 18)
        desc_lines = self.wrap_text(self.current_introduction['description'], font_small, panel_width - 20)
        
        y_offset = panel_y + 75
        for line in desc_lines:
            desc_text = font_small.render(line, True, (255, 255, 255))
            desc_rect = desc_text.get_rect(center=(panel_x + panel_width // 2, y_offset))
            screen.blit(desc_text, desc_rect)
            y_offset += 20
        
        # Draw counter strategy
        counter_text = font_small.render(f"Strategy: {self.current_introduction['counters']}", True, (0, 255, 0))
        counter_rect = counter_text.get_rect(center=(panel_x + panel_width // 2, panel_y + panel_height - 15))
        screen.blit(counter_text, counter_rect)
        
        # Draw progress bar
        progress = self.introduction_timer / self.introduction_duration
        bar_width = panel_width - 40
        bar_height = 4
        bar_x = panel_x + 20
        bar_y = panel_y + panel_height - 30
        
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list:
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def has_active_introduction(self) -> bool:
        """Check if an introduction is currently being displayed"""
        return self.current_introduction is not None
    
    def reset_introductions(self):
        """Reset all introductions (for new game)"""
        self.introduced_enemies.clear()
        self.current_introduction = None
        self.introduction_timer = 0 