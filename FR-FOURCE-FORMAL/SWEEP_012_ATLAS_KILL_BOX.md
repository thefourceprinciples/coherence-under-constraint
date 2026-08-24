# FR–FOURCE–FORMAL–012
## The Atlas Kill Box
### Held-out generators, decoys, nulls, and numerical selectivity criteria before CSH-002

Status: PRE-HYPOTHESIS FALSIFICATION DESIGN / NO NEW DATA

CSH-001 remains strongly falsified. No CSH-002 is authorized by this sweep. This document exists to make the Organizational Atlas vulnerable before a new hypothesis is written.

## 1. Purpose

The Atlas architecture is only scientifically useful if it can fail on untouched systems. The central danger after CSH-001 is post-failure overfitting: redesigning the next bench around exactly the patterns already observed.

Therefore the next program must separate:

- design generators used to debug implementation;
- calibration generators used to estimate numerical variability;
- held-out evidentiary generators never inspected before execution.

Any future CSH-002 must be judged on the held-out family.

## 2. Generator families

### G1 — Static modular hierarchy

A 16-node stochastic binary system with four local modules:

`A = {0..3}`
`B = {4..7}`
`C = {8..11}`
`D = {12..15}`

Composite levels:

`O1 = A + B`
`O2 = C + D`

External level:

`O1 | O2`

Coupling strengths are nested but heterogeneous so no single scalar threshold uniquely identifies every level.

Purpose: test multiscale boundary recovery.

### G2 — Temporal organization without strong static modularity

Static pairwise coupling is approximately homogeneous, but update rules create a slow latent temporal regime shared by one subset of nodes and a distinct regime in another.

Purpose: create a case where simple static coupling should not be sufficient, but temporal/predictive probes should have an advantage.

### G3 — Interventional organization with observational mimicry

Two candidate systems are tuned to have closely matched observational transition statistics, while intervention responses differ because causal directionality differs.

Purpose: require interventional probes to add information unavailable from purely observational baselines.

### G4 — Constituent-role substitution

Relational roles are preserved while node-local nuisance parameters, update biases, and labels are replaced at a defined midpoint.

Purpose: test whether level-specific organizational features persist despite local realization change.

### G5 — Nested organization with conflict

Two valid organizational levels are intentionally arranged so that a metric optimized for one level should perform poorly on another.

Purpose: ensure the atlas tolerates principled cross-scale disagreement rather than rewarding same-partition consensus.

### G6 — Structureless / adversarial null-like generator

No stable planted hierarchy, but low-order statistics and partition-size preferences are engineered to create plausible decoy signals.

Purpose: measure false organizational recovery.

## 3. Data split

Before any future code execution:

- 20 design seeds per generator family for implementation debugging only;
- 30 calibration seeds per family for estimating variance and fixing thresholds;
- 30 held-out evidentiary seeds per family sealed until CSH-002 execution.

Held-out seeds must be generated from a deterministic seed schedule committed before implementation results are inspected.

No evidentiary seed may be moved into calibration after execution begins.

## 4. Metric-to-target commitments

Each metric must declare a target level before any held-out run.

Provisional allowed mapping:

### Boundary-separation probe B
Primary target: external/composite cut where cross-boundary dependence is minimized relative to within-level dependence.

Allowed targets:
- G1: O1|O2
- G4: preserved external boundary if unchanged

Not licensed to claim recovery of local A/B/C/D modules unless separately preregistered.

### Predictive-temporal probe P
Primary target: coarse-graining that preserves future predictive structure.

Allowed target:
- G2 temporal regime partition

### Interventional probe I
Primary target: causal partition under declared intervention class.

Allowed target:
- G3 causal grouping
- G1 local module relations only if intervention semantics explicitly define them

### Persistence/retention probe R
Primary target: declared macrostate whose retention is part of the generator definition.

### Robustness probe RB
Primary target: the same level as its unperturbed parent metric. RB may not choose a new level post hoc.

No metric is allowed to claim universal systemhood.

## 5. Decoy library

Every generator family must contain at least one decoy designed to fool a plausible method.

### DQ1 — Coupling decoy
Strong static coupling that does not correspond to the declared temporal or causal target.

### DQ2 — Balance decoy
A 50/50 partition favored by macrostate geometry but not by ground truth.

### DQ3 — Correlation decoy
High observational correlation caused by a common driver without direct organizational integration.

### DQ4 — Intervention decoy
Large intervention effect concentrated on one node or hub that does not define the declared organizational level.

### DQ5 — Persistence decoy
A stable but trivial macrostate with little causal or predictive significance.

A valid metric must beat its own relevant decoy, not merely rank the ground-truth partition above random chance.

## 6. Null families

### N1 — Generator null
Destroy planted organization while preserving degree distribution, weight distribution, marginal activity, and as many low-order statistics as practical.

### N2 — Geometry null
Randomize target labels while preserving partition-size distribution exactly.

Purpose: measure biases caused by split size or combinatorial candidate geometry.

### N3 — Temporal null
Preserve static coupling and one-step marginals while phase-shuffling or otherwise destroying longer temporal structure.

### N4 — Intervention null
Preserve observational statistics while randomizing or symmetrizing the intervention-response map.

### N5 — Agreement null
Construct method outputs from matched nuisance-preserving surrogates and measure expected cross-method overlap/rank correlation.

Cross-method agreement above chance is not evidence unless it exceeds N5.

## 7. Selective destruction interventions

Each legitimate organizational level must have a paired destruction intervention.

### X1 — Local-module destruction
Randomize a preregistered fraction of edges defining A/B/C/D while preserving composite O1|O2 cross-boundary statistics as closely as possible.

### X2 — Composite-boundary destruction
Increase or rewire O1↔O2 relations toward the within-composite distribution while preserving local-module structure.

### X3 — Temporal-regime destruction
Destroy the slow latent temporal dependency while preserving static coupling.

### X4 — Causal-direction destruction
Symmetrize or reverse selected causal edges while matching observational statistics where possible.

### X5 — Global destruction
Destroy all declared organizational levels.

### XC1 — Constituent-role substitution control
Change node-local nuisance properties while preserving all defining relations.

### XC2 — Isomorphic label permutation control
Pure relabeling; all level assignments must remain invariant after inverse mapping.

## 8. Numerical selectivity criteria

The following are provisional calibration targets to be frozen only after calibration data, not evidentiary data, are generated.

For a target metric q and target level l:

`Recovery(q,l)` = percentile rank of the true target among admissible candidates.

`Selectivity(q,l,X_l)` = degradation of target recovery under the intervention designed to destroy l.

`Specificity(q,l,X_k)` = degradation under interventions aimed at another level k.

A metric-level pair is eligible for evidentiary testing only if calibration supports thresholds satisfying all of:

1. Recovery: target is within the top 5% in at least 80% of calibration seeds.
2. Null rejection: median target rank beats the corresponding null by at least 20 percentile points.
3. Selective destruction: target-specific intervention worsens recovery by at least 20 percentile points in at least 80% of calibration seeds.
4. Cross-level sparing: non-target intervention worsens recovery by less than 10 percentile points in at least 80% of calibration seeds.
5. Decoy rejection: true target outranks the preregistered decoy in at least 80% of calibration seeds.
6. Label invariance: percentile rank changes by no more than 2 points in at least 90% of calibration seeds.
7. Baseline burden: if a simpler equal-information baseline matches or exceeds performance on all primary criteria, the richer metric earns no novelty claim.

These numbers are not yet CSH-002 thresholds. They are kill-box eligibility targets for deciding whether a metric-target pair deserves entry into the evidentiary hypothesis.

## 9. Atlas-level success must not be defined by universal convergence

The atlas passes a generator family only if each preregistered target level shows the expected selective signature under its licensed metrics.

Example for G1:

- B recovers O1|O2;
- local intervention probe recovers A/B/C/D structure if licensed;
- X1 selectively damages local-level recovery while sparing O1|O2;
- X2 selectively damages O1|O2 while sparing local modules;
- XC1 and XC2 preserve both;
- no required same-partition agreement exists between local and external probes.

Thus success is a structured matrix of predicted effects, not one consensus score.

## 10. Failure modes that must kill CSH-002 if retained

Any future CSH-002 should include hard failure gates for at least the following:

### K1 — Wrong-level recovery
A metric systematically ranks a different level than its preregistered target.

### K2 — Nonselective destruction
Targeted perturbation damages all levels similarly, making causal localization impossible.

### K3 — Decoy capture
A decoy beats the true target at or above the preregistered failure frequency.

### K4 — Null equivalence
Performance is indistinguishable from the relevant null ensemble.

### K5 — Baseline dominance
A simpler equal-information baseline matches/exceeds the richer method on all primary tasks.

### K6 — Representation contamination
Label permutation or isomorphic encoding materially changes recovery.

### K7 — Generator overfit
The mapping works on G1 but fails on a held-out generator family designed to instantiate the same organizational relation differently.

A CSH-002 that does not expose itself to these failure modes is not ready.

## 11. Holdout requirement

The strongest anti-rescue rule becomes:

> No claim of support may be based solely on the generator family used to design the metric.

At least one generator family with a different microscopic implementation but the same preregistered organizational relation must remain untouched until the final evidentiary run.

This is necessary to distinguish learning a structural principle from learning the quirks of one simulator.

## 12. Provenance tags

Every design choice for CSH-002 must be labeled:

- PRE-001: existed before CSH-001 result;
- POST-001: motivated by CSH-001 failure diagnostics;
- NULL-010: derived from Sweep 010 null reconstruction;
- ATLAS-011: derived from Sweep 011 architecture;
- KILL-012: introduced in this kill-box sweep.

This prevents post-failure insight from later being presented as independent prior prediction.

## 13. What would authorize CSH-002?

CSH-002 is authorized only after all of the following are committed before evidentiary execution:

1. exact generator definitions for G1–G6;
2. deterministic design/calibration/holdout seed schedules;
3. exact metric-to-target mappings;
4. exact decoy definitions;
5. exact N1–N5 null algorithms;
6. exact X1–X5 and XC1–XC2 interventions;
7. calibration-derived numerical thresholds frozen without held-out access;
8. hard failure rules K1–K7;
9. simple-baseline definitions with equal information access;
10. provenance tags for every major design choice;
11. one code-complete smoke path that is explicitly non-evidentiary;
12. a separate manual workflow pinned to the frozen evidentiary commit.

Only then should the new hypothesis receive an identifier.

## Foundation verdict

The Organizational Atlas is not yet a theory. It is a candidate experimental architecture that now has a defined kill box.

The crucial shift from CSH-001 is this:

> We no longer ask whether all methods converge on one partition. We ask whether each method recovers the organizational level it is theoretically licensed to detect, rejects its relevant decoys/nulls, and responds selectively when that level's defining relations are destroyed.

This architecture can fail locally, globally, by decoy capture, by null equivalence, by baseline dominance, by representation contamination, or by generator overfit.

That is enough vulnerability to justify the next step.

Next: `FR–FOURCE–FORMAL–013 — CSH-002 Authorization Gate: freeze generators, seed schedules, metric-to-target mappings, interventions, null algorithms, and calibration protocol before writing the new hypothesis.`
