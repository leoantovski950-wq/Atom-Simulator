# Architecture

## Module boundaries

```
physics/
  constants.py          # CODATA, unit helpers, tolerance policy
  atomic_model.py       # Z, A, charge, shells (classical counts)
  quantum_engine.py     # E_n, transitions, wavelengths (hydrogenic)
  electromagnetism.py   # Coulomb, E, U (classical point charges)
  validation.py         # Input domain guards
  logging_system.py     # Logger factory
```

Ownership:
- QuantumEngine owns energy eigenvalues and photon quantities.
- AtomicModel owns particle counts and configuration strings.
- ElectromagnetismEngine owns classical force / field calculations.
- No module imports a future RenderingEngine or UIController.

## Error model

- Domain violations → `ValueError` or `ValidationError`.
- No silent NaN propagation; finite checks on critical paths.
- Deterministic: pure functions of inputs; no hidden RNG.

## Extension points

- SimulationController can hold an AtomicSpecies + QuantumEngine and step transitions.
- RenderingEngine should consume EnergyLevel / Transition / AtomicSpecies objects only.
- DataRepository can version species definitions and measured spectra later.

## Numerical policy

- Internal SI.
- Display conversion explicit (JOULE_TO_EV, / NM, …).
- Default rtol 1e-9, atol 1e-12; energy comparisons in tests use 1e-4 … 1e-6 eV as appropriate.
