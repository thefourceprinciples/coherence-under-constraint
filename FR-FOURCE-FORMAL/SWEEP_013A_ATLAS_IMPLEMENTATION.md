# FR–FOURCE–FORMAL–013A
## Build the Atlas
### Design-only implementation before calibration

Status: IMPLEMENTATION / DESIGN SEEDS ONLY / NON-EVIDENTIARY

This transition implements the frozen Sweep 013 contract without executing calibration seeds 3000–3029 or held-out seeds 4000–4029.

## Implemented

- dedicated branch `fr-fource-formal-013a` from `fr-fource-formal`;
- frozen JSON registry for design/calibration/held-out seed classes;
- executable firewall that refuses any non-design seed in 013A;
- deterministic G1–G6 generator constructors;
- explicit generator truth/level manifests and decoy declarations;
- Q-BND, Q-TMP, Q-INT, Q-RET, and Q-PERT license registry with information access, baselines, nulls, and decoys;
- N1–N5 semantic null registry;
- X1–X5 plus XC1/XC2 intervention audit skeletons;
- preservation-report outputs for every intervention rather than assuming selectivity;
- design-output manifests clearly stamped `DESIGN_ONLY_NON_EVIDENTIARY`;
- tests rejecting calibration and held-out seed access and checking generator determinism/G6 absence of planted positive truth.

## Scientific boundary

013A does not establish that any probe is valid. The generator implementations and intervention transformations must be adversarially reviewed before calibration. In particular, the current intervention code emits design-stage preservation summaries; exact preservation tolerances are not inferred from design outcomes and must be frozen before calibration interpretation.

No calibration seed or held-out seed has been intentionally executed as part of this transition.

## GitHub housekeeping

Historical PR #6 for the CSH-001 implementation was closed as stale/non-mergeable after its frozen SHA had already been executed and preserved in run 32676070569. Closing it does not alter the CSH-001 result or provenance.

## Next gate

1. run CI/design-only smoke checks on 013A;
2. adversarially review G1–G6 semantics, target licenses, null implementations, and selective interventions;
3. fix implementation defects using design seeds only;
4. freeze a calibration-ready SHA;
5. only then authorize a separate calibration run on 3000–3029.

CSH-002 remains unfrozen and held-out execution remains prohibited.
