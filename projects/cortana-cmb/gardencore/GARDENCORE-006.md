# GARDENCORE-006 — Local Truth Is Not Global Truth

Goal: extend GardenCore beyond local Jacobian/Fisher analysis into global inverse-problem reasoning.

## Forward map
`F(x,y) = (x^2-y^2, 2xy)`

Jacobian determinant:
`det J = 4(x^2+y^2)`

The Jacobian is full-rank everywhere except the origin, so the map is locally invertible almost everywhere.

But globally:
`F(z) = F(-z)`

Therefore every nonzero observation has a two-branch inverse fiber.

## Bench
Truth is randomly chosen between `z=(0.8,-0.6)` and `-z` with equal probability.

Candidate extra measurements include:
- a high-local-information but sign-symmetric measurement `g_sym=5(x^2+y^2)`
- branch-separating measurements such as `g_x=x`

The local Fisher-only policy selects `g_sym` because it has the largest derivative information, but `g_sym(z)=g_sym(-z)` and thus has zero global branch-separation power.

A global-aware policy scores candidate measurements by separation of surviving inverse branches and selects `g_x=x`.

## Results
Monte Carlo trials: 2000.

Mean reconstruction error:
- local Fisher policy ≈ 1.0154
- global-aware policy ≈ 0.0127

Branch identification accuracy:
- local Fisher policy ≈ 49.5%
- global-aware policy = 100.0%

## Verdict
- full-rank local Jacobian guarantees global uniqueness: FAIL
- local Fisher information alone guarantees a useful next measurement: FAIL
- explicit global fiber analysis detects the ambiguity: PASS
- branch-separating measurement design improves branch identification: PASS
- branch-separating measurement design improves mean reconstruction: PASS

## Architectural update
GardenCore now requires four distinct layers:
1. local observability — Jacobian rank/kernel/singular spectrum
2. statistical recoverability — Fisher information/noise/posterior uncertainty
3. global identifiability — inverse fibers, branch multiplicity, topology
4. obstruction analysis — whether approximation/refinement can close the remaining defect

This sweep is the bridge into the planned nonsofic obstruction bench.
