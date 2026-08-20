from dataclasses import dataclass
import numpy as np

@dataclass
class SpectrumReport:
    singular_values: np.ndarray
    relative_singular_values: np.ndarray
    rank: int
    kernel_dim: int
    condition_nonzero: float

def analyze_operator(T, rtol=None):
    T = np.asarray(T, dtype=float)
    s = np.linalg.svd(T, compute_uv=False)
    if len(s) == 0:
        return SpectrumReport(s, s, 0, T.shape[1], np.inf)
    tol = (max(T.shape) * np.finfo(float).eps * s[0]) if rtol is None else (rtol * s[0])
    nz = s[s > tol]
    rank = int(len(nz))
    kernel_dim = int(T.shape[1] - rank)
    rel = nz / nz[0] if len(nz) else np.array([])
    cond = float(nz[0] / nz[-1]) if len(nz) else np.inf
    return SpectrumReport(s, rel, rank, kernel_dim, cond)

def threshold_count(report, epsilon):
    return int(np.sum(report.relative_singular_values >= epsilon))

def null_space(T, rtol=None):
    T = np.asarray(T, dtype=float)
    U, s, Vh = np.linalg.svd(T, full_matrices=True)
    if len(s) == 0:
        return np.eye(T.shape[1])
    tol = (max(T.shape) * np.finfo(float).eps * s[0]) if rtol is None else (rtol * s[0])
    rank = int(np.sum(s > tol))
    return Vh[rank:].T

def stack_channels(*channels):
    return np.vstack([np.asarray(c, dtype=float) for c in channels])

def row_normalize(T):
    T = np.asarray(T, dtype=float)
    norms = np.linalg.norm(T, axis=1, keepdims=True)
    return T / np.where(norms == 0, 1.0, norms)

def choose_next_measurement(base_T, candidates, normalize=True):
    base = row_normalize(base_T) if normalize else np.asarray(base_T, dtype=float)
    best = None
    for label, row in candidates:
        r = np.asarray(row, dtype=float).reshape(1, -1)
        rr = row_normalize(r) if normalize else r
        M = np.vstack([base, rr])
        rep = analyze_operator(M)
        min_nonzero = rep.singular_values[rep.rank-1] if rep.rank else 0.0
        score = (rep.rank, float(min_nonzero), -rep.condition_nonzero)
        if best is None or score > best['score']:
            best = {'label': label, 'row': row, 'report': rep, 'score': score}
    return best
