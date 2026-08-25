# GardenCore CASE–001 — Real Fan Vibration Sensor Audit

## Dataset
UCI Accelerometer dataset (Sampaio et al., 2019; DOI 10.24432/C5Q61V).
Raw data: 153,000 accelerometer samples.
Physical design: 3 fan rotor-weight configurations x 17 operating speeds x 3,000 samples.

## Pre-registered benchmark
Target: `wconfid` (three physical configurations).
Control/nuisance: `pctid` operating speed.
Windowing: non-overlapping 100-sample windows inside each configuration-speed block.
Windows: 1,530.
Features per axis: mean, standard deviation, RMS, mean absolute magnitude, peak-to-peak, skewness, kurtosis, crest factor.
Validation: leave-one-speed-out (17 folds).
Classifier: fixed standardized logistic regression for every sensor configuration.
Compared: speed-only, X, Y, Z, XY, XZ, YZ, XYZ.

## Primary result
- XYZ mean balanced accuracy: 82.6%
- best reduced configuration YZ: 79.5%
- gap vs XYZ: 3.1 percentage points
- best single axis Y: 75.5%
- speed-only control: 33.3% (chance)

Pre-registered reduced-sensor equivalence rule: within 2 percentage points of XYZ.
Result: **FAIL**. No reduced configuration met that threshold.

## GardenCore diagnostic reading
- Y is the strongest single axis by held-speed accuracy and feature mutual information.
- Adding Z to Y raises mean accuracy from 75.5% to 79.5%.
- Full XYZ adds another ~3.1 points.
- Redundancy is incomplete: the third axis cannot be removed without measurable average loss under this protocol.
- Performance remains speed-sensitive; XYZ fold SD is ~0.140.
- Held-out 30% fan speed is the clearest blind spot, with XYZ balanced accuracy ~51.1%.

## Paired held-speed comparison against XYZ
- XYZ vs X: +16.9 points mean advantage; XYZ better in 14/17 folds; Wilcoxon p=0.0024
- XYZ vs Y: +7.1 points; XYZ better in 10/17 folds; p=0.0663
- XYZ vs Z: +15.6 points; XYZ better in 16/17 folds; p=0.00035
- XYZ vs XY: +3.7 points; 8 wins / 1 tie / 8 losses; p=0.2445
- XYZ vs XZ: +9.1 points; XYZ better in 14/17 folds; p=0.00665
- XYZ vs YZ: +3.1 points; 10 wins / 3 ties / 4 losses; p=0.0958

## Per-class recall
Y:
- config 1: 78.2%
- config 2: 61.2%
- config 3: 87.1%

YZ:
- config 1: 77.5%
- config 2: 70.4%
- config 3: 90.6%

XYZ:
- config 1: 76.7%
- config 2: 79.0%
- config 3: 92.2%

## Commercial claim outcome
Claim: GardenCore can identify a cheaper reduced sensor set matching the full three-axis baseline.
CASE–001 result: **NOT SUPPORTED** under the preregistered 2-point equivalence threshold.

Claim: GardenCore can rank sensor channels, quantify sensor-removal loss, identify operating-regime fragility, and preserve negative results on real measured vibration data.
CASE–001 result: **SUPPORTED**.

## Scope
This is one public physical fan experiment and one fixed feature/model protocol. It does not establish superiority over dedicated industrial condition-monitoring systems. It is the first empirical case study, not a general validation.
