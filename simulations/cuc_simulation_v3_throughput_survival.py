"""
CUC Simulation v3
Figures 1C–1D — Throughput–Dissipation Coherence Proxy

Historical toy prototype. In this model, "throughput" multiplies coupling and
"survival" is a coherence threshold; neither is yet an independent v0.2 CUC
measure. See simulations/README.md for limitations.
"""

import numpy as np
import matplotlib.pyplot as plt


np.random.seed(21)

N = 48
T = 220
dt = 0.06

omega = np.random.normal(0.0, 0.6, size=N)

group = np.zeros(N, dtype=int)
group[N // 2 :] = 1
mask0 = group == 0
mask1 = group == 1

adj = np.zeros((N, N), dtype=float)
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        adj[i, j] = 1.0 if group[i] == group[j] else 0.18

row_sums = adj.sum(axis=1)


def order_parameter(theta):
    return np.abs(np.exp(1j * theta).mean())


def simulate_once(K=1.35, boundary_strength=0.45, throughput=1.0, dissipation=0.15):
    theta = np.random.uniform(-np.pi, np.pi, size=N)
    coherence_history = np.zeros(T)

    for t in range(T):
        mean0 = np.angle(np.exp(1j * theta[mask0]).mean())
        mean1 = np.angle(np.exp(1j * theta[mask1]).mean())

        phase_diff = theta[None, :] - theta[:, None]
        coupling_term = (adj * np.sin(phase_diff)).sum(axis=1) / row_sums

        target = np.where(group == 0, mean0, mean1)
        dtheta = (
            omega
            + throughput * K * coupling_term
            + boundary_strength * np.sin(target - theta)
        )

        noise = np.random.normal(0.0, np.sqrt(dt) * dissipation, size=N)
        theta = theta + dt * dtheta + noise
        theta = (theta + np.pi) % (2 * np.pi) - np.pi
        coherence_history[t] = order_parameter(theta)

    return coherence_history[int(0.7 * T) :].mean()


K_FIXED = 1.35
BOUNDARY_FIXED = 0.45

throughput_values = np.linspace(0.55, 1.45, 18)
dissipation_values = np.linspace(0.05, 0.32, 18)

phase_map = np.zeros((len(dissipation_values), len(throughput_values)))

for dissipation_index, dissipation in enumerate(dissipation_values):
    for throughput_index, throughput in enumerate(throughput_values):
        values = [
            simulate_once(
                K=K_FIXED,
                boundary_strength=BOUNDARY_FIXED,
                throughput=throughput,
                dissipation=dissipation,
            )
            for _ in range(2)
        ]
        phase_map[dissipation_index, throughput_index] = np.mean(values)

threshold = 0.55
boundary_throughput = np.full(len(dissipation_values), np.nan)
for dissipation_index in range(len(dissipation_values)):
    row = phase_map[dissipation_index]
    passing = np.where(row >= threshold)[0]
    if len(passing) > 0:
        boundary_throughput[dissipation_index] = throughput_values[passing[0]]

plt.figure(figsize=(9, 6))
image = plt.imshow(
    phase_map,
    origin="lower",
    aspect="auto",
    extent=[
        throughput_values.min(),
        throughput_values.max(),
        dissipation_values.min(),
        dissipation_values.max(),
    ],
)
plt.colorbar(image, label="Sustained coherence (mean final R)")
plt.xlabel("Throughput multiplier E")
plt.ylabel("Noise / dissipation proxy D")
plt.title("CUC Prototype v3: Throughput–Dissipation Coherence Map")
plt.tight_layout()
map_path = "figure_1C_throughput_map.png"
plt.savefig(map_path, dpi=300)
print("Saved image to:", map_path)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(boundary_throughput, dissipation_values)
plt.xlabel("Minimum throughput multiplier above coherence threshold")
plt.ylabel("Noise / dissipation proxy D")
plt.title(f"CUC Prototype v3: Coherence Boundary (R ≥ {threshold:.2f})")
plt.tight_layout()
boundary_path = "figure_1D_survival_boundary.png"
plt.savefig(boundary_path, dpi=300)
print("Saved image to:", boundary_path)
plt.show()

