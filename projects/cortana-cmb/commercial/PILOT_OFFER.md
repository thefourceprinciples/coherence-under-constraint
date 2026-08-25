# GardenCore Sensor Audit — Pilot Offer v0.1

GardenCore audits whether an engineering sensor system can actually distinguish the faults, parameters, or hidden states it is supposed to observe — and recommends the next measurement or sensor location that most reduces uncertainty.

## Best first customers
- industrial machinery test teams
- vibration / condition-monitoring engineers
- OEM R&D labs
- reliability teams with existing sensor data or simulation models
- university / contract engineering labs

## Customer provides
At least one of:
1. sensitivity / Jacobian matrix
2. finite-element or reduced-order model
3. mode shapes + frequencies
4. labeled experimental sensor dataset
5. forward simulator plus candidate sensor locations

Plus target faults/parameters, known sensor noise or repeatability, placement constraints, and relevant cost limits.

## GardenCore returns
1. Blind Spot Map
2. Recoverability Report
3. Global Ambiguity Flags
4. Obstruction / Model-Class Flags
5. Sensor Value Ranking
6. Configuration Tradeoff Map
7. Provenance Ledger
8. Executive Recommendation

## Pilot success criteria
A pilot succeeds only if GardenCore demonstrates at least one of:
- identifies a blind spot missed by the current sensor plan
- predicts a verifiable ambiguity
- recommends a lower-cost set with comparable recoverability
- recommends an added measurement that materially reduces posterior uncertainty
- improves held-out fault reconstruction/detection against the customer baseline

## Initial pilot pricing
Starter Audit — $1,500
- one asset/model
- up to 20 candidate measurements/sensors
- blind-spot + conditioning audit
- one placement recommendation
- concise technical report

Engineering Pilot — $4,500
- one asset family or richer model
- up to 100 candidate measurements
- noise-aware Fisher analysis
- global ambiguity screening where tractable
- candidate configuration comparison
- held-out/simulated validation
- technical report + review call

Custom / Enterprise Proof — scoped

Pricing is initial pilot pricing, not validated market pricing.

## Evidence boundary
GardenCore has passed controlled mathematical, simulation, and adversarial benches. It has not yet established superiority on customer field data. The commercial pilot is explicitly designed to test that claim.
