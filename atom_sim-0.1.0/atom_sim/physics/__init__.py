"""PhysicsCore package for the atom simulator.

Modules:
- atomic_model: classical particle counts, isotopes, ions
- quantum_engine: hydrogenic energy levels and transitions
- electromagnetism: Coulomb, fields, potential energy
- validation: input guards and numerical checks
- constants: CODATA values and unit helpers
- logging_system: structured logging
"""

from .atomic_model import AtomicSpecies, ElectronShell, hydrogen, helium, ParticleType
from .quantum_engine import QuantumEngine, EnergyLevel, Transition, TransitionType
from .electromagnetism import ElectromagnetismEngine, Vector3
from .validation import ValidationError, require_positive, assert_close
from .constants import (
    RYDBERG,
    ELEMENTARY_CHARGE,
    JOULE_TO_EV,
    ENERGY_TOL_EV,
)
from .logging_system import configure_logging, get_logger

__all__ = [
    "AtomicSpecies",
    "ElectronShell",
    "hydrogen",
    "helium",
    "ParticleType",
    "QuantumEngine",
    "EnergyLevel",
    "Transition",
    "TransitionType",
    "ElectromagnetismEngine",
    "Vector3",
    "ValidationError",
    "require_positive",
    "assert_close",
    "RYDBERG",
    "ELEMENTARY_CHARGE",
    "JOULE_TO_EV",
    "ENERGY_TOL_EV",
    "configure_logging",
    "get_logger",
]

__version__ = "0.1.0"
