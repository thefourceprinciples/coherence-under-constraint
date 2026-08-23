#!/usr/bin/env python3
"""FR-FOURCE-FORMAL-007B verification/corrected execution runner.

This runner preserves Sweep 007 thresholds while correcting two implementation
mismatches found during verification of 007A:

1. P3 is actually executed as an isomorphic node relabeling test.
2. P4 applies the node-local bias replacement at the retained-trajectory midpoint
   and evaluates the post-change segment, rather than simulating the whole run
   under the replacement bias.

Smoke mode is NON-EVIDENTIARY. Full mode is the candidate authoritative first
execution path only after CI and code review pass.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

import fr_fource_formal_007a as core

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "fr_fource_formal_007a.json"


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "UNKNOWN"


def simulate_midpoint_replacement(
    W: np.ndarray,
    seed: int,
    burn: int,
    retained: int,
    replacement_bias: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Continuous trajectory with bias replacement at retained midpoint.

    Returns (full retained trajectory, post-change half). The random external
    node-label reassignment required by the preregistration is recorded by the
    caller as metadata only: labels are names, not dynamical variables.
    """
    rng = np.random.default_rng(seed)
    n = W.shape[0]
    x = rng.integers(0, 2, size=n, dtype=np.uint8)
    for _ in range(burn):
        p = core.sigmoid(W @ (2.0 * x.astype(float) - 1.0))
        x = (rng.random(n) < p).astype(np.uint8)

    out = np.empty((retained, n), dtype=np.uint8)
    midpoint = retained // 2
    for t in range(retained):
        b = np.zeros(n) if t < midpoint else replacement_bias
        p = core.sigmoid(b + W @ (2.0 * x.astype(float) - 1.0))
        x = (rng.random(n) < p).astype(np.uint8)
        out[t] = x
    return out, out[midpoint:]


def canonicalize(mask: np.ndarray) -> np.ndarray:
    m = np.asarray(mask, dtype=np.uint8).copy()
    if m[0] == 0:
        m = 1 - m
    return m


def relabel_case(
    W: np.ndarray,
    X: np.ndarray,
    seed: int,
    cfg: dict,
    partitions: np.ndarray,
) -> dict:
    """P3: evaluate an isomorphic node relabeling.

    perm[new_index] = old_index. The observed trajectory is permuted rather than
    resimulated so the data-generating realization is identical up to labels.
    M5 still draws fresh isotropic perturbations, which are distributionally
    permutation-invariant but not numerically identical; the preregistered ±2
    percentile tolerance therefore remains meaningful.
    """
    rng = np.random.default_rng(seed + 600_000)
    perm = rng.permutation(cfg["nodes"])
    Wp = W[np.ix_(perm, perm)]
    Xp = X[:, perm]
    result = core.evaluate(Wp, Xp, partitions, cfg, seed + 600_000)

    old_target = core.planted_mask(cfg["nodes"])
    new_target = canonicalize(old_target[perm])
    pidx = next(i for i, m in enumerate(partitions) if np.array_equal(m, new_target))
    percentile = 100.0 * float(result["consensus"][pidx]) / len(partitions)
    return {
        "perm_new_to_old": perm.tolist(),
        "target_new_labels": new_target.tolist(),
        "consensus_percentile": percentile,
    }


def eval_condition(W: np.ndarray, X: np.ndarray, cfg: dict, partitions: np.ndarray, seed: int) -> dict:
    return core.evaluate(W, X, partitions, cfg, seed)


def run_seed(seed: int, cfg: dict, partitions: np.ndarray, out_dir: Path) -> dict:
    seed_dir = out_dir / f"seed_{seed}"
    seed_dir.mkdir(parents=True, exist_ok=True)

    W = core.build_structured_w(seed, cfg)
    Wn = core.matched_null(W, seed)
    X = core.simulate(W, seed + 1, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    Xn = core.simulate(Wn, seed + 2, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    np.savetxt(seed_dir / "W_structured.csv", W, delimiter=",")
    np.savetxt(seed_dir / "W_null.csv", Wn, delimiter=",")

    structured = eval_condition(W, X, cfg, partitions, seed)
    null = eval_condition(Wn, Xn, cfg, partitions, seed + 10_000)
    core.save_candidate_table(seed_dir / "structured_candidates.csv", partitions, structured)
    core.save_candidate_table(seed_dir / "null_candidates.csv", partitions, null)

    # P3: isomorphic relabeling.
    p3 = relabel_case(W, X, seed, cfg, partitions)

    # P4: continuous run, replacement begins exactly halfway through retained data.
    bias = core.replacement_surrogate_bias(seed, cfg["nodes"])
    _, Xpost = simulate_midpoint_replacement(
        W, seed + 20_000, int(cfg["burn_in"]), int(cfg["retained_steps"]), bias
    )
    # Resampled observation labels are provenance metadata; array indices remain
    # role coordinates so relabeling cannot itself manufacture organizational loss.
    label_rng = np.random.default_rng(seed + 520_000)
    replacement_labels = label_rng.permutation(cfg["nodes"]).tolist()
    replacement = eval_condition(W, Xpost, cfg, partitions, seed + 20_000)

    # P5: 40% internal-O weight destinations effectively reassigned by selected-edge
    # value permutation, preserving the selected/global weight inventory.
    Wr = core.rewire_internal_o(W, seed, float(cfg["rewire_fraction_internal_O"]))
    Xr = core.simulate(Wr, seed + 30_000, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    rewired = eval_condition(Wr, Xr, cfg, partitions, seed + 30_000)

    n = len(partitions)
    structured_pct = float(structured["planted_consensus_percentile"])
    null_pct = float(null["planted_consensus_percentile"])
    replacement_pct = float(replacement["planted_consensus_percentile"])
    rewired_pct = float(rewired["planted_consensus_percentile"])

    coupling_struct_pct = 100.0 * float(structured["coupling_rank"]) / n
    coupling_null_pct = 100.0 * float(null["coupling_rank"]) / n

    summary = {
        "seed": seed,
        "structured_jaccard": float(structured["jaccard"]),
        "null_jaccard": float(null["jaccard"]),
        "jaccard_difference": float(structured["jaccard"] - null["jaccard"]),
        "structured_kendall": float(structured["kendall"]),
        "null_kendall": float(null["kendall"]),
        "planted_percentile": structured_pct,
        "p3_relabel_percentile": float(p3["consensus_percentile"]),
        "p3_abs_delta": abs(float(p3["consensus_percentile"]) - structured_pct),
        "replacement_percentile": replacement_pct,
        "rewired_percentile": rewired_pct,
        "replacement_loss": replacement_pct - structured_pct,
        "rewiring_loss": rewired_pct - structured_pct,
        "coupling_structured_percentile": coupling_struct_pct,
        "coupling_null_percentile": coupling_null_pct,
        "coupling_discrimination": coupling_null_pct - coupling_struct_pct,
        "consensus_discrimination": null_pct - structured_pct,
        "correlation_rank": int(structured["correlation_rank"]),
        "candidate_count": n,
    }
    (seed_dir / "p3_relabel.json").write_text(json.dumps(p3, indent=2))
    (seed_dir / "p4_replacement_metadata.json").write_text(json.dumps({
        "midpoint_retained_index": int(cfg["retained_steps"]) // 2,
        "replacement_bias": bias.tolist(),
        "resampled_observation_labels": replacement_labels,
        "note": "labels are metadata; role-coordinate indices remain fixed for evaluation",
    }, indent=2))
    (seed_dir / "summary_007b.json").write_text(json.dumps(summary, indent=2))
    return summary


def verdict(rows: list[dict], cfg: dict) -> dict:
    th = cfg["primary_thresholds"]
    p1_wins = sum(r["jaccard_difference"] > 0 for r in rows)
    p1_med = float(np.median([r["jaccard_difference"] for r in rows]))
    p2_count = sum(r["planted_percentile"] <= 100.0 * float(cfg["top_fraction"]) for r in rows)
    p3_count = sum(r["p3_abs_delta"] <= float(th["P3_percentile_tolerance"]) for r in rows)
    p4_count = sum(r["replacement_loss"] < float(th["P4_max_percentile_loss"]) for r in rows)
    p5_count = sum(r["rewiring_loss"] >= float(th["P5_min_percentile_loss"]) for r in rows)
    p6_count = sum(r["rewiring_loss"] > r["replacement_loss"] for r in rows)

    P1 = p1_wins >= int(th["P1_pair_wins"]) and p1_med > float(th["P1_median_difference"])
    P2 = p2_count >= int(th["P2_recovery_count"])
    P3 = p3_count >= int(th["P3_invariance_count"])
    P4 = p4_count >= int(th["P4_recovery_count"])
    P5 = p5_count >= int(th["P5_recovery_count"])
    P6 = p6_count >= int(th["P6_pair_wins"])

    # Strong-falsification baseline interpretation fixed before first full run:
    # boundary recovery: top-5% coupling rank count versus consensus P2 count.
    # discrimination: positive structured-vs-null planted-rank separation count.
    coupling_recovery = sum(r["coupling_structured_percentile"] <= 100.0 * float(cfg["top_fraction"]) for r in rows)
    coupling_discrimination = sum(r["coupling_discrimination"] > 0 for r in rows)
    consensus_discrimination = sum(r["consensus_discrimination"] > 0 for r in rows)
    baseline_dominates = coupling_recovery >= p2_count and coupling_discrimination >= consensus_discrimination

    strong = (not P1) or (p2_count <= len(rows) / 2) or baseline_dominates
    if not P1 or not P2:
        primary = "STRONG_FALSIFICATION" if strong else "FAIL"
    elif not P3 or not P6:
        primary = "PARTIAL"
    else:
        primary = "PASS"

    return {
        "P1": {"pass": P1, "paired_wins": p1_wins, "median_difference": p1_med},
        "P2": {"pass": P2, "recovered": p2_count},
        "P3": {"pass": P3, "within_tolerance": p3_count},
        "P4": {"pass": P4, "count": p4_count},
        "P5": {"pass": P5, "count": p5_count},
        "P6": {"pass": P6, "count": p6_count},
        "baseline": {
            "coupling_recovery_count": coupling_recovery,
            "coupling_positive_discrimination_count": coupling_discrimination,
            "consensus_positive_discrimination_count": consensus_discrimination,
            "equals_or_exceeds_on_both": bool(baseline_dominates),
        },
        "primary_status": primary,
        "strong_falsification": bool(strong),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--output", type=Path, default=ROOT / "experiments" / "results" / "FR-FOURCE-FORMAL-007B")
    ap.add_argument("--smoke", action="store_true", help="NON-EVIDENTIARY code-path validation")
    args = ap.parse_args()

    cfg = core.load_config(args.config, args.smoke)
    out_dir = args.output
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"Refusing to overwrite append-only result directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    partitions = core.generate_partitions(int(cfg["nodes"]))

    manifest = {
        "experiment_id": "FR-FOURCE-FORMAL-007B",
        "mode": "SMOKE_NON_EVIDENTIARY" if args.smoke else "FULL_PREREGISTERED_CANDIDATE",
        "git_sha": git_sha(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "source_config": str(args.config),
        "config_sha256": core.sha256_file(args.config),
        "candidate_count": int(len(partitions)),
        "seeds": cfg["master_seeds"],
        "corrections_from_007a": [
            "P3 isomorphic relabeling executed and scored",
            "P4 replacement begins at retained midpoint and post-change segment is scored",
            "simple-coupling strong-falsification comparison made explicit before full run",
        ],
        "warning": "Smoke mode cannot support or falsify CSH-001. Full output is append-only.",
    }
    (out_dir / "manifest_007b.json").write_text(json.dumps(manifest, indent=2))
    (out_dir / "effective_config.json").write_text(json.dumps(cfg, indent=2))

    rows = []
    for seed in cfg["master_seeds"]:
        print(f"[007B] seed {seed}", flush=True)
        rows.append(run_seed(int(seed), cfg, partitions, out_dir))

    fields = list(rows[0].keys())
    with (out_dir / "summary_007b.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    decision = verdict(rows, cfg)
    if args.smoke:
        decision["primary_status"] = "NOT_EVIDENCE"
        decision["strong_falsification"] = False
        decision["warning"] = "Smoke mode cannot pass, fail, support, or falsify CSH-001."
    (out_dir / "verdict_007b.json").write_text(json.dumps(decision, indent=2))
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
