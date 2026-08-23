# FR–FOURCE–FORMAL–007A — executable protocol

Status: implementation branch. No empirical claim is promoted by code existence.

Canonical preregistration: `FR-FOURCE-FORMAL/SWEEP_007_PREREGISTRATION.md`.

Authoritative runner: `experiments/fr_fource_formal_007a_runner.py`.
Low-level implementation library: `experiments/fr_fource_formal_007a.py`.
Frozen implementation config: `experiments/configs/fr_fource_formal_007a.json`.

## Run modes

Full preregistered run:

```bash
python experiments/fr_fource_formal_007a_runner.py \
  --output experiments/results/FR-FOURCE-FORMAL-007A-first
```

Non-evidentiary smoke run:

```bash
python experiments/fr_fource_formal_007a_runner.py \
  --smoke \
  --output /tmp/fr-fource-007a-smoke
```

Smoke mode exists only to expose syntax/runtime defects. A smoke result MUST NOT be described as pass, fail, support, falsification, pilot evidence, or a reason to alter thresholds.

## Implementation details fixed before the first result run

These choices fill estimator details left open by Sweep 007 without changing its primary thresholds.

- Binary majority uses strict majority; ties map to 0.
- M1 estimates pairwise lag-one conditional mutual information `I(X_i(t+1); X_j(t) | X_i(t))` with Jeffreys-style pseudocount 0.5, then scores mean within-side minus mean cross-side CMI.
- M2 uses a four-state macro process from the two side majorities. Transition probabilities use pseudocount 0.5. The first 70% trains a first-order Markov predictor and the held-out 30% supplies negative log loss. Metric score is negative NLL so larger is better.
- M3 uses 512 sampled baseline contexts in full mode. For every source node, `do(source=0)` and `do(source=1)` are evaluated against the known one-step simulator. Jensen–Shannon divergence between target Bernoulli response distributions defines the directed intervention-effect matrix. Partition score is within-side minus cross-side effect.
- M4 is three-step macrostate retention minus the marginal-frequency chance retention `sum_s p(s)^2`.
- M5 compares each candidate's unperturbed 4x4 macro transition matrix to matrices recovered from perturbed systems. It uses sigma 0.05, 0.10, and 0.20 with 20 copies per sigma. Each perturbed copy uses burn-in 500 and 4,000 retained steps. M5 is deliberately expensive and is not replaced by a cheaper proxy in the full run.
- Conservative-family ranks are M1 alone (statistical boundary), median rank of M2/M4/M5 (macro dynamics), and M3 alone (interventional). This prevents the shared-majority representation from being counted as three independent witnesses.
- Consensus rank is the median of the three family ranks and is descriptive only.
- P3 applies an isomorphic random node permutation to both W and the observed trajectory, maps the planted boundary through that permutation, and compares its consensus percentile with baseline.
- P4 changes node-local biases at retained index 10,000 while preserving W. Observation labels are resampled as metadata; labels do not reorder dynamics because isomorphic relabeling is tested separately by P3. The post-change half is evaluated against the baseline planted-boundary percentile.
- P5 permutes weights on 40% of directed internal-O edge locations. Because the primary graph is dense, this is a relational-weight rewiring/damage operation rather than edge deletion; the global weight inventory is preserved on those selected locations.

## Append-only output contract

The authoritative runner refuses to write into a nonempty output directory. The first full run must therefore remain immutable.

Each run writes:

- `manifest.json` with git SHA, config hash, Python/NumPy/platform and seeds;
- `effective_config.json`;
- structured, null, and rewired W matrices per seed;
- all structured and null candidate scores/ranks per seed;
- P3 permutation record;
- P4 replacement metadata;
- per-seed primary summary;
- aggregate `primary_summary.csv`;
- aggregate `verdict.json`.

## Failure discipline

P1 or P2 failure is primary failure. Strong-falsification rules from Sweep 007 remain authoritative. P3/P6 failure after P1/P2 success narrows the claim. No threshold, seed, metric, planted partition, or null is changed after the first full result. Any revised hypothesis is CSH-002 and requires a new preregistration and untouched test data.

## Known computational burden

M5 dominates runtime because it ranks every allowed partition across all perturbed copies. The full evidentiary run should be executed on a stable machine with sufficient compute. Performance optimization is allowed only if it is mathematically output-equivalent; changing sample counts, candidate space, noise levels, or estimator definitions is not an optimization.
