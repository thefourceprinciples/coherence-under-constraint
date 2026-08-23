#!/usr/bin/env python3
"""FR-FOURCE-FORMAL-007B corrected execution runner.

This runner preserves the frozen Sweep 007 hypotheses and thresholds while
repairing implementation-fidelity defects found before any evidentiary run.
Smoke mode is NON-EVIDENTIARY. Full mode refuses a dirty checkout.
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


def tracked_tree_clean() -> bool:
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
        )
        return status.strip() == ""
    except Exception:
        return False


def simulate_midpoint_replacement(W, seed, burn, retained, replacement_bias):
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


def canonicalize(mask):
    m = np.asarray(mask, dtype=np.uint8).copy()
    if m[0] == 0:
        m = 1 - m
    return m


def uninterrupted_retention_score(macro, horizon):
    if horizon < 1 or len(macro) <= horizon:
        return 0.0
    base = macro[:-horizon]
    retained = np.ones(len(base), dtype=bool)
    for step in range(1, horizon + 1):
        retained &= macro[step:step + len(base)] == base
    observed = float(np.mean(retained))
    freqs = np.bincount(macro, minlength=4).astype(float)
    freqs /= freqs.sum()
    chance = float(np.sum(freqs ** (horizon + 1)))
    return observed - chance


def intervention_matrix(W, X, seed, contexts, bias=None):
    rng = np.random.default_rng(seed + 200_000)
    n = W.shape[0]
    b = np.zeros(n) if bias is None else np.asarray(bias, dtype=float)
    idx = rng.choice(len(X), size=min(contexts, len(X)), replace=False)
    base = X[idx].astype(float)
    E = np.zeros((n, n), dtype=float)
    for src in range(n):
        x0, x1 = base.copy(), base.copy()
        x0[:, src] = 0.0
        x1[:, src] = 1.0
        p0 = core.sigmoid(b + (2.0 * x0 - 1.0) @ W.T)
        p1 = core.sigmoid(b + (2.0 * x1 - 1.0) @ W.T)
        for tgt in range(n):
            if tgt != src:
                E[tgt, src] = core.bernoulli_js(float(p0[:, tgt].mean()), float(p1[:, tgt].mean()))
    return E


def score_static_metrics(W, X, partitions, cfg, seed, bias=None):
    alpha = float(cfg["pseudocount"])
    cmi = core.lag_cmi_matrix(X, alpha)
    inter = intervention_matrix(W, X, seed, int(cfg["intervention_contexts"]), bias=bias)
    m1 = np.empty(len(partitions)); m2 = np.empty(len(partitions))
    m3 = np.empty(len(partitions)); m4 = np.empty(len(partitions))
    for k, mask in enumerate(partitions):
        macro = core.strict_majority_macro(X, mask)
        m1[k] = core.partition_contrast(cmi, mask)
        m2[k] = -core.markov_nll(macro, float(cfg["train_fraction"]), alpha)
        m3[k] = core.partition_contrast(inter, mask)
        m4[k] = uninterrupted_retention_score(macro, int(cfg["m4_horizon"]))
    return {"M1": m1, "M2": m2, "M3": m3, "M4": m4}


def perturbational_robustness(W, X, partitions, cfg, seed, bias=None):
    alpha = float(cfg["pseudocount"])
    base_tm = np.asarray([core.transition_matrix(core.strict_majority_macro(X, mask), alpha) for mask in partitions])
    divergence = np.zeros(len(partitions), dtype=float)
    count = 0
    for sidx, sigma in enumerate(cfg["m5_sigmas"]):
        for copy in range(int(cfg["m5_copies_per_sigma"])):
            rseed = seed + 300_000 + sidx * 10_000 + copy
            rng = np.random.default_rng(rseed)
            Wp = W + rng.normal(0.0, float(sigma), size=W.shape)
            np.fill_diagonal(Wp, 0.0)
            Xp = core.simulate(Wp, rseed, int(cfg["m5_burn_in"]), int(cfg["m5_retained_steps"]), bias=bias)
            for k, mask in enumerate(partitions):
                tm = core.transition_matrix(core.strict_majority_macro(Xp, mask), alpha)
                divergence[k] += core.js_discrete(base_tm[k], tm)
            count += 1
    return -divergence / max(count, 1)


def evaluate(W, X, partitions, cfg, seed, bias=None):
    scores = score_static_metrics(W, X, partitions, cfg, seed, bias=bias)
    scores["M5"] = perturbational_robustness(W, X, partitions, cfg, seed, bias=bias)
    ranks = {k: core.ranks_desc(v) for k, v in scores.items()}
    fam = core.family_ranks(ranks)
    cons = core.consensus_rank(fam)
    top_n = max(1, math.ceil(len(partitions) * float(cfg["top_fraction"])))
    planted = core.planted_mask(cfg["nodes"])
    pidx = next(i for i, m in enumerate(partitions) if np.array_equal(m, planted))
    return {
        "scores": scores, "ranks": ranks, "family_ranks": fam, "consensus": cons,
        "top_n": top_n, "planted_index": pidx,
        "planted_consensus_rank": float(cons[pidx]),
        "planted_consensus_percentile": 100.0 * float(cons[pidx]) / len(partitions),
        "planted_in_top_set": bool(float(cons[pidx]) <= top_n),
        "jaccard": core.mean_pairwise_jaccard(fam, top_n),
        "kendall": core.family_kendall(fam),
        "coupling_rank": int(core.ranks_desc(core.coupling_baseline(W, partitions))[pidx]),
        "correlation_rank": int(core.ranks_desc(core.correlation_baseline(X, partitions))[pidx]),
    }


def relabel_case(W, X, seed, cfg, partitions):
    rng = np.random.default_rng(seed + 600_000)
    perm = rng.permutation(cfg["nodes"])
    Wp = W[np.ix_(perm, perm)]
    Xp = X[:, perm]
    result = evaluate(Wp, Xp, partitions, cfg, seed + 600_000)
    old_target = core.planted_mask(cfg["nodes"])
    new_target = canonicalize(old_target[perm])
    pidx = next(i for i, m in enumerate(partitions) if np.array_equal(m, new_target))
    percentile = 100.0 * float(result["consensus"][pidx]) / len(partitions)
    return {"perm_new_to_old": perm.tolist(), "target_new_labels": new_target.tolist(), "consensus_percentile": percentile}


def run_seed(seed, cfg, partitions, out_dir):
    seed_dir = out_dir / f"seed_{seed}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    W = core.build_structured_w(seed, cfg)
    Wn = core.matched_null(W, seed)
    X = core.simulate(W, seed + 1, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    Xn = core.simulate(Wn, seed + 2, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    np.savetxt(seed_dir / "W_structured.csv", W, delimiter=",")
    np.savetxt(seed_dir / "W_null.csv", Wn, delimiter=",")

    structured = evaluate(W, X, partitions, cfg, seed)
    null = evaluate(Wn, Xn, partitions, cfg, seed + 10_000)
    core.save_candidate_table(seed_dir / "structured_candidates.csv", partitions, structured)
    core.save_candidate_table(seed_dir / "null_candidates.csv", partitions, null)

    p3 = relabel_case(W, X, seed, cfg, partitions)

    bias = core.replacement_surrogate_bias(seed, cfg["nodes"])
    _, Xpost = simulate_midpoint_replacement(W, seed + 20_000, int(cfg["burn_in"]), int(cfg["retained_steps"]), bias)
    label_rng = np.random.default_rng(seed + 520_000)
    replacement_labels = label_rng.permutation(cfg["nodes"]).tolist()
    replacement = evaluate(W, Xpost, partitions, cfg, seed + 20_000, bias=bias)
    core.save_candidate_table(seed_dir / "replacement_candidates.csv", partitions, replacement)

    Wr = core.rewire_internal_o(W, seed, float(cfg["rewire_fraction_internal_O"]))
    Xr = core.simulate(Wr, seed + 30_000, int(cfg["burn_in"]), int(cfg["retained_steps"]))
    rewired = evaluate(Wr, Xr, partitions, cfg, seed + 30_000)
    np.savetxt(seed_dir / "W_rewired.csv", Wr, delimiter=",")
    core.save_candidate_table(seed_dir / "rewired_candidates.csv", partitions, rewired)

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
        "planted_in_top_set": bool(structured["planted_in_top_set"]),
        "p3_relabel_percentile": float(p3["consensus_percentile"]),
        "p3_abs_delta": abs(float(p3["consensus_percentile"]) - structured_pct),
        "replacement_percentile": replacement_pct,
        "rewired_percentile": rewired_pct,
        "replacement_loss": replacement_pct - structured_pct,
        "rewiring_loss": rewired_pct - structured_pct,
        "coupling_structured_percentile": coupling_struct_pct,
        "coupling_null_percentile": coupling_null_pct,
        "coupling_in_top_set": bool(structured["coupling_rank"] <= structured["top_n"]),
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


def verdict(rows, cfg):
    th = cfg["primary_thresholds"]
    p1_wins = sum(r["jaccard_difference"] > 0 for r in rows)
    p1_med = float(np.median([r["jaccard_difference"] for r in rows]))
    p2_count = sum(bool(r["planted_in_top_set"]) for r in rows)
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
    coupling_recovery = sum(bool(r["coupling_in_top_set"]) for r in rows)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--output", type=Path, default=ROOT / "experiments" / "results" / "FR-FOURCE-FORMAL-007B")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if not args.smoke and not tracked_tree_clean():
        raise SystemExit("Refusing full run: tracked working tree differs from HEAD")
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
        "tracked_tree_clean_at_start": tracked_tree_clean(),
        "python": sys.version, "platform": platform.platform(), "numpy": np.__version__,
        "source_config": str(args.config), "config_sha256": core.sha256_file(args.config),
        "candidate_count": int(len(partitions)), "seeds": cfg["master_seeds"],
        "pre_run_corrections": [
            "P3 isomorphic relabeling executed and scored",
            "P4 replacement begins at retained midpoint and post-change segment is scored",
            "P4 replacement bias propagated through M3 and M5 simulations",
            "M4 requires uninterrupted retention through the full horizon",
            "P2 and coupling baseline use the same integer top-set cutoff",
            "full execution refuses tracked dirty working tree",
            "replacement and rewiring candidate artifacts are preserved for audit",
            "simple-coupling strong-falsification comparison fixed before full run",
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
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    decision = verdict(rows, cfg)
    if args.smoke:
        decision["primary_status"] = "NOT_EVIDENCE"
        decision["strong_falsification"] = False
        decision["warning"] = "Smoke mode cannot pass, fail, support, or falsify CSH-001."
    (out_dir / "verdict_007b.json").write_text(json.dumps(decision, indent=2))
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
