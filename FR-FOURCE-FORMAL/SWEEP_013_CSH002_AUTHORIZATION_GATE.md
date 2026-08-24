# FR–FOURCE–FORMAL–013
## CSH-002 Authorization Gate
### Freeze the experimental commitments before writing the new hypothesis

Status: PRE-HYPOTHESIS FREEZE / NO NEW EVIDENTIARY DATA

CSH-001 remains strongly falsified. CSH-002 is not yet an evidentiary claim. This sweep converts the Atlas Kill Box into an exact design contract. No calibration or held-out outcomes are inspected here.

## 1. Scope

The next experiment will test selective multiscale organizational recoverability, not universal same-partition convergence.

The object is an organizational atlas indexed by probe, target level, intervention, horizon, and null. Cross-scale disagreement is permitted and expected in some generator families.

## 2. Data partitions

Three disjoint seed classes are frozen now:

- design seeds: 2000–2009;
- calibration seeds: 3000–3029;
- held-out evidentiary seeds: 4000–4029.

Design seeds may be inspected while implementing and debugging. Calibration seeds may be inspected only after implementation fidelity is established and are used to decide whether a metric-target pair is eligible for preregistration. Held-out seeds must not be executed until CSH-002, its thresholds, and its code SHA are frozen.

No seed may migrate between classes.

## 3. Generator contract

The implementation must contain six named families with deterministic construction from seed.

### G1 — Static modular hierarchy

Purpose: recover nested structure from static relational organization.

Required levels:
- L1: four local modules A, B, C, D;
- L2: O1=A+B and O2=C+D;
- L3: O1|O2.

The implementation must make within-module relations strongest, within-composite cross-module relations intermediate, and cross-composite relations weakest, while avoiding a single hard-coded metric threshold as the definition of truth.

### G2 — Temporal organization without strong static modularity

Purpose: require temporal probes to add information beyond static coupling.

Static time-averaged coupling must be deliberately insufficient to reliably recover the declared target. The target must be encoded in transition/regime structure across time.

### G3 — Observational mimic / interventional difference

Purpose: test causal probes.

Paired systems must be approximately matched on declared observational summaries while differing in preregistered intervention response at the target level.

### G4 — Constituent-role substitution

Purpose: test organization under local nuisance replacement.

A role-preserving transformation changes node-local nuisance parameters/identities while preserving the declared relational role map.

### G5 — Nested conflict

Purpose: force legitimate cross-scale disagreement.

At least two probes must have different preregistered target levels such that success at one level does not imply high rank at the other.

### G6 — Adversarial decoy-rich null-like family

Purpose: false-positive control.

No privileged planted organizational hierarchy is declared. The family must contain strong nuisance cues such as balanced partitions, hubs, common drivers, or stable trivial macrostates.

A method that confidently reports the preregistered positive-control signature on G6 fails false-positive control.

## 4. Target-level registry

Each metric implementation must register exactly:

- metric ID;
- information access;
- target generator families;
- licensed target level(s);
- commensurability class;
- relevant null(s);
- relevant decoy(s);
- relevant destruction intervention(s);
- simplest equal-information baseline.

No target level may be added after calibration results are seen. A metric may be declared ineligible rather than remapped.

## 5. Initial probe registry

The first implementation may reuse concepts from CSH-001, but their licenses are narrowed.

### Q-BND — boundary separation

Information: static relational matrix.
Primary license: external/composite boundary levels such as G1-L3.
Baseline: raw coupling cut/separation statistic with identical matrix access.
Relevant nulls: N1, N2.
Relevant decoys: DQ1 coupling decoy, DQ2 balance decoy.

### Q-TMP — temporal predictive structure

Information: trajectories only, with no privileged access to generator labels.
Primary license: G2 temporal target.
Baseline: static coupling plus simple one-step activity statistics.
Relevant nulls: N3 and N2 where geometry applies.
Relevant decoys: DQ5 trivial persistence.

### Q-INT — interventional separation

Information: declared intervention responses.
Primary license: G3 causal target and any explicitly registered intervention-defined level.
Baseline: observational association using the same variables but no intervention labels.
Relevant nulls: N4.
Relevant decoys: DQ3 common-driver and DQ4 hub-effect decoys.

### Q-RET — level-specific retention

Information: declared macrostate trajectory at one registered level.
Primary license: only levels whose macrostate definition is preregistered independently of outcomes.
Relevant nulls: N3.
Relevant decoy: DQ5.

### Q-PERT — level-specific perturbational robustness

Information: baseline and perturbed trajectories/relations.
Primary license: only the level directly targeted by the registered perturbation.
Relevant nulls: N1/N3/N4 according to perturbation type.

No universal median rank or all-probe consensus is permitted.

## 6. Decoy contract

- DQ1 coupling decoy: strong static separation not aligned with the registered non-static target.
- DQ2 balance decoy: balanced candidate partitions with no planted functional privilege.
- DQ3 common-driver decoy: correlated groups produced by a shared external driver rather than direct target organization.
- DQ4 hub decoy: a node/group with large intervention effect that does not define the registered system boundary.
- DQ5 persistence decoy: stable or absorbing macrostate with no registered organizational role.

Every positive generator must contain at least one relevant decoy or an explicit reason the decoy is inapplicable.

## 7. Null algorithms

The exact code will be reviewed before calibration, but the semantic invariants are frozen now.

### N1 generator null

Randomize the relations that encode the registered target while preserving declared low-order nuisance summaries as closely as algorithmically possible. The preserved summaries must be written to the run manifest.

### N2 geometry null

Condition comparison on candidate split size or compare against candidates sampled from the same split-size class. This prevents balanced-partition preference from masquerading as target recovery.

### N3 temporal null

Destroy temporal ordering beyond the preregistered preserved horizon while retaining marginal activity and static summaries. The chosen block/shuffle algorithm must be fixed before calibration.

### N4 intervention null

Break the mapping between intervention identity and response while preserving the empirical response distribution as closely as possible.

### N5 agreement null

Where same-target probes are combined, estimate expected agreement after independently applying their relevant nuisance-preserving null transformations. No cross-scale probes enter N5 aggregation.

## 8. Selective destruction contract

### X1 local-module destruction

Randomize relations defining L1 while minimizing change to the registered higher-level boundary summary.

### X2 composite/external-boundary destruction

Randomize relations defining L3 while minimizing change to registered internal-module summaries.

### X3 temporal-regime destruction

Destroy the longer-horizon transition/regime relation while preserving static summaries.

### X4 causal-direction destruction

Alter/scramble the registered intervention-response mapping while preserving observational summaries.

### X5 global destruction

Destroy all registered organizational levels and serves only as a positive sensitivity control.

### XC1 constituent-role substitution

Change nuisance identity/local parameters while preserving the registered relational role map.

### XC2 isomorphic relabeling

Apply a one-to-one permutation consistently to all relevant structures and labels.

Each implementation must emit a preservation report quantifying how well non-target invariants were held fixed. A selective-destruction result is uninterpretable if the preservation report fails its preregistered tolerance.

## 9. Calibration eligibility gates

A metric-target pair may proceed from calibration into CSH-002 only if all applicable gates are satisfied on seeds 3000–3029:

- E1 recovery: target is top 5% in at least 24/30 seeds;
- E2 null margin: target rank percentile exceeds the relevant matched-null target by at least 20 points in median and is positive in at least 24/30 pairs;
- E3 targeted destruction: target worsens by at least 20 percentile points in at least 24/30 valid selective-destruction pairs;
- E4 selectivity: non-target registered levels worsen by less than 10 percentile points in at least 24/30 valid pairs;
- E5 decoy rejection: target outranks every applicable preregistered decoy in at least 24/30 seeds;
- E6 label invariance: absolute rank-percentile change <=2 points in at least 27/30 seeds;
- E7 baseline value-add: richer probe must outperform or uniquely discriminate at least one preregistered task that its equal-information baseline does not. Otherwise it may remain descriptive but cannot support a novelty claim.

Calibration is a gate, not evidence for CSH-002. Passing calibration authorizes freezing a hypothesis; it does not count toward its evidentiary success.

## 10. Held-out kill gates

The future held-out test must preserve the previously defined K1–K7 failure classes:

- K1 wrong-level recovery;
- K2 nonselective destruction;
- K3 decoy capture;
- K4 null equivalence;
- K5 baseline dominance;
- K6 representation contamination;
- K7 generator overfit.

Exact hypothesis-level pass/fail aggregation will be written only after calibration identifies which metric-target pairs are eligible, and before any 4000-series seed is run.

## 11. Cross-generator generalization requirement

At least one eligible probe principle must be tested on a held-out microscopic realization not used to tune its implementation. Passing only on the generator family that motivated the probe cannot establish general organizational recoverability.

Where possible, the holdout realization should preserve the abstract target relation while changing node count, microscopic parameterization, or update rule.

## 12. Provenance dependency graph

All design commitments must be tagged:

- PRE-001: inherited from pre-falsification work;
- POST-001: motivated by CSH-001 outcome/diagnostic;
- NULL-010: introduced by null reconstruction;
- ATLAS-011: introduced by organizational-atlas formalization;
- KILL-012: introduced by kill-box design;
- AUTH-013: frozen or sharpened in this authorization gate.

The eventual preregistration must expose these tags rather than presenting all predictions as independent pre-existing theory.

## 13. Authorization decision

This sweep authorizes implementation and calibration only.

It does **not** authorize held-out execution and does **not** yet freeze CSH-002.

The next transition is:

`013 design freeze`
`-> 013A implementation`
`-> adversarial code review + smoke tests`
`-> calibration on 3000–3029`
`-> freeze eligible metric-target pairs and exact CSH-002 predictions`
`-> freeze implementation SHA and held-out workflow`
`-> only then execute 4000–4029 once`

No 4000-series held-out seed may be executed before the preregistration and code SHA are frozen.

## Foundation verdict

The project now has a concrete firewall between learning from CSH-001 and testing CSH-002. The next scientific task is not another conceptual rescue. It is to implement this contract and determine, using calibration data only, whether any metric-target pair earns the right to face untouched evidence.
