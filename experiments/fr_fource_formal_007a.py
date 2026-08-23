#!/usr/bin/env python3
"""FR-FOURCE-FORMAL-007A executable bench.

Implements the frozen Sweep 007 preregistration. Full mode is evidentiary only
when executed from a clean checkout with the committed config unchanged.
Smoke mode is for code-path validation and MUST NOT be interpreted as evidence.

Dependencies: Python 3.10+, numpy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "fr_fource_formal_007a.json"


def sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -40.0, 40.0)
    return 1.0 / (1.0 + np.exp(-x))


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "UNKNOWN"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_config(path: Path, smoke: bool) -> dict:
    cfg = json.loads(path.read_text())
    if smoke:
        s = cfg["smoke_mode"]
        cfg = json.loads(json.dumps(cfg))
        cfg["master_seeds"] = s["seeds"]
        cfg["burn_in"] = s["burn_in"]
        cfg["retained_steps"] = s["retained_steps"]
        cfg["intervention_contexts"] = s["intervention_contexts"]
        cfg["m5_copies_per_sigma"] = s["m5_copies_per_sigma"]
        cfg["m5_burn_in"] = s["m5_burn_in"]
        cfg["m5_retained_steps"] = s["m5_retained_steps"]
        cfg["status"] = "SMOKE_NON_EVIDENTIARY"
    return cfg


def generate_partitions(n: int) -> np.ndarray:
    """All binary partitions modulo complement; node 0 side first; both sides >=2."""
    masks = []
    for bits in range(1 << (n - 1)):
        mask = np.zeros(n, dtype=np.uint8)
        mask[0] = 1
        for j in range(1, n):
            mask[j] = (bits >> (j - 1)) & 1
        k = int(mask.sum())
        if 2 <= k <= n - 2:
            masks.append(mask)
    return np.asarray(masks, dtype=np.uint8)


def planted_mask(n: int = 12) -> np.ndarray:
    m = np.zeros(n, dtype=np.uint8)
    m[:8] = 1
    return m


def mask_key(mask: np.ndarray) -> str:
    left = np.where(mask == 1)[0].tolist()
    right = np.where(mask == 0)[0].tolist()
    return f"{left}|{right}"


def build_structured_w(seed: int, cfg: dict) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = cfg["nodes"]
    W = np.zeros((n, n), dtype=float)
    A, B, E = map(set, (cfg["blocks"]["A"], cfg["blocks"]["B"], cfg["blocks"]["E"]))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if i in A and j in A:
                base = cfg["weights"]["within_A"]
            elif i in B and j in B:
                base = cfg["weights"]["within_B"]
            elif (i in A and j in B) or (i in B and j in A):
                base = cfg["weights"]["A_B"]
            elif i in E and j in E:
                lo, hi = cfg["weights"]["within_E_uniform"]
                base = rng.uniform(lo, hi)
            else:
                base = cfg["weights"]["O_E"]
            W[i, j] = base + rng.normal(0.0, cfg["weights"]["construction_jitter_sigma"])
    np.fill_diagonal(W, 0.0)
    return W


def block_membership(i: int) -> int:
    return 0 if i < 8 else 1


def matched_null(W: np.ndarray, seed: int) -> np.ndarray:
    """Permute destinations independently for each source while preserving outgoing weights."""
    n = W.shape[0]
    for attempt in range(1000):
        rng = np.random.default_rng(seed + 100_000 + attempt)
        out = np.zeros_like(W)
        all_block_membership_preserved = True
        for src in range(n):
            destinations = np.array([i for i in range(n) if i != src])
            vals = W[destinations, src].copy()
            perm = rng.permutation(destinations)
            for old_dst, new_dst, value in zip(destinations, perm, vals):
                out[new_dst, src] = value
                if block_membership(old_dst) != block_membership(new_dst):
                    all_block_membership_preserved = False
        np.fill_diagonal(out, 0.0)
        if not all_block_membership_preserved:
            return out
    raise RuntimeError("Failed to construct a nontrivial matched null")


def simulate(W: np.ndarray, seed: int, burn: int, retained: int, bias: np.ndarray | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = W.shape[0]
    b = np.zeros(n) if bias is None else np.asarray(bias, dtype=float)
    x = rng.integers(0, 2, size=n, dtype=np.uint8)
    out = np.empty((retained, n), dtype=np.uint8)
    total = burn + retained
    for t in range(total):
        p = sigmoid(b + W @ (2.0 * x.astype(float) - 1.0))
        x = (rng.random(n) < p).astype(np.uint8)
        if t >= burn:
            out[t - burn] = x
    return out


def strict_majority_macro(X: np.ndarray, mask: np.ndarray) -> np.ndarray:
    left = X[:, mask == 1]
    right = X[:, mask == 0]
    a = (2 * left.sum(axis=1) > left.shape[1]).astype(np.uint8)
    b = (2 * right.sum(axis=1) > right.shape[1]).astype(np.uint8)
    return (2 * a + b).astype(np.uint8)


def cmi_binary(y: np.ndarray, x: np.ndarray, z: np.ndarray, alpha: float) -> float:
    counts = np.full((2, 2, 2), alpha, dtype=float)
    np.add.at(counts, (y.astype(int), x.astype(int), z.astype(int)), 1.0)
    p = counts / counts.sum()
    p_xz = p.sum(axis=0)
    p_yz = p.sum(axis=1)
    p_z = p.sum(axis=(0, 1))
    val = 0.0
    for yy in range(2):
        for xx in range(2):
            for zz in range(2):
                q = p[yy, xx, zz]
                val += q * math.log((q * p_z[zz]) / (p_yz[yy, zz] * p_xz[xx, zz]))
    return val


def lag_cmi_matrix(X: np.ndarray, alpha: float) -> np.ndarray:
    n = X.shape[1]
    cur, nxt = X[:-1], X[1:]
    M = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                M[i, j] = cmi_binary(nxt[:, i], cur[:, j], cur[:, i], alpha)
    return M


def partition_contrast(matrix: np.ndarray, mask: np.ndarray) -> float:
    n = len(mask)
    within, cross = [], []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            (within if mask[i] == mask[j] else cross).append(matrix[i, j])
    return float(np.mean(within) - np.mean(cross))


def markov_nll(macro: np.ndarray, train_fraction: float, alpha: float) -> float:
    cut = max(2, min(len(macro) - 2, int(len(macro) * train_fraction)))
    counts = np.full((4, 4), alpha, dtype=float)
    np.add.at(counts, (macro[:cut-1], macro[1:cut]), 1.0)
    probs = counts / counts.sum(axis=1, keepdims=True)
    prev, nxt = macro[cut:-1], macro[cut+1:]
    return float(-np.mean(np.log(probs[prev, nxt] + 1e-15)))


def retention_score(macro: np.ndarray, horizon: int) -> float:
    observed = float(np.mean(macro[:-horizon] == macro[horizon:]))
    freqs = np.bincount(macro, minlength=4).astype(float)
    freqs /= freqs.sum()
    chance = float(np.sum(freqs * freqs))
    return observed - chance


def bernoulli_js(p: float, q: float) -> float:
    eps = 1e-12
    p, q = np.clip([p, q], eps, 1 - eps)
    m = 0.5 * (p + q)
    def kl(a: float, b: float) -> float:
        return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))
    return 0.5 * kl(float(p), float(m)) + 0.5 * kl(float(q), float(m))


def intervention_matrix(W: np.ndarray, X: np.ndarray, seed: int, contexts: int) -> np.ndarray:
    """One-step average causal-effect proxy using balanced do(source=0/1) contexts."""
    rng = np.random.default_rng(seed + 200_000)
    n = W.shape[0]
    idx = rng.choice(len(X), size=min(contexts, len(X)), replace=False)
    base = X[idx].astype(float)
    E = np.zeros((n, n), dtype=float)  # target, source
    for src in range(n):
        x0, x1 = base.copy(), base.copy()
        x0[:, src] = 0.0
        x1[:, src] = 1.0
        p0 = sigmoid((2.0 * x0 - 1.0) @ W.T)
        p1 = sigmoid((2.0 * x1 - 1.0) @ W.T)
        for tgt in range(n):
            if tgt != src:
                E[tgt, src] = bernoulli_js(float(p0[:, tgt].mean()), float(p1[:, tgt].mean()))
    return E


def transition_matrix(macro: np.ndarray, alpha: float) -> np.ndarray:
    counts = np.full((4, 4), alpha, dtype=float)
    np.add.at(counts, (macro[:-1], macro[1:]), 1.0)
    return counts / counts.sum(axis=1, keepdims=True)


def js_discrete(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=float).ravel()
    q = np.asarray(q, dtype=float).ravel()
    p /= p.sum(); q /= q.sum()
    m = 0.5 * (p + q)
    nzp, nzq = p > 0, q > 0
    klp = np.sum(p[nzp] * np.log(p[nzp] / m[nzp]))
    klq = np.sum(q[nzq] * np.log(q[nzq] / m[nzq]))
    return float(0.5 * (klp + klq))


def score_static_metrics(W: np.ndarray, X: np.ndarray, partitions: np.ndarray, cfg: dict, seed: int) -> dict[str, np.ndarray]:
    alpha = float(cfg["pseudocount"])
    cmi = lag_cmi_matrix(X, alpha)
    inter = intervention_matrix(W, X, seed, int(cfg["intervention_contexts"]))
    m1 = np.empty(len(partitions)); m2 = np.empty(len(partitions)); m3 = np.empty(len(partitions)); m4 = np.empty(len(partitions))
    for k, mask in enumerate(partitions):
        macro = strict_majority_macro(X, mask)
        m1[k] = partition_contrast(cmi, mask)
        m2[k] = -markov_nll(macro, float(cfg["train_fraction"]), alpha)
        m3[k] = partition_contrast(inter, mask)
        m4[k] = retention_score(macro, int(cfg["m4_horizon"]))
    return {"M1": m1, "M2": m2, "M3": m3, "M4": m4}


def perturbational_robustness(W: np.ndarray, X: np.ndarray, partitions: np.ndarray, cfg: dict, seed: int) -> np.ndarray:
    """M5: inverse mean JS divergence of candidate macro transition matrices.

    This is intentionally the expensive portion of the preregistered full bench.
    """
    alpha = float(cfg["pseudocount"])
    base_tm = []
    for mask in partitions:
        base_tm.append(transition_matrix(strict_majority_macro(X, mask), alpha))
    base_tm = np.asarray(base_tm)
    divergence = np.zeros(len(partitions), dtype=float)
    count = 0
    for sidx, sigma in enumerate(cfg["m5_sigmas"]):
        for copy in range(int(cfg["m5_copies_per_sigma"])):
            rseed = seed + 300_000 + sidx * 10_000 + copy
            rng = np.random.default_rng(rseed)
            Wp = W + rng.normal(0.0, float(sigma), size=W.shape)
            np.fill_diagonal(Wp, 0.0)
            Xp = simulate(Wp, rseed, int(cfg["m5_burn_in"]), int(cfg["m5_retained_steps"]))
            for k, mask in enumerate(partitions):
                tm = transition_matrix(strict_majority_macro(Xp, mask), alpha)
                divergence[k] += js_discrete(base_tm[k], tm)
            count += 1
    return -divergence / max(count, 1)


def ranks_desc(scores: np.ndarray) -> np.ndarray:
    order = np.argsort(-scores, kind="mergesort")
    ranks = np.empty(len(scores), dtype=int)
    ranks[order] = np.arange(1, len(scores) + 1)
    return ranks


def family_ranks(metric_ranks: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    macro = np.median(np.stack([metric_ranks["M2"], metric_ranks["M4"], metric_ranks["M5"]]), axis=0)
    return {"boundary": metric_ranks["M1"].astype(float), "macro": macro, "interventional": metric_ranks["M3"].astype(float)}


def mean_pairwise_jaccard(family: dict[str, np.ndarray], top_n: int) -> float:
    sets = []
    for r in family.values():
        sets.append(set(np.where(r <= top_n)[0].tolist()))
    vals = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            u = sets[i] | sets[j]
            vals.append(len(sets[i] & sets[j]) / len(u) if u else 1.0)
    return float(np.mean(vals))


def kendall_tau(a: np.ndarray, b: np.ndarray) -> float:
    n = len(a)
    conc = disc = 0
    for i in range(n - 1):
        d1 = a[i+1:] - a[i]
        d2 = b[i+1:] - b[i]
        prod = d1 * d2
        conc += int(np.sum(prod > 0)); disc += int(np.sum(prod < 0))
    den = conc + disc
    return (conc - disc) / den if den else 0.0


def family_kendall(family: dict[str, np.ndarray]) -> float:
    vals = list(family.values())
    return float(np.mean([kendall_tau(vals[i], vals[j]) for i in range(3) for j in range(i+1, 3)]))


def consensus_rank(family: dict[str, np.ndarray]) -> np.ndarray:
    return np.median(np.stack(list(family.values())), axis=0)


def coupling_baseline(W: np.ndarray, partitions: np.ndarray) -> np.ndarray:
    A = np.abs(W)
    return np.asarray([partition_contrast(A, m) for m in partitions])


def correlation_baseline(X: np.ndarray, partitions: np.ndarray) -> np.ndarray:
    C = np.nan_to_num(np.abs(np.corrcoef(X.T)), nan=0.0)
    np.fill_diagonal(C, 0.0)
    return np.asarray([partition_contrast(C, m) for m in partitions])


def evaluate(W: np.ndarray, X: np.ndarray, partitions: np.ndarray, cfg: dict, seed: int) -> dict:
    scores = score_static_metrics(W, X, partitions, cfg, seed)
    scores["M5"] = perturbational_robustness(W, X, partitions, cfg, seed)
    ranks = {k: ranks_desc(v) for k, v in scores.items()}
    fam = family_ranks(ranks)
    cons = consensus_rank(fam)
    top_n = max(1, math.ceil(len(partitions) * float(cfg["top_fraction"])))
    planted = planted_mask(cfg["nodes"])
    pidx = next(i for i, m in enumerate(partitions) if np.array_equal(m, planted))
    return {
        "scores": scores,
        "ranks": ranks,
        "family_ranks": fam,
        "consensus": cons,
        "top_n": top_n,
        "planted_index": pidx,
        "planted_consensus_rank": float(cons[pidx]),
        "planted_consensus_percentile": 100.0 * float(cons[pidx]) / len(partitions),
        "jaccard": mean_pairwise_jaccard(fam, top_n),
        "kendall": family_kendall(fam),
        "coupling_rank": int(ranks_desc(coupling_baseline(W, partitions))[pidx]),
        "correlation_rank": int(ranks_desc(correlation_baseline(X, partitions))[pidx]),
    }


def rewire_internal_o(W: np.ndarray, seed: int, fraction: float) -> np.ndarray:
    rng = np.random.default_rng(seed + 400_000)
    out = W.copy()
    edges = [(i, j) for i in range(8) for j in range(8) if i != j]
    k = max(1, round(len(edges) * fraction))
    chosen = rng.choice(len(edges), size=k, replace=False)
    vals = np.array([out[edges[idx]] for idx in chosen])
    vals = rng.permutation(vals)
    for idx, val in zip(chosen, vals):
        out[edges[idx]] = val
    return out


def replacement_surrogate_bias(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 500_000)
    # Node-local changes are deliberately small enough not to redefine relational roles.
    return rng.normal(0.0, 0.10, size=n)


def save_candidate_table(path: Path, partitions: np.ndarray, result: dict) -> None:
    fields = ["partition", "M1", "M2", "M3", "M4", "M5", "rM1", "rM2", "rM3", "rM4", "rM5", "family_boundary", "family_macro", "family_interventional", "consensus_rank"]
    with path.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(fields)
        for i, mask in enumerate(partitions):
            w.writerow([
                mask_key(mask),
                *[float(result["scores"][m][i]) for m in ("M1","M2","M3","M4","M5")],
                *[int(result["ranks"][m][i]) for m in ("M1","M2","M3","M4","M5")],
                float(result["family_ranks"]["boundary"][i]), float(result["family_ranks"]["macro"][i]), float(result["family_ranks"]["interventional"][i]), float(result["consensus"][i])
            ])


def run_seed(seed: int, cfg: dict, partitions: np.ndarray, out_dir: Path) -> dict:
    seed_dir = out_dir / f"seed_{seed}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    W = build_structured_w(seed, cfg)
    Wn = matched_null(W, seed)
    X = simulate(W, seed + 1, cfg["burn_in"], cfg["retained_steps"])
    Xn = simulate(Wn, seed + 2, cfg["burn_in"], cfg["retained_steps"])
    np.savetxt(seed_dir / "W_structured.csv", W, delimiter=",")
    np.savetxt(seed_dir / "W_null.csv", Wn, delimiter=",")

    structured = evaluate(W, X, partitions, cfg, seed)
    null = evaluate(Wn, Xn, partitions, cfg, seed + 10_000)
    save_candidate_table(seed_dir / "structured_candidates.csv", partitions, structured)
    save_candidate_table(seed_dir / "null_candidates.csv", partitions, null)

    # P4 surrogate: node-local bias change while W roles remain fixed.
    bias = replacement_surrogate_bias(seed, cfg["nodes"])
    Xrep = simulate(W, seed + 20_000, cfg["burn_in"], cfg["retained_steps"], bias=bias)
    replacement = evaluate(W, Xrep, partitions, cfg, seed + 20_000)

    # P5 relational damage.
    Wr = rewire_internal_o(W, seed, cfg["rewire_fraction_internal_O"])
    Xr = simulate(Wr, seed + 30_000, cfg["burn_in"], cfg["retained_steps"])
    rewired = evaluate(Wr, Xr, partitions, cfg, seed + 30_000)

    summary = {
        "seed": seed,
        "structured_jaccard": structured["jaccard"],
        "null_jaccard": null["jaccard"],
        "jaccard_difference": structured["jaccard"] - null["jaccard"],
        "structured_kendall": structured["kendall"],
        "null_kendall": null["kendall"],
        "planted_percentile": structured["planted_consensus_percentile"],
        "replacement_percentile": replacement["planted_consensus_percentile"],
        "rewired_percentile": rewired["planted_consensus_percentile"],
        "replacement_loss": replacement["planted_consensus_percentile"] - structured["planted_consensus_percentile"],
        "rewiring_loss": rewired["planted_consensus_percentile"] - structured["planted_consensus_percentile"],
        "coupling_rank": structured["coupling_rank"],
        "correlation_rank": structured["correlation_rank"],
        "candidate_count": len(partitions),
    }
    (seed_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def verdict(rows: list[dict], cfg: dict) -> dict:
    th = cfg["primary_thresholds"]
    p1_wins = sum(r["jaccard_difference"] > 0 for r in rows)
    p1_med = float(np.median([r["jaccard_difference"] for r in rows]))
    p2 = sum(r["planted_percentile"] <= 100.0 * cfg["top_fraction"] for r in rows)
    p4 = sum(r["replacement_loss"] < th["P4_max_percentile_loss"] for r in rows)
    p5 = sum(r["rewiring_loss"] >= th["P5_min_percentile_loss"] for r in rows)
    p6 = sum(r["rewiring_loss"] > r["replacement_loss"] for r in rows)
    P1 = p1_wins >= th["P1_pair_wins"] and p1_med > th["P1_median_difference"]
    P2 = p2 >= th["P2_recovery_count"]
    return {
        "P1": {"pass": P1, "paired_wins": p1_wins, "median_difference": p1_med},
        "P2": {"pass": P2, "recovered": p2},
        "P3": {"pass": None, "status": "implemented separately after primary run; no rescue value"},
        "P4": {"pass": p4 >= th["P4_recovery_count"], "count": p4},
        "P5": {"pass": p5 >= th["P5_recovery_count"], "count": p5},
        "P6": {"pass": p6 >= th["P6_pair_wins"], "count": p6},
        "primary_status": "PASS" if P1 and P2 else "FAIL",
        "note": "Strong-falsification baseline comparison must be evaluated from preserved candidate/baseline outputs. P3 label permutation is intentionally not inferred from unpermuted data."
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--output", type=Path, default=ROOT / "experiments" / "results" / "FR-FOURCE-FORMAL-007A")
    ap.add_argument("--smoke", action="store_true", help="Non-evidentiary code-path check")
    args = ap.parse_args()

    cfg = load_config(args.config, args.smoke)
    out_dir = args.output
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"Refusing to overwrite append-only result directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    partitions = generate_partitions(cfg["nodes"])

    manifest = {
        "experiment_id": cfg["experiment_id"],
        "mode": "SMOKE_NON_EVIDENTIARY" if args.smoke else "FULL_PREREGISTERED",
        "git_sha": git_sha(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "config_sha256": sha256_file(args.config),
        "candidate_count": int(len(partitions)),
        "seeds": cfg["master_seeds"],
        "warning": "Smoke results are never evidence. Full results are append-only and must be interpreted against Sweep 007 without threshold changes."
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (out_dir / "effective_config.json").write_text(json.dumps(cfg, indent=2))

    rows = []
    for seed in cfg["master_seeds"]:
        print(f"[007A] seed {seed}", flush=True)
        rows.append(run_seed(int(seed), cfg, partitions, out_dir))

    fields = list(rows[0].keys())
    with (out_dir / "summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    decision = verdict(rows, cfg)
    if args.smoke:
        decision["primary_status"] = "NOT_EVIDENCE"
        decision["warning"] = "Smoke mode cannot pass, fail, support, or falsify CSH-001."
    (out_dir / "verdict.json").write_text(json.dumps(decision, indent=2))
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
