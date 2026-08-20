import numpy as np
from scipy.special import spherical_jn, gammaln

chi_star = 14000.0
ells = np.arange(2, 31)
nk = 120
k = np.logspace(-5, -2, nk)
dlnk = np.gradient(np.log(k))
x = k * chi_star

# Channel 1: large-angle Sachs-Wolfe temperature transfer
Delta_T = np.array([0.2 * spherical_jn(l, x) for l in ells])
A_T = 4 * np.pi * (Delta_T ** 2) * dlnk[None, :]

# Fiducial primordial spectrum
A_s, n_s, k_pivot = 2.1e-9, 0.965, 0.05
P_fid = A_s * (k / k_pivot) ** (n_s - 1)

# Cosmic-variance whitening for T
C_T = A_T @ P_fid
sigma_T = np.sqrt(2 / (2 * ells + 1)) * C_T
A_Tw = A_T / sigma_T[:, None]

# Channel 2: polarization-like spin-2 toy transfer.
# NOT a full physical EE calculation. Used only to test whether a distinct
# second response channel shrinks the exact reconstruction kernel.
spin2 = np.exp(0.5 * np.array([gammaln(l + 3) - gammaln(l - 1) for l in ells]))
source_proxy = (x / (1 + x)) * np.exp(-(k / 0.01) ** 2)
Delta_Etoy = np.array([
    0.02 * spin2[i] * spherical_jn(l, x) / (x**2 + 1e-30)
    for i, l in enumerate(ells)
]) * source_proxy[None, :]

A_E = 4 * np.pi * (Delta_Etoy ** 2) * dlnk[None, :]
C_E = A_E @ P_fid
sigma_E = np.sqrt(2 / (2 * ells + 1)) * C_E
A_Ew = A_E / sigma_E[:, None]

A_stack = np.vstack([A_Tw, A_Ew])

def metrics(A):
    s = np.linalg.svd(A, compute_uv=False)
    tol = max(A.shape) * np.finfo(float).eps * s[0]
    s_nz = s[s > tol]
    rel = s_nz / s_nz[0]
    rank = len(s_nz)
    return {
        "rank": rank,
        "kernel_dim": nk - rank,
        "relative": rel,
        "condition": s_nz[0] / s_nz[-1],
        "ge_0p1": int((rel >= 0.1).sum()),
        "ge_0p01": int((rel >= 0.01).sum()),
        "ge_0p001": int((rel >= 0.001).sum()),
    }

for name, A in [("TT", A_Tw), ("E-toy", A_Ew), ("TT+E-toy", A_stack)]:
    m = metrics(A)
    print(name)
    print("  rank:", m["rank"])
    print("  kernel dimension:", m["kernel_dim"])
    print("  condition number:", m["condition"])
    print("  rel sigma >= 0.1:", m["ge_0p1"])
    print("  rel sigma >= 0.01:", m["ge_0p01"])
    print("  rel sigma >= 0.001:", m["ge_0p001"])
