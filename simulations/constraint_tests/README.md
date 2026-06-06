# Constraint Tests

This directory will contain computational experiments that test how changing constraints affects coherence, persistence, and transition behavior.

Planned tests:

1. **Constraint strength sweep**
   - vary boundary strength;
   - measure coherence response;
   - identify ranges associated with dispersion, stability, brittleness, and collapse.

2. **Throughput variation**
   - vary input flow;
   - compare persistence against dissipative loss;
   - test the condition `P_in ≥ P_diss`.

3. **Interface perturbation**
   - perturb boundary/interface regions;
   - compare impact against equivalent perturbations in non-interface regions.

Each test should include:

- hypothesis;
- model assumptions;
- parameters;
- results;
- limitations;
- next experiment.
