# FR–FOURCE–FORMAL–007B
## Verification and First-Run Readiness

Status: IMPLEMENTATION VERIFICATION — NOT EVIDENCE
Date: 2026-08-23

## Purpose

Sweep 007B prevents implementation defects from being mistaken for scientific outcomes. It audits 007A against the frozen Sweep 007 preregistration before any full evidentiary run.

## CI finding

The first implementation CI run failed at partition-space validation because the workflow installed `requirements-dev.txt` but not `requirements.txt`; NumPy was unavailable at runtime. Repository validation and Python compilation had passed. This was an infrastructure defect, not a CSH-001 result.

Correction: validation now installs both development and runtime requirements.

## Alignment findings

Two substantive preregistration-to-code mismatches were identified before any full run:

1. P3 was described in the implementation PR but 007A left P3 unexecuted (`pass: None`).
2. P4 simulated the entire condition under the replacement bias rather than introducing the replacement at retained t=10,000 and evaluating the post-change segment.

Because these were discovered before the first full run, correcting them does not alter an observed scientific result and does not violate the non-rescue rule.

## 007B corrections

`experiments/fr_fource_formal_007b.py` now:

- executes P3 using an isomorphic node permutation and scores the permuted planted partition;
- permutes trajectory columns and the weight matrix consistently;
- applies the P4 node-local bias replacement at the retained-trajectory midpoint;
- evaluates P4 on the post-change half of the continuous trajectory;
- records resampled external observation labels as provenance metadata rather than dynamical variables;
- fixes the preregistered simple-coupling strong-falsification comparison before the first full run;
- leaves every P1–P6 numerical threshold unchanged.

## Strong-falsification baseline operationalization

The frozen preregistration required strong falsification if simple coupling equals or exceeds conservative consensus on both boundary recovery and structured-vs-null discrimination, but did not fully specify that comparison statistic.

Before any full run, 007B fixes:

- boundary recovery = count of seeds where planted O|E is top 5% under coupling, compared with P2 consensus recovery count;
- discrimination = count of paired seeds where planted O|E coupling-rank percentile is better in structured than matched-null dynamics, compared with the analogous consensus percentile discrimination count.

If coupling equals or exceeds consensus on both counts, baseline-dominance strong falsification triggers.

This interpretation is now frozen before the first full run.

## Smoke-test boundary

CI runs 007B with `--smoke` using the predeclared reduced smoke configuration. Smoke output must report `NOT_EVIDENCE` and cannot pass, fail, support, or falsify CSH-001.

Smoke verifies imports, dependencies, all 2,035 candidate partitions, P1–P6 code paths, P3/P4 provenance artifacts, append-only writing, and termination without implementation exceptions.

## First-run readiness gate

The full preregistered run may begin only after:

1. CI passes repository validation and Python compilation;
2. partition validation reports exactly 2,035 candidates and exactly one planted O|E candidate;
3. corrected 007B smoke completes as NON-EVIDENTIARY;
4. no known mismatch remains between frozen preregistration and authoritative runner;
5. exact implementation commit SHA is recorded before execution.

## Scientific status

No CSH-001 prediction has been tested by this sweep.

Allowed: the implementation has undergone an explicit preregistration-alignment audit.

Not allowed: CSH-001 is supported/falsified; convergent systemhood or Fource has been detected; smoke output has evidentiary value.

## Decision

Do not open Sweep 008 until a first full append-only run exists.

007B verification -> passing CI/smoke gate -> freeze implementation SHA -> full preregistered execution -> Sweep 008 verdict.
