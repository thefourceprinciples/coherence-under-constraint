import numpy as np
from scipy.special import spherical_jn


CHI_STAR_MPC = 14_000.0
ELLS = np.arange(2, 31)
N_K = 120
K_MPC_INV = np.logspace(-5, -2, N_K)


def build_whitened_operator():
    """Return the discretized Sachs-Wolfe operator after cosmic-variance whitening."""
    dlnk = np.gradient(np.log(K_MPC_INV))
    transfer = np.array(
        [0.2 * spherical_jn(ell, K_MPC_INV * CHI_STAR_MPC) for ell in ELLS]
    )
    operator = 4.0 * np.pi * transfer**2 * dlnk[None, :]

    amplitude, tilt, pivot = 2.1e-9, 0.965, 0.05
    primordial_spectrum = amplitude * (K_MPC_INV / pivot) ** (tilt - 1.0)
    angular_spectrum = operator @ primordial_spectrum
    sigma_cosmic_variance = (
        np.sqrt(2.0 / (2.0 * ELLS + 1.0)) * angular_spectrum
    )
    return operator / sigma_cosmic_variance[:, None]


def main():
    whitened_operator = build_whitened_operator()
    singular_values = np.linalg.svd(whitened_operator, compute_uv=False)

    # Match NumPy's default matrix-rank convention, but expose the tolerance so
    # the reported numerical kernel is reproducible and correctly qualified.
    rank_tolerance = (
        max(whitened_operator.shape)
        * np.finfo(singular_values.dtype).eps
        * singular_values[0]
    )
    rank = int(np.count_nonzero(singular_values > rank_tolerance))
    relative_singular_values = singular_values / singular_values[0]

    print("shape:", whitened_operator.shape)
    print("rank tolerance:", rank_tolerance)
    print("numerical rank:", rank)
    print("numerical kernel dimension:", N_K - rank)
    print(
        "transmitted-space condition number:",
        singular_values[0] / singular_values[rank - 1],
    )
    print("relative singular values:", relative_singular_values)


if __name__ == "__main__":
    main()
