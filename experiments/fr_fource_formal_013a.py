#!/usr/bin/env python3
"""FR-FOURCE-FORMAL-013A Atlas bench.

Implementation phase only. This executable refuses calibration and held-out seeds.
It constructs deterministic generator manifests, probe licenses, null/decoy registries,
and selective-intervention preservation reports for design seeds 2000-2009.

No output from this file is evidentiary for CSH-002.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "fr_fource_formal_013a.json"


@dataclass(frozen=True)
class GeneratorSpec:
    id: str
    levels: tuple[str, ...]
    purpose: str


GENERATOR_SPECS = {
    "G1": GeneratorSpec("G1", ("L1:A/B/C/D", "L2:O1/O2", "L3:O1|O2"), "static modular hierarchy"),
    "G2": GeneratorSpec("G2", ("TEMP",), "temporal organization hidden from static coupling"),
    "G3": GeneratorSpec("G3", ("CAUSAL",), "observational mimic with interventional difference"),
    "G4": GeneratorSpec("G4", ("ROLE",), "constituent-role substitution"),
    "G5": GeneratorSpec("G5", ("LOW", "HIGH"), "nested cross-scale conflict"),
    "G6": GeneratorSpec("G6", tuple(), "decoy-rich null-like world"),
}


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def classify_seed(seed: int, cfg: dict[str, Any]) -> str:
    for name, seeds in cfg["seed_classes"].items():
        if seed in seeds:
            return name
    raise ValueError(f"seed {seed} is outside frozen classes")


def enforce_firewall(seeds: list[int], cfg: dict[str, Any]) -> None:
    classes = {classify_seed(s, cfg) for s in seeds}
    if classes != {"design"}:
        raise RuntimeError(
            f"013A firewall violation: only design seeds are executable; requested classes={sorted(classes)}"
        )
    if not cfg["firewall"].get("allow_design", False):
        raise RuntimeError("design execution disabled")


def symmetric_block_matrix(n: int, groups: list[list[int]], within: float, between: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    W = np.full((n, n), between, dtype=float)
    np.fill_diagonal(W, 0.0)
    for group in groups:
        idx = np.ix_(group, group)
        W[idx] = within + rng.normal(0, 0.02, size=(len(group), len(group)))
    np.fill_diagonal(W, 0.0)
    return 0.5 * (W + W.T)


def build_generator(gid: str, seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    if gid == "G1":
        groups = [list(range(0,3)), list(range(3,6)), list(range(6,9)), list(range(9,12))]
        W = np.full((12,12), 0.10)
        np.fill_diagonal(W, 0)
        for g in groups:
            W[np.ix_(g,g)] = 1.20
        for a,b in ((groups[0],groups[1]),(groups[2],groups[3])):
            W[np.ix_(a,b)] = 0.55; W[np.ix_(b,a)] = 0.55
        W += rng.normal(0,0.015,W.shape); np.fill_diagonal(W,0)
        truth = {"L1": groups, "L2": [groups[0]+groups[1], groups[2]+groups[3]], "L3": [list(range(0,6)),list(range(6,12))]}
        return {"W": W, "truth": truth, "decoys": {"DQ2": [list(range(0,6)),list(range(6,12))]}}
    if gid == "G2":
        W = rng.normal(0,0.08,(12,12)); np.fill_diagonal(W,0)
        phase = rng.integers(0,2,12).tolist()
        return {"W": W, "truth": {"TEMP": {"phase_partition": phase, "period": 4}}, "decoys": {"DQ1": "static-coupling"}}
    if gid == "G3":
        W = rng.normal(0,0.12,(12,12)); np.fill_diagonal(W,0)
        intervention_map = {str(i): int((i+3)%12) for i in range(12)}
        return {"W": W, "truth": {"CAUSAL": intervention_map}, "decoys": {"DQ3":"common-driver", "DQ4":"hub"}}
    if gid == "G4":
        groups = [list(range(0,4)),list(range(4,8)),list(range(8,12))]
        W = symmetric_block_matrix(12,groups,1.0,0.15,seed)
        nuisance = rng.normal(0,1,12).tolist()
        return {"W": W, "truth": {"ROLE": groups}, "nuisance": nuisance, "decoys": {"DQ1":"raw-node-identity"}}
    if gid == "G5":
        low = [list(range(0,3)),list(range(3,6)),list(range(6,9)),list(range(9,12))]
        W = symmetric_block_matrix(12,low,1.1,0.18,seed)
        return {"W": W, "truth": {"LOW":low, "HIGH":[list(range(0,6)),list(range(6,12))]}, "decoys": {"DQ2":"balanced-alternative"}}
    if gid == "G6":
        W = rng.normal(0,0.35,(12,12)); np.fill_diagonal(W,0)
        W[:,0] += 0.8  # hub decoy
        return {"W": W, "truth": {}, "decoys": {"DQ2":"balanced", "DQ4":"hub", "DQ5":"stable-trivial"}}
    raise KeyError(gid)


def null_manifest(gid: str) -> dict[str, Any]:
    return {
        "N1": "target-relation randomization with preserved declared low-order summaries",
        "N2": "split-size-conditioned geometry comparison",
        "N3": "temporal shuffle/block null preserving marginals/static summaries",
        "N4": "intervention-label/response remapping",
        "N5": "same-target agreement after nuisance-preserving transforms",
        "applicable": {
            "G1": ["N1","N2"], "G2": ["N2","N3"], "G3": ["N4"],
            "G4": ["N1"], "G5": ["N1","N2"], "G6": ["N1","N2","N3","N4"]
        }[gid],
    }


def selective_interventions(gid: str, obj: dict[str, Any], seed: int) -> dict[str, Any]:
    """Emit design-stage intervention declarations + preservation audit placeholders.

    Numeric preservation tolerances are not invented here; those belong to the
    calibration freeze. We do emit exact pre/post summaries needed to review them.
    """
    W = np.asarray(obj["W"], float)
    rng = np.random.default_rng(seed + 900_000)
    reports: dict[str, Any] = {}
    for xid in ("X1","X2","X3","X4","X5","XC1","XC2"):
        Wp = W.copy()
        if xid == "X5":
            vals = W[~np.eye(len(W),dtype=bool)].copy(); rng.shuffle(vals); Wp[~np.eye(len(W),dtype=bool)] = vals
        elif xid == "XC2":
            p = rng.permutation(len(W)); Wp = W[np.ix_(p,p)]
        elif xid in ("X1","X2") and gid in ("G1","G5"):
            # design-stage targeted transforms; exact preservation tolerances reviewed before calibration.
            if xid == "X1":
                blocks = obj["truth"].get("L1", obj["truth"].get("LOW", []))
                for block in blocks:
                    idx = np.ix_(block,block); vals = Wp[idx].ravel(); rng.shuffle(vals); Wp[idx] = vals.reshape(len(block),len(block))
            else:
                half = len(W)//2
                cross = [(i,j) for i in range(half) for j in range(half,len(W))] + [(j,i) for i,j in [(i,j) for i in range(half) for j in range(half,len(W))]]
                vals = np.array([Wp[i,j] for i,j in cross]); rng.shuffle(vals)
                for (i,j),v in zip(cross,vals): Wp[i,j]=v
        reports[xid] = {
            "frobenius_change": float(np.linalg.norm(Wp-W)),
            "mean_abs_weight_before": float(np.mean(np.abs(W))),
            "mean_abs_weight_after": float(np.mean(np.abs(Wp))),
            "status": "DESIGN_AUDIT_ONLY"
        }
    return reports


def run(seed: int, cfg: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"seed":seed, "seed_class":classify_seed(seed,cfg), "status":cfg["status"], "generators":{}}
    for gid in cfg["generators"]:
        obj = build_generator(gid, seed)
        out["generators"][gid] = {
            "spec": asdict(GENERATOR_SPECS[gid]),
            "truth": obj.get("truth",{}),
            "decoys": obj.get("decoys",{}),
            "null_manifest": null_manifest(gid),
            "matrix_summary": {"shape": list(obj["W"].shape), "mean": float(np.mean(obj["W"])), "sd": float(np.std(obj["W"]))},
            "interventions": selective_interventions(gid,obj,seed),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--seed", type=int, action="append")
    ap.add_argument("--output", type=Path, default=ROOT/"experiments"/"results"/"FR-FOURCE-FORMAL-013A-DESIGN")
    args = ap.parse_args()
    cfg = load_config(args.config)
    seeds = args.seed or list(cfg["seed_classes"]["design"])
    enforce_firewall(seeds,cfg)
    args.output.mkdir(parents=True,exist_ok=True)
    manifest = {"status":cfg["status"], "seeds":seeds, "probe_registry":cfg["probes"], "runs":[]}
    for seed in seeds:
        r = run(seed,cfg); manifest["runs"].append(r)
        (args.output/f"design_seed_{seed}.json").write_text(json.dumps(r,indent=2,sort_keys=True))
    (args.output/"manifest_013a.json").write_text(json.dumps(manifest,indent=2,sort_keys=True))
    print(json.dumps({"status":cfg["status"],"seeds":seeds,"output":str(args.output)},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
