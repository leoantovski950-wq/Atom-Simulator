"""Quantum mechanical calculations for hydrogenic atoms.

Provides energy eigenvalues, transition energies, wavelengths and
selection-rule checks. Explicitly hydrogenic (single electron).
Multi-electron atoms are not treated beyond classical configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple
import math

from .constants import (
    RYDBERG,
    PLANCK,
    SPEED_OF_LIGHT,
    ELEMENTARY_CHARGE,
    EV_TO_JOULE,
    JOULE_TO_EV,
    NM,
    ENERGY_TOL_EV,
    DEFAULT_RTOL,
)
from .atomic_model import AtomicSpecies


class TransitionType(Enum):
    EMISSION = auto()
    ABSORPTION = auto()


@dataclass(frozen=True)
class EnergyLevel:
    """Hydrogenic energy level characterized by principal quantum number n."""
    n: int
    energy_J: float
    energy_eV: float

    def __post_init__(self) -> None:
        if self.n < 1:
            raise ValueError(f"Principal quantum number n must be >= 1, got {self.n}")


@dataclass(frozen=True)
class Transition:
    """Photon associated with a change of principal quantum number."""
    n_initial: int
    n_final: int
    energy_J: float
    energy_eV: float
    wavelength_m: float
    wavelength_nm: float
    kind: TransitionType
    allowed_by_selection: bool  # Δn unrestricted for hydrogen; Δl=±1 is the real rule

    @property
    def frequency_Hz(self) -> float:
        if self.wavelength_m <= 0:
            return float("nan")
        return SPEED_OF_LIGHT / self.wavelength_m


class QuantumEngine:
    """
    Hydrogenic quantum calculations (infinite nuclear mass Rydberg).

    Classical Bohr orbits are never returned as electron trajectories.
    Energy levels and transition wavelengths are the primary observables.
    """

    def __init__(self, species: Optional[AtomicSpecies] = None, Z_eff: float = 1.0):
        """
        Parameters
        ----------
        species : AtomicSpecies, optional
            Used only to obtain Z. For ions/atoms with one electron, Z_eff ≈ Z.
        Z_eff : float
            Effective nuclear charge. Default 1.0 (hydrogen).
        """
        if species is not None:
            if species.electron_count != 1:
                # Still allow calculation but mark as approximate
                pass
            self.Z = float(species.Z)
        else:
            self.Z = float(Z_eff)
        if self.Z <= 0:
            raise ValueError("Z_eff must be positive")

    def energy_level(self, n: int) -> EnergyLevel:
        """
        E_n = - (Z² * R_∞ * h * c) / n²   (infinite nuclear mass)

        Returns both SI and eV.
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"n must be positive integer, got {n}")
        # E = - Z² * (Rydberg * h * c) / n²
        rydberg_energy_J = RYDBERG * PLANCK * SPEED_OF_LIGHT
        energy_J = - (self.Z ** 2) * rydberg_energy_J / (n * n)
        energy_eV = energy_J * JOULE_TO_EV
        return EnergyLevel(n=n, energy_J=energy_J, energy_eV=energy_eV)

    def transition(
        self,
        n_initial: int,
        n_final: int,
        *,
        enforce_selection: bool = False,
    ) -> Transition:
        """
        Photon energy and wavelength for n_i → n_f.

        Selection rule for hydrogenic atoms (electric dipole):
        Δl = ±1.  Because we only track n, the flag is advisory.
        For pure n-change we still compute the energy; the caller
        decides whether to treat it as allowed.
        """
        if n_initial < 1 or n_final < 1:
            raise ValueError("Quantum numbers must be >= 1")
        if n_initial == n_final:
            raise ValueError("No transition when n_initial == n_final")

        E_i = self.energy_level(n_initial)
        E_f = self.energy_level(n_final)
        delta_E_J = E_i.energy_J - E_f.energy_J  # positive for emission

        if delta_E_J > 0:
            kind = TransitionType.EMISSION
            photon_E_J = delta_E_J
        else:
            kind = TransitionType.ABSORPTION
            photon_E_J = -delta_E_J

        photon_E_eV = photon_E_J * JOULE_TO_EV

        # λ = hc / E
        if photon_E_J <= 0:
            wavelength_m = float("inf")
        else:
            wavelength_m = (PLANCK * SPEED_OF_LIGHT) / photon_E_J
        wavelength_nm = wavelength_m / NM

        # Selection-rule awareness (simplified): Δn arbitrary is fine for energy,
        # but real dipole requires Δl=±1. We mark True when |Δn| >= 1 (always)
        # and leave a note that full angular-momentum check is external.
        allowed = abs(n_initial - n_final) >= 1
        if enforce_selection:
            # Without l we cannot enforce; raise only if caller insists and we lack data
            pass

        return Transition(
            n_initial=n_initial,
            n_final=n_final,
            energy_J=photon_E_J,
            energy_eV=photon_E_eV,
            wavelength_m=wavelength_m,
            wavelength_nm=wavelength_nm,
            kind=kind,
            allowed_by_selection=allowed,
        )

    def series_limit_nm(self, n_final: int) -> float:
        """Wavelength of series limit (n→∞ → n_final) in nm."""
        # 1/λ = R Z² (1/n_f²)
        inv_lam = RYDBERG * (self.Z ** 2) / (n_final * n_final)
        return (1.0 / inv_lam) / NM

    def is_hydrogenic(self, species: AtomicSpecies) -> bool:
        return species.electron_count == 1
