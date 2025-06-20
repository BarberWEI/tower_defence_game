from .enemy import Enemy
from .basic_enemy import BasicEnemy
from .fast_enemy import FastEnemy
from .tank_enemy import TankEnemy
from .shielded_enemy import ShieldedEnemy
from .invisible_enemy import InvisibleEnemy
from .flying_enemy import FlyingEnemy
from .regenerating_enemy import RegeneratingEnemy
from .splitting_enemy import SplittingEnemy
from .teleporting_enemy import TeleportingEnemy
from .mega_boss import MegaBoss
from .speed_boss import SpeedBoss

# New powerful bosses
from .timelord_boss import TimeLordBoss
from .necromancer_boss import NecromancerBoss
from .shadow_king import ShadowKing
from .crystal_overlord import CrystalOverlord

# New tower-immune enemies
from .armored_enemy import ArmoredEnemy
from .energy_shield_enemy import EnergyShieldEnemy
from .grounded_enemy import GroundedEnemy
from .fire_elemental_enemy import FireElementalEnemy
from .toxic_enemy import ToxicEnemy
from .phase_shift_enemy import PhaseShiftEnemy
from .blast_proof_enemy import BlastProofEnemy

# New specialized enemies
from .spectral_enemy import SpectralEnemy
from .crystalline_enemy import CrystallineEnemy
from .toxic_mutant_enemy import ToxicMutantEnemy
from .void_enemy import VoidEnemy
from .adaptive_enemy import AdaptiveEnemy

__all__ = [
    'Enemy', 'BasicEnemy', 'FastEnemy', 'TankEnemy', 'ShieldedEnemy',
    'InvisibleEnemy', 'FlyingEnemy', 'RegeneratingEnemy', 'SplittingEnemy',
    'TeleportingEnemy', 'MegaBoss', 'SpeedBoss',
    'TimeLordBoss', 'NecromancerBoss', 'ShadowKing', 'CrystalOverlord',
    'ArmoredEnemy', 'EnergyShieldEnemy', 'GroundedEnemy', 'FireElementalEnemy',
    'ToxicEnemy', 'PhaseShiftEnemy', 'BlastProofEnemy',
    'SpectralEnemy', 'CrystallineEnemy', 'ToxicMutantEnemy', 'VoidEnemy', 'AdaptiveEnemy'
] 