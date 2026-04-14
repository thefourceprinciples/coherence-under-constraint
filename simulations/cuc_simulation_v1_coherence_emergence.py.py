import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)

N = 60
T = 600
dt = 0.05
time = np.arange(T) * dt

omega = np.random.normal(0.0, 0.6, size=N)

group = np.zeros(N, dtype=int)
group[N // 2:] = 1

adj = np.zeros((N, N), dtype=float)
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        adj[i, j] = 1.0 if group[i] == group[j] else 0.18

def order_parameter(theta):
    return np.abs(np.exp(1j * theta).mean())

def simulate(K=1.5, boundary_strength=0.0, throughput=1.0, dissipation=0.15):
    theta = np.random.uniform(-np.pi, np.pi, size=N)
    R_hist = np.zeros(T)
    row_sums = adj.sum(axis=1)

    for t in range(T):
        mean0 = np.angle(np.exp(1j * theta[group == 0]).mean())
        mean1 = np.angle(np.exp(1j * theta[group == 1]).mean())

        dtheta = omega.copy()
        phase_diff = theta[None, :] - theta[:, None]
        coupling_term = (adj * np.sin(phase_diff)).sum(axis=1) / row_sums
        dtheta += throughput * K * coupling_term

        target = np.where(group == 0, mean0, mean1)
        dtheta += boundary_strength * np.sin(target - theta)

        noise = np.random.normal(0.0, np.sqrt(dt) * dissipation, size=N)
        theta = theta + dt * dtheta + noise
        theta = (theta + np.pi) % (2 * np.pi) - np.pi
        R_hist[t] = order_parameter(theta)

    return R_hist

R1 = simulate(K=0.65, boundary_strength=0.00, throughput=0.85, dissipation=0.22)
R2 = simulate(K=1.20, boundary_strength=0.35, throughput=1.00, dissipation=0.17)
R3 = simulate(K=1.80, boundary_strength=0.70, throughput=1.15, dissipation=0.12)

plt.figure(figsize=(10, 6))
plt.plot(time, R1, label='Low coupling / weak constraint')
plt.plot(time, R2, label='Balanced CUC regime')
plt.plot(time, R3, label='High coupling / strong constraint')
plt.xlabel('Time')
plt.ylabel('Global coherence R(t)')
plt.title('CUC Prototype: Coherence Emergence Under Constraint')
plt.ylim(0, 1.02)
plt.legend()
plt.tight_layout()
plt.show()
