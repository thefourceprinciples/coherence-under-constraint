import numpy as np
import matplotlib.pyplot as plt

np.random.seed(21)

N = 48
T = 220
dt = 0.06

omega = np.random.normal(0.0, 0.6, size=N)

group = np.zeros(N, dtype=int)
group[N // 2:] = 1
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
    R_hist = np.zeros(T)

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
        R_hist[t] = order_parameter(theta)

    return R_hist[int(0.7 * T):].mean()

K_fixed = 1.35
B_fixed = 0.45

throughput_values = np.linspace(0.55, 1.45, 18)
dissipation_values = np.linspace(0.05, 0.32, 18)

phase_map = np.zeros((len(dissipation_values), len(throughput_values)))

for di, D in enumerate(dissipation_values):
    for ti, E in enumerate(throughput_values):
        vals = [
            simulate_once(
                K=K_fixed,
                boundary_strength=B_fixed,
                throughput=E,
                dissipation=D
            )
            for _ in range(2)
        ]
        phase_map[di, ti] = np.mean(vals)

threshold = 0.55
boundary_E = np.full(len(dissipation_values), np.nan)
for di in range(len(dissipation_values)):
    row = phase_map[di]
    idx = np.where(row >= threshold)[0]
    if len(idx) > 0:
        boundary_E[di] = throughput_values[idx[0]]

plt.figure(figsize=(9, 6))
im = plt.imshow(
    phase_map,
    origin='lower',
    aspect='auto',
    extent=[
        throughput_values.min(), throughput_values.max(),
        dissipation_values.min(), dissipation_values.max()
    ],
)
plt.colorbar(im, label='Sustained coherence (mean final R)')
plt.xlabel('Throughput E')
plt.ylabel('Dissipation D')
plt.title('CUC Simulation v3: Throughput–Dissipation Survival Map')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(boundary_E, dissipation_values)
plt.xlabel('Minimum throughput for survival')
plt.ylabel('Dissipation D')
plt.title(f'CUC Simulation v3: Survival Boundary (R ≥ {threshold:.2f})')
plt.tight_layout()
plt.savefig("figure_1C_throughput_map.png", dpi=300)
plt.show()
