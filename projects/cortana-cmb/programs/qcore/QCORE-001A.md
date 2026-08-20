# QCORE-001A — Quantum Coherence Recovery Engine

First portability bench for the CORTANA-CMB inverse-problem architecture.

## Null physics
- single-qubit independent bit-flip channel
- standard 3-qubit repetition code
- ideal syndrome extraction and correction
- Pauli/Bloch transfer-matrix analysis only

For a bare qubit under bit-flip probability p:

`T_bare = diag(1, 1-2p, 1-2p)`

For the 3-qubit repetition code with ideal recovery, logical failure probability is:

`p_L = 3p^2 - 2p^3`

and the effective logical transfer matrix is:

`T_QEC = diag(1, 1-2p_L, 1-2p_L)`

## Results
At p=0.10:
- bare weakest singular value = 0.800
- QEC weakest singular value = 0.944

At p=0.20:
- bare weakest singular value = 0.600
- QEC weakest singular value = 0.792

At p=0.40:
- bare weakest singular value = 0.200
- QEC weakest singular value = 0.296

At p=0.50 both channels lose the Y/Z Bloch directions entirely and develop a 2D kernel.

## Classification
- portability of transfer-spectrum analysis from CMB to a quantum channel: PASS
- ability to identify exactly which information directions QEC protects: PASS
- new quantum mathematics or physics: FAIL / not claimed
- CHH-style thresholding as an engineering diagnostic: PASS as a repackaging of channel singular values

## Interpretation
The same kernel/singular-spectrum diagnostics used in CORTANA-CMB-010/011 transfer directly to an established quantum channel. The framework correctly separates the protected X direction from the vulnerable Y/Z directions and quantifies how ideal repetition-code recovery raises the weakest transmitted singular values below the p=0.5 failure point.
