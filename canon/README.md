# CUC canon registry

This directory contains machine-readable records for the Coherence Under Constraint canon.

## Authority

The human-readable [`CHARTER.md`](../CHARTER.md) is the governing draft. These registries make its symbols and claims easier to audit, validate, and connect to software.

## Files

- [`symbols.yml`](symbols.yml) — canonical symbols, meanings, types, and ranges
- [`claims.yml`](claims.yml) — registered hypotheses, scopes, predictions, falsifiers, and evidence levels

Future additions may include:

- one raw `.tex` source file per canonical equation;
- an equation registry linking source, assumptions, tests, and implementations;
- a branch registry connecting Garden identities and legacy aliases;
- experiment manifests linking claims to configurations and outputs.

## Status vocabulary

- `root-invariant`
- `definition`
- `modeling-commitment`
- `derived-result`
- `hypothesis`
- `reduced-model`
- `empirical-finding`
- `application-mapping`
- `metaphor`
- `speculative`
- `quarantined`
- `deprecated`
- `falsified`

## Change rule

A correction that changes an equation’s denominator, normalization, sign, exponent, range, or interpretation is a formal change. It requires a new version, rationale, compatibility note, and updated tests.

