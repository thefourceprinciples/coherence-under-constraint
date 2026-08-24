# FR–FOURCE–FORMAL–009
## Failure Anatomy
### Why did Convergent Systemhood lose?

Status: POST-RESULT DIAGNOSTIC / NO RESCUE

Evidence source: preserved first-run artifact from GitHub Actions run `32676070569`, attempt 1.
Frozen implementation SHA: `bb9d63da17bdd40b9be27a862307bf5cc907a9e7`.
CSH-001 verdict remains: **STRONG_FALSIFICATION**.

This sweep asks why the preregistered construction failed. It does not alter any CSH-001 threshold, prediction, null, seed, metric, or verdict. Any future hypothesis must receive a new identifier and new preregistration.

## 1. The primary failure was metric conflict, not absence of planted structure

The planted O|E boundary was extremely visible to the boundary-separation metric M1:

- structured M1 planted rank median: 2
- structured M1 mean rank: 4.33
- structured M1 placed the planted boundary in the top 5% in 30/30 seeds

But the macro-dynamics family strongly rejected the same partition:

- M2 planted rank median: 1977.5 of 2035
- M5 planted rank median: 1371
- macro-family planted rank median: 1561.5
- macro family placed the planted boundary in the top 5% in 0/30 seeds

The interventional family was intermediate:

- M3 planted rank median: 112.5
- M3 placed the planted boundary in the top 5% in 12/30 seeds

Because the final consensus was the median of the three conservative family ranks, the very strong M1 signal was usually cancelled by the macro family's strong disagreement. The final planted consensus rank therefore had median 112.5 and entered the frozen top set in only 12/30 seeds.

Diagnostic conclusion: the consensus construction assumed that different notions of systemhood should rank the *same partition* highly. The bench itself did not justify that assumption.

## 2. The structured generator contained multiple organizational levels

The planted dynamics were not merely O versus E. They also contained strong internal modules:

- A = nodes 0–3
- B = nodes 4–7
- O = A + B
- E = nodes 8–11

Within A and B coupling was stronger than A–B coupling, while O–E coupling was weakest.

A post-result audit of the interventional metric found that its top-ranked partition separated A from B in **30/30 structured seeds**. In contrast, none of those top M3 partitions was the exact O|E boundary.

This means the interventional family was not simply failing to detect organization. It was consistently detecting a *different planted organizational level*.

The boundary metric M1 concentrated near O|E, while M3 concentrated on A|B. The macro family preferred still different coarse-grainings.

Diagnostic conclusion: CSH-001 operationalized systemhood as same-partition convergence in a generator that was already hierarchically organized. The test penalized disagreement that can arise when valid methods detect different levels of the same multiscale structure.

This does not rescue CSH-001. It identifies a mismatch between the hypothesis's same-partition convergence criterion and the structure of its own positive-control generator.

## 3. Why did nulls converge more?

Pairwise family-rank correlations were systematically higher in matched nulls than structured systems.

Median Spearman correlations across 30 seeds:

Structured:
- boundary vs macro: -0.0029
- boundary vs interventional: 0.2490
- macro vs interventional: -0.1667

Null:
- boundary vs macro: 0.2085
- boundary vs interventional: 0.4809
- macro vs interventional: 0.1015

Top-5% pairwise Jaccard overlap showed the same pattern.

Structured median overlap:
- boundary/macro: 0.0000
- boundary/interventional: 0.0489
- macro/interventional: 0.0089

Null median overlap:
- boundary/macro: 0.0108
- boundary/interventional: 0.1792
- macro/interventional: 0.0203

Thus P1 did not fail merely because the structured signal was weak. The structured system caused the three families to specialize in different organizational cuts, while the null produced more mutually correlated rankings.

One identified confound is partition geometry. In null systems, the macro family showed a strong preference for more balanced split sizes: median Spearman correlation between macro-family rank and distance from a 6|6 split was about 0.525. This shared geometric bias can create apparent convergence without corresponding to planted organization.

Diagnostic conclusion: cross-method agreement is not automatically evidence of systemhood. Different methods can agree because of common representation geometry or other shared nuisance structure. The original convergence statistic did not sufficiently distinguish agreement-on-organization from agreement-on-bias.

## 4. Why did the simple coupling baseline win?

The coupling baseline placed the planted O|E boundary at rank 1 in all 30 structured seeds and positively discriminated structured from matched nulls in all 30 pairs.

That result is unsurprising in hindsight: the synthetic generator defined O|E primarily through a deliberately large contrast between within-O and O–E coupling strengths. A baseline with direct access to the interaction matrix therefore had a near-direct view of the generative ground truth.

The conservative consensus attempted to infer a broader notion of organization from predictive, interventional, boundary, retention, and robustness behavior. On this generator, that additional machinery discarded rather than added discriminative information.

Diagnostic conclusion: CSH-001 did not establish value beyond the simplest sufficient statistic of the planted architecture. Any future bench must distinguish at least two questions:

1. Can the planted boundary be recovered?
2. Does a richer systemhood formalism add information that a simple generative statistic does not already contain?

The first bench conflated them.

## 5. P5 attacked internal organization while preserving the tested boundary

P5 rewired 40% of relationships wholly *inside O* while leaving the O|E separation structurally intact.

Observed outcome:

- P5 required >=20 percentile-point degradation in 24/30 seeds
- observed count: 0/30
- median rewiring loss: approximately -1.744 percentile points
- 29/30 rewiring losses were negative, meaning the planted O|E consensus rank usually improved

The post-result metric audit explains part of this. After rewiring:

- M1 planted median rank remained 3
- M3 planted median rank improved from 112.5 to 66
- macro-family planted rank remained poor
- final consensus median rank improved from 112.5 to 66

The intervention changed internal A/B organization without directly breaking the O/E boundary. It therefore need not make O|E less identifiable and can even suppress internal multiscale competition, making O|E comparatively easier for some metrics to rank.

Diagnostic conclusion: P5 was not a clean destruction test for the particular O|E identity being scored. A future boundary-destruction intervention would need to alter O–E coupling or otherwise erase the defining relation of the target boundary.

Again, this is a design diagnosis, not a retroactive reinterpretation of P5. P5 remains failed.

## 6. What P3 and P4 actually tell us

P3 passed in 28/30 seeds. This supports a narrow implementation property: the constructed ranking was mostly invariant under isomorphic relabeling.

P4 passed in 30/30 seeds. The replacement surrogate changed node-local biases after the midpoint while preserving relational roles and W. The planted boundary remained stable under that perturbation.

However, P4 should not be inflated into a general result about matter replacement. It is a synthetic local-bias surrogate, not physical constituent substitution. Its scientific meaning is limited to the implemented model.

## 7. CSH-001 failed for at least four separable reasons

### F1 — Same-partition convergence was too strong
Different metrics targeted different legitimate organizational scales.

### F2 — Metric families were not commensurable
Boundary separation, predictive compression, intervention structure, retention, and robustness were treated as if they were alternative measurements of one latent variable. The run shows they were not.

### F3 — Null convergence was contaminated by shared nuisance structure
Metric agreement in nulls can arise from common partition geometry and residual dependence rather than organization.

### F4 — The relational-damage intervention was target-mismatched
Internal-O rewiring changed internal organization without destroying the O|E relation used as the recovery target.

These four diagnoses are compatible and need not be reduced to one cause.

## 8. What we are not allowed to conclude

The failure does not justify:

- changing the CSH-001 threshold from top 5% to top 6%;
- emphasizing the planted median percentile of ~5.53% as a near-pass;
- deleting seeds;
- replacing the null after seeing the result;
- dropping the macro family because it behaved badly;
- redefining P5 after the fact;
- declaring P3/P4 the 'real' hypothesis;
- appealing to a deeper hidden Fource to override the bench.

All such moves would be rescue inflation.

## 9. What genuinely survives the postmortem

The run supports three methodological lessons rather than CSH-001 itself:

1. **Systemhood may be multiscale.** Different operational probes can reproducibly identify different levels of one structured generator.
2. **Agreement requires a null for agreement itself.** Cross-method convergence can be generated by shared biases and must not be treated as independent corroboration by default.
3. **Perturbations must target the identity-defining relation.** Internal change cannot be assumed to destroy an external boundary.

These are diagnostic observations from CSH-001 and must be independently formalized before becoming predictions.

## 10. CSH-002 is not yet authorized

The next step should not be to immediately rewrite the hypothesis around the observed result.

Before any CSH-002 preregistration, the project should perform a design-neutral reconstruction with three tasks:

- identify which metric families are theoretically expected to agree at the same scale and which are expected to detect different scales;
- construct a multiscale ground-truth generator where A, B, O, and E are separately labeled as legitimate organizational targets before analysis;
- define destruction interventions that selectively erase A/B organization, O/E organization, or both.

Only after those choices are specified independently of new outcome data should a new hypothesis be frozen.

## Foundation verdict

CSH-001 did not fail because the planted system was invisible. It failed because the proposed **convergence operator was not a valid universalizer of the different organizational signals present in the bench**.

The most important positive-control fact is almost the inverse of the original hypothesis: the structured system produced *more disagreement* among methods because different methods locked onto different levels of its hierarchy, while the null made the methods more mutually correlated.

That is not evidence for Fource. It is a warning that multiscale organization cannot be tested by demanding naive same-partition consensus.

Next: `FR–FOURCE–FORMAL–010 — The Null Reconstruction After Failure: What Would We Build If We Had Never Invented CSH-001?`
