# GARDENCORE-002 — Baseline Challenge

Goal: compare GardenCore against direct domain-specific SVD/observability analysis and identify whether the unified wrapper adds any measurable value beyond established mathematics.

## Numerical result
GardenCore exactly matches direct baseline SVD calculations for rank, kernel dimension, and nonzero condition number across:
- CMB
- QCORE bare channel
- QCORE repetition-code channel
- LATENT tomography
- SPECTRA structural-frequency sensitivity

## Performance
No meaningful runtime advantage was demonstrated on the toy benches. GardenCore is not a faster SVD engine.

## Added value
GardenCore provides:
- one consistent report schema across domains
- explicit kernel reporting
- thresholded recoverability hooks
- channel stacking
- standardized normalization
- candidate measurement scoring
- active next-measurement recommendation

## LATENT example
Under the common normalized scorer, the preferred next 4-cell probe is `(1,4,5,8)`, yielding rank 5 and kernel dimension 3 from Probe A alone.

## Verdict
- better mathematics than direct SVD: FAIL
- faster computation: FAIL / no demonstrated advantage
- cleaner cross-domain diagnostics: PASS
- more actionable experimental-design workflow than bare ad hoc SVD alone: PASS
- evidence for reusable engineering abstraction: PASS
- superior domain-specific solver: NOT ESTABLISHED

The current value proposition is architectural consistency and actionability, not novel mathematics or computational speed.
