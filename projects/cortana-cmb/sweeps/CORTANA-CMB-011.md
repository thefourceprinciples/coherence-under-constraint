# CORTANA–CMB–011 — Kernel Collapse

Goal: test the prediction from CORTANA–CMB–010 that adding an independent observational response channel should shrink the Chronovisor Kernel and/or strengthen weak transmitted directions.

## Bench design

Baseline: the same large-angle Sachs–Wolfe TT transfer used in 010.

Second channel: a polarization-like spin-2 toy projection with a distinct response kernel. This is NOT a full physical EE transfer calculation; it is an architecture-level two-channel test. A research-grade follow-up must replace it with CAMB/CLASS polarization transfer functions.

## Results

TT-only:
- rank = 29
- kernel dimension = 91
- relative singular directions >= 0.01 = 26
- relative singular directions >= 0.001 = 29

Combined TT + second channel:
- rank = 54
- kernel dimension = 66
- relative singular directions >= 0.01 = 28
- relative singular directions >= 0.001 = 33

Kernel reduction: 25 dimensions.
Rank gain: 25 dimensions.

## Classification

- Prediction that an independent response channel can shrink the exact kernel: PASS in this toy bench.
- Prediction that all newly visible directions become strongly recoverable: FAIL.
- Practical recoverability gain: PARTIAL PASS; many new directions are extremely ill-conditioned.
- CHH interpretation: exact visibility and useful recoverability are distinct thresholds.
- Physical CMB validation: PENDING CAMB/CLASS EE implementation.

## Key lesson

More channels can reduce exact non-identifiability without proportionally improving usable inference. Kernel dimension, singular-value spectrum, and thresholded recoverability must all be tracked separately.
