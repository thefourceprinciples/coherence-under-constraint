# GARDENCORE-009 — Adversarial Cross-Domain Gauntlet

Goal: attack the four-layer GardenCore architecture with deliberately misleading synthetic cases and verify that failure modes are classified without rescue assumptions.

## Cases
10 adversarial/control cases were tested, including:
- full rank with catastrophic conditioning
- full local rank with global two-to-one ambiguity
- unique inverse but noise-dominated sensing
- apparent defect floor that disappears when the approximation class expands
- persistent fixed-class obstruction
- exact local kernel
- kernel removal that merely shifts the problem into statistical fragility
- simultaneous global ambiguity and statistical fragility
- numerical plateau without invariant support
- well-resolved control

## Result
Primary classification accuracy: 10/10 = 100%.

## Confirmed lessons
- full rank can still be statistically unusable
- full local rank can coexist with global ambiguity
- unique inverse can still be noise dominated
- apparent floors should not be promoted to obstruction without a fixed approximation class/invariant
- fixed-class obstruction is distinct from poor conditioning
- removing a kernel can merely move the problem into statistical fragility
- multiple failure modes can coexist
- universal scalarization can reverse rankings depending on arbitrary weights

## Scalarization attack
Two tradeoff vectors were ranked under different weightings. Changing the weights flipped the preferred system, confirming that no universal scalar ordering is justified without an explicit domain utility function.

## Architectural correction
A single primary diagnosis label is too crude. GardenCore should preserve multilabel states across:
1. local nonidentifiability
2. statistical fragility
3. global ambiguity
4. obstruction

## Verdict
- four-layer architecture survives adversarial synthetic cases: PASS
- single-label classification is sufficient: FAIL
- universal scalar ranking is robust: FAIL
- GardenCore may proceed to a v1.0 claims/specification sweep: YES
