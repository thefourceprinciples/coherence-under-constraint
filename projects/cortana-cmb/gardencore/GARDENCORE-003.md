# GARDENCORE-003 — Real-World Escalation

Structural-dynamics proxy with higher dimension, partial sensing, sparse damage, and measurement noise.

## System
- 10 DOF mass-spring chain
- 11 hidden spring-stiffness parameters
- first 6 modal frequencies
- partial mode-shape sensing at 4 DOFs over 4 modes
- sparse two-spring damage
- additive measurement noise

## Local observability
Frequency-only:
- rank = 6
- kernel dimension = 5
- condition number ≈ 6.342

Mode-shape-only:
- rank = 11
- kernel dimension = 0
- condition number ≈ 6.66e10

Combined:
- rank = 11
- kernel dimension = 0
- condition number ≈ 8.233

## Noisy reconstruction
Best ridge reconstruction L2 error:
- frequency-only = 0.0727
- combined = 0.0789

## Verdict
- scaling from toy 4-DOF to noisier 10-DOF structural inverse problem: PASS
- frequency-only sensing remains underdetermined: PASS
- complementary mode-shape sensing removes local kernel: PASS
- combined sensing improves reconstruction error: FAIL in this realization
- GardenCore diagnostics remain useful at larger scale: PASS
- real-world field superiority: NOT ESTABLISHED; this is a realistic simulation proxy, not measured field data

## Key lesson
Identifiability and estimation quality are different. An added channel can eliminate an exact kernel while worsening noisy reconstruction when weighting, model mismatch, or regularization are not optimal. GardenCore must therefore track observability, conditioning, noise weighting, and reconstruction error separately rather than treating kernel collapse as sufficient evidence of practical improvement.
