"""Physical constants used by the atom simulator.

Values taken from scipy.constants (CODATA 2018 / 2022 recommended).
All internal calculations use SI units.
"""

from __future__ import annotations

from dataclasses import dataclass
from scipy import constants as _C

# CODATA values (scipy 1.17)
ELECTRON_MASS = _C.m_e          # kg
PROTON_MASS = _C.m_p            # kg
NEUTRON_MASS = _C.m_n           # kg
ELEMENTARY_CHARGE = _C.e        # C
PLANCK = _C.h                   # J s
HBAR = _C.hbar                  # J s
SPEED_OF_LIGHT = _C.c           # m/s
VACUUM_PERMITTIVITY = _C.epsilon_0  # F/m
RYDBERG = _C.Rydberg            # 1/m  (infinite nuclear mass)
BOLTZMANN = _C.k                # J/K
AVOGADRO = _C.N_A

# Derived / conventional
EV_TO_JOULE = ELEMENTARY_CHARGE
JOULE_TO_EV = 1.0 / ELEMENTARY_CHARGE
ANGSTROM = 1e-10                # m
NM = 1e-9                       # m

# Common reference value used in many textbooks (rounded)
HYDROGEN_GROUND_STATE_EV = -13.6

# Numerical policy
DEFAULT_RTOL = 1e-9
DEFAULT_ATOL = 1e-12
ENERGY_TOL_EV = 1e-4            # tolerance for eV comparisons in tests


@dataclass(frozen=True)
class Unit:
    """Simple unit label for telemetry / display conversion."""
    name: str
    si_factor: float  # multiply SI value by this to get display unit


class Units:
    eV = Unit("eV", JOULE_TO_EV)
    nm = Unit("nm", 1.0 / NM)
    angstrom = Unit("Å", 1.0 / ANGSTROM)
    kg = Unit("kg", 1.0)
    C = Unit("C", 1.0)
    J = Unit("J", 1.0)
    m = Unit("m", 1.0)
