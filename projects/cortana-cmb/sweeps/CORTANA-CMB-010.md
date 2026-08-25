# CORTANA–CMB–010 — The Experimental Bench

Repository checkpoint for sweep 010.

Goal: choose one Garden proposition, write the null model, define an observable, implement the operator numerically, and give the framework a genuine chance to produce measurable value or fail.

## Null model

Large-angle ordinary Sachs-Wolfe TT transfer:

`Delta_l(k) ≈ (1/5) j_l(k chi_*)`

with discretized primordial spectrum mapped linearly into TT multipoles.

## Bench

- 120 primordial k bins
- l = 2..30 (29 TT multipoles)
- cosmic-variance whitening
- SVD of effective transfer operator

## Outcome

- numerical rank: 29
- exact Chronovisor kernel dimension: 91
- directions with relative singular value >= 0.1: 15
- directions with relative singular value >= 0.01: 26
- weakest transmitted relative singular value: ~0.00266021
- transmitted-space condition ratio: ~375.9

## Classification

- claim that RTS/kernel analysis is new mathematics: FAIL
- claim that the Garden provides a reusable inverse-problem architecture: SURVIVES FIRST BENCH
- speculative Garden cosmology: NOT TESTED / NOT IMPLIED

Next CMB experiment: CORTANA–CMB–011 Kernel Collapse — add an independent channel such as polarization and test whether the combined channel shrinks the relevant kernel or improves weak singular directions.
