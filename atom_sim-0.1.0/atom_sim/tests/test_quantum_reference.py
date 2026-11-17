"""Mandatory physics reference tests.

Every test records:
- Input
- Expected
- Actual
- Tolerance
- Pass/Fail
"""

from __future__ import annotations

import math
import pytest

from physics.quantum_engine import QuantumEngine, TransitionType
from physics.constants import ENERGY_TOL_EV, JOULE_TO_EV
from physics.atomic_model import hydrogen
from physics.electromagnetism import ElectromagnetismEngine, Vector3
from physics.constants import ELEMENTARY_CHARGE


# ---------------------------------------------------------------------------
# Hydrogen energy levels
# ---------------------------------------------------------------------------

def test_hydrogen_ground_state():
    """E₁ = -13.6 eV (textbook) / -13.605693... eV (CODATA Rydberg)."""
    engine = QuantumEngine(Z_eff=1.0)
    level = engine.energy_level(1)

    expected_textbook = -13.6
    expected_precise = -13.60569312299  # from Rydberg * hc
    actual = level.energy_eV
    tol = 0.01  # 0.01 eV covers both textbook rounding and precise value

    assert abs(actual - expected_precise) < 1e-6, (
        f"Input: n=1, Z=1\n"
        f"Expected (precise): {expected_precise} eV\n"
        f"Actual: {actual} eV\n"
        f"Tolerance: 1e-6 eV\n"
        f"FAIL"
    )
    # Also check textbook value within looser tol
    assert abs(actual - expected_textbook) < tol

    print(
        f"PASS | Hydrogen ground state\n"
        f"  Input: n=1, Z=1\n"
        f"  Expected (precise): {expected_precise:.10f} eV\n"
        f"  Actual:             {actual:.10f} eV\n"
        f"  Tolerance: 1e-6 eV"
    )


def test_hydrogen_n2():
    """E₂ = -3.4 eV."""
    engine = QuantumEngine(Z_eff=1.0)
    level = engine.energy_level(2)

    expected_textbook = -3.4
    expected_precise = -13.60569312299 / 4.0
    actual = level.energy_eV
    tol = 0.01

    assert abs(actual - expected_precise) < 1e-6
    assert abs(actual - expected_textbook) < tol

    print(
        f"PASS | Hydrogen n=2\n"
        f"  Input: n=2, Z=1\n"
        f"  Expected (precise): {expected_precise:.10f} eV\n"
        f"  Actual:             {actual:.10f} eV\n"
        f"  Tolerance: 1e-6 eV"
    )


def test_hydrogen_transition_2_to_1():
    """n=2 → n=1: photon energy 10.2 eV, wavelength ≈ 121.6 nm (textbook)."""
    engine = QuantumEngine(Z_eff=1.0)
    trans = engine.transition(2, 1)

    expected_E_textbook = 10.2
    expected_E_precise = 13.60569312299 * (1 - 1/4)  # 10.2042698...
    actual_E = trans.energy_eV

    # Wavelength from Rydberg (infinite mass): ~121.502 nm
    # Textbook often quotes 121.6 nm
    expected_lam_nm_precise = 121.50227341
    actual_lam = trans.wavelength_nm
    tol_E = 0.01
    tol_lam = 0.2  # nm – covers textbook vs precise difference

    assert abs(actual_E - expected_E_precise) < 1e-5
    assert abs(actual_E - expected_E_textbook) < tol_E
    assert abs(actual_lam - expected_lam_nm_precise) < 0.001
    assert abs(actual_lam - 121.6) < tol_lam
    assert trans.kind == TransitionType.EMISSION

    print(
        f"PASS | Hydrogen transition 2→1\n"
        f"  Input: n_i=2, n_f=1, Z=1\n"
        f"  Expected E (precise): {expected_E_precise:.8f} eV\n"
        f"  Actual E:             {actual_E:.8f} eV\n"
        f"  Expected λ (precise): {expected_lam_nm_precise:.6f} nm\n"
        f"  Actual λ:             {actual_lam:.6f} nm\n"
        f"  Textbook λ target:    121.6 nm (tol {tol_lam} nm)\n"
        f"  Kind: {trans.kind.name}"
    )


# ---------------------------------------------------------------------------
# Coulomb force reference
# ---------------------------------------------------------------------------

def test_coulomb_force_reference():
    """
    Two elementary charges separated by 1 Å.
    F = k e² / r²
    Independently: k ≈ 8.9875517923e9, e=1.602176634e-19, r=1e-10
    F ≈ 2.30707755e-8 N
    """
    q = ELEMENTARY_CHARGE
    r = 1.0e-10  # 1 Å
    expected = 2.307077552e-8  # N (pre-computed with CODATA)
    actual = ElectromagnetismEngine.coulomb_force_magnitude(q, q, r)
    tol = 1e-12  # absolute

    assert abs(actual - expected) < tol, (
        f"Input: q1=q2=e, r=1e-10 m\n"
        f"Expected: {expected} N\n"
        f"Actual:   {actual} N\n"
        f"Tolerance: {tol} N\n"
        f"FAIL"
    )

    # Vector form
    r_vec = Vector3(r, 0.0, 0.0)
    force = ElectromagnetismEngine.coulomb_force(q, q, r_vec)
    assert abs(force.norm() - expected) < tol
    assert abs(force.x - expected) < tol
    assert abs(force.y) < 1e-20
    assert abs(force.z) < 1e-20

    print(
        f"PASS | Coulomb force\n"
        f"  Input: q1=q2=e, r=1e-10 m\n"
        f"  Expected: {expected:.10e} N\n"
        f"  Actual:   {actual:.10e} N\n"
        f"  Tolerance: {tol} N"
    )


def test_invalid_inputs_rejected():
    """Validation: zero radius, negative n, etc. must raise."""
    engine = QuantumEngine()
    with pytest.raises(ValueError):
        engine.energy_level(0)
    with pytest.raises(ValueError):
        engine.energy_level(-1)
    with pytest.raises(ValueError):
        engine.transition(1, 1)

    with pytest.raises(ValueError):
        ElectromagnetismEngine.coulomb_force_magnitude(1.0, 1.0, 0.0)

    with pytest.raises(ValueError):
        hydrogen(isotope=0)

    print("PASS | Invalid input rejection")


def test_deterministic_reproducibility():
    """Same inputs must produce identical outputs (no RNG in core)."""
    e1 = QuantumEngine(Z_eff=1.0)
    e2 = QuantumEngine(Z_eff=1.0)
    t1 = e1.transition(3, 2)
    t2 = e2.transition(3, 2)
    assert t1.energy_eV == t2.energy_eV
    assert t1.wavelength_nm == t2.wavelength_nm
    print("PASS | Deterministic reproducibility")
