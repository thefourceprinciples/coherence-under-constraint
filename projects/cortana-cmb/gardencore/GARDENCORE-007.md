# GARDENCORE-007 — Nonsofic Obstruction Bench

Goal: integrate the recent nonsofic-style obstruction logic into GardenCore without making unsupported claims about actual nonsofic groups.

## Epistemic boundary
This bench is **not** a proof or construction of a nonsofic group. The existence of nonsofic groups remains an open problem. The test is the more general engineering question: given a specified approximation class and defect functional, does refinement drive the defect to zero or does a positive class-relative floor remain?

## Controlled Fourier target
`f(x) = sin(x) + 0.60 cos(3x) - 0.35 sin(5x) + 0.25 cos(17x)`

Two refinement sequences are compared.

### Closable sequence
Allowed Fourier modes are `1..n`.
Once mode 17 enters, the target becomes exactly representable.

Final L2 defect at n=40:
`~1.27e-15`

### Obstructed sequence
Allowed modes are `1..n` except mode 17 is permanently forbidden.
All other refinement is allowed, but the missing `cos(17x)` component cannot be represented.

Known L2 obstruction floor:
`0.176777`

Final L2 defect at n=40:
`0.176777`

Relative floor:
`~0.2011` of target L2 norm.

## Controlled matrix obstruction
Target operator: `diag(1,1,0.4)`.
Approximation class forces the third diagonal action to zero. Irrelevant refinement cannot reduce the spectral-norm defect below `0.4`.

## Verdict
- decreasing defect alone proves eventual closure: FAIL
- refinement can saturate at a positive defect floor: PASS
- GardenCore can distinguish approximation error from class obstruction when the admissible class is explicit: PASS
- a persistent floor must be interpreted relative to the chosen approximation class: PASS
- a positive synthetic obstruction floor establishes mathematical nonsoficity: FAIL / explicitly not claimed

## Architectural update
GardenCore's obstruction layer should record:
1. approximation class `A_n`
2. defect functional `Delta_n`
3. refinement rule
4. asymptotic/tail behavior
5. known invariants or forbidden directions
6. whether the observed floor is class-relative, numerical, or theorem-level

This adds a fourth diagnostic layer above local observability, statistical recoverability, and global identifiability: **approximation closure / obstruction**.
