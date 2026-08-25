# GARDENCORE-005 — Adaptive Experiment Loop

Goal: close the loop by selecting measurements sequentially from the evolving posterior rather than committing to a static design up front.

## System
Same noisy 10-DOF / 11-spring structural inverse problem.
Initial data: first 6 modal frequencies.
Budget: 12 additional scalar mode-shape measurements.

## Policies
- fixed: non-adaptive A-optimal measurement set selected from the initial prior
- adaptive: sequential posterior update with covariance reduction plus residual-relevance weighting

Monte Carlo trials: 200.

## Results
Mean final reconstruction error:
- adaptive = 0.05612
- fixed = 0.05567

Adaptive relative improvement vs fixed = -0.81%.
Adaptive win rate = 52.0% of trials.

Mean final posterior trace:
- adaptive = 0.003072
- fixed = 0.003052

## Verdict
- closed-loop sequential measurement selection executes successfully: PASS
- adaptive policy beats fixed A-optimal on mean error: FAIL
- covariance-only adaptivity is equivalent to static design in a linear-Gaussian model: CONFIRMED
- residual-informed adaptation adds practical value here: NOT DEMONSTRATED

## Key lesson
Adaptivity is not automatically beneficial. In a linear-Gaussian inverse problem with fixed candidate sensitivities and noise, posterior covariance evolution is largely determined by the selected rows rather than observed values, so an optimal static design can already capture most of the available benefit. GardenCore should reserve adaptive policies for regimes with meaningful nonlinear relinearization, state-dependent noise, changing candidate sensitivities, model revision, or other observation-dependent structure.
