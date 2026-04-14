import numpy as np
import matplotlib.pyplot as plt

np.random.seed(11)

N = 48
T = 220
dt = 0.06

omega = np.random.normal(0.0, 0.6, size=N)

group = np.zeros(N, dtype=int)
group[N // 2:] = 1

adj = np.zeros((N, N), dtype=float)
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        adj[i, j] = 1.0 if group[i] == group[j] else 0.18

row_sums = adj.sum(axis=1)
mask0 = group == 0
mask1 = group == 1

def order_parameter(theta):
    return np.abs(np.exp(1j * theta).mean())

def simulate_once(K=1.5, boundary_strength=0.0, throughput=1.0, dissipation=0.15):
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

K_values = np.linspace(0.2, 2.4, 18)
B_values = np.linspace(0.0, 1.2, 18)
throughput = 1.0
dissipation = 0.16

phase_map = np.zeros((len(B_values), len(K_values)))

for bi, B in enumerate(B_values):
    for ki, K in enumerate(K_values):
        vals = [simulate_once(K=K, boundary_strength=B, throughput=throughput, dissipation=dissipation) for _ in range(2)]
        phase_map[bi, ki] = np.mean(vals)

plt.figure(figsize=(9, 6))
im = plt.imshow(
    phase_map,
    origin='lower',
    aspect='auto',
    extent=[K_values.min(), K_values.max(), B_values.min(), B_values.max()],
)
plt.colorbar(im, label='Sustained coherence (mean final R)')
plt.xlabel('Coupling strength K')
plt.ylabel('Constraint strength B')
plt.title('CUC Simulation v2: Phase Diagram of Sustained Coherence')
plt.tight_layout()
plt.show()
