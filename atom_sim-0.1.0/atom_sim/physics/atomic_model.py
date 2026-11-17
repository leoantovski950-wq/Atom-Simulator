"""Atomic structure model: protons, neutrons, electrons, isotopes, ions.

Classical particle counts only. Quantum state lives in QuantumEngine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import math

from .constants import (
    ELECTRON_MASS,
    PROTON_MASS,
    NEUTRON_MASS,
    ELEMENTARY_CHARGE,
    DEFAULT_ATOL,
)


class ParticleType(Enum):
    PROTON = auto()
    NEUTRON = auto()
    ELECTRON = auto()


@dataclass(frozen=True)
class Nucleon:
    type: ParticleType
    # Future: position, spin, etc. Currently count-only.


@dataclass
class ElectronShell:
    """Shell occupancy (n, max electrons = 2n²)."""
    n: int
    electrons: int = 0

    @property
    def capacity(self) -> int:
        return 2 * self.n * self.n

    def can_add(self, count: int = 1) -> bool:
        return self.electrons + count <= self.capacity

    def add(self, count: int = 1) -> None:
        if not self.can_add(count):
            raise ValueError(
                f"Shell n={self.n} capacity {self.capacity}, "
                f"current {self.electrons}, cannot add {count}"
            )
        self.electrons += count


@dataclass
class AtomicSpecies:
    """
    Represents an atom, ion or isotope by Z, A and charge state.
    Electron configuration is optional and classical (Aufbau approximation).
    """
    Z: int                          # atomic number (protons)
    A: int                          # mass number (protons + neutrons)
    charge: int = 0                 # net charge in units of e (positive = cation)
    symbol: str = ""
    name: str = ""
    shells: List[ElectronShell] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.Z < 1:
            raise ValueError(f"Z must be >= 1, got {self.Z}")
        if self.A < self.Z:
            raise ValueError(f"A={self.A} < Z={self.Z}")
        if abs(self.charge) > self.Z + 5:  # soft limit
            raise ValueError(f"Unphysical charge {self.charge} for Z={self.Z}")
        n_electrons = self.Z - self.charge
        if n_electrons < 0:
            raise ValueError(
                f"Negative electron count: Z={self.Z}, charge={self.charge}"
            )
        if not self.shells and n_electrons > 0:
            self._build_ground_config(n_electrons)

    @property
    def N(self) -> int:
        """Neutron number."""
        return self.A - self.Z

    @property
    def electron_count(self) -> int:
        return self.Z - self.charge

    @property
    def is_ion(self) -> bool:
        return self.charge != 0

    @property
    def is_isotope(self) -> bool:
        # Relative to most common; we do not hard-code abundances here.
        return True  # every A is an isotope of Z

    def mass_kg(self, include_electrons: bool = True) -> float:
        """Approximate rest mass in kg (no binding energy correction)."""
        m = self.Z * PROTON_MASS + self.N * NEUTRON_MASS
        if include_electrons:
            m += self.electron_count * ELECTRON_MASS
        return m

    def mass_u(self, include_electrons: bool = True) -> float:
        """Approximate mass in unified atomic mass units."""
        # 1 u ≈ 1.66053906660e-27 kg
        u = 1.66053906660e-27
        return self.mass_kg(include_electrons) / u

    def _build_ground_config(self, n_electrons: int) -> None:
        """Simple Aufbau filling by shell (not subshell). Sufficient for visualization."""
        remaining = n_electrons
        n = 1
        while remaining > 0:
            shell = ElectronShell(n=n)
            take = min(remaining, shell.capacity)
            shell.electrons = take
            self.shells.append(shell)
            remaining -= take
            n += 1
            if n > 20:
                raise RuntimeError("Electron configuration overflow")

    def configuration_string(self) -> str:
        parts = []
        for s in self.shells:
            if s.electrons > 0:
                parts.append(f"{s.n}s/p/d...:{s.electrons}")
        return " ".join(parts) if parts else "bare nucleus"

    def validate(self) -> None:
        """Raise on inconsistent internal state."""
        if self.Z < 1 or self.A < self.Z:
            raise ValueError("Invalid Z/A")
        total_e = sum(s.electrons for s in self.shells)
        expected = self.electron_count
        if total_e != expected:
            raise ValueError(
                f"Shell occupancy {total_e} != expected electrons {expected}"
            )


def hydrogen(isotope: int = 1, charge: int = 0) -> AtomicSpecies:
    """Factory for hydrogen and its isotopes / ions."""
    if isotope < 1:
        raise ValueError("isotope mass number must be >= 1")
    names = {1: ("H", "Hydrogen"), 2: ("D", "Deuterium"), 3: ("T", "Tritium")}
    sym, name = names.get(isotope, (f"H{isotope}", f"Hydrogen-{isotope}"))
    return AtomicSpecies(Z=1, A=isotope, charge=charge, symbol=sym, name=name)


def helium(isotope: int = 4, charge: int = 0) -> AtomicSpecies:
    return AtomicSpecies(Z=2, A=isotope, charge=charge, symbol="He", name="Helium")
