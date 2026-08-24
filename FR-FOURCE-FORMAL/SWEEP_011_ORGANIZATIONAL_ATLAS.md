# FR–FOURCE–FORMAL–011
## The Organizational Atlas
### Formalizing levels, selective destruction, and metric-to-target commitments before CSH-002

Status: PRE-HYPOTHESIS ARCHITECTURE / NO NEW DATA

CSH-001 remains strongly falsified. This sweep converts the null reconstruction into a formal design object while withholding any new hypothesis identifier. Nothing here may be scored against fresh data until the commitments below are frozen.

## 1. Core object: an organizational atlas

Let a dynamical system be represented by microstate X(t) evolving under transition law D.

Let P be a candidate partition or coarse-graining of the microvariables. Let q index an operational probe. Let l index a declared organizational level. Let i denote an intervention class. Let tau denote a time horizon. Let N denote a null ensemble.

Define an atlas entry:

`A(P,q,l,i,tau,N)`

as the calibrated score returned by probe q for candidate partition P under the declared level, intervention class, temporal horizon, and null reference.

The organizational atlas is the full collection:

`OA = {A(P,q,l,i,tau,N)}`

over all preregistered candidates and probes.

No scalar systemhood score is defined at this stage.

## 2. Declared levels in the next synthetic family

A future benchmark family should contain at least three legitimate organizational scales, all fixed before execution.

Level L1 — local modules

`A = {0,1,2,3}`
`B = {4,5,6,7}`

Target relations: strong within-A and within-B organization; weaker A–B interaction.

Level L2 — composite organization

`O = A + B`

Target relation: A and B jointly form a higher-level subsystem with dynamics not reducible to simply labelling one local module as the whole system.

Level L3 — environment boundary

`O | E`

where E contains the environmental degrees of freedom.

Target relation: O has a privileged interaction profile relative to E.

The exact generator need not be identical to CSH-001. Indeed, a new family should be constructed from scratch and held out from all design-tuning data.

## 3. Metric-to-target commitment matrix

Before execution, every metric must declare which target level it is theoretically expected to detect.

Provisional classes:

### Boundary-separation probes

Allowed target: L3 O|E.

Primary question:
Does the candidate partition isolate a subsystem whose cross-boundary statistical or dynamical dependence is reduced relative to within-side organization?

These probes are not automatically expected to recover L1 A|B.

### Interventional probes

Allowed targets: L1 or L2 depending on the intervention semantics.

Primary question:
Do controlled perturbations reveal causal autonomy, directed influence, or modular response at the declared level?

An intervention probe must specify whether it is intended to distinguish A from B, O from E, or another predefined level.

### Predictive-compression probes

Allowed target: whichever level minimizes predictive description while retaining preregistered future observables.

Important restriction:
Predictive compression is not presumed to target the same level as boundary separation. The target observable set must be fixed before execution.

### Retention / persistence probes

Allowed target: a declared macrostate at a declared level.

Primary question:
Does that macrostate remain stable over the stated temporal horizon relative to its matched temporal null?

### Perturbational-robustness probes

Allowed target: the declared level whose defining relations are being perturbed.

Primary question:
How much does the atlas signal for that level degrade under a perturbation designed to damage that level specifically?

## 4. Commensurability classes

Metrics may only be combined if they are preregistered in the same commensurability class.

Class C1 — same-target estimators
Different estimators intended to recover the same level from the same general information type.

Class C2 — complementary properties
Metrics characterizing distinct properties of one level. These remain a vector unless a formal aggregation rule is independently justified.

Class C3 — cross-scale probes
Metrics intentionally sensitive to different levels. These must never be collapsed into one consensus rank.

Class C4 — nuisance-correlated probes
Metrics whose apparent agreement can arise from shared candidate geometry, sample-size effects, or common preprocessing. Their dependence must be explicitly calibrated.

Class C5 — antagonistic probes
Metrics where improvement in one property can legitimately worsen another. Aggregation is prohibited unless a theory predicts a tradeoff surface.

## 5. Selective-destruction intervention library

Every declared organizational level receives a destruction intervention and at least one preservation control.

### D1 — destroy A/B modularity

Goal: disrupt within-A and within-B structure or erase the contrast separating the local modules while approximately preserving the outer O|E boundary.

Expected atlas effect:
L1-sensitive probes decrease.
L3-sensitive boundary probes remain comparatively stable.

### D2 — destroy O|E boundary

Goal: increase or randomize O–E interactions until the external boundary is erased while approximately preserving internal A/B organization.

Expected atlas effect:
L3-sensitive boundary probes decrease.
L1-sensitive probes remain comparatively stable.

### D3 — destroy both levels

Goal: erase both internal modularity and external boundary structure.

Expected atlas effect:
Signals at L1 and L3 both decrease.

### C1 — constituent-role substitution control

Change local identities or node-specific nuisance parameters while preserving the interaction roles defining the target level.

Expected atlas effect:
Target-level signals remain comparatively stable.

### C2 — label permutation control

Apply an isomorphic permutation of node labels.

Expected atlas effect:
All level assignments are preserved after inverse mapping.

## 6. Selectivity matrix

The most important future test is not generic degradation but selective degradation.

For target level l and intervention d, define:

`Delta(l,d) = A_before(l) - A_after(l,d)`

A selective intervention should satisfy a contrast such as:

`Delta(target,d) > Delta(non-target,d)`

by a preregistered margin or effect-size criterion.

This produces a destruction matrix:

`D[l,d]`

whose diagonal entries should be large for correctly targeted interventions and whose off-diagonal entries should remain smaller when unrelated levels are preserved.

This matrix is more informative than one universal persistence score because it tests whether the proposed atlas distinguishes levels causally.

## 7. Required null atlas

For every probe q, define a matched null distribution before interpreting its raw score.

Required null families:

### N1 — generator-null
Remove target organization while preserving low-order graph or activity statistics.

### N2 — geometry-null
Preserve candidate partition-size distribution and assess preferences for balanced or otherwise geometrically favored splits.

### N3 — temporal-null
Preserve static state frequencies or coupling statistics while destroying sequential dependence.

### N4 — intervention-null
Preserve observational distributions while scrambling the directional or causal relation relevant to the intervention probe where feasible.

### N5 — agreement-null
Estimate the cross-probe agreement expected from common nuisance structure alone.

Scores entering the atlas should be reported both raw and null-calibrated.

## 8. Simple-baseline equivalence rule

For each atlas target, define the simplest baseline with access to the same information.

A richer probe is scientifically interesting only if at least one of the following is true:

- it recovers a target the baseline misses;
- it discriminates two systems the baseline regards as equivalent;
- it correctly predicts selective destruction while the baseline does not;
- it generalizes to a held-out generator family where the baseline fails.

If the simple baseline matches or exceeds performance on the intended task, the richer probe is classified as redundant for that task.

## 9. Atlas topology

The atlas should explicitly represent relationships among organizational levels.

Possible relations include:

`nested(P1,P2)`
`overlaps(P1,P2)`
`incompatible(P1,P2)`
`refines(P1,P2)`
`coarse_grains(P1,P2)`
`lineage_continuous(P_t,P_t+1)`

This allows a hierarchy or partial order instead of a flat ranking.

For the synthetic family:

`A subset O`
`B subset O`
`O disjoint E`

and the atlas should be capable of reporting that M1-like and M3-like probes identify different but structurally related nodes in the hierarchy.

## 10. Identity in the atlas

Define an organizational feature F_l(t) at level l.

Token continuity is not equality of partitions across time. Instead require:

1. a lineage relation connecting successive realizations;
2. persistence of the level-defining relations within declared tolerance;
3. no unacknowledged branch or duplication event if numerical identity is being claimed;
4. selective robustness to nuisance or constituent substitution;
5. loss under destruction of the defining relations.

A trajectory:

`F_l(t0) -> F_l(t1) -> ... -> F_l(tn)`

constitutes organizational continuity only relative to its declared atlas coordinates.

## 11. What would count as evidence beyond CSH-001?

A future evidentiary result would need to show more than boundary recovery.

A strong result would look like this:

- a boundary probe recovers L3 on held-out systems;
- an intervention probe independently recovers L1 where predicted;
- D1 selectively erases L1 while sparing L3;
- D2 selectively erases L3 while sparing L1;
- null-calibrated signals outperform matched baselines where richer information should matter;
- label permutation and constituent-role controls leave the corresponding atlas features intact;
- the same preregistered mapping generalizes to a second generator family with different microscopic implementation.

That would support a theory of multiscale organizational recoverability. It would still not establish a new physical force or substrate.

## 12. Candidate future hypothesis shape — not yet authorized

A possible future hypothesis may eventually take the form:

> Preregistered probes targeted to distinct organizational levels will recover those levels above matched nulls, and level-specific interventions will selectively degrade the corresponding atlas features more than non-target levels, across held-out microscopic realizations.

This is only a candidate shape. It is not assigned CSH-002 until numerical thresholds, generator families, holdouts, nulls, and metric-to-target mappings are frozen independently of new outcome data.

## 13. Mandatory preregistration items before CSH-002

Before a new hypothesis identifier is allowed, freeze:

- generator family and hidden holdout family;
- level ontology and exact target partitions/coarse-grainings;
- metric-to-target commitment matrix;
- commensurability classes;
- selective-destruction interventions D1–D3;
- constituent and relabeling controls;
- null families N1–N5;
- simple baselines with equal information access;
- raw and null-calibrated score definitions;
- selectivity effect-size criteria;
- success/failure thresholds;
- random seeds or blind holdout-generation procedure;
- provenance graph identifying which design choices were motivated by CSH-001 postmortem findings.

## Foundation verdict

The Organizational Atlas replaces the failed idea that organization should reveal itself through universal same-partition convergence.

Its central object is a multiscale, task-indexed, null-calibrated map of organizational features and their selective causal fragility.

The critical experimental signature is not agreement everywhere. It is **correct localization and selective destruction**:

> the right probe finds the level it was designed to find, the right intervention destroys that level, and other levels survive when they should.

If this cannot be achieved under preregistered controls and held-out realizations, the atlas program should also be cut back rather than protected.

No CSH-002 is authorized yet.

Next: `FR–FOURCE–FORMAL–012 — The Atlas Kill Box: specify held-out generator families, decoys, nulls, and numerical selectivity criteria before freezing CSH-002.`
