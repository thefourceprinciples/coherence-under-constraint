# Historical simulation prototypes

This directory preserves the first computational prototypes associated with Coherence Under Constraint.

They are useful for provenance, code repair, and baseline reconstruction. They are **toy simulations**, not empirical validation of CUC and not the v0.2 reference benchmark.

## Files

| File | Purpose | Primary output |
|---|---|---|
| `cuc_simulation_v1_coherence_emergence.py` | Time-domain oscillator coherence in three illustrative regimes | `figure_1A_coherence_emergence.png` |
| `cuc_simulation_v2_phase_diagram.py` | Coupling and alignment-constraint sweep | `figure_1B_phase_diagram.png` |
| `cuc_simulation_v3_throughput_survival.py` | Throughput-multiplier and noise sweep | `figure_1C_throughput_map.png`, `figure_1D_survival_boundary.png` |
| `cuc_simulation_v4_unified_plate.py` | Combines Figures 1A–1D | `cuc_simulation_v4_unified_figure.png` |
| `cuc_generate_all_figures.py` | Runs v1 through v4 from the simulation directory | all outputs above |

## Install

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

For headless environments:

```bash
export MPLBACKEND=Agg
python simulations/cuc_generate_all_figures.py
```

Or run the prototypes individually:

```bash
python simulations/cuc_simulation_v1_coherence_emergence.py
python simulations/cuc_simulation_v2_phase_diagram.py
python simulations/cuc_simulation_v3_throughput_survival.py
python simulations/cuc_simulation_v4_unified_plate.py
```

## Known scientific limitations

- **Throughput-coupling confound:** throughput multiplies coupling strength in v1–v3; it is not an independently modeled resource flow.
- **Constraint-alignment confound:** boundary strength is implemented as attraction to a module mean, so part of the expected coherence effect is built into the intervention.
- **Global-metric limitation:** the prototypes primarily report one global phase-order parameter and do not jointly measure local and interface coherence.
- **Survival proxy:** v3 labels a sustained-coherence threshold as survival without an independent organization or viability criterion.
- **Illustrative thresholds:** parameter ranges and the threshold are exploratory rather than preregistered or calibrated.
- **Limited replication:** the sweeps use few replicates and have not completed held-out or cross-model validation.

These limitations are research targets, not details to hide. The v0.2 benchmark described in [`experiments/README.md`](../experiments/README.md) is designed to separate these variables and compare CUC-specific terms with ordinary baselines.

## Output integrity

Do not treat a generated plot as an empirical finding. A promoted result must be linked to a claim, code version, configuration, seed policy, uncertainty analysis, and experiment manifest.

