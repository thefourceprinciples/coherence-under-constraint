# GardenCore Sensor Audit — Sales Launch 001

## Offer
GardenCore Sensor Audit is a model-and-data audit for vibration and condition-monitoring systems.

Core question: **Are your sensors actually preserving the diagnostic information you think they are?**

GardenCore does not replace a vibration analyst or claim to predict every machine fault. It audits the sensing/inference pipeline and reports:
- weak or redundant channels
- operating-regime blind spots
- sensitivity to representation and feature choice
- loss from removing measurements
- complementary channel value
- uncertainty / conditioning where model structure permits
- provenance and explicit negative results

## Evidence
### CASE-001 — raw observation baseline
On the UCI Accelerometer physical fan experiment, isolated raw acceleration samples produced near-chance condition classification. A two-axis XZ representation slightly exceeded XYZ, but absolute performance was too weak to support a sensor-removal claim.

### CASE-001A — vibration feature reconstruction
After reconstructing the observations as 100-sample vibration windows with time-domain vibration features and evaluating by leave-one-operating-speed-out validation:
- XYZ: 82.6% mean balanced accuracy
- YZ: 79.5%
- XY: 78.9%
- Y: 75.5%
- speed-only: 33.3% chance

The apparent raw-sample XZ advantage did not survive improved signal representation. Full XYZ became best, and the audit identified a strong operating-regime blind spot around the held-out 30% speed condition.

Commercial lesson: sometimes the correct recommendation is not 'remove a sensor' but 'fix the representation before changing the hardware.'

## First paid pilot
### GardenCore Sensor Audit — Founding Pilot
Price hypothesis: **$1,500 fixed fee**.

Customer provides:
- one vibration/condition-monitoring dataset OR sensitivity/modal/FE model
- sensor/channel descriptions
- target condition/fault/parameter
- operating-state labels if available

Deliverables:
1. sensing-pipeline audit
2. channel/configuration ranking
3. blind-spot and operating-regime map
4. reduced-vs-full sensor comparison
5. representation audit
6. concise engineering report
7. one review call

Pilot boundary: research/engineering decision support; not a safety certification, automated maintenance authorization, or replacement for qualified engineering judgment.

## Qualification
Good first customer:
- already collects vibration or condition-monitoring data
- has rotating equipment, test rigs, fans, pumps, motors, gearboxes, or similar assets
- has uncertainty about sensor/channel value or monitoring blind spots
- can provide historical data without requiring new hardware installation

Avoid initially:
- safety-critical certification decisions
- customers requiring guaranteed fault-detection performance
- projects where no baseline or validation outcome exists

## Outreach message
Subject: A different kind of vibration-data audit

Hi [Name],

I'm piloting GardenCore Sensor Audit, an engineering analysis for teams that already collect vibration or condition-monitoring data.

Instead of simply fitting another fault classifier, the audit asks whether the sensing pipeline itself is preserving useful diagnostic information: which channels are valuable or redundant, where operating conditions create blind spots, whether dropping a sensor actually costs information, and whether the representation of the signal is hiding information already present in the hardware.

In our first public physical-data case study, raw instantaneous accelerometer samples were nearly non-diagnostic and misleadingly suggested that a two-axis configuration beat all three axes. After reconstructing the same measurements as vibration windows and testing on unseen operating speeds, performance rose to 82.6% balanced accuracy and the full XYZ configuration became best. The result prevented the wrong hardware conclusion rather than forcing a sensor-reduction success story.

I'm looking for a small number of founding pilot datasets from real rotating equipment or test rigs. The pilot is a fixed $1,500 analysis and includes channel/configuration ranking, blind-spot mapping, reduced-vs-full comparison, representation audit, and a technical report.

Would you be open to a short conversation about a dataset or machine where sensor value is currently uncertain?

Best,
Gage Fry
GardenCore / The Fource Principles

## Sales rule
Do not claim industrial superiority yet. Sell the **audit and falsifiable pilot**. CASE-001/001A is evidence that the workflow can produce a useful correction on real physical measurements, not proof of generalized industrial performance.
