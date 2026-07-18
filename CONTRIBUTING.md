# Contributing to Coherence Under Constraint

CUC welcomes rigorous criticism, replication, formal correction, negative results, and carefully bounded extensions.

The project is not improved by making every idea sound established. It is improved by making every claim traceable, testable, and revisable.

## Before contributing

Read:

1. [`README.md`](README.md) for the public overview;
2. [`CHARTER.md`](CHARTER.md) for definitions and claim boundaries;
3. [`canon/claims.yml`](canon/claims.yml) for registered hypotheses;
4. [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for collaboration expectations.

## Useful contributions

- identify circular definitions or hidden assumptions;
- improve an operational measure;
- propose and implement a rival model;
- reproduce, falsify, or bound an existing result;
- add tests, configuration, or documentation;
- report a null or negative result;
- correct domain-specific mistakes;
- improve accessibility without weakening claim boundaries;
- identify ethical, safety, consent, or power concerns.

## Claim classes

Every substantive contribution must use one of these statuses:

- root invariant;
- definition;
- modeling commitment;
- derived result;
- hypothesis;
- reduced model;
- empirical finding;
- application mapping;
- metaphor or mnemonic;
- speculative branch;
- quarantined, deprecated, or falsified claim.

Do not promote a claim’s status implicitly through tone or placement.

## Proposing a formal claim

Open a **Formal claim** issue and provide:

- a stable proposed identifier;
- an exact claim;
- its model class and domain;
- independent and dependent variables;
- predicted direction or functional form;
- assumptions;
- a rival or null model;
- an explicit falsifier;
- current evidence level;
- equations and implementation references.

Claims without a plausible failure condition remain metaphors, definitions, or speculative prompts.

## Proposing an experiment

Open an **Experiment** issue and specify:

- which claim is being tested;
- the perturbation protocol;
- independent manipulations;
- outcome metrics;
- baselines and ablations;
- random-seed policy;
- stopping rule;
- uncertainty and held-out evaluation;
- expected artifacts;
- conditions that would count against the claim.

## Equation policy

Canonical equations must be stored as raw LaTeX inside fenced blocks:

````text
```latex
\[
P_T
=
\Pr
\left[
\tau_{\mathrm{fail}}>T
\right]
\]
```
````

Each canonical equation requires a stable identifier. A rendered image may accompany the source but cannot replace it.

## Code expectations

- keep variables independent when the claim requires independent manipulation;
- make randomness reproducible through a declared seed policy;
- avoid machine-specific paths;
- write outputs to explicit directories;
- connect figures to exact code and configuration;
- distinguish simulated data from illustrative curves;
- include tests for new formulas and boundary cases;
- document known failure regimes.

## Pull requests

A pull request should:

- explain what changed and why;
- name affected claim and equation identifiers;
- state whether formal meaning changed;
- include validation performed;
- disclose limitations and unresolved objections;
- avoid unrelated changes.

Major ontology or root changes require a ratification record rather than ordinary maintenance.

## Cross-domain applications

An application must define the literal system, environment, boundary, state, organization, viability region, constraints, coherence observable, throughput, perturbation, horizon, failure condition, rival model, and falsifier.

Shared vocabulary does not establish shared mechanism. Do not translate metaphorical similarity into causal equivalence.

## Human and social applications

When people are involved:

- disagreement is not automatically noise;
- imposed alignment is not consent;
- persistence is not automatically desirable;
- affected people should participate in defining organization and viability;
- surveillance, exclusion, and power asymmetries must be disclosed.

## License

By contributing, you agree that your contribution may be distributed under the repository’s MIT License unless a file explicitly states another license.

