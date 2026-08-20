# GARDENCORE-001 — Common Kernel Extraction

GardenCore 0.1.0 extracts the repeated inverse-problem machinery that survived the CORTANA-CMB, QCORE, LATENT, and SPECTRA benches into one reusable software layer.

Core API:
- `analyze_operator(T)`
- `null_space(T)`
- `threshold_count(report, epsilon)`
- `stack_channels(...)`
- `row_normalize(T)`
- `choose_next_measurement(base_T, candidates)`

The library does not claim new mathematics. It packages standard SVD, rank, null-space, conditioning, and measurement-design logic into one portable workflow.

## Verification

The shared API was rerun against four domains:
- CMB-010: 120 hidden bins -> rank 29, kernel 91
- QCORE-001A: bit-flip channel directions and QEC improvement reproduced
- LATENT-001A: hidden-state kernel collapse and probe-design logic reproduced
- SPECTRA-001A: structural frequency-only kernel reproduced

Unit tests: 4/4 passed.

Result: PASS for software-level portability of the common operator/kernel architecture.
