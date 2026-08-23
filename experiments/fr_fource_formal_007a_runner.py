#!/usr/bin/env python3
"""Authoritative FR-FOURCE-FORMAL-007A orchestration.

This module imports the low-level metric/generator implementation from
fr_fource_formal_007a.py and executes the frozen primary controls, including
P3 isomorphic relabeling and P4 midpoint constituent-replacement surrogate.

Smoke mode is non-evidentiary. Full mode writes append-only artifacts.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np

import fr_fource_formal_007a as core

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "fr_fource_formal_007a.json"


def canonical(mask: np.ndarray) -> np.ndarray:
    mask = mask.astype(np.uint8).copy()
    if mask[0] == 0:
        mask = 1 - mask
    return mask


def partition_index(partitions: np.ndarray, mask: np.ndarray) -> int:
    target = canonical(mask)
    for i, candidate in enumerate(partitions):
        if np.array_equal(candidate, target):
            return i
    raise ValueError(f"Partition not found: {target.tolist()}")


def percentile(result: dict, partitions: np.ndarray, mask: np.ndarray) -> float:
    i = partition_index(partitions, mask)
    return 100.0 * float(result["consensus"][i]) / len(partitions)


def baseline_percentile(result: dict, which: str, n_candidates: int) -> float:
    rank = result[f"{which}_rank"]
    return 100.0 * float(rank) / n_candidates


def simulate_midpoint_replacement(W: np.ndarray, seed: int, cfg: dict) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """P4 surrogate: change node-local biases at retained midpoint; preserve W.

    Observation labels are resampled as metadata only. They do not reorder
    dynamics, because label permutation is separately tested by P3.
    """
    rng = np.random.default_rng(seed + 500_000)
    n = W.shape[0]
    burn = int(cfg["burn_in"])
    retained = int(cfg["retained_steps"])
    midpoint = retained // 2
    bias_after = rng.normal(0.0, 0.10, size=n)
    labels_after = [f"unit_{v:08x}" for v in rng.integers(0, 2**32, size=n, dtype=np.uint64)]

    x = rng.integers(0, 2, size=n, dtype=np.uint8)
    out = np.empty((retained, n), dtype=np.uint8)
    for t in range(burn + retained):
        rt = t - burn
        b = bias_after if rt >= midpoint else np.zeros(n)
        p = core.sigmoid(b + W @ (2.0 * x.astype(float) - 1.0))
        x = (rng.random(n) < p).astype(np.uint8)
        if t >= burn:
            out[rt] = x
    return out[midpoint:], bias_after, labels_after


def isomorphic_relabel(W: np.ndarray, X: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed + 600_000)
    perm = rng.permutation(W.shape[0])
    return W[np.ix_(perm, perm)], X[:, perm], perm


def evaluate_primary_seed(seed: int, cfg: dict, partitions: np.ndarray, seed_dir: Path) -> dict:
    seed_dir.mkdir(parents=True, exist_ok=True)
    W = core.build_structured_w(seed, cfg)
    Wn = core.matched_null(W, seed)
    X = core.simulate(W, seed + 1, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    Xn = core.simulate(Wn, seed + 2, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    np.savetxt(seed_dir / "W_structured.csv", W, delimiter=",")
    np.savetxt(seed_dir / "W_null.csv", Wn, delimiter=",")

    base = core.evaluate(W, X, partitions, cfg, seed)
    null = core.evaluate(Wn, Xn, partitions, cfg, seed + 10_000)
    core.save_candidate_table(seed_dir / "structured_candidates.csv", partitions, base)
    core.save_candidate_table(seed_dir / "null_candidates.csv", partitions, null)

    planted = core.planted_mask(int(cfg["nodes"]))
    base_pct = percentile(base, partitions, planted)
    null_pct = percentile(null, partitions, planted)

    # P3 — exact isomorphic relabel of observed trajectory and dynamics.
    Wp, Xp, perm = isomorphic_relabel(W, X, seed)
    relabeled = core.evaluate(Wp, Xp, partitions, cfg, seed)
    planted_permuted = planted[perm]
    relabel_pct = percentile(relabeled, partitions, planted_permuted)
    (seed_dir / "P3_permutation.json").write_text(json.dumps({
        "permutation_new_index_to_old_index": perm.tolist(),
        "mapped_planted_mask": canonical(planted_permuted).tolist(),
        "baseline_percentile": base_pct,
        "relabeled_percentile": relabel_pct,
        "absolute_difference": abs(relabel_pct - base_pct)
    }, indent=2))

    # P4 — midpoint node-local replacement surrogate, W unchanged.
    Xrep_post, bias_after, labels_after = simulate_midpoint_replacement(W, seed, cfg)
    replacement = core.evaluate(W, Xrep_post, partitions, cfg, seed + 20_000)
    replacement_pct = percentile(replacement, partitions, planted)
    (seed_dir / "P4_replacement_metadata.json").write_text(json.dumps({
        "change_time_retained_index": int(cfg["retained_steps"]) // 2,
        "bias_after": bias_after.tolist(),
        "observation_labels_after": labels_after,
        "W_changed": False,
        "baseline_percentile": base_pct,
        "post_change_percentile": replacement_pct,
        "percentile_loss": replacement_pct - base_pct
    }, indent=2))

    # P5 — relational rewiring.
    Wr = core.rewire_internal_o(W, seed, float(cfg["rewire_fraction_internal_O"]))
    Xr = core.simulate(Wr, seed + 30_000, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    rewired = core.evaluate(Wr, Xr, partitions, cfg, seed + 30_000)
    rewired_pct = percentile(rewired, partitions, planted)
    np.savetxt(seed_dir / "W_rewired.csv", Wr, delimiter=",")

    row = {
        "seed": seed,
        "candidate_count": len(partitions),
        "structured_jaccard": base["jaccard"],
        "null_jaccard": null["jaccard"],
        "jaccard_difference": base["jaccard"] - null["jaccard"],
        "structured_kendall": base["kendall"],
        "null_kendall": null["kendall"],
        "planted_percentile": base_pct,
        "null_planted_percentile": null_pct,
        "P3_relabel_percentile": relabel_pct,
        "P3_abs_difference": abs(relabel_pct - base_pct),
        "P4_replacement_percentile": replacement_pct,
        "P4_loss": replacement_pct - base_pct,
        "P5_rewired_percentile": rewired_pct,
        "P5_loss": rewired_pct - base_pct,
        "P6_rewire_minus_replacement": (rewired_pct - base_pct) - (replacement_pct - base_pct),
        "coupling_percentile": baseline_percentile(base, "coupling", len(partitions)),
        "null_coupling_percentile": baseline_percentile(null, "coupling", len(partitions)),
        "correlation_percentile": baseline_percentile(base, "correlation", len(partitions)),
        "null_correlation_percentile": baseline_percentile(null, "correlation", len(partitions)),
    }
    (seed_dir / "primary_summary.json").write_text(json.dumps(row, indent=2))
    return row


def paired_discrimination(rows: list[dict], prefix: str) -> tuple[int, float]:
    if prefix == "consensus":
        diffs = [r["null_planted_percentile"] - r["planted_percentile"] for r in rows]
    else:
        diffs = [r[f"null_{prefix}_percentile"] - r[f"{prefix}_percentile"] for r in rows]
    return sum(d > 0 for d in diffs), float(np.median(diffs))


def decide(rows: list[dict], cfg: dict, smoke: bool) -> dict:
    th = cfg["primary_thresholds"]
    top_pct = 100.0 * float(cfg["top_fraction"])
    p1_wins = sum(r["jaccard_difference"] > 0 for r in rows)
    p1_med = float(np.median([r["jaccard_difference"] for r in rows]))
    p2_count = sum(r["planted_percentile"] <= top_pct for r in rows)
    p3_count = sum(r["P3_abs_difference"] <= th["P3_percentile_tolerance"] for r in rows)
    p4_count = sum(r["P4_loss"] < th["P4_max_percentile_loss"] for r in rows)
    p5_count = sum(r["P5_loss"] >= th["P5_min_percentile_loss"] for r in rows)
    p6_count = sum(r["P6_rewire_minus_replacement"] > 0 for r in rows)

    P1 = p1_wins >= th["P1_pair_wins"] and p1_med > th["P1_median_difference"]
    P2 = p2_count >= th["P2_recovery_count"]
    P3 = p3_count >= th["P3_invariance_count"]
    P4 = p4_count >= th["P4_recovery_count"]
    P5 = p5_count >= th["P5_recovery_count"]
    P6 = p6_count >= th["P6_pair_wins"]

    consensus_recovery = p2_count
    coupling_recovery = sum(r["coupling_percentile"] <= top_pct for r in rows)
    cons_disc_wins, cons_disc_med = paired_discrimination(rows, "consensus")
    coup_disc_wins, coup_disc_med = paired_discrimination(rows, "coupling")
    baseline_dominates = (
        coupling_recovery >= consensus_recovery
        and coup_disc_wins >= cons_disc_wins
        and coup_disc_med >= cons_disc_med
    )
    planted_at_or_below_half = p2_count <= len(rows) / 2
    strong = (not P1) or planted_at_or_below_half or baseline_dominates

    if smoke:
        status = "NOT_EVIDENCE"
    elif strong:
        status = "STRONG_FALSIFICATION"
    elif not (P1 and P2):
        status = "FAIL"
    elif not (P3 and P6):
        status = "PARTIAL"
    else:
        status = "PASS"

    return {
        "mode": "SMOKE_NON_EVIDENTIARY" if smoke else "FULL_PREREGISTERED",
        "P1": {"pass": P1 if not smoke else None, "paired_wins": p1_wins, "median_difference": p1_med},
        "P2": {"pass": P2 if not smoke else None, "recovery_count": p2_count},
        "P3": {"pass": P3 if not smoke else None, "within_tolerance_count": p3_count},
        "P4": {"pass": P4 if not smoke else None, "within_loss_limit_count": p4_count},
        "P5": {"pass": P5 if not smoke else None, "rewiring_damage_count": p5_count},
        "P6": {"pass": P6 if not smoke else None, "rewiring_exceeds_replacement_count": p6_count},
        "baseline": {
            "consensus_boundary_recovery": consensus_recovery,
            "coupling_boundary_recovery": coupling_recovery,
            "consensus_discrimination_wins": cons_disc_wins,
            "coupling_discrimination_wins": coup_disc_wins,
            "consensus_discrimination_median": cons_disc_med,
            "coupling_discrimination_median": coup_disc_med,
            "coupling_equals_or_exceeds_consensus_on_both": baseline_dominates
        },
        "primary_status": status,
        "non_rescue": "Thresholds and unfavorable seeds are not altered after this result. Any revised hypothesis becomes CSH-002."
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Run FR-FOURCE-FORMAL-007A")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--output", type=Path, default=ROOT / "experiments" / "results" / "FR-FOURCE-FORMAL-007A-first")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    cfg = core.load_config(args.config, args.smoke)
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"Append-only contract: refusing overwrite of {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    partitions = core.generate_partitions(int(cfg["nodes"]))

    manifest = {
        "experiment_id": cfg["experiment_id"],
        "runner": "fr_fource_formal_007a_runner.py",
        "mode": "SMOKE_NON_EVIDENTIARY" if args.smoke else "FULL_PREREGISTERED",
        "git_sha": core.git_sha(),
        "config_sha256": core.sha256_file(args.config),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "candidate_count": len(partitions),
        "seeds": cfg["master_seeds"],
        "preregistration": "FR-FOURCE-FORMAL/SWEEP_007_PREREGISTRATION.md",
        "warning": "Smoke mode cannot support or falsify CSH-001."
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (args.output / "effective_config.json").write_text(json.dumps(cfg, indent=2))

    rows: list[dict] = []
    for seed in cfg["master_seeds"]:
        print(f"[007A] primary seed {seed}", flush=True)
        rows.append(evaluate_primary_seed(int(seed), cfg, partitions, args.output / f"seed_{seed}"))

    with (args.output / "primary_summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    decision = decide(rows, cfg, args.smoke)
    (args.output / "verdict.json").write_text(json.dumps(decision, indent=2))
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
