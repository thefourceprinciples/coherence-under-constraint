# GARDENCORE-004 — Noise-Aware Design

Goal: repair the failure found in GARDENCORE-003 by replacing rank/kernel-only measurement selection with covariance-aware Fisher design.

## System
Same 10-DOF / 11-spring noisy structural inverse problem as GARDENCORE-003.

## Designs compared
- baseline fixed 16 mode-shape measurements
- A-optimal design: greedily minimize posterior covariance trace
- D-optimal design: greedily maximize Fisher log-determinant

Monte Carlo trials: 200.

## Mean best reconstruction error
- baseline = 0.04565
- A-optimal = 0.04245
- D-optimal = 0.04275

Improvement vs baseline:
- A-optimal ≈ 7.00%
- D-optimal ≈ 6.36%

## Information metrics
All designs remain full-rank. A-optimal reduces posterior covariance trace from about 0.02474 to 0.00264; D-optimal yields about 0.00321 and the highest Fisher log-determinant.

## Verdict
- noise-aware design improves expected reconstruction quality: PASS
- kernel collapse alone is insufficient: CONFIRMED
- Fisher/covariance-aware selection adds practical value beyond rank-only selection: PASS
- GardenCore should treat uncertainty-aware design as a core feature: YES

## Key lesson
Observability is necessary but not sufficient. Practical experimental design should optimize expected information or posterior uncertainty under the measurement-noise model, not merely maximize rank or minimize kernel dimension.
