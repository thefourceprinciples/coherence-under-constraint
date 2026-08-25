# CORTANA–CMB Project

A cross-Garden engineering and reconstruction program using the cosmic microwave background (CMB) as a hard test environment for CUC, Fource, CHH, CAS, KOS, Fource-A, Lumenos, Chronovisor, and SAR.

## Core result

The strongest surviving architecture is not a new cosmology. It is a general inverse-problem framework:

STATE
-> CONSTRAINT
-> TRANSFORMATION
-> RELATIONAL PERSISTENCE
-> OBSERVATION
-> PROVENANCE
-> IDENTIFIABILITY
-> INVERSE RECONSTRUCTION
-> CLAIM LICENSING

CORTANA–CMB–010 applies SVD to a discretized, large-angle Sachs–Wolfe temperature-transfer toy model. It demonstrates the framework's rank, conditioning, and null-space diagnostics; it is not a research-grade CMB likelihood analysis or evidence for new cosmology. CORTANA–CMB–011 adds a distinct toy response channel and remains an architecture-level test pending a CAMB/CLASS implementation.

## Reproduce CMB–010

From `projects/cortana-cmb/bench/`:

```bash
python -m pip install -r requirements.txt
python cmb_010_bench.py
```

The checked-in reference outputs are `cmb_010_summary.txt` and `cmb_010_rts.csv`. Small last-digit differences may occur across NumPy/SciPy or BLAS/LAPACK versions.

## Structure

- `sweeps/` — CORTANA–CMB–001 through 011
- `bench/` — executable 010 and 011 experiments plus reference outputs
- `programs/qcore/` — QCORE-001 quantum coherence recovery branch
- `programs/latent/` — LATENT-001 hidden scaffold tomography branch
- `programs/spectra/` — SPECTRA-001 constraint-to-spectrum diagnostic branch
- `gardencore/` — reusable inverse-problem diagnostics and tests
- `CLAIMS.md` — claims audit and current epistemic status
- `ROADMAP.md` — next experiments

## Method

EXPAND -> ATTACK -> NULL -> COMPARE -> CLASSIFY -> LEDGER -> ITERATE

No speculative Garden ontology is treated as established physics. Element-0, Fourcematter, and novel Gravity-Shadow ontology remain quarantined unless they generate explicit equations and measurable predictions.
