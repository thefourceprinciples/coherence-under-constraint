# LATENT-001A — Hidden Scaffold Tomography

Third-domain portability bench for the CORTANA-CMB inverse-problem architecture.

## Hidden state
8 unknown cell contrasts in a toy 1D object.

## Probe A
Four line-integral style measurements produce a response matrix with:
- rank = 4
- kernel dimension = 4
- nonzero condition number ≈ 2.593

A null-space perturbation generates a physically different hidden state whose Probe-A measurements are identical to machine precision.

## Probe B
A second, distinct probe geometry has:
- rank = 3
- kernel dimension = 5

Combined A+B:
- rank = 7
- kernel dimension = 1
- nonzero condition number ≈ 27.144

Thus the combined probe set collapses the latent kernel from 4 dimensions to 1.

## Active probe design
A rank-first search over candidate 4-cell binary probe paths finds an added probe covering cells (1,4,7,8), increasing Probe A rank from 4 to 5 and shrinking the kernel from 4 to 3.

## Classification
- direct demonstration of hidden-state non-identifiability under one probe: PASS
- null-space perturbation with exactly identical observations under Probe A: PASS
- kernel collapse using an independent probe geometry: PASS
- active experimental design that shrinks the kernel: PASS
- new tomography mathematics: FAIL / not claimed

## Key lesson
The same kernel/SVD architecture used for the CMB and quantum channels also diagnoses latent-state observability and can guide measurement design. Exact visibility and conditioning remain separate: adding probes can reduce the kernel while worsening numerical conditioning in the surviving subspace.
