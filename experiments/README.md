# CUC reference experimental program

## Purpose

The first v0.2 benchmark is a modular oscillator system designed to test whether CUC variables add reproducible explanatory or predictive value beyond ordinary coupling, topology, energy balance, and flexible statistical baselines.

This benchmark does not claim that all persistent systems are oscillators. It provides a transparent system in which phase, amplitude, topology, boundaries, perturbations, and return can be manipulated independently.

## Questions

The initial benchmark asks:

1. Does aggregate Fource predict subsequent coherence beyond its component variables?
2. Do local, interface, and global coherence contribute differently to survival?
3. Does constraint fitness outperform raw constraint strength?
4. Does independent throughput exhibit an operating window?
5. Does interface mismatch reveal failure before global coherence?
6. Does the Darkness composite add stable predictive value?
7. Does the complete OCP gate distinguish resilient return from apparent repetition?

## Baseline dynamics

The ordinary comparison model is:

```latex
\[
d\theta_i
=
\left[
\omega_i
+
\sum_{j=1}^{N}
K_{ij}
\sin
\left(
\theta_j-\theta_i-\alpha_{ij}
\right)
\right]dt
+
\sigma_i\,dW_i(t)
\]
```

The Fource-augmented comparison is:

```latex
\[
d\theta_i
=
\left[
\omega_i
+
\kappa
\sum_{j=1}^{N}
a_{ij}
g\!\left(\widetilde{\Phi}_{ij}\right)
\sin
\left(
\theta_j-\theta_i-\alpha_{ij}
\right)
\right]dt
+
\sigma_i\,dW_i(t)
\]
```

The ordinary and augmented models must receive equal parameter budgets or an explicit model-complexity penalty.

## Independent variables

Manipulate independently:

- ordinary coupling gain;
- amplitude distribution;
- phase-error transformation;
- Fource regularization and bounding function;
- within-module connectivity;
- between-module connectivity;
- constraint strength;
- constraint topology;
- throughput or resource availability;
- noise intensity and correlation;
- intrinsic-frequency heterogeneity;
- delay;
- dissipation when amplitude dynamics are modeled;
- boundary leakage;
- interface error;
- perturbation amplitude, duration, and target.

Do not implement throughput only by multiplying coupling when testing a distinct throughput claim. Do not define constraint solely as an alignment force when testing whether constraint produces alignment.

## Outcomes

Record at least:

- global coherence;
- mean local coherence;
- interface coherence;
- local-global divergence;
- organization distance;
- viability;
- continuous survival;
- occupancy persistence;
- failure time and location;
- return probability and time;
- repair cost;
- resource or energy accounting.

## Required comparisons

1. Uncoupled units.
2. Ordinary Kuramoto-style coupling.
3. Amplitude-only weighted coupling.
4. Phase-error-only coupling.
5. Fource-augmented coupling.
6. Topology and energy-balance model without coherence terms.
7. Flexible statistical predictor without CUC structure.
8. Darkness-term ablations.
9. Global-only coherence model.
10. Multiscale coherence model.

## Experimental design

The full design is conceptually:

```latex
\[
\mathrm{Design}
=
\mathrm{Coupling}
\times
\mathrm{Constraint}
\times
\mathrm{Throughput}
\times
\mathrm{Noise}
\times
\mathrm{Topology}
\times
\mathrm{Perturbation}
\]
```

Early experiments may use a fractional-factorial or space-filling design, but every interaction claimed must be estimable.

## Reproducibility contract

Each run must include:

- a stable experiment identifier;
- linked claim identifiers;
- software commit;
- environment lock;
- complete configuration;
- seed policy;
- input hashes;
- output manifest;
- expected figures and tables;
- convergence and numerical-stability checks;
- deviations from preregistration;
- negative and null results.

## Promotion criterion

A CUC claim advances beyond formal specification only when a preregistered CUC variable provides reproducible out-of-sample prediction, explanation, or intervention value beyond appropriate ordinary dynamical and statistical baselines.

If no such gain appears, the framework remains a potentially useful vocabulary but has not demonstrated distinctive empirical power.

## Planned layout

```text
experiments/
├── README.md
├── protocols/
├── preregistrations/
├── configs/
├── results/
└── manifests/
```

Empty directories will be created only when an actual protocol or artifact is ready to occupy them.

