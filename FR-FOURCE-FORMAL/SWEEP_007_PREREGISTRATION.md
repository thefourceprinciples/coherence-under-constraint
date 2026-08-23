# FR–FOURCE–FORMAL–007
## The CMB-Style Bench: Preregistered Convergent-Systemhood Falsification Test

Status: PREREGISTERED DESIGN — DO NOT ALTER PRIMARY THRESHOLDS AFTER FIRST RESULT RUN
Date: 2026-08-23

## 1. Target hypothesis

CSH-001: Dynamically organized systems will produce greater agreement among methodologically nonredundant system-identification procedures than matched null systems, and this agreement will preferentially track organizational architecture rather than microscopic constituent identity.

This bench tests recoverable organizational structure. It does not test a new force, field, substance, aether, dark component, or fundamental ontology.

## 2. Primary synthetic system

Use 12 binary nodes with synchronous stochastic updates.

Ground-truth blocks:
- A = nodes 0–3
- B = nodes 4–7
- E = nodes 8–11

Target organizational partition:
- O = A ∪ B = nodes 0–7
- environment = E = nodes 8–11

Update rule for node i:

p(x_i(t+1)=1) = sigmoid(b_i + sum_j W_ij (2 x_j(t)-1))

Base weights:
- within A: +1.20
- within B: +1.20
- A <-> B: +0.70
- O <-> E: +0.15
- within E: independently drawn once per seed from Uniform(-0.20, +0.20)
- self edges: 0
- biases: 0

All edge values receive independent Gaussian jitter N(0, 0.05) once at generator construction. Randomness must be seeded.

Simulation:
- burn-in: 1,000 steps
- retained trajectory: 20,000 steps per replicate
- replicates per condition: 30
- master seeds: integers 1000–1029

## 3. Matched null

For each structured replicate construct a degree/weight-distribution matched null by permuting the destinations of nonzero directed edges while preserving each source node's outgoing multiset of weights. Reject and redraw a null if it accidentally reproduces the planted O|E partition exactly.

The null is allowed to score highly. No post hoc null weakening is permitted.

## 4. Candidate partition space

Primary search space: every nontrivial binary partition of 12 nodes modulo complement symmetry, excluding singleton-vs-rest partitions.

Canonical representation: the side containing node 0 is listed first.

The planted O|E partition is one candidate but is not supplied to any metric as privileged information.

Nested exploratory partitions may be evaluated after the primary binary test, but they cannot rescue a failed primary test.

## 5. Five metric families

Each metric produces a ranking over candidate partitions. All metrics are normalized only for reporting; primary convergence uses ranks.

### M1 — Boundary separation

Estimate one-step conditional mutual information across the proposed boundary and within each side. Prefer partitions with high within-side dependence and low residual cross-boundary dependence. Estimator and pseudocount must be fixed before execution.

### M2 — Predictive compression

For each partition, compress each side to its binary majority macrostate. Fit a first-order empirical Markov predictor on 70% of the retained trajectory and score held-out 30% negative log loss for predicting the two macrostates. Penalize representation size equally across candidates because all primary candidates produce two binary macrostates. Prefer lower held-out loss.

### M3 — Interventional/causal separation

Using the known simulator only, perform single-node do-interventions at t on each node (forced 0 and forced 1, balanced) and measure the Jensen-Shannon divergence of t+1 response distributions within versus across candidate sides. Prefer partitions with stronger within-side than cross-side intervention effects.

### M4 — Viability / macrostate retention

Define the candidate macrostate as the pair of side-majorities. Estimate the probability that this macrostate remains unchanged over the next 3 steps under baseline stochastic evolution. Prefer higher retention after matching for marginal macrostate frequency.

This is an operational retention metric, not a claim that persistence equals biological viability.

### M5 — Perturbational robustness

Add independent Gaussian perturbations to all weights at sigma = 0.05, 0.10, 0.20, generating 20 perturbed copies per replicate. Recompute the candidate's macro transition matrix. Score inverse Jensen-Shannon divergence from its unperturbed macro transition matrix. Prefer higher stability.

## 6. Method-dependence ledger

Before interpreting agreement, record shared dependencies:

- M1 and M2: observational trajectory dependence; no simulator interventions.
- M3: simulator/intervention dependence; structurally distinct evidence source.
- M4: observational dynamics and chosen majority macrostate.
- M5: simulator perturbations and chosen majority macrostate.

M2, M4, and M5 share the same majority coarse-graining and therefore are not three independent witnesses.
M1 and M2 share trajectory data.
M3 is the strongest independence anchor in the primary bench.

Primary results must report raw five-way agreement and a conservative family-level agreement where {M2,M4,M5} counts as one macro-dynamics family, M1 as one statistical-boundary family, and M3 as one interventional family.

No claim of five independent corroborations is allowed.

## 7. Primary convergence statistics

For each replicate:

1. Compute each metric's rank for the planted O|E partition.
2. Record whether O|E is in each metric's top 5% of candidate partitions.
3. Compute top-5% set overlap among metric families using mean pairwise Jaccard overlap.
4. Compute Kendall rank concordance among metric-family rankings.
5. Compute a consensus rank by median rank across the three conservative families; this is a descriptive aggregator, not a new physical scalar.

## 8. Preregistered primary predictions

P1 — Structured-vs-null convergence:
The median conservative-family top-set Jaccard convergence across structured replicates must exceed matched null convergence in at least 24 of 30 paired seeds, and the paired median difference must be > 0.05.

P2 — Boundary recovery:
The planted O|E partition must lie in the top 5% consensus ranks in at least 24 of 30 structured replicates.

P3 — Constituent/label invariance:
After a random node relabeling with dynamics permuted isomorphically, mapping the recovered partition back through the inverse permutation must preserve its consensus rank within ±2 percentile points in at least 27 of 30 replicates.

P4 — Constituent replacement surrogate:
At t=10,000, independently resample node-local biases and observation labels while preserving W's relational role structure. The planted partition's post-change consensus percentile must degrade by <10 percentile points in at least 24 of 30 replicates.

P5 — Relational rewiring sensitivity:
Randomly rewire 40% of edges internal to O while preserving the global weight multiset. The planted partition must lose at least 20 consensus percentile points relative to baseline in at least 24 of 30 replicates.

P6 — Replacement vs rewiring contrast:
For at least 24 of 30 paired seeds, relational rewiring must degrade planted-boundary consensus more than the constituent-replacement surrogate.

## 9. Secondary predictions

These are preregistered but do not independently establish CSH-001.

S1 — Observation degradation:
At 75%, 50%, and 25% randomly retained time points, recovery should degrade monotonically in aggregate; failure of strict monotonicity in individual seeds is allowed.

S2 — Nested generator:
A separate hierarchical generator with strong A/B substructure and weaker A<->B coupling may return both A|rest/B|rest and O|E-like nondominated partitions. No unique winner is required.

S3 — Coupling confound:
A decoy generator with strong cross-boundary raw coupling but interventionally separable macro-organization should prevent simple mean absolute coupling from matching the full conservative-family consensus.

## 10. Explicit failure rules

### CSH-001 primary failure

CSH-001 fails this bench if either P1 or P2 fails.

### Strong falsification

Record STRONG FALSIFICATION if:
- structured systems do not exceed matched null convergence by P1; OR
- the planted boundary is recovered at or below 50% of replicates; OR
- a simple coupling-strength baseline equals or exceeds conservative-family consensus on both boundary recovery and structured-vs-null discrimination.

### Partial failure

If P1 and P2 pass but P3 or P6 fails, the claim must be narrowed: convergence may detect structure but not representation/constituent-independent organizational identity.

### Non-rescue rule

No failed preregistered prediction may be rescued by changing thresholds, redefining the planted organization, removing unfavorable seeds, weakening the null, adding a new metric, or appealing to hidden/deeper coherence. Any revised hypothesis becomes CSH-002 and requires a new preregistration and untouched test data.

## 11. Baselines

Required baselines:
- mean absolute coupling modularity/rank
- observational correlation modularity/rank
- random partition ranking

CSH-001 is not interesting if the proposed convergence procedure merely reproduces a single simple coupling statistic.

## 12. Reporting

Preserve for every run:
- configuration JSON
- git commit SHA
- Python/package versions
- seed
- generated W matrix
- null W matrix
- all candidate metric scores
- all ranks
- baseline scores
- perturbation outputs
- summary CSV/JSON
- failures/exceptions

Raw results are append-only. Never overwrite the first preregistered run.

## 13. Claims boundary before execution

Allowed now:
- CSH-001 is falsifiable under this bench.
- The bench tests cross-method recovery of planted organization against matched nulls.
- The metrics are only partially independent and their dependency structure is explicitly recorded.

Not allowed now:
- CSH-001 is supported.
- Fource has been detected.
- convergent systemhood is a new law of physics.
- recovered organization is ontologically fundamental.

## 14. Prior-art pressure identified during preregistration

The bench is not the first attempt to identify systems or causal boundaries from dynamics. Existing work searches hypothetical partitions for organizational closure and nested individuality, Markov-blanket approaches identify statistical partitions, causal representation learning addresses identifiability from trajectories, and multi-objective/Pareto methods already exist in system identification. Therefore novelty, if any, must lie in the specific preregistered cross-method falsification architecture and its independence/provenance controls, not in the generic idea of system identification, partition search, or Pareto analysis.

## 15. Decision after first run

Do not write the Results, Discussion verdict, or Fource interpretation until the frozen bench has executed.

Possible outcomes:
- PASS: P1 and P2 pass; report remaining prediction outcomes separately.
- PARTIAL: P1/P2 pass but invariance/contrast controls fail.
- FAIL: P1 or P2 fails.
- STRONG FALSIFICATION: one of the strong-falsification conditions is met.

The result determines Sweep 008. The theory does not determine the result.