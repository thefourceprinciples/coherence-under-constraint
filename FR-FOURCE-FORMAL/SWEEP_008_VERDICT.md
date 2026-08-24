# FR–FOURCE–FORMAL–008
## The Verdict Sweep
### First preregistered execution of CSH-001

Status: FIRST EVIDENTIARY RUN COMPLETE

Run: GitHub Actions run 32676070569, attempt 1
Frozen implementation SHA: `bb9d63da17bdd40b9be27a862307bf5cc907a9e7`
Artifact: `FR-FOURCE-FORMAL-007C-32676070569-attempt-1`
Artifact SHA-256: `5d23a360651430505315b20fec48dbe5f7934a8dedf37ba8b707c915dac5e63c`
Artifact size: 49,039,204 bytes
Preserved files: 307 including result checksum ledger

## Machine verdict

The first preregistered execution returned:

- P1: FAIL — structured systems exceeded matched-null convergence in only 1/30 paired seeds; median structured-minus-null convergence difference = -0.03886139817515447.
- P2: FAIL — planted O|E boundary recovered in the top 5% consensus in 12/30 seeds, below the preregistered 24/30 requirement and below the strong-falsification <=50% boundary.
- P3: PASS — relabeling invariance held within tolerance in 28/30 seeds.
- P4: PASS — constituent-replacement surrogate remained within the preregistered degradation tolerance in 30/30 seeds.
- P5: FAIL — relational rewiring produced the required >=20 percentile-point degradation in 0/30 seeds.
- P6: FAIL — rewiring degraded consensus more than constituent replacement in only 4/30 paired seeds.
- Simple coupling baseline: recovered the planted boundary in 30/30 seeds and positively discriminated structured from null systems in 30/30; conservative consensus positively discriminated in 26/30. The preregistered baseline-dominance strong-falsification condition therefore triggered.

Primary status: **STRONG_FALSIFICATION**.

## Integrity check

The workflow successfully:

- checked out the exact frozen implementation commit;
- verified a clean tracked tree;
- ran seeds 1000–1029 without deletion;
- preserved the structured, null, replacement, and rewired candidate tables and matrices;
- wrote the machine verdict before interpretation;
- hashed the preserved bundle and uploaded it as the first-run artifact.

After download, all 306 files listed in `RESULT_SHA256SUMS.txt` were independently rechecked successfully after normalizing the archive's original result-directory prefix. The GitHub artifact digest also matches the uploaded artifact metadata.

## What is falsified

The result falsifies **CSH-001 as preregistered on this bench**. In particular, the proposed cross-method convergence construction did not outperform its matched nulls and did not recover the planted organization reliably enough. It was also dominated by a much simpler coupling baseline.

The result does **not** establish that organization is unreal, that coarse-grained systemhood is always arbitrary, or that all possible formulations of CUC/Fource are false. Those are broader claims than CSH-001 tested.

No rescue of CSH-001 is permitted. Any revised hypothesis must be assigned a new identifier, use a new preregistration, and leave this result intact.

## Surviving observations

Two preregistered properties did survive:

1. Label invariance: P3 passed 28/30.
2. Constituent-replacement tolerance: P4 passed 30/30.

These are not sufficient to support CSH-001 because P1/P2 were primary gates and the coupling baseline dominated. They may, however, motivate narrower future questions if independently justified.

## Post-result diagnostic observations — not rescue claims

The preserved data show several important patterns worth attacking before any CSH-002 is proposed:

- median structured convergence was ~0.0212 while median null convergence was ~0.0653; the null systems therefore generated substantially more cross-family top-set agreement under the chosen convergence statistic;
- planted-boundary consensus percentile had median ~5.53%, narrowly missing the nominal top-5% boundary on average, but only 12/30 seeds actually entered the frozen top set;
- the simple coupling baseline placed the planted boundary at rank 1 in every structured seed (0.04914 percentile), showing that the generative architecture was detectable but the proposed consensus construction lost information relative to the trivial baseline;
- median replacement loss was ~+0.123 percentile points, consistent with P4 robustness;
- median rewiring loss was ~-1.744 percentile points, meaning the P5 perturbation generally improved rather than degraded the planted boundary's consensus rank; 29/30 rewiring losses were negative.

The last observation raises a post hoc design question: rewiring relationships wholly inside O may alter internal organization while leaving the O|E block boundary largely intact, so P5 may not be a well-targeted intervention for the specific planted boundary. This does not change the recorded failure of CSH-001. It is a candidate design issue to investigate only in a future, separately preregistered CSH-002.

## Foundation verdict

CSH-001 did what a useful scientific hypothesis must be allowed to do: it lost.

The first executable descendant of the Fource/CUC formalization was not supported by its own frozen test. The correct response is preservation, diagnosis, and subtraction—not threshold adjustment or metaphysical rescue.

The immediate next task is not to rerun 007C. It is a postmortem that asks why the conservative consensus underperformed nulls and simple coupling, whether the metrics were measuring genuinely distinct notions of systemhood, and whether any narrower hypothesis can be motivated before seeing new data.
