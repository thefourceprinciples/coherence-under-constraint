# Coherence Under Constraint

**A falsifiable research framework for studying how organized systems persist, fail, recover, and transform under constraint.**

[![Status: Draft research program](https://img.shields.io/badge/status-draft%20research%20program-8a6d3b)](CHARTER.md)
[![Version: 0.2.0-draft.1](https://img.shields.io/badge/version-0.2.0--draft.1-4c6ef5)](VERSION.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Author:** Gage Fry  
**Lineage:** The Fource Principles / Framework Garden  
**Canonical Garden identity:** G01-T003  
**Legacy identity:** FR-003  
**Current status:** Formalized research framework; not yet empirically validated or peer reviewed

---

## The root question

When a system changes under pressure, what must survive for it to remain the same organized system?

Coherence Under Constraint, abbreviated **CUC**, begins with one invariant:

> **A structure persists when its organization survives the constraints acting upon it.**

CUC studies the conditions under which an organization survives, fails, returns, or transforms while facing boundaries, perturbations, limited resources, throughput demands, noise, dissipation, and interface mismatch.

The framework is intended to support explicit models and testable comparisons. It is not offered as a universal physical law or as a replacement for established sciences.

## Start here

- [CUC Canon v0.2 Charter](CHARTER.md) — complete ontology, equations, hypotheses, falsifiers, evidence ladder, governance, and research constitution
- [Canon registry](canon/README.md) — status rules, symbols, and machine-readable claims
- [Experimental program](experiments/README.md) — the reference modular-oscillator benchmark
- [Public FAQ](docs/faq.md) — concise answers to predictable questions and objections
- [Reddit release draft](docs/reddit-release.md) — a public-facing doorway into the framework
- [Existing simulations](simulations/README.md) — historical computational prototypes and known limitations

## The v0.2 correction

The original public scaffold used this historical mnemonic:

```text
Structure = Coherence × Constraint × Throughput
```

That expression remains useful as provenance, but it is not a definition or validated law. It leaves several questions unresolved:

- What organization is being preserved?
- Over what time horizon?
- Which constraints enable organization and which destroy it?
- Is throughput too low, adequate, or excessive?
- Is the system coherent locally, across interfaces, or globally?
- Does high coherence support viability, or merely synchronized collapse?

CUC v0.2 therefore defines persistence independently of coherence. Let `I_O(t)` indicate that organization remains within a declared equivalence class and `I_V(t)` indicate that the system remains viable. Continuous persistence over horizon `T` is:

```latex
\[
P_T^{\mathrm{cont}}
=
\Pr_{\Pi}
\left[
I_O(t)I_V(t)=1
\quad
\forall t\in[0,T]
\right]
\]
```

The subscript `\Pi` identifies the initial-condition and perturbation protocol. This makes a persistence claim conditional, measurable, and falsifiable.

## Conceptual architecture

```text
local interaction
      │
      ▼
Fource functional ──► local/interface/global coherence
                              │
constraints ──────────────────┤
throughput adequacy ──────────┤
boundary quality ─────────────┤──► organizational persistence
viability requirements ───────┤
Darkness / degradation ───────┤
perturbation protocol ─────────┘
                              │
                              ▼
                    failure, repair, or return
                              │
                              ▼
                   OCP bounded-return tests
```

The layers have different roles:

- **Fource** is a proposed local, amplitude-weighted, phase-error-limited interaction functional that may generate coherence in appropriate dynamical models.
- **Coherence** is a declared relation among selected variables at a specified scale and time window.
- **CUC proper** evaluates whether organization and viability persist under declared constraints and perturbations.
- **Darkness** is a derived diagnostic of modeled degradation, including noise, boundary failure, and interface mismatch.
- **The Orbital Coherence Principle** is a validation protocol for bounded relational return.

## Canonical distinctions

CUC v0.2 distinguishes:

- state from organization;
- organization from viability;
- local coherence from interface and global coherence;
- coherence generation from coherence persistence;
- constraint magnitude from constraint fitness;
- raw throughput from throughput adequacy;
- useful dissipation from organization-degrading loss;
- persistence from robustness, resilience, return, adaptation, and transformation;
- descriptive coherence from ethical value.

These distinctions are meant to prevent circular definitions and overclaiming.

## Initial hypothesis program

The Charter registers ten testable hypotheses. The first experimental season prioritizes five:

1. **Local compatibility:** amplitude-weighted phase compatibility predicts subsequent coherence beyond its component variables.
2. **Coherence and survival:** relevant coherence measures improve held-out survival prediction beyond topology and energy balance.
3. **Constraint fitness:** organization-compatible constraint architecture predicts persistence better than raw constraint magnitude.
4. **Throughput window:** throughput-dependent systems exhibit viable operating regions rather than unlimited monotonic benefit.
5. **Interface bottleneck:** interface coherence predicts failures hidden by mean local coherence.

Each claim has a falsifier. Machine-readable records live in [`canon/claims.yml`](canon/claims.yml).

## Evidence status

| Layer | Current status |
|---|---|
| Root invariant | Canonical organizing commitment |
| Ontology and persistence definitions | Draft formal specification |
| Fource Sub-Theorem | Conditional hypothesis-bearing mechanism |
| Darkness Functional | Derived diagnostic requiring calibration |
| Existing oscillator scripts | Toy computational prototypes |
| Reference benchmark | Designed; implementation pending |
| Cross-domain applications | Mappings requiring independent evidence |
| Universal-law claim | Not made |
| Empirical validation | Not yet achieved |
| Peer review | Not yet completed |

Mathematical notation alone does not elevate evidence. A formally specified model remains formal until it survives reproducible tests and comparison with simpler alternatives.

## What CUC is not

CUC is not currently:

- a newly discovered fundamental force;
- proof that all systems are oscillators;
- a replacement for control theory, synchronization theory, thermodynamics, network science, biology, psychology, sociology, or survival analysis;
- evidence for consciousness, portals, or speculative cosmology;
- a claim that coherence is always good;
- an empirically established universal law.

Coherent systems can be brittle, coercive, harmful, or synchronized toward failure. Ethical value must be assessed independently.

## Reference benchmark

The next core experiment is a modular oscillator benchmark that manipulates independently:

- ordinary coupling;
- Fource transformation and regularization;
- constraint strength and topology;
- throughput or resource availability;
- noise and heterogeneity;
- delay and dissipation;
- boundary leakage and interface error;
- perturbation amplitude, duration, and target.

Primary outcomes include global, local, and interface coherence; organization distance; survival; failure time; return time; and repair cost. Ordinary Kuramoto-style coupling, amplitude-only weighting, phase-error-only weighting, topology-only models, and flexible statistical predictors serve as competing baselines.

See [experiments/README.md](experiments/README.md).

## Existing simulations

The repository contains April 2026 oscillator prototypes. They demonstrate early computational directions but do not validate CUC. Known limitations include:

- throughput is implemented as a multiplier on coupling and is therefore confounded with coupling strength;
- constraint is implemented as an alignment term, partly building the expected effect into the model;
- most results use one global phase-order parameter;
- current parameter thresholds are illustrative;
- the prototypes have not yet undergone systematic held-out validation or cross-model replication.

Their purpose in v0.2 is provenance and baseline reconstruction. They will be retained while the reference benchmark is developed.

### Run the historical prototypes

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export MPLBACKEND=Agg
python simulations/cuc_simulation_v1_coherence_emergence.py
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## Repository map

```text
.
├── README.md
├── CHARTER.md
├── CHANGELOG.md
├── VERSION.md
├── CITATION.cff
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── canon/
│   ├── README.md
│   ├── symbols.yml
│   └── claims.yml
├── docs/
│   ├── paper.md
│   ├── glossary.md
│   ├── faq.md
│   └── reddit-release.md
├── experiments/
│   └── README.md
├── scripts/
│   └── validate_repo.py
├── simulations/
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── workflows/
    └── PULL_REQUEST_TEMPLATE.md
```

## Contributing and critique

CUC is being opened for rigorous criticism, not protected from it. Useful contributions include:

- identifying circular or unmeasurable definitions;
- supplying stronger rival models;
- reproducing or breaking computational results;
- proposing independent operationalizations;
- documenting negative results;
- correcting mathematical, statistical, or domain errors;
- improving the ethical and governance boundaries.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Formal claims should use the claim issue template and name a falsifier.

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

Suggested draft citation:

> Fry, G. (2026). *Coherence Under Constraint: Foundational Charter and Research Program* (v0.2.0-draft.1). The Fource Principles.

## License

Code and repository documentation are released under the [MIT License](LICENSE), unless a file states otherwise.

---

> **No coherence without a relation. No persistence without an organization. No constraint without an admissible set. No survival without a horizon. No theory without a falsifier.**
