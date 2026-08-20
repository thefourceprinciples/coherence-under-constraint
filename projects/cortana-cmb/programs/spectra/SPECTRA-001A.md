# SPECTRA-001A — Constraint-to-Spectrum Diagnostic Engine

Fourth-domain portability bench for the CORTANA-CMB inverse-problem architecture.

## System
- 4 masses
- 5 springs
- hidden structural state = fractional changes in five spring constants
- primary observable = four natural frequencies

## Results
Frequency-only sensitivity:
- rank = 3
- kernel dimension = 2
- condition number ≈ 2.806

Selected mode-shape sensitivity:
- rank = 5
- kernel dimension = 0
- condition number ≈ 1.66e11

Combined frequency + mode-shape sensitivity:
- rank = 5
- kernel dimension = 0
- condition number ≈ 2.174

A structural perturbation was constructed along a frequency-only null direction. Its linearized frequency response is essentially zero while its mode-shape response is nonzero, demonstrating a damage pattern that can hide from resonance-frequency measurements to first order but become visible through mode-shape sensing.

Best single additional mode-shape measurement found in the candidate set:
- DOF 3
- mode 4
- frequency-only rank 3 -> 4
- kernel dimension 2 -> 1
- condition number ≈ 2.0

## Classification
- frequency-only structural blind directions: PASS
- hidden-to-first-order damage pattern exposed by mode shape: PASS
- combined observables remove exact local kernel: PASS
- active observable/sensor design reduces diagnostic kernel: PASS
- same kernel/SVD architecture ports to a fourth domain: PASS
- new structural dynamics mathematics: FAIL / not claimed

## Key lesson
Constraint geometry is encoded in spectral response, but frequency data alone may not uniquely identify structural changes. Complementary mode-shape information can collapse the diagnostic kernel while improving practical conditioning relative to mode-shape-only inversion.
