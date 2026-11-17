"""Classical electromagnetism utilities used by the atomic model.

Coulomb force, potential energy, electric field of a point charge.
All calculations in SI. No quantum corrections.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import math

from .constants import (
    ELEMENTARY_CHARGE,
    VACUUM_PERMITTIVITY,
    DEFAULT_ATOL,
    DEFAULT_RTOL,
)


@dataclass(frozen=True)
class Vector3:
    x: float
    y: float
    z: float

    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def unit(self) -> "Vector3":
        n = self.norm()
        if n < DEFAULT_ATOL:
            raise ValueError("Cannot normalize zero vector")
        return Vector3(self.x / n, self.y / n, self.z / n)

    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, s: float) -> "Vector3":
        return Vector3(self.x * s, self.y * s, self.z * s)


class ElectromagnetismEngine:
    """Static point-charge electrostatics."""

    k = 1.0 / (4.0 * math.pi * VACUUM_PERMITTIVITY)  # N m² C⁻²

    @staticmethod
    def coulomb_force(
        q1: float,
        q2: float,
        r_vec: Vector3,
    ) -> Vector3:
        """
        Force on charge 2 due to charge 1.
        F = k * q1 * q2 / r² * r_hat
        """
        r = r_vec.norm()
        if r < DEFAULT_ATOL:
            raise ValueError("Coulomb force undefined at r = 0")
        magnitude = ElectromagnetismEngine.k * q1 * q2 / (r * r)
        return r_vec.unit().scale(magnitude)

    @staticmethod
    def coulomb_force_magnitude(q1: float, q2: float, r: float) -> float:
        if r < DEFAULT_ATOL:
            raise ValueError("r must be > 0")
        return abs(ElectromagnetismEngine.k * q1 * q2 / (r * r))

    @staticmethod
    def electrostatic_potential_energy(q1: float, q2: float, r: float) -> float:
        """U = k * q1 * q2 / r  (zero at infinity)."""
        if r < DEFAULT_ATOL:
            raise ValueError("r must be > 0")
        return ElectromagnetismEngine.k * q1 * q2 / r

    @staticmethod
    def electric_field(q: float, r_vec: Vector3) -> Vector3:
        """E field at position relative to point charge q."""
        r = r_vec.norm()
        if r < DEFAULT_ATOL:
            raise ValueError("Electric field undefined at charge location")
        magnitude = ElectromagnetismEngine.k * q / (r * r)
        return r_vec.unit().scale(magnitude)

    @staticmethod
    def bohr_radius_classical(Z: float = 1.0, n: int = 1) -> float:
        """
        Classical Bohr radius a0 * n² / Z.
        Provided only for comparison with quantum expectation values.
        Not used as an electron trajectory.
        """
        # a0 = 4πε0 ħ² / (m_e e²) ≈ 5.29177210903e-11 m
        a0 = 5.29177210903e-11
        return a0 * (n * n) / Z
