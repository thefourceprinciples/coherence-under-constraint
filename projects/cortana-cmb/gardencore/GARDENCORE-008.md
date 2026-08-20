# GARDENCORE-008 — Unified CUC/Fource Operator

Goal: reconnect the executable GardenCore benches to the wider Garden without collapsing heterogeneous diagnostics into an unjustified universal scalar.

## Core decision
Do **not** define one universal coherence number.

Define a typed constrained-transformation record and a diagnostic vector:

`Q = (L, S, G, O)`

where:
- `L` = local observability loss
- `S` = statistical fragility
- `G` = global ambiguity
- `O` = approximation obstruction

Lower is better in each coordinate, but the coordinates are not assumed commensurable.

## Comparison rule
Use componentwise partial order / Pareto dominance unless a domain supplies an explicit justified utility function.

This preserves tradeoffs already observed in the benches. For example, LATENT A+B reduces the kernel relative to LATENT A but worsens conditioning, so neither dominates the other under the local/statistical coordinates.

## Typed object
A UnifiedDiagnostic record should contain:

### carrier
- hidden space
- observable space
- forward map
- constraints

### local
- Jacobian/operator
- rank
- kernel
- singular spectrum

### statistical
- noise model
- Fisher information
- posterior covariance

### global
- inverse fibers
- branch multiplicity
- branch separation

### obstruction
- approximation class
- defect functional
- refinement rule
- asymptotic floor
- floor status

### provenance
- assumptions
- evidence class
- failure modes
- inherited dependencies

## Garden mapping
- CUC: constrained carrier/transform/survival structure
- Fource: interpretive relational-coherence layer over changes in the diagnostic record; not identified with a scalar
- CHH: threshold/boundary questions across diagnostic coordinates
- CAS: claim, evidence, assumption, provenance, and classification discipline
- KOS: dependency and relation graph
- Chronovisor: reconstruction workflow over forward maps, inverse fibers, uncertainty, obstruction, and provenance

## Claim status
- one typed schema can represent diagnostics exercised in GARDENCORE-001 through 007: PASS
- a single universal scalar is justified: FAIL
- Pareto/partial-order comparison preserves observed tradeoffs: PASS
- CUC/Fource are mathematically proven equivalent to GardenCore: FAIL / not claimed
- GardenCore operationalizes selected CUC/Fource questions in executable form: PROVISIONAL PASS

## Design principle
The framework should preserve distinctions rather than erase them through premature scalarization. Domain-specific utility functions may be added later, but their weights and assumptions must be explicit and provenance-tracked.
