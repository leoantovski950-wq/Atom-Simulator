# atom-sim 0.1.0

Modular atomic physics core for hydrogenic systems.

## Status (2026-11-17)

| Component              | Status      | Notes                                      |
|------------------------|-------------|--------------------------------------------|
| PhysicsCore / constants| IMPLEMENTED | CODATA via scipy                           |
| AtomicModel            | IMPLEMENTED | Z, A, charge, shell occupancy              |
| QuantumEngine          | IMPLEMENTED | Hydrogenic E_n, transitions, λ             |
| ElectromagnetismEngine | IMPLEMENTED | Coulomb, E-field, potential energy         |
| ValidationEngine       | IMPLEMENTED | Domain checks, finite checks               |
| LoggingSystem          | IMPLEMENTED | Structured logger                          |
| SimulationController   | INCOMPLETE  | Not started                                |
| RenderingEngine        | INCOMPLETE  | Explicitly out of current scope            |
| UIController           | INCOMPLETE  | Explicitly out of current scope            |
| Full interactive viz   | INCOMPLETE  | Deferred                                   |

Mandatory physics reference tests: **6/6 PASSED** (executed 2026-11-17).

## Quick start

```bash
cd atom_sim
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/ -v
```

## Example

```python
from physics import QuantumEngine, hydrogen

engine = QuantumEngine(Z_eff=1.0)
print(engine.energy_level(1).energy_eV)          # ≈ -13.6057 eV
t = engine.transition(2, 1)
print(t.energy_eV, t.wavelength_nm)              # ≈ 10.204 eV, 121.502 nm
```

## Physics notes

- Energies use the infinite-nuclear-mass Rydberg constant.
- Textbook values (−13.6 eV, 121.6 nm) are recovered within stated tolerances.
- Reduced-mass and fine-structure corrections are **not** included.
- Multi-electron atoms receive only classical shell filling; no Hartree–Fock or CI.
- Bohr radii are supplied for comparison only; they are never treated as electron trajectories.

## Architecture

See `docs/architecture.md`.

## License

MIT (or as declared by the containing project).
